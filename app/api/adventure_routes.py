import random

from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required

from app.game.forest_rules import (
    ARMORS,
    BANK_INTEREST_RATE,
    BASE_MANA,
    BASE_SPECIALTY_USES,
    BASIC_SPECIAL_COST,
    BASIC_SPECIAL_MOVE,
    BASIC_SPECIAL_NAME,
    MAX_LEVEL,
    WEAPONS,
    armor_for_tier,
    build_dragon,
    build_forest_creature,
    build_master,
    dragon_reset_stats,
    effective_attack,
    effective_defense,
    forest_fights_per_day,
    game_day_key,
    healing_cost,
    purchase_price,
    roll_enemy_damage,
    roll_player_damage,
    roll_special_damage,
    title_for_dragon_kills,
    weapon_for_tier,
    xp_after_death,
    xp_required,
)
from app.models import AdventureState, db

adventure_routes = Blueprint("adventure", __name__)

ENCOUNTERS = {}


def clear_encounter(user_id):
    ENCOUNTERS.pop(user_id, None)


def get_encounter(user_id):
    return ENCOUNTERS.get(user_id)


def apply_new_day_if_needed(state):
    current_day = game_day_key()
    if state.game_day == current_day:
        return []

    log = ["A new Arcana game day begins."]
    if state.bank_gold > 0:
        interest = max(1, int(state.bank_gold * BANK_INTEREST_RATE))
        state.bank_gold += interest
        log.append(f"The Academy Bank pays {interest} gold in interest.")

    state.game_day = current_day
    state.alive = True
    state.hp = state.max_hp
    state.mana = state.max_mana
    state.turns = forest_fights_per_day(state.dragon_fights)
    state.specialty_uses = BASE_SPECIALTY_USES
    state.location = "town"
    clear_encounter(state.user_id)
    return log


def get_or_create_state():
    state = AdventureState.query.filter_by(user_id=current_user.id).first()
    if not state:
        state = AdventureState(
            user_id=current_user.id,
            gold=100,
            mana=BASE_MANA,
            max_mana=BASE_MANA,
            game_day=game_day_key(),
            turns=forest_fights_per_day(0),
            specialty_uses=BASE_SPECIALTY_USES,
        )
        db.session.add(state)
        db.session.commit()
        return state, ["Welcome to Arcana Academy. Your first game day has begun."]

    log = apply_new_day_if_needed(state)
    if log:
        db.session.commit()
    return state, log


def equipment_catalog(catalog):
    return [
        {"tier": tier, "name": item["name"], "power": item["power"], "cost": item["cost"]}
        for tier, item in enumerate(catalog)
    ]


def battle_payload(state):
    encounter = get_encounter(state.user_id)
    if not encounter:
        return None
    monster = encounter["monster"]
    return {
        "kind": monster["kind"],
        "monster": monster["name"],
        "monster_level": monster["level"],
        "monster_hp": encounter["monster_hp"],
        "max_monster_hp": monster["max_hp"],
        "player_hp": state.hp,
        "hunt_mode": monster.get("hunt_mode"),
    }


def state_payload(state):
    payload = state.to_dict()
    payload.update(
        {
            "title": title_for_dragon_kills(state.dragon_kills),
            "xp_required": xp_required(state.level),
            "can_challenge_master": state.alive
            and state.level < MAX_LEVEL
            and state.xp >= xp_required(state.level),
            "can_hunt_dragon": state.alive and state.level >= MAX_LEVEL,
            "max_forest_fights": forest_fights_per_day(state.dragon_fights),
            "effective_attack": effective_attack(state.attack, state.weapon_level),
            "effective_defense": effective_defense(state.defense, state.armor_level),
            "weapon": weapon_for_tier(state.weapon_level),
            "armor": armor_for_tier(state.armor_level),
            "healing_cost": healing_cost(state.hp, state.max_hp, state.level),
            "special_moves": [
                {
                    "id": BASIC_SPECIAL_MOVE,
                    "name": BASIC_SPECIAL_NAME,
                    "mana_cost": BASIC_SPECIAL_COST,
                    "rounds": 1,
                    "description": "A focused arcane attack that deals double normal damage for one round.",
                }
            ],
        }
    )
    return payload


