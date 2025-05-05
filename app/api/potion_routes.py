from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import Potion, db

potion_routes = Blueprint('potions', __name__)


@potion_routes.route('/all')

def get_all_potions():
    """
    Get all potions.
    """
    potions = Potion.query.all()
    return jsonify({'potions': [potion.to_dict() for potion in potions]})


@potion_routes.route('/')
@login_required
def get_potions():
    """
    Get all potions for the logged-in user.
    """
    potions = Potion.query.filter_by(user_id=current_user.id).all()
    return jsonify({'potions': [potion.to_dict() for potion in potions]})


@potion_routes.route('/<int:id>')
def get_potion(id):
    """
    Get a potion by ID.
    """
    potion = Potion.query.filter_by(id=id).first()

    if not potion:
        return jsonify({'error': 'Potion not found'}), 404

    return jsonify(potion.to_dict())


@potion_routes.route('/', methods=['POST'])
@login_required
def create_potion():
    """
    Create a new potion for the logged-in user.
    """
    print(f'Creating potion for user: {current_user.id}')
    print(f'Request data: {request.get_json()}')

    data = request.get_json()
    url = data.get("url")
    name = data.get("name")
    description = data.get("description")
    regeneration = data.get("regeneration", 0.00)
    cost = data.get("cost", 0.00)
    type = data.get("type")
    element = data.get("element")

    if not name:
        return jsonify({'error': 'Potion name is required'}), 400
    if not description:
        return jsonify({'error': 'Potion description is required'}), 400
    if not url:
        return jsonify({'error': 'Potion URL is required'}), 400
    if not regeneration:
        return jsonify({'error': 'Potion regeneration is required'}), 400
    if not cost:
        return jsonify({'error': 'Potion cost is required'}), 400
    if not type:
        return jsonify({'error': 'Potion type is required'}), 400
    if not element:
        return jsonify({'error': 'Potion element is required'}), 400

    # Check if the potion already exists for the user
    existing_potion = Potion.query.filter_by(user_id=current_user.id, name=name).first()
    if existing_potion:
        return jsonify({'error': 'Potion with this name already exists'}), 400
    # Create a new potion
    new_potion = Potion(user_id=current_user.id, url=url, name=name, description=description, regeneration=regeneration, cost=cost, type=type, element=element)
    db.session.add(new_potion)
    db.session.commit()

    return jsonify(new_potion.to_dict()), 201


@potion_routes.route('/<int:id>', methods=['PUT'])
@login_required
def update_potion(id):
    """
    Update a potion.
    """
    potion = Potion.query.filter_by(id=id, user_id=current_user.id).first()

    if not potion:
        return jsonify({'error': 'Potion not found'}), 404

    data = request.get_json()
    new_url = data.get('url')
    new_name = data.get('name')
    new_description = data.get('description')
    new_regeneration = data.get('regeneration')
    new_cost = data.get('cost')
    new_type = data.get('type')
    new_element = data.get('element')



    if new_url is not None:
        potion.url = new_url
    if new_name is not None:
        potion.name = new_name
    if new_description is not None:
        potion.description = new_description
    if new_regeneration is not None:
        potion.damage = new_regeneration
    if new_cost is not None:
        potion.cost = new_cost
    if new_type is not None:
        potion.mana_cost = new_type
    if new_element is not None:
        potion.element = new_element
    # Check if the spell already exists for the user



    db.session.commit()
    return jsonify(potion.to_dict())


@potion_routes.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_potion(id):
    """
    Delete a user's potion.
    """
    potion = Potion.query.filter_by(id=id, user_id=current_user.id).first()

    if not potion:
        return jsonify({'error': 'Potion not found'}), 404

    db.session.delete(potion)
    db.session.commit()
    return jsonify({'message': 'Potion deleted successfully'})
