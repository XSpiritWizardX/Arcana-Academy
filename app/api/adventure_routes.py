import random

from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required

from app.game.adventure_rules import (
    INTENT_GUARD,
    INTENT_HEAVY,
    VALID_ACTIONS,
    calculate_monster_damage,
    calculate_player_damage,
    defeat_gold_loss,
    intent_message,
    is_dragon_boss,
    roll_monster_intent,
    training_cost,
)
from app.models import AdventureState, db

adventure_routes = Blueprint("adventure", __name__)

ENCOUNTERS = {}


def get_or_create_state():
    state = AdventureState.query.filter_by(user_id=current_user.id).first()
    if not state:
        state = AdventureState(user_id=current_user.id)
        db.session.add(state)
        db.session.commit()
    return state


def level_up_if_needed(state: AdventureState):
    levels_gained = 0
    needed = state.level * 50
    while state.xp >= needed:
        state.level += 1
        state.max_hp += 5
        state.attack += 1
        state.defense += 1
        state.hp = state.max_hp
        levels_gained += 1
        needed = state.level * 50
    return levels_gained


AREAS = {
    "fields": {
        "name": "Fields",
        "requires_level": 1,
        "monsters": [
            {"id": "rat", "name": "Field Rat", "hp": 6, "attack": 2, "defense": 0, "gold": (1, 5), "xp": (3, 6)},
            {"id": "wolf", "name": "Stray Wolf", "hp": 10, "attack": 3, "defense": 1, "gold": (4, 10), "xp": (6, 12)},
            {"id": "boar", "name": "Wild Boar", "hp": 12, "attack": 3, "defense": 1, "gold": (5, 10), "xp": (7, 12)},
        ],
    },
    "forest": {
        "name": "Forest",
        "requires_level": 3,
        "monsters": [
            {"id": "bandit", "name": "Forest Bandit", "hp": 24, "attack": 7, "defense": 3, "gold": (12, 20), "xp": (16, 26)},
            {"id": "bear", "name": "Wild Bear", "hp": 30, "attack": 8, "defense": 3, "gold": (14, 24), "xp": (18, 28)},
            {"id": "ent", "name": "Young Ent", "hp": 34, "attack": 9, "defense": 4, "gold": (16, 26), "xp": (20, 32)},
        ],
    },
    "graveyard": {
        "name": "Graveyard",
        "requires_level": 8,
        "monsters": [
            {"id": "ghost", "name": "Restless Ghost", "hp": 40, "attack": 10, "defense": 5, "gold": (18, 32), "xp": (26, 42)},
            {"id": "wraith", "name": "Wraith", "hp": 48, "attack": 12, "defense": 6, "gold": (20, 36), "xp": (30, 48)},
            {"id": "lichling", "name": "Lichling", "hp": 54, "attack": 13, "defense": 6, "gold": (22, 38), "xp": (34, 52)},
        ],
    },
    "mountain": {
        "name": "Mountain",
        "requires_level": 15,
        "monsters": [
            {"id": "dragonling", "name": "Dragonling", "hp": 70, "attack": 16, "defense": 8, "gold": (26, 44), "xp": (40, 64)},
            {"id": "dragon", "name": "Green Dragon", "hp": 110, "attack": 20, "defense": 10, "gold": (40, 70), "xp": (70, 120)},
            {"id": "golem", "name": "Stone Golem", "hp": 90, "attack": 18, "defense": 9, "gold": (30, 52), "xp": (48, 84)},
        ],
    },
    "desert": {
        "name": "Desert",
        "requires_level": 20,
        "monsters": [
            {"id": "scorpion", "name": "Giant Scorpion", "hp": 90, "attack": 20, "defense": 9, "gold": (34, 56), "xp": (52, 86)},
            {"id": "sandwraith", "name": "Sand Wraith", "hp": 100, "attack": 22, "defense": 10, "gold": (36, 60), "xp": (58, 94)},
            {"id": "djinn", "name": "Lesser Djinn", "hp": 110, "attack": 24, "defense": 11, "gold": (40, 64), "xp": (64, 102)},
        ],
    },
    "swamp": {
        "name": "Swamp",
        "requires_level": 25,
        "monsters": [
            {"id": "boglurker", "name": "Bog Lurker", "hp": 120, "attack": 26, "defense": 12, "gold": (40, 68), "xp": (70, 110)},
            {"id": "hydraling", "name": "Hydra Spawn", "hp": 135, "attack": 28, "defense": 13, "gold": (42, 72), "xp": (76, 120)},
            {"id": "witch", "name": "Swamp Witch", "hp": 130, "attack": 29, "defense": 12, "gold": (44, 76), "xp": (80, 126)},
        ],
    },
    "ruins": {
        "name": "Ruins",
        "requires_level": 30,
        "monsters": [
            {"id": "skeletonking", "name": "Skeleton King", "hp": 150, "attack": 32, "defense": 14, "gold": (48, 80), "xp": (90, 140)},
            {"id": "gargoyle", "name": "Gargoyle", "hp": 165, "attack": 34, "defense": 15, "gold": (50, 84), "xp": (96, 150)},
            {"id": "warlock", "name": "Ancient Warlock", "hp": 160, "attack": 36, "defense": 14, "gold": (54, 88), "xp": (102, 158)},
        ],
    },
    "volcano": {
        "name": "Volcano",
        "requires_level": 35,
        "monsters": [
            {"id": "magmaling", "name": "Magmaling", "hp": 190, "attack": 38, "defense": 18, "gold": (60, 96), "xp": (120, 190)},
            {"id": "firegiant", "name": "Fire Giant", "hp": 210, "attack": 42, "defense": 20, "gold": (70, 110), "xp": (140, 210)},
            {"id": "phoenix", "name": "Phoenix", "hp": 200, "attack": 44, "defense": 18, "gold": (74, 118), "xp": (150, 225)},
        ],
    },
    "sky": {
        "name": "Sky",
        "requires_level": 40,
        "monsters": [
            {"id": "griffin", "name": "Griffin", "hp": 230, "attack": 46, "defense": 22, "gold": (80, 126), "xp": (170, 260)},
            {"id": "stormdrake", "name": "Storm Drake", "hp": 260, "attack": 50, "defense": 24, "gold": (90, 138), "xp": (190, 290)},
            {"id": "celestial", "name": "Celestial Guardian", "hp": 300, "attack": 55, "defense": 26, "gold": (100, 150), "xp": (220, 340)},
        ],
    },
    "abyss": {
        "name": "Abyss",
        "requires_level": 50,
        "monsters": [
            {"id": "voidspawn", "name": "Void Spawn", "hp": 340, "attack": 60, "defense": 30, "gold": (120, 180), "xp": (260, 380)},
            {"id": "eldritch", "name": "Eldritch Horror", "hp": 380, "attack": 65, "defense": 32, "gold": (130, 200), "xp": (300, 420)},
            {"id": "abyssal_dragon", "name": "Abyssal Dragon", "hp": 420, "attack": 70, "defense": 35, "gold": (150, 240), "xp": (340, 480)},
        ],
    },
}


