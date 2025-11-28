from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required

from app.game.engine import GameService, state_to_dict

game_routes = Blueprint("game", __name__)
service = GameService()


@game_routes.route("/session", methods=["POST"])
@login_required
def start_session():
    state = service.create_session(current_user.id)
    return jsonify(state_to_dict(state)), 201


@game_routes.route("/session/<session_id>", methods=["GET"])
@login_required
def get_state(session_id):
    state = service.get_session(session_id, current_user.id)
    if not state:
        return jsonify({"error": "Session not found"}), 404
    return jsonify(state_to_dict(state))


@game_routes.route("/session/<session_id>/move", methods=["POST"])
@login_required
def move(session_id):
    state = service.get_session(session_id, current_user.id)
    if not state:
        return jsonify({"error": "Session not found"}), 404
    data = request.get_json() or {}
    direction = data.get("direction")
    err = service.move(state, state.current_entity().id, direction)
    if err:
        return jsonify({"error": err}), 400
    # let AI respond
    service.end_turn(state)
    service.ai_take_turn(state)
    return jsonify(state_to_dict(state))


@game_routes.route("/session/<session_id>/attack", methods=["POST"])
@login_required
def attack(session_id):
    state = service.get_session(session_id, current_user.id)
    if not state:
        return jsonify({"error": "Session not found"}), 404
    data = request.get_json() or {}
    target_id = data.get("target_id")
    err = service.attack(state, state.current_entity().id, target_id)
    if err:
        return jsonify({"error": err}), 400
    # let AI respond
    service.end_turn(state)
    service.ai_take_turn(state)
    return jsonify(state_to_dict(state))