def response_payload(state, log=None):
    return {
        "state": state_payload(state),
        "battle": battle_payload(state),
        "log": log or [],
        "shops": {
            "weapons": equipment_catalog(WEAPONS),
            "armor": equipment_catalog(ARMORS),
        },
    }


def town_action_error(state):
    if not state.alive:
        return "You are dead. The town is beyond your reach until the next game day."
    if get_encounter(state.user_id):
        return "Finish or flee from your current battle first."
    return None


def defeat_player(state, log):
    lost_gold = state.gold
    old_xp = state.xp
    state.gold = 0
    state.xp = xp_after_death(state.xp)
    state.hp = 0
    state.alive = False
    state.turns = 0
    state.location = "graveyard"
    clear_encounter(state.user_id)
    log.append(
        f"You have fallen. You lose {lost_gold} carried gold and {old_xp - state.xp} experience."
    )
    log.append("Your banked gold remains safe. You will rise again on the next game day.")


def award_forest_victory(state, encounter, log):
    monster = encounter["monster"]
    gold_gain = random.randint(*monster["gold"])
    xp_gain = random.randint(*monster["xp"])
    state.gold += gold_gain
    state.xp += xp_gain
    log.append(f"You defeat {monster['name']} and gain {gold_gain} gold and {xp_gain} experience.")

    gem_chance = 0.03 if monster.get("hunt_mode") == "slum" else 0.08 if monster.get("hunt_mode") == "thrill" else 0.05
    if random.random() < gem_chance:
        state.gems += 1
        log.append("Something glitters in the leaves: you found a gem.")

    if encounter["damage_taken"] == 0 and monster.get("hunt_mode") != "slum":
        state.turns += 1
        log.append("Flawless victory! You recover the forest fight you spent.")

    clear_encounter(state.user_id)
    if state.level < MAX_LEVEL and state.xp >= xp_required(state.level):
        log.append("You have enough experience to challenge your Academy Master.")
    elif state.level >= MAX_LEVEL:
        log.append("You are powerful enough to hunt the Emerald Archdragon.")


def award_master_victory(state, log):
    old_level = state.level
    state.xp = max(0, state.xp - xp_required(old_level))
    state.level += 1
    state.max_hp += 5
    state.attack += 1
    state.defense += 1
    state.hp = state.max_hp
    state.location = "town"
    clear_encounter(state.user_id)
    log.append(f"You defeat your master and advance to level {state.level}!")
    if state.level == MAX_LEVEL:
        log.append("There are no more masters. The Emerald Archdragon now waits in the forest.")


def award_dragon_victory(state, log):
    state.dragon_kills += 1
    state.dragon_points += 1

    reset = dragon_reset_stats(state.dragon_attack, state.dragon_defense, state.dragon_hp)
    state.level = reset["level"]
    state.xp = reset["xp"]
    state.hp = reset["hp"]
    state.max_hp = reset["max_hp"]
    state.attack = reset["attack"]
    state.defense = reset["defense"]
    state.weapon_level = reset["weapon_level"]
    state.armor_level = reset["armor_level"]
    state.gold = 0
    state.bank_gold = 0
    state.gems = 0
    state.mana = state.max_mana
    state.turns = forest_fights_per_day(state.dragon_fights)
    state.specialty_uses = BASE_SPECIALTY_USES
    state.alive = True
    state.location = "town"
    state.game_day = game_day_key()
    clear_encounter(state.user_id)

    log.append("The Emerald Archdragon falls. Arcana will remember your victory.")
    log.append("Your mortal progress resets, and you receive 1 Dragon Point to spend permanently.")


def resolve_victory(state, encounter, log):
    kind = encounter["monster"]["kind"]
    if kind == "master":
        award_master_victory(state, log)
    elif kind == "dragon":
        award_dragon_victory(state, log)
    else:
        award_forest_victory(state, encounter, log)