def area_summaries():
    return [
        {
            "id": area_id,
            "name": area["name"],
            "requires_level": area["requires_level"],
        }
        for area_id, area in AREAS.items()
    ]


def roll_monster(level: int, area_key: str):
    area = AREAS[area_key]
    pool = area["monsters"]
    if len(pool) > 1 and level > area["requires_level"] + 2:
        return random.choice(pool[1:])
    return random.choice(pool)


def clear_encounter(user_id: int):
    ENCOUNTERS.pop(user_id, None)


def get_encounter(user_id: int):
    return ENCOUNTERS.get(user_id)


def battle_to_dict(state: AdventureState, encounter):
    if not encounter:
        return None
    monster = encounter["monster"]
    intent = encounter["monster_intent"]
    return {
        "area": encounter["area"],
        "monster": monster["name"],
        "monster_hp": encounter["monster_hp"],
        "max_monster_hp": monster["hp"],
        "player_hp": state.hp,
        "round": encounter["round"],
        "spell_cooldown": encounter["spell_cooldown"],
        "intent": intent,
        "intent_message": intent_message(monster["name"], intent),
    }


def adventure_payload(state: AdventureState, log=None):
    encounter = get_encounter(current_user.id)
    payload = {
        "state": state.to_dict(),
        "battle": battle_to_dict(state, encounter),
        "areas": area_summaries(),
        "training_cost": training_cost(state.level),
        "next_level_xp": state.level * 50,
    }
    if log is not None:
        payload["log"] = log
    return payload


