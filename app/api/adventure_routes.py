import random

from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required

from app.models import AdventureState, db

adventure_routes = Blueprint("adventure", __name__)

ENCOUNTERS = {}
TUTORIAL_PROGRESS = {}

TUTORIAL_CHAIN = [
    [{"id": "beetle", "name": "Scrap Beetle", "hp": 8, "attack": 2, "defense": 0, "gold": (2, 4), "xp": (4, 8)}],
    [
        {"id": "beetle", "name": "Scrap Beetle", "hp": 8, "attack": 2, "defense": 0, "gold": (2, 4), "xp": (4, 8)},
        {"id": "beetle", "name": "Scrap Beetle", "hp": 8, "attack": 2, "defense": 0, "gold": (2, 4), "xp": (4, 8)},
    ],
    [{"id": "scorpion", "name": "Dust Scorpion", "hp": 12, "attack": 3, "defense": 1, "gold": (3, 6), "xp": (6, 10)}],
    [
        {"id": "scorpion", "name": "Dust Scorpion", "hp": 12, "attack": 3, "defense": 1, "gold": (3, 6), "xp": (6, 10)},
        {"id": "beetle", "name": "Scrap Beetle", "hp": 8, "attack": 2, "defense": 0, "gold": (2, 4), "xp": (4, 8)},
    ],
    [
        {"id": "scorpion", "name": "Dust Scorpion", "hp": 12, "attack": 3, "defense": 1, "gold": (3, 6), "xp": (6, 10)},
        {"id": "scorpion", "name": "Dust Scorpion", "hp": 12, "attack": 3, "defense": 1, "gold": (3, 6), "xp": (6, 10)},
        {"id": "beetle", "name": "Scrap Beetle", "hp": 8, "attack": 2, "defense": 0, "gold": (2, 4), "xp": (4, 8)},
    ],
]


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


def format_enemies(enemies):
    """Clone enemies into serializable form with max_hp kept for UI."""
    return [
        {
            "id": e["id"],
            "name": e["name"],
            "hp": e["hp"],
            "max_hp": e["hp"],
            "attack": e["attack"],
            "defense": e["defense"],
            "gold": e["gold"],
            "xp": e["xp"],
        }
        for e in enemies
    ]


def tutorial_progress(user_id):
    idx = TUTORIAL_PROGRESS.get(user_id, 0)
    total = len(TUTORIAL_CHAIN)
    return {"stage": idx + 1, "total": total}


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
    is_tutorial = area == "tutorial"
    area_info = {"name": "Dustfall Tutorial", "requires_level": 1} if is_tutorial else AREAS.get(area, AREAS["fields"])

    if state.level < area_info["requires_level"]:
        return jsonify({"error": f"{area_info['name']} unlocks at level {area_info['requires_level']}."}), 400
    if state.turns <= 0:
        return jsonify({"error": "No turns left. Rest to recover."}), 400

    intro_log = ""
    if is_tutorial:
        idx = min(TUTORIAL_PROGRESS.get(current_user.id, 0), len(TUTORIAL_CHAIN) - 1)
        stage_enemies = TUTORIAL_CHAIN[idx]
        enemies = format_enemies(stage_enemies)
        ENCOUNTERS[current_user.id] = {
            "area": area,
            "enemies": enemies,
            "tutorial_stage": idx,
        }
        names = ", ".join({e["name"] for e in enemies})
        intro_log = f"Tutorial stage {idx + 1}/{len(TUTORIAL_CHAIN)}: {names} await."
    else:
        monster = roll_monster(state.level, area)
        enemies = format_enemies([monster])
        ENCOUNTERS[current_user.id] = {
            "area": area,
            "enemies": enemies,
        }
        intro_log = f"You encounter a {monster['name']} in the {area_info['name']}."

    return jsonify({
        "state": state.to_dict(),
        "battle": {
            "enemies": enemies,
            "player_hp": state.hp,
            "tutorial_progress": tutorial_progress(current_user.id) if is_tutorial else None,
        },
        "log": [intro_log],
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

    enemies = encounter.get("enemies", [])
    area = encounter.get("area")
    log = []

    alive_targets = [e for e in enemies if e["hp"] > 0]

    def end_and_reward():
        gold_gain = sum(random.randint(*e["gold"]) for e in enemies)
        xp_gain = sum(random.randint(*e["xp"]) for e in enemies)
        state.gold += gold_gain
        state.xp += xp_gain
        names = ", ".join({e["name"] for e in enemies})
        log.append(f"You defeated {names}! +{gold_gain} gold, +{xp_gain} xp.")
        level_up_if_needed(state)
        if area == "tutorial":
            idx = encounter.get("tutorial_stage", 0)
            next_idx = (idx + 1) % len(TUTORIAL_CHAIN)
            TUTORIAL_PROGRESS[current_user.id] = next_idx
            log.append(f"Tutorial progress: {next_idx + 1}/{len(TUTORIAL_CHAIN)} ready.")
        clear_encounter(current_user.id)

    state.turns -= 1

    if action == "run":
        if random.random() < 0.65:
            log.append("You successfully fled.")
            clear_encounter(current_user.id)
        else:
            log.append("You failed to flee!")
            total_dmg = 0
            for enemy in alive_targets:
                dmg = max(1, enemy["attack"] - state.defense + random.randint(0, 2))
                total_dmg += dmg
                log.append(f"{enemy['name']} clips you for {dmg} damage.")
            state.hp -= total_dmg
            log.append(f"Your HP: {max(state.hp,0)}")
    else:
        # attack, spell, or defend
        if not alive_targets:
            clear_encounter(current_user.id)
            return jsonify({"error": "No enemies left."}), 400
        target = alive_targets[0]
        dmg_bonus = 0
        if action == "spell":
            dmg_bonus = 2
        dmg_to_monster = max(1, state.attack + dmg_bonus - target["defense"] + random.randint(0, 2))
        target["hp"] = max(0, target["hp"] - dmg_to_monster)
        log.append(f"You strike the {target['name']} for {dmg_to_monster} damage. {target['name']} HP: {target['hp']}")

        if target["hp"] <= 0 and all(e["hp"] <= 0 for e in enemies):
            end_and_reward()
        else:
            incoming = [e for e in enemies if e["hp"] > 0]
            for enemy in incoming:
                dmg_to_player = max(1, enemy["attack"] - state.defense + random.randint(0, 2))
                if action == "defend":
                    dmg_to_player = max(1, dmg_to_player // 2)
                state.hp -= dmg_to_player
                log.append(f"{enemy['name']} hits you for {dmg_to_player} damage.")
            log.append(f"Your HP: {max(state.hp,0)}")
            encounter["enemies"] = enemies

    if state.hp <= 0:
        state.hp = state.max_hp
        state.gold = max(0, state.gold - 5)
        clear_encounter(current_user.id)
        log.append("You were defeated and crawl back to town, losing some gold.")

    db.session.commit()
    return jsonify({
        "state": state.to_dict(),
        "battle": None if not get_encounter(current_user.id) else {
            "enemies": get_encounter(current_user.id)["enemies"],
            "player_hp": state.hp,
            "tutorial_progress": tutorial_progress(current_user.id) if area == "tutorial" else None,
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
