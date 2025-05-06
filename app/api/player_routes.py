from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import Player, db

player_routes = Blueprint('players', __name__)


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
    print(f'Creating player for user: {current_user.id}')
    print(f'Request data: {request.get_json()}')

    data = request.get_json()
    url = data.get("url")
    name = data.get("name")
    magic_class = data.get("magic_class")
    element = data.get("element")
    level = data.get("level")
    xp = data.get("xp")
    gold = data.get("gold")
    health = data.get("health")
    mana = data.get("mana")
    damage = data.get("damage")
    speed = data.get("speed")
    strength = data.get("strength")
    intellect = data.get("intellect")
    dexterity = data.get("dexterity")
    vitality = data.get("vitality")
    if not name:
        return jsonify({'error': 'Player name is required'}), 400
    if not magic_class:
        return jsonify({'error': 'Player magic_class is required'}), 400
    if not url:
        return jsonify({'error': 'Player URL is required'}), 400
    if not element:
        return jsonify({'error': 'Player element is required'}), 400
    if not level:
        return jsonify({'error': 'Player level is required'}), 400
    if not xp:
        return jsonify({'error': 'Player xp is required'}), 400
    if not gold:
        return jsonify({'error': 'Player gold is required'}), 400
    if not health:
        return jsonify({'error': 'Player health is required'}), 400
    if not mana:
        return jsonify({'error': 'Player mana is required'}), 400
    if not damage:
        return jsonify({'error': 'Player damage is required'}), 400
    if not speed:
        return jsonify({'error': 'Player speed is required'}), 400
    if not strength:
        return jsonify({'error': 'Player strength is required'}), 400
    if not intellect:
        return jsonify({'error': 'Player intellect is required'}), 400
    if not dexterity:
        return jsonify({'error': 'Player dexterity is required'}), 400
    if not vitality:
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

    data = request.get_json()
    new_url = data.get('url')
    new_name = data.get('name')
    new_magic_class = data.get('magic_class')
    new_element = data.get('element')
    new_level = data.get("level")
    new_xp = data.get("xp")
    new_gold = data.get("gold")
    new_health = data.get("health")
    new_mana = data.get("mana")
    new_damage = data.get("damage")
    new_speed = data.get("speed")
    new_strength = data.get("strength")
    new_intellect = data.get("intellect")
    new_dexterity = data.get("dexterity")
    new_vitality = data.get("vitality")



    if new_url is not None:
        player.url = new_url
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