def reject_town_action_during_battle():
    if get_encounter(current_user.id):
        return jsonify({"error": "Finish the encounter or flee before using town actions."}), 400
    return None


@adventure_routes.route("/state", methods=["GET"])
@login_required
def get_state():
    state = get_or_create_state()
    return jsonify(adventure_payload(state))


@adventure_routes.route("/rest", methods=["POST"])
@login_required
def rest():
    blocked = reject_town_action_during_battle()
    if blocked:
        return blocked
    state = get_or_create_state()
    state.hp = state.max_hp
    state.turns = 10
    db.session.commit()
    return jsonify(adventure_payload(state, ["You rest at the inn, restoring HP and turns."]))


@adventure_routes.route("/start", methods=["POST"])
@login_required
def start_encounter():
    state = get_or_create_state()
    if get_encounter(current_user.id):
        return jsonify({"error": "You are already in combat. Finish the fight or flee first."}), 400

    data = request.get_json(silent=True) or {}
    area = data.get("area", "fields")
    if area not in AREAS:
        return jsonify({"error": "Unknown adventure area."}), 400

    area_info = AREAS[area]
    if state.level < area_info["requires_level"]:
        return jsonify({"error": f"{area_info['name']} unlocks at level {area_info['requires_level']}."}), 400
    if state.turns <= 0:
        return jsonify({"error": "No turns left. Rest to recover."}), 400

    monster = roll_monster(state.level, area)
    encounter = {
        "area": area,
        "monster": monster,
        "monster_hp": monster["hp"],
        "round": 1,
        "spell_cooldown": 0,
        "monster_intent": roll_monster_intent(),
    }
    ENCOUNTERS[current_user.id] = encounter
    log = [
        f"You encounter a {monster['name']} in the {area_info['name']}.",
        intent_message(monster["name"], encounter["monster_intent"]),
    ]
    return jsonify(adventure_payload(state, log))


@adventure_routes.route("/action", methods=["POST"])
@login_required
def take_action():
    state = get_or_create_state()
    data = request.get_json(silent=True) or {}
    action = data.get("action")
    encounter = get_encounter(current_user.id)

    if not encounter:
        return jsonify({"error": "No active encounter. Start a hunt first."}), 400
    if action not in VALID_ACTIONS:
        return jsonify({"error": "Choose attack, spell, defend, or run."}), 400
    if action == "spell" and encounter["spell_cooldown"] > 0:
        return jsonify({"error": f"Arcane Blast is ready in {encounter['spell_cooldown']} round(s)."}), 400
    if state.turns <= 0:
        clear_encounter(current_user.id)
        return jsonify({"error": "No turns left. Rest to recover."}), 400

    monster = encounter["monster"]
    monster_intent = encounter["monster_intent"]
    log = []
    state.turns -= 1

    def end_and_reward():
        gold_gain = random.randint(*monster["gold"])
        xp_gain = random.randint(*monster["xp"])
        state.gold += gold_gain
        state.xp += xp_gain
        if is_dragon_boss(monster["id"]):
            state.dragon_kills += 1
            log.append("Dragon slain! Your dragon-kill record increases.")
        log.append(f"You defeated the {monster['name']}! +{gold_gain} gold, +{xp_gain} xp.")
        levels_gained = level_up_if_needed(state)
        if levels_gained:
            log.append(f"Level up! You reached level {state.level} and your HP is fully restored.")
        clear_encounter(current_user.id)

    if action == "run":
        if random.random() < 0.65:
            log.append("You successfully fled back to town.")
            clear_encounter(current_user.id)
        else:
            log.append("You failed to flee!")
            damage = calculate_monster_damage(
                monster["attack"],
                state.defense,
                monster_intent,
                defending=False,
            )
            if damage:
                state.hp -= damage
                if monster_intent == INTENT_HEAVY:
                    log.append(f"{monster['name']} punishes the escape with a crushing blow for {damage} damage.")
                else:
                    log.append(f"{monster['name']} hits you for {damage} damage.")
            else:
                log.append(f"{monster['name']} stays behind its guard instead of pursuing.")
    else:
        defending = action == "defend"
        if defending:
            log.append("You brace for impact, sacrificing your attack to sharply reduce incoming damage.")
        else:
            damage, critical = calculate_player_damage(
                state.attack,
                monster["defense"],
                action,
                monster_intent,
            )
            encounter["monster_hp"] -= damage
            if action == "spell":
                encounter["spell_cooldown"] = 2
                log.append(f"Arcane Blast tears through the {monster['name']} for {damage} damage.")
            else:
                prefix = "Critical hit! " if critical else ""
                if monster_intent == INTENT_GUARD:
                    log.append(f"{prefix}The {monster['name']}'s guard absorbs part of your strike: {damage} damage.")
                else:
                    log.append(f"{prefix}You strike the {monster['name']} for {damage} damage.")

        if encounter["monster_hp"] <= 0:
            encounter["monster_hp"] = 0
            end_and_reward()
        else:
            damage = calculate_monster_damage(
                monster["attack"],
                state.defense,
                monster_intent,
                defending=defending,
            )
            if damage:
                state.hp -= damage
                if monster_intent == INTENT_HEAVY:
                    log.append(f"{monster['name']} unleashes its heavy attack for {damage} damage.")
                else:
                    log.append(f"{monster['name']} strikes for {damage} damage.")
            else:
                log.append(f"{monster['name']} holds its guard and does not attack this round.")

    if state.hp <= 0:
        loss = defeat_gold_loss(state.gold)
        state.hp = state.max_hp
        state.gold -= loss
        clear_encounter(current_user.id)
        log.append(f"You were defeated and return to town, losing {loss} carried gold.")
    elif get_encounter(current_user.id):
        encounter = get_encounter(current_user.id)
        if action != "spell" and encounter["spell_cooldown"] > 0:
            encounter["spell_cooldown"] -= 1

        if state.turns <= 0:
            clear_encounter(current_user.id)
            log.append("Exhausted, you retreat to town. Rest before hunting again.")
        else:
            encounter["round"] += 1
            encounter["monster_intent"] = roll_monster_intent()
            log.append(intent_message(monster["name"], encounter["monster_intent"]))

    db.session.commit()
    return jsonify(adventure_payload(state, log))


