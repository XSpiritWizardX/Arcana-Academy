from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required

from app.api.upload_helper import (
    allowed_file,
    get_unique_filename,
    upload_file_to_cloudinary,
)
from app.models import Player, db

player_routes = Blueprint('players', __name__)


def _parse_decimal(field_name, value):
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        raise ValueError(f"{field_name} must be a number")


@player_routes.route('/all')

def get_all_players():
    """
    Get all players.
    """
    players = Player.query.all()
    return jsonify({'players': [player.to_dict() for player in players]})


@player_routes.route('/')
@login_required
def get_players():
    """
    Get all players for the logged-in user.
    """
    players = Player.query.filter_by(user_id=current_user.id).all()
    return jsonify({'players': [player.to_dict() for player in players]})


@player_routes.route('/<int:id>')
def get_player(id):
    """
    Get a player by ID.
    """
    player = Player.query.filter_by(id=id).first()

    if not player:
        return jsonify({'error': 'Player not found'}), 404

    return jsonify(player.to_dict())


@player_routes.route('/', methods=['POST'])
@login_required
def create_player():
    """
    Create a new player for the logged-in user.
    """
    image = request.files.get("image")
    data = request.form if request.form else (request.get_json(silent=True) or {})

    if not image:
        return jsonify({'error': 'Player image is required'}), 400
    if not allowed_file(image.filename):
        return jsonify({'error': 'File type not permitted'}), 400

    image.filename = get_unique_filename(image.filename)
    upload = upload_file_to_cloudinary(image)
    if "url" not in upload:
        return jsonify(upload), 400

    url = upload["url"]
    name = data.get("name")
    magic_class = data.get("magic_class")
    element = data.get("element")

    try:
        level = _parse_decimal("level", data.get("level"))
        xp = _parse_decimal("xp", data.get("xp"))
        gold = _parse_decimal("gold", data.get("gold"))
        health = _parse_decimal("health", data.get("health"))
        mana = _parse_decimal("mana", data.get("mana"))
        damage = _parse_decimal("damage", data.get("damage"))
        speed = _parse_decimal("speed", data.get("speed"))
        strength = _parse_decimal("strength", data.get("strength"))
        intellect = _parse_decimal("intellect", data.get("intellect"))
        dexterity = _parse_decimal("dexterity", data.get("dexterity"))
        vitality = _parse_decimal("vitality", data.get("vitality"))
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    if not name:
        return jsonify({'error': 'Player name is required'}), 400
    if not magic_class:
        return jsonify({'error': 'Player magic_class is required'}), 400
    if not url:
        return jsonify({'error': 'Player URL is required'}), 400
    if not element:
        return jsonify({'error': 'Player element is required'}), 400
    if level is None:
        return jsonify({'error': 'Player level is required'}), 400
    if xp is None:
        return jsonify({'error': 'Player xp is required'}), 400
    if gold is None:
        return jsonify({'error': 'Player gold is required'}), 400
    if health is None:
        return jsonify({'error': 'Player health is required'}), 400
    if mana is None:
        return jsonify({'error': 'Player mana is required'}), 400
    if damage is None:
        return jsonify({'error': 'Player damage is required'}), 400
    if speed is None:
        return jsonify({'error': 'Player speed is required'}), 400
    if strength is None:
        return jsonify({'error': 'Player strength is required'}), 400
    if intellect is None:
        return jsonify({'error': 'Player intellect is required'}), 400
    if dexterity is None:
        return jsonify({'error': 'Player dexterity is required'}), 400
    if vitality is None:
        return jsonify({'error': 'Player vitality is required'}), 400




    # Check if the player already exists for the user
    existing_player = Player.query.filter_by(user_id=current_user.id, name=name).first()
    if existing_player:
        return jsonify({'error': 'Player with this name already exists'}), 400
    # Create a new player
    new_player = Player(user_id=current_user.id, url=url, name=name, magic_class=magic_class, element=element, level=level,xp=xp,gold=gold,health=health,mana=mana,damage=damage,speed=speed,strength=strength,intellect=intellect,dexterity=dexterity,vitality=vitality)
    db.session.add(new_player)
    db.session.commit()

    return jsonify(new_player.to_dict()), 201


@player_routes.route('/<int:id>', methods=['PUT'])
@login_required
def update_player(id):
    """
    Update a player.
    """
    player = Player.query.filter_by(id=id, user_id=current_user.id).first()

    if not player:
        return jsonify({'error': 'Player not found'}), 404

    data = request.form if request.form else (request.get_json(silent=True) or {})
    image = request.files.get("image")

    if image:
        if not allowed_file(image.filename):
            return jsonify({'error': 'File type not permitted'}), 400
        image.filename = get_unique_filename(image.filename)
        upload = upload_file_to_cloudinary(image)
        if "url" not in upload:
            return jsonify(upload), 400
        player.url = upload["url"]

    new_name = data.get('name')
    new_magic_class = data.get('magic_class')
    new_element = data.get('element')

    try:
        new_level = _parse_decimal("level", data.get("level")) if 'level' in data else None
        new_xp = _parse_decimal("xp", data.get("xp")) if 'xp' in data else None
        new_gold = _parse_decimal("gold", data.get("gold")) if 'gold' in data else None
        new_health = _parse_decimal("health", data.get("health")) if 'health' in data else None
        new_mana = _parse_decimal("mana", data.get("mana")) if 'mana' in data else None
        new_damage = _parse_decimal("damage", data.get("damage")) if 'damage' in data else None
        new_speed = _parse_decimal("speed", data.get("speed")) if 'speed' in data else None
        new_strength = _parse_decimal("strength", data.get("strength")) if 'strength' in data else None
        new_intellect = _parse_decimal("intellect", data.get("intellect")) if 'intellect' in data else None
        new_dexterity = _parse_decimal("dexterity", data.get("dexterity")) if 'dexterity' in data else None
        new_vitality = _parse_decimal("vitality", data.get("vitality")) if 'vitality' in data else None
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400



    if new_name is not None:
        player.name = new_name
    if new_magic_class is not None:
        player.magic_class = new_magic_class
    if new_element is not None:
        player.element = new_element
    if new_level is not None:
        player.level = new_level
    if new_xp is not None:
        player.xp = new_xp
    if new_gold is not None:
        player.gold = new_gold
    if new_health is not None:
        player.health = new_health
    if new_mana is not None:
        player.mana = new_mana
    if new_damage is not None:
        player.damage = new_damage
    if new_speed is not None:
        player.speed = new_speed
    if new_strength is not None:
        player.strength = new_strength
    if new_intellect is not None:
        player.intellect = new_intellect
    if new_dexterity is not None:
        player.dexterity = new_dexterity
    if new_vitality is not None:
        player.vitality = new_vitality
    # Check if the layer already exists for the user



    db.session.commit()
    return jsonify(player.to_dict())


@player_routes.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_player(id):
    """
    Delete a user's player.
    """
    player = Player.query.filter_by(id=id, user_id=current_user.id).first()

    if not player:
        return jsonify({'error': 'Player not found'}), 404

    db.session.delete(player)
    db.session.commit()
    return jsonify({'message': 'Player deleted successfully'})
