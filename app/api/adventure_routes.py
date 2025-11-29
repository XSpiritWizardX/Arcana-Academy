import random

from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required

from app.models import AdventureState, db

adventure_routes = Blueprint("adventure", __name__)


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


def roll_monster(level: int):
    pool = [
        {"id": "rat", "name": "Forest Rat", "hp": 6, "attack": 2, "defense": 0, "gold": (1, 5), "xp": (3, 6)},
        {"id": "wolf", "name": "Wolf", "hp": 10, "attack": 3, "defense": 1, "gold": (4, 10), "xp": (6, 12)},
        {"id": "bandit", "name": "Bandit", "hp": 12, "attack": 4, "defense": 2, "gold": (8, 16), "xp": (10, 18)},
        {"id": "dragon", "name": "Green Dragon", "hp": 40, "attack": 8, "defense": 4, "gold": (25, 40), "xp": (40, 80)},
    ]
    if level < 3:
        return random.choice(pool[:2])
    if level < 5:
        return random.choice(pool[:3])
    return pool[-1]


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


@adventure_routes.route("/explore", methods=["POST"])
@login_required
def explore():
    state = get_or_create_state()
    if state.turns <= 0:
        return jsonify({"error": "No turns left. Rest to recover."}), 400

    monster = roll_monster(state.level)
    log = []
    monster_hp = monster["hp"]
    battle_log = []

    while state.turns > 0 and monster_hp > 0 and state.hp > 0:
        state.turns -= 1
        dmg_to_monster = max(1, state.attack - monster["defense"] + random.randint(0, 2))
        monster_hp -= dmg_to_monster
        battle_log.append(
            f"You strike the {monster['name']} for {dmg_to_monster} damage. "
            f"Monster HP: {max(monster_hp, 0)}"
        )

        if monster_hp <= 0:
            break

        dmg_to_player = max(1, monster["attack"] - state.defense + random.randint(0, 2))
        state.hp -= dmg_to_player
        battle_log.append(
            f"{monster['name']} hits you for {dmg_to_player} damage. "
            f"Your HP: {max(state.hp, 0)}"
        )

    if state.hp <= 0:
        state.hp = state.max_hp
        state.gold = max(0, state.gold - 5)
        db.session.commit()
        log.append("You were defeated and crawl back to town, losing some gold.")
        return jsonify({"state": state.to_dict(), "log": log + battle_log, "battle": {
            "monster": monster["name"],
            "monster_hp": max(monster_hp, 0),
            "player_hp": state.hp
        }})

    if monster_hp <= 0:
        gold_gain = random.randint(*monster["gold"])
        xp_gain = random.randint(*monster["xp"])
        state.gold += gold_gain
        state.xp += xp_gain
        log.append(f"You defeated the {monster['name']}! +{gold_gain} gold, +{xp_gain} xp.")
        level_up_if_needed(state)
    else:
        log.append("The monster survives. You may need more turns to finish it.")

    db.session.commit()
    return jsonify({"state": state.to_dict(), "log": log + battle_log, "battle": {
        "monster": monster["name"],
        "monster_hp": max(monster_hp, 0),
        "player_hp": state.hp
    }})


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
