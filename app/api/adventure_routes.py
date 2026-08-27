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
from app.game.world_rules import (
    ACADEMY_TOWN,
    MYSTERY_TOWN,
    STANDARD_TOWNS,
    build_travel_enemy,
    direct_destinations,
    jewelry_info,
    mount_info,
    risky_travel_ambush,
    town_info,
    town_places,
    travels_per_day,
    wander_destination,
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

    if state.town == MYSTERY_TOWN:
        state.town = ACADEMY_TOWN
        log.append("At New Day, Veilcross is gone. You awaken back at Arcana Academy with no road leading to where it stood.")

    state.game_day = current_day
    state.alive = True
    state.hp = state.max_hp
    state.mana = state.max_mana
    state.turns = forest_fights_per_day(state.dragon_fights)
    state.travels = travels_per_day(state.mount)
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
            travels=travels_per_day(""),
            specialty_uses=BASE_SPECIALTY_USES,
            town=ACADEMY_TOWN,
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
        "travel_destination": encounter.get("travel_destination"),
    }


def state_payload(state):
    payload = state.to_dict()
    current_town = town_info(state.town)
    payload.update(
        {
            "title": title_for_dragon_kills(state.dragon_kills),
            "xp_required": xp_required(state.level),
            "can_challenge_master": state.alive
            and state.level < MAX_LEVEL
            and state.xp >= xp_required(state.level),
            "can_hunt_dragon": state.alive and state.level >= MAX_LEVEL,
            "max_forest_fights": forest_fights_per_day(state.dragon_fights),
            "max_travels": travels_per_day(state.mount),
            "effective_attack": effective_attack(state.attack, state.weapon_level),
            "effective_defense": effective_defense(state.defense, state.armor_level),
            "weapon": weapon_for_tier(state.weapon_level),
            "armor": armor_for_tier(state.armor_level),
            "healing_cost": healing_cost(state.hp, state.max_hp, state.level),
            "town_info": {"id": state.town, **current_town},
            "local_places": town_places(state.town),
            "travel_destinations": direct_destinations(state.town),
            "mount_info": mount_info(state.mount),
            "jewelry_info": jewelry_info(state.jewelry),
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
        return "You are dead. The living world is beyond your reach until the next game day."
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

    base_gem_chance = 0.03 if monster.get("hunt_mode") == "slum" else 0.08 if monster.get("hunt_mode") == "thrill" else 0.05
    gem_chance = base_gem_chance + jewelry_info(state.jewelry)["gem_bonus"]
    if random.random() < gem_chance:
        state.gems += 1
        log.append("Something glitters nearby: you found a gem.")

    if (
        monster.get("kind") == "forest"
        and encounter["damage_taken"] == 0
        and monster.get("hunt_mode") != "slum"
    ):
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
    state.travels = travels_per_day(state.mount)
    state.specialty_uses = BASE_SPECIALTY_USES
    state.alive = True
    state.town = ACADEMY_TOWN
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
    elif kind == "travel":
        destination = encounter.get("travel_destination", state.town)
        award_forest_victory(state, encounter, log)
        state.town = destination
        state.location = "town"
        log.append(f"With the road clear, you continue on to {town_info(destination)['name']}.")
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


def complete_travel(state, destination, log):
    previous = town_info(state.town)["name"]
    state.town = destination
    state.location = "town"
    if destination == MYSTERY_TOWN:
        log.append(
            "The road folds strangely around you. Through a curtain of pale mist, a town appears where no town should exist: Veilcross."
        )
    else:
        log.append(f"You travel from {previous} to {town_info(destination)['name']}.")


def start_travel(state, destination, log):
    safe_travel = state.travels > 0
    if safe_travel:
        state.travels -= 1
        complete_travel(state, destination, log)
        return False

    log.append("You have used all of your safe travels for this New Day. You continue anyway, knowing the road is dangerous.")
    if not risky_travel_ambush():
        complete_travel(state, destination, log)
        return False

    monster = build_travel_enemy(state.level)
    state.location = "travel"
    ENCOUNTERS[state.user_id] = {
        "monster": monster,
        "monster_hp": monster["hp"],
        "damage_taken": 0,
        "travel_destination": destination,
    }
    log.append(f"Before you reach your destination, {monster['name']} blocks the road!")
    return True


@adventure_routes.route("/state", methods=["GET"])
@login_required
def get_state():
    state, log = get_or_create_state()
    return jsonify(response_payload(state, log))


@adventure_routes.route("/travel", methods=["POST"])
@login_required
def travel():
    state, new_day_log = get_or_create_state()
    error = town_action_error(state)
    if error:
        return jsonify({"error": error}), 400

    data = request.get_json(silent=True) or {}
    mode = data.get("mode", "direct")
    if mode == "wander":
        destination = wander_destination(state.town)
        log = list(new_day_log)
        log.append("You leave the road signs behind and wander with no destination in mind...")
    else:
        destination = data.get("destination")
        if destination not in STANDARD_TOWNS:
            return jsonify({"error": "That destination cannot be reached by a known road."}), 400
        if destination == state.town:
            return jsonify({"error": "You are already there."}), 400
        log = list(new_day_log)

    started_battle = start_travel(state, destination, log)
    db.session.commit()
    status = 201 if started_battle else 200
    return jsonify(response_payload(state, log)), status


@adventure_routes.route("/local/action", methods=["POST"])
@login_required
def local_action():
    state, new_day_log = get_or_create_state()
    error = town_action_error(state)
    if error:
        return jsonify({"error": error}), 400

    data = request.get_json(silent=True) or {}
    action = data.get("action")
    log = list(new_day_log)

    if state.town == "highfield" and action == "buy_courser":
        if state.mount in {"plains_courser", "mistwalker"}:
            return jsonify({"error": "You already own a mount at least this capable."}), 400
        if state.gold < 400 or state.gems < 1:
            return jsonify({"error": "A Plains Courser costs 400 gold and 1 gem."}), 400
        state.gold -= 400
        state.gems -= 1
        state.mount = "plains_courser"
        state.travels += 1
        log.append("Highfield Stable sells you a Plains Courser. You gain +1 safe travel every New Day.")

    elif state.town == "highfield" and action == "bar_meal":
        if state.gold < 15:
            return jsonify({"error": "A hot meal and drink at The Copper Cup costs 15 gold."}), 400
        state.gold -= 15
        healed = min(state.max_hp - state.hp, 4)
        restored = min(state.max_mana - state.mana, 2)
        state.hp += healed
        state.mana += restored
        log.append(f"The Copper Cup restores {healed} HP and {restored} Mana for 15 gold.")

    elif state.town == "highfield" and action in {"pawn_weapon", "pawn_armor"}:
        is_weapon = action == "pawn_weapon"
        tier = state.weapon_level if is_weapon else state.armor_level
        catalog = WEAPONS if is_weapon else ARMORS
        if tier <= 0:
            return jsonify({"error": f"You have no upgraded {'weapon' if is_weapon else 'armor'} to pawn."}), 400
        value = max(1, catalog[tier]["cost"] // 2)
        item_name = catalog[tier]["name"]
        state.gold += value
        if is_weapon:
            state.weapon_level = 0
        else:
            state.armor_level = 0
        log.append(f"The Highfield pawn broker gives you {value} gold for {item_name}.")

    elif state.town == "highfield" and action == "buy_ration":
        if state.gold < 50:
            return jsonify({"error": "Road provisions cost 50 gold."}), 400
        if state.travels >= travels_per_day(state.mount) + 2:
            return jsonify({"error": "You cannot carry any more road provisions today."}), 400
        state.gold -= 50
        state.travels += 1
        log.append("The Plains Merchant packs you fresh road provisions. You gain 1 additional safe travel today.")

    elif state.town == "lunewater" and action == "buy_pendant":
        if state.jewelry == "moonwater_pendant":
            return jsonify({"error": "You already wear a Moonwater Pendant."}), 400
        if state.gold < 250 or state.gems < 2:
            return jsonify({"error": "The Moonwater Pendant costs 250 gold and 2 gems."}), 400
        state.gold -= 250
        state.gems -= 2
        state.jewelry = "moonwater_pendant"
        log.append("The Moonstone Jeweler fits you with a Moonwater Pendant. Your chance to find gems after victories increases.")

    elif state.town == "lunewater" and action == "river_tonic":
        if state.gold < 25:
            return jsonify({"error": "Moonwater tonic costs 25 gold."}), 400
        state.gold -= 25
        restored = min(state.max_mana - state.mana, 4)
        state.mana += restored
        log.append(f"A cool Moonwater tonic restores {restored} Mana.")

    elif state.town == "lunewater" and action == "inn_rest":
        if state.gold < 20:
            return jsonify({"error": "A room at The Willow Inn costs 20 gold."}), 400
        state.gold -= 20
        healed = min(state.max_hp - state.hp, max(3, state.max_hp // 3))
        state.hp += healed
        log.append(f"A quiet rest at The Willow Inn restores {healed} HP.")

    elif state.town == "lunewater" and action == "alchemist_draught":
        if state.gold < 40:
            return jsonify({"error": "Silverleaf Mana Draught costs 40 gold."}), 400
        state.gold -= 40
        restored = min(state.max_mana - state.mana, 6)
        state.mana += restored
        log.append(f"Silverleaf Mana Draught restores {restored} Mana.")

    elif state.town == "stonevein" and action == "etch_mana_rune":
        if state.mana_runes >= 10:
            return jsonify({"error": "The Rune Hall says your mortal frame cannot hold another Mana rune."}), 400
        cost = 200 + state.mana_runes * 100
        if state.gold < cost or state.gems < 1:
            return jsonify({"error": f"Your next Mana rune costs {cost} gold and 1 gem."}), 400
        state.gold -= cost
        state.gems -= 1
        state.mana_runes += 1
        state.max_mana += 1
        state.mana += 1
        log.append(f"The Rune Hall etches a permanent Mana rune into your training focus. Maximum Mana rises to {state.max_mana}.")

    elif state.town == "stonevein" and action == "sell_gem":
        if state.gems < 1:
            return jsonify({"error": "You have no gem to sell."}), 400
        state.gems -= 1
        state.gold += 175
        log.append("The Stonevein Gem Broker pays you 175 gold for a raw gem.")

    elif state.town == "stonevein" and action == "stonebarrel_meal":
        if state.gold < 20:
            return jsonify({"error": "Stonebarrel stew and ale costs 20 gold."}), 400
        state.gold -= 20
        healed = min(state.max_hp - state.hp, 5)
        restored = min(state.max_mana - state.mana, 3)
        state.hp += healed
        state.mana += restored
        log.append(f"Stonebarrel fare restores {healed} HP and {restored} Mana.")

    elif state.town == MYSTERY_TOWN and action == "whispering_well":
        if state.gems < 1:
            return jsonify({"error": "The Whispering Well accepts only a gem."}), 400
        state.gems -= 1
        restored = state.max_mana - state.mana
        state.mana = state.max_mana
        log.append(f"The gem disappears before it reaches the water. Your Mana is fully restored (+{restored}).")

    elif state.town == MYSTERY_TOWN and action == "curio_trade":
        if state.gems < 1:
            return jsonify({"error": "The Curio Dealer wants one gem."}), 400
        state.gems -= 1
        gold = random.randint(125, 325)
        state.gold += gold
        log.append(f"The Curio Dealer weighs your gem, smiles without explanation, and gives you {gold} gold.")

    elif state.town == MYSTERY_TOWN and action == "mystery_rest":
        cost = 30
        if state.gold < cost:
            return jsonify({"error": "The Lanternless Inn asks for 30 gold."}), 400
        state.gold -= cost
        state.hp = state.max_hp
        log.append("You sleep without remembering closing your eyes. You awaken fully healed.")

    elif state.town == MYSTERY_TOWN and action == "buy_mistwalker":
        if state.mount == "mistwalker":
            return jsonify({"error": "The Mistwalker already follows you."}), 400
        if state.gold < 750 or state.gems < 3:
            return jsonify({"error": "The Mistwalker costs 750 gold and 3 gems."}), 400
        previous_bonus = mount_info(state.mount)["travel_bonus"]
        state.gold -= 750
        state.gems -= 3
        state.mount = "mistwalker"
        new_bonus = mount_info(state.mount)["travel_bonus"]
        state.travels += max(0, new_bonus - previous_bonus)
        log.append("A pale Mistwalker chooses you at the Lost Stable. It grants +2 safe travels every New Day.")

    else:
        return jsonify({"error": "That service is not available in this town."}), 400

    db.session.commit()
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
        if monster["kind"] not in {"forest", "travel"}:
            return jsonify({"error": "You cannot flee this challenge."}), 400
        if random.random() < 0.65:
            clear_encounter(state.user_id)
            state.location = "town"
            db.session.commit()
            message = "You escape back toward town." if monster["kind"] == "forest" else "You abandon the dangerous road and retreat to the town you came from."
            return jsonify(response_payload(state, log + [message]))

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