def maybe_forest_event(state, hunt_mode):
    if random.random() >= 0.10:
        return None

    event = random.choice(["cache", "spring", "scholar", "gem"])
    if event == "cache":
        gold = random.randint(max(2, state.level * 4), max(4, state.level * 8))
        state.gold += gold
        return [f"You find an abandoned satchel containing {gold} gold. No forest fight is spent."]
    if event == "spring":
        healed = min(state.max_hp - state.hp, max(1, state.max_hp // 4))
        state.hp += healed
        return [f"A hidden spring restores {healed} HP. No forest fight is spent."]
    if event == "scholar":
        gained = max(3, state.level * (4 if hunt_mode == "slum" else 6))
        state.xp += gained
        return [f"A wandering scholar teaches you a forgotten lesson. +{gained} experience."]

    state.gems += 1
    return ["You discover a raw arcane gem beneath an ancient root. No forest fight is spent."]


@adventure_routes.route("/state", methods=["GET"])
@login_required
def get_state():
    state, log = get_or_create_state()
    return jsonify(response_payload(state, log))


@adventure_routes.route("/start", methods=["POST"])
@login_required
def start_encounter():
    state, new_day_log = get_or_create_state()
    if not state.alive:
        return jsonify({"error": "The dead cannot hunt the forest."}), 400
    if get_encounter(state.user_id):
        return jsonify({"error": "You are already in battle."}), 400
    if state.turns <= 0:
        return jsonify({"error": "You have no forest fights left this game day."}), 400

    data = request.get_json(silent=True) or {}
    hunt_mode = data.get("mode", "normal")
    if hunt_mode not in {"slum", "normal", "thrill"}:
        return jsonify({"error": "Unknown hunt mode."}), 400

    event_log = maybe_forest_event(state, hunt_mode)
    if event_log:
        db.session.commit()
        return jsonify(response_payload(state, new_day_log + event_log))

    monster = build_forest_creature(state.level, hunt_mode)
    state.turns -= 1
    state.location = "forest"
    ENCOUNTERS[state.user_id] = {
        "monster": monster,
        "monster_hp": monster["hp"],
        "damage_taken": 0,
    }
    db.session.commit()
    log = new_day_log + [f"You encounter {monster['name']}, level {monster['level']}."]
    return jsonify(response_payload(state, log)), 201


@adventure_routes.route("/master/start", methods=["POST"])
@login_required
def start_master_challenge():
    state, new_day_log = get_or_create_state()
    error = town_action_error(state)
    if error:
        return jsonify({"error": error}), 400
    if state.level >= MAX_LEVEL:
        return jsonify({"error": "There are no more Academy Masters to challenge."}), 400
    if state.xp < xp_required(state.level):
        return jsonify({"error": "You need more experience before challenging your master."}), 400

    monster = build_master(state.level)
    state.location = "training"
    ENCOUNTERS[state.user_id] = {
        "monster": monster,
        "monster_hp": monster["hp"],
        "damage_taken": 0,
    }
    db.session.commit()
    return jsonify(response_payload(state, new_day_log + [f"{monster['name']} accepts your challenge."])), 201


@adventure_routes.route("/dragon/start", methods=["POST"])
@login_required
def start_dragon_hunt():
    state, new_day_log = get_or_create_state()
    error = town_action_error(state)
    if error:
        return jsonify({"error": error}), 400
    if state.level < MAX_LEVEL:
        return jsonify({"error": "Only a level 15 hero may hunt the Emerald Archdragon."}), 400

    monster = build_dragon(state.dragon_kills)
    state.location = "dragon"
    ENCOUNTERS[state.user_id] = {
        "monster": monster,
        "monster_hp": monster["hp"],
        "damage_taken": 0,
    }
    db.session.commit()
    return jsonify(response_payload(state, new_day_log + ["You follow scorched tracks deep into the forbidden grove..."])), 201


@adventure_routes.route("/action", methods=["POST"])
@login_required
def take_action():
    state, new_day_log = get_or_create_state()
    encounter = get_encounter(state.user_id)
    if not encounter:
        return jsonify({"error": "You are not currently in battle."}), 400
    if not state.alive:
        clear_encounter(state.user_id)
        return jsonify({"error": "You are dead."}), 400

    data = request.get_json(silent=True) or {}
    action = data.get("action", "fight")
    monster = encounter["monster"]
    log = list(new_day_log)

    if action == "run":
        if monster["kind"] != "forest":
            return jsonify({"error": "You cannot flee this challenge."}), 400
        if random.random() < 0.65:
            clear_encounter(state.user_id)
            state.location = "town"
            db.session.commit()
            return jsonify(response_payload(state, log + ["You escape back toward town."]))

        damage = roll_enemy_damage(monster["attack"], state.defense, state.armor_level)
        state.hp -= damage
        encounter["damage_taken"] += damage
        log.append(f"You fail to escape. {monster['name']} hits you for {damage} damage.")
        if state.hp <= 0:
            defeat_player(state, log)
        db.session.commit()
        return jsonify(response_payload(state, log))

    if action == "special":
        move = data.get("move")
        if move != BASIC_SPECIAL_MOVE:
            return jsonify({"error": "That special skill is not available."}), 400
        if state.mana < BASIC_SPECIAL_COST:
            return jsonify({"error": f"{BASIC_SPECIAL_NAME} requires {BASIC_SPECIAL_COST} mana."}), 400

        state.mana -= BASIC_SPECIAL_COST
        damage = roll_special_damage(state.attack, state.weapon_level, monster["defense"])
        encounter["monster_hp"] -= damage
        log.append(
            f"You unleash {BASIC_SPECIAL_NAME} for {damage} damage. "
            f"{BASIC_SPECIAL_COST} mana is consumed."
        )

        if encounter["monster_hp"] <= 0:
            encounter["monster_hp"] = 0
            resolve_victory(state, encounter, log)
        else:
            counter = roll_enemy_damage(monster["attack"], state.defense, state.armor_level)
            state.hp -= counter
            encounter["damage_taken"] += counter
            log.append(f"{monster['name']} hits you for {counter} damage.")
            if state.hp <= 0:
                defeat_player(state, log)

        db.session.commit()
        return jsonify(response_payload(state, log))

    rounds_raw = data.get("rounds", 1)
    if rounds_raw == "end":
        rounds = 1000
    else:
        try:
            rounds = int(rounds_raw)
        except (TypeError, ValueError):
            rounds = 1
        if rounds not in {1, 5, 10}:
            rounds = 1

    for _ in range(rounds):
        damage = roll_player_damage(state.attack, state.weapon_level, monster["defense"])
        encounter["monster_hp"] -= damage
        log.append(f"You hit {monster['name']} for {damage} damage.")

        if encounter["monster_hp"] <= 0:
            encounter["monster_hp"] = 0
            resolve_victory(state, encounter, log)
            break

        damage = roll_enemy_damage(monster["attack"], state.defense, state.armor_level)
        state.hp -= damage
        encounter["damage_taken"] += damage
        log.append(f"{monster['name']} hits you for {damage} damage.")

        if state.hp <= 0:
            defeat_player(state, log)
            break

    db.session.commit()
    return jsonify(response_payload(state, log))


@adventure_routes.route("/heal", methods=["POST"])
@login_required
def heal():
    state, new_day_log = get_or_create_state()
    error = town_action_error(state)
    if error:
        return jsonify({"error": error}), 400

    cost = healing_cost(state.hp, state.max_hp, state.level)
    if cost <= 0:
        return jsonify(response_payload(state, new_day_log + ["You are already at full health."]))
    if state.gold < cost:
        return jsonify({"error": f"Full healing costs {cost} gold."}), 400

    state.gold -= cost
    state.hp = state.max_hp
    db.session.commit()
    return jsonify(response_payload(state, new_day_log + [f"The healer restores you to full health for {cost} gold."]))


@adventure_routes.route("/rest", methods=["POST"])
@login_required
def rest_compatibility():
    return heal()


@adventure_routes.route("/shop/weapon", methods=["POST"])
@login_required
def buy_weapon():
    state, new_day_log = get_or_create_state()
    error = town_action_error(state)
    if error:
        return jsonify({"error": error}), 400

    data = request.get_json(silent=True) or {}
    try:
        tier = int(data.get("tier"))
    except (TypeError, ValueError):
        return jsonify({"error": "Choose a valid weapon tier."}), 400
    if tier < 1 or tier >= len(WEAPONS):
        return jsonify({"error": "Choose a valid weapon tier."}), 400

    price = purchase_price(WEAPONS, state.weapon_level, tier)
    if price is None:
        return jsonify({"error": "That weapon is not an upgrade."}), 400
    if state.gold < price:
        return jsonify({"error": f"You need {price} gold for that upgrade after trade-in."}), 400

    state.gold -= price
    state.weapon_level = tier
    db.session.commit()
    return jsonify(response_payload(state, new_day_log + [f"You equip {WEAPONS[tier]['name']} for {price} gold."]))


@adventure_routes.route("/shop/armor", methods=["POST"])
@login_required
def buy_armor():
    state, new_day_log = get_or_create_state()
    error = town_action_error(state)
    if error:
        return jsonify({"error": error}), 400

    data = request.get_json(silent=True) or {}
    try:
        tier = int(data.get("tier"))
    except (TypeError, ValueError):
        return jsonify({"error": "Choose a valid armor tier."}), 400
    if tier < 1 or tier >= len(ARMORS):
        return jsonify({"error": "Choose a valid armor tier."}), 400

    price = purchase_price(ARMORS, state.armor_level, tier)
    if price is None:
        return jsonify({"error": "That armor is not an upgrade."}), 400
    if state.gold < price:
        return jsonify({"error": f"You need {price} gold for that upgrade after trade-in."}), 400

    state.gold -= price
    state.armor_level = tier
    db.session.commit()
    return jsonify(response_payload(state, new_day_log + [f"You equip {ARMORS[tier]['name']} for {price} gold."]))


@adventure_routes.route("/bank/deposit", methods=["POST"])
@login_required
def bank_deposit():
    state, new_day_log = get_or_create_state()
    error = town_action_error(state)
    if error:
        return jsonify({"error": error}), 400

    data = request.get_json(silent=True) or {}
    try:
        amount = int(data.get("amount", 0))
    except (TypeError, ValueError):
        amount = 0
    if amount <= 0:
        return jsonify({"error": "Deposit must be positive."}), 400
    if state.gold < amount:
        return jsonify({"error": "You do not have that much carried gold."}), 400

    state.gold -= amount
    state.bank_gold += amount
    db.session.commit()
    return jsonify(response_payload(state, new_day_log + [f"You deposit {amount} gold."]))


@adventure_routes.route("/bank/withdraw", methods=["POST"])
@login_required
def bank_withdraw():
    state, new_day_log = get_or_create_state()
    error = town_action_error(state)
    if error:
        return jsonify({"error": error}), 400

    data = request.get_json(silent=True) or {}
    try:
        amount = int(data.get("amount", 0))
    except (TypeError, ValueError):
        amount = 0
    if amount <= 0:
        return jsonify({"error": "Withdrawal must be positive."}), 400
    if state.bank_gold < amount:
        return jsonify({"error": "You do not have that much gold in the bank."}), 400

    state.bank_gold -= amount
    state.gold += amount
    db.session.commit()
    return jsonify(response_payload(state, new_day_log + [f"You withdraw {amount} gold."]))


@adventure_routes.route("/dragon/allocate", methods=["POST"])
@login_required
def allocate_dragon_point():
    state, new_day_log = get_or_create_state()
    if state.dragon_points <= 0:
        return jsonify({"error": "You do not have an unspent Dragon Point."}), 400

    data = request.get_json(silent=True) or {}
    stat = data.get("stat")
    if stat not in {"attack", "defense", "hp", "fights"}:
        return jsonify({"error": "Choose attack, defense, hp, or fights."}), 400

    state.dragon_points -= 1
    if stat == "attack":
        state.dragon_attack += 1
        state.attack += 1
        message = "Your Dragon Point permanently increases attack."
    elif stat == "defense":
        state.dragon_defense += 1
        state.defense += 1
        message = "Your Dragon Point permanently increases defense."
    elif stat == "hp":
        state.dragon_hp += 1
        state.max_hp += 5
        state.hp += 5
        message = "Your Dragon Point permanently increases maximum HP."
    else:
        state.dragon_fights += 1
        state.turns += 1
        message = "Your Dragon Point permanently adds one forest fight to every game day."

    db.session.commit()
    return jsonify(response_payload(state, new_day_log + [message]))