@adventure_routes.route("/bank/deposit", methods=["POST"])
@login_required
def bank_deposit():
    blocked = reject_town_action_during_battle()
    if blocked:
        return blocked
    state = get_or_create_state()
    data = request.get_json() or {}
    amount = int(data.get("amount", 0))
    if amount <= 0:
        return jsonify({"error": "Deposit must be positive"}), 400
    if state.gold < amount:
        return jsonify({"error": "Not enough gold"}), 400
    state.gold -= amount
    state.bank_gold += amount
    db.session.commit()
    return jsonify(adventure_payload(state, [f"You deposit {amount} gold."]))


@adventure_routes.route("/bank/withdraw", methods=["POST"])
@login_required
def bank_withdraw():
    blocked = reject_town_action_during_battle()
    if blocked:
        return blocked
    state = get_or_create_state()
    data = request.get_json() or {}
    amount = int(data.get("amount", 0))
    if amount <= 0:
        return jsonify({"error": "Withdraw must be positive"}), 400
    if state.bank_gold < amount:
        return jsonify({"error": "Not enough gold in bank"}), 400
    state.bank_gold -= amount
    state.gold += amount
    db.session.commit()
    return jsonify(adventure_payload(state, [f"You withdraw {amount} gold."]))


@adventure_routes.route("/train", methods=["POST"])
@login_required
def train():
    blocked = reject_town_action_during_battle()
    if blocked:
        return blocked
    state = get_or_create_state()
    data = request.get_json() or {}
    stat = data.get("stat", "attack")
    cost = training_cost(state.level)
    if state.gold < cost:
        return jsonify({"error": f"Not enough gold to train. Training costs {cost} gold."}), 400
    state.gold -= cost
    if stat == "defense":
        state.defense += 1
        msg = "Defense increased."
    elif stat == "hp":
        state.max_hp += 2
        state.hp = state.max_hp
        msg = "Max HP increased."
    else:
        state.attack += 1
        msg = "Attack increased."
    db.session.commit()
    return jsonify(adventure_payload(state, [f"{msg} Training cost: {cost} gold."]))
