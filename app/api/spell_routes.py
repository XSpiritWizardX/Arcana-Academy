from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import Spell, db

spell_routes = Blueprint('spells', __name__)


@spell_routes.route('/all')
@login_required
def get_all_spells():
    """
    Get all spells.
    """
    spells = Spell.query.all()
    return jsonify({'spells': [spell.to_dict() for spell in spells]})


@spell_routes.route('/')
@login_required
def get_spells():
    """
    Get all spells for the logged-in user.
    """
    spells = Spell.query.filter_by(user_id=current_user.id).all()
    return jsonify({'spells': [spell.to_dict() for spell in spells]})


@spell_routes.route('/<int:id>')
@login_required
def get_spell(id):
    """
    Get a spell by ID for the logged-in user.
    """
    spell = Spell.query.filter_by(id=id, user_id=current_user.id).first()

    if not spell:
        return jsonify({'error': 'Spell not found'}), 404

    return jsonify(spell.to_dict())


@spell_routes.route('/', methods=['POST'])
@login_required
def create_spell():
    """
    Create a new spell for the logged-in user.
    """
    print(f'Creating spell for user: {current_user.id}')
    print(f'Request data: {request.get_json()}')

    data = request.get_json()
    url = data.get("url")
    name = data.get("name")
    description = data.get("description")
    damage = data.get("damage", 0.00)
    cost = data.get("cost", 0.00)
    mana_cost = data.get("mana_cost", 0.00)
    element = data.get("element")

    if not name:
        return jsonify({'error': 'Spell name is required'}), 400
    if not description:
        return jsonify({'error': 'Spell description is required'}), 400
    if not url:
        return jsonify({'error': 'Spell URL is required'}), 400
    if not damage:
        return jsonify({'error': 'Spell damage is required'}), 400
    if not cost:
        return jsonify({'error': 'Spell cost is required'}), 400
    if not mana_cost:
        return jsonify({'error': 'Spell mana cost is required'}), 400
    if not element:
        return jsonify({'error': 'Spell element is required'}), 400

    # Check if the spell already exists for the user
    existing_spell = Spell.query.filter_by(user_id=current_user.id, name=name).first()
    if existing_spell:
        return jsonify({'error': 'Spell with this name already exists'}), 400
    # Create a new spell
    new_spell = Spell(user_id=current_user.id, url=url, name=name, description=description, damage=damage, cost=cost, mana_cost=mana_cost, element=element)
    db.session.add(new_spell)
    db.session.commit()

    return jsonify(new_spell.to_dict()), 201


@spell_routes.route('/<int:id>', methods=['PUT'])
@login_required
def update_spell(id):
    """
    Update a spell.
    """
    spell = Spell.query.filter_by(id=id, user_id=current_user.id).first()

    if not spell:
        return jsonify({'error': 'Spell not found'}), 404

    data = request.get_json()
    new_url = data.get('url')
    new_name = data.get('name')
    new_description = data.get('description')
    new_damage = data.get('damage')
    new_cost = data.get('cost')
    new_mana_cost = data.get('mana_cost')
    new_element = data.get('element')



    if new_url is not None:
        spell.url = new_url
    if new_name is not None:
        spell.name = new_name
    if new_description is not None:
        spell.description = new_description
    if new_damage is not None:
        spell.damage = new_damage
    if new_cost is not None:
        spell.cost = new_cost
    if new_mana_cost is not None:
        spell.mana_cost = new_mana_cost
    if new_element is not None:
        spell.element = new_element
    # Check if the spell already exists for the user



    db.session.commit()
    return jsonify(spell.to_dict())


@spell_routes.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_spell(id):
    """
    Delete a user's spell.
    """
    spell = Spell.query.filter_by(id=id, user_id=current_user.id).first()

    if not spell:
        return jsonify({'error': 'Spell not found'}), 404

    db.session.delete(spell)
    db.session.commit()
    return jsonify({'message': 'Spell deleted successfully'})
