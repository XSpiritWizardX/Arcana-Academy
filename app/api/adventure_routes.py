import random

from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required

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
    needed = state.level * 50
    while state.xp >= needed:
        state.level += 1
        state.max_hp += 5
        state.attack += 1
        state.defense += 1
        state.hp = state.max_hp
        needed = state.level * 50


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


def roll_monster(level: int, area_key: str):
    area = AREAS.get(area_key, AREAS["fields"])
    pool = area["monsters"]
    # weight higher-level monsters slightly as level increases
    if len(pool) > 1 and level > area["requires_level"] + 2:
        return random.choice(pool[1:])
    return random.choice(pool)


def clear_encounter(user_id: int):
    if user_id in ENCOUNTERS:
        ENCOUNTERS.pop(user_id, None)


def get_encounter(user_id: int):
    return ENCOUNTERS.get(user_id)


@adventure_routes.route("/state", methods=["GET"])
@login_required
def get_state():
    state = get_or_create_state()
    return jsonify({"state": state.to_dict()})


@adventure_routes.route("/rest", methods=["POST"])
@login_required
def rest():
    state = get_or_create_state()
    state.hp = state.max_hp
    state.turns = 10
    db.session.commit()
    return jsonify({"state": state.to_dict()})


@adventure_routes.route("/start", methods=["POST"])
@login_required
def start_encounter():
    state = get_or_create_state()
    data = request.get_json(silent=True) or {}
    area = data.get("area", "fields")
    area_info = AREAS.get(area, AREAS["fields"])

    if state.level < area_info["requires_level"]:
        return jsonify({"error": f"{area_info['name']} unlocks at level {area_info['requires_level']}."}), 400
    if state.turns <= 0:
        return jsonify({"error": "No turns left. Rest to recover."}), 400

    monster = roll_monster(state.level, area)
    ENCOUNTERS[current_user.id] = {
        "area": area,
        "monster": monster,
        "monster_hp": monster["hp"],
    }
    return jsonify({
        "state": state.to_dict(),
        "battle": {
            "monster": monster["name"],
            "monster_hp": monster["hp"],
            "max_monster_hp": monster["hp"],
            "player_hp": state.hp,
        },
        "log": [f"You encounter a {monster['name']} in the {area_info['name']}."],
    })


@adventure_routes.route("/action", methods=["POST"])
@login_required
def take_action():
    state = get_or_create_state()
    data = request.get_json(silent=True) or {}
    action = data.get("action")
    encounter = get_encounter(current_user.id)
    if not encounter:
        return jsonify({"error": "No active encounter. Start a hunt first."}), 400
    if state.turns <= 0:
        clear_encounter(current_user.id)
        return jsonify({"error": "No turns left. Rest to recover."}), 400

    monster = encounter["monster"]
    monster_hp = encounter["monster_hp"]
    log = []

    def end_and_reward():
        gold_gain = random.randint(*monster["gold"])
        xp_gain = random.randint(*monster["xp"])
        state.gold += gold_gain
        state.xp += xp_gain
        log.append(f"You defeated the {monster['name']}! +{gold_gain} gold, +{xp_gain} xp.")
        level_up_if_needed(state)
        clear_encounter(current_user.id)

    state.turns -= 1

    if action == "run":
        if random.random() < 0.65:
            log.append("You successfully fled.")
            clear_encounter(current_user.id)
        else:
            log.append("You failed to flee!")
            dmg_to_player = max(1, monster["attack"] - state.defense + random.randint(0, 2))
            state.hp -= dmg_to_player
            log.append(f"{monster['name']} hits you for {dmg_to_player} damage. Your HP: {max(state.hp,0)}")
    else:
        # attack or defend
        dmg_bonus = 0
        if action == "spell":
            dmg_bonus = 2
        dmg_to_monster = max(1, state.attack + dmg_bonus - monster["defense"] + random.randint(0, 2))
        monster_hp -= dmg_to_monster
        log.append(f"You strike the {monster['name']} for {dmg_to_monster} damage. Monster HP: {max(monster_hp,0)}")

        if monster_hp <= 0:
            encounter["monster_hp"] = 0
            end_and_reward()
        else:
            dmg_to_player = max(1, monster["attack"] - state.defense + random.randint(0, 2))
            if action == "defend":
                dmg_to_player = max(1, dmg_to_player // 2)
            state.hp -= dmg_to_player
            log.append(f"{monster['name']} hits you for {dmg_to_player} damage. Your HP: {max(state.hp,0)}")
            encounter["monster_hp"] = monster_hp

    if state.hp <= 0:
        state.hp = state.max_hp
        state.gold = max(0, state.gold - 5)
        clear_encounter(current_user.id)
        log.append("You were defeated and crawl back to town, losing some gold.")

    db.session.commit()
    return jsonify({
        "state": state.to_dict(),
        "battle": None if not get_encounter(current_user.id) else {
            "monster": monster["name"],
            "monster_hp": get_encounter(current_user.id)["monster_hp"],
            "max_monster_hp": monster["hp"],
            "player_hp": state.hp,
        },
        "log": log,
    })


@adventure_routes.route("/bank/deposit", methods=["POST"])
@login_required
def bank_deposit():
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
    return jsonify({"state": state.to_dict(), "log": [f"You deposit {amount} gold."]})


@adventure_routes.route("/bank/withdraw", methods=["POST"])
@login_required
def bank_withdraw():
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
    return jsonify({"state": state.to_dict(), "log": [f"You withdraw {amount} gold."]})


@adventure_routes.route("/train", methods=["POST"])
@login_required
def train():
    state = get_or_create_state()
    data = request.get_json() or {}
    stat = data.get("stat", "attack")
    cost = 20
    if state.gold < cost:
        return jsonify({"error": "Not enough gold to train"}), 400
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
    return jsonify({"state": state.to_dict(), "log": [msg]})
