from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required

from app.api.upload_helper import (
    allowed_file,
    get_unique_filename,
    upload_file_to_cloudinary,
)
from app.models import Potion, db

potion_routes = Blueprint('potions', __name__)


def _parse_decimal(field_name, value):
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        raise ValueError(f"{field_name} must be a number")


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
    image = request.files.get("image")
    data = request.form if request.form else (request.get_json(silent=True) or {})

    if not image:
        return jsonify({'error': 'Potion image is required'}), 400
    if not allowed_file(image.filename):
        return jsonify({'error': 'File type not permitted'}), 400

    image.filename = get_unique_filename(image.filename)
    upload = upload_file_to_cloudinary(image)
    if "url" not in upload:
        return jsonify(upload), 400

    url = upload["url"]
    name = data.get("name")
    description = data.get("description")
    potion_type = data.get("type")
    element = data.get("element")

    try:
        regeneration = _parse_decimal("regeneration", data.get("regeneration"))
        cost = _parse_decimal("cost", data.get("cost"))
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    if not name:
        return jsonify({'error': 'Potion name is required'}), 400
    if not description:
        return jsonify({'error': 'Potion description is required'}), 400
    if not url:
        return jsonify({'error': 'Potion URL is required'}), 400
    if regeneration is None:
        return jsonify({'error': 'Potion regeneration is required'}), 400
    if cost is None:
        return jsonify({'error': 'Potion cost is required'}), 400
    if not potion_type:
        return jsonify({'error': 'Potion type is required'}), 400
    if not element:
        return jsonify({'error': 'Potion element is required'}), 400

    # Check if the potion already exists for the user
    existing_potion = Potion.query.filter_by(user_id=current_user.id, name=name).first()
    if existing_potion:
        return jsonify({'error': 'Potion with this name already exists'}), 400
    # Create a new potion
    new_potion = Potion(user_id=current_user.id, url=url, name=name, description=description, regeneration=regeneration, cost=cost, type=potion_type, element=element)
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

    data = request.form if request.form else (request.get_json(silent=True) or {})
    image = request.files.get("image")

    if image:
        if not allowed_file(image.filename):
            return jsonify({'error': 'File type not permitted'}), 400
        image.filename = get_unique_filename(image.filename)
        upload = upload_file_to_cloudinary(image)
        if "url" not in upload:
            return jsonify(upload), 400
        potion.url = upload["url"]

    new_name = data.get('name')
    new_description = data.get('description')
    new_type = data.get('type')
    new_element = data.get('element')

    try:
        new_regeneration = (
            _parse_decimal("regeneration", data.get('regeneration'))
            if 'regeneration' in data
            else None
        )
        new_cost = _parse_decimal("cost", data.get('cost')) if 'cost' in data else None
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400



    if new_name is not None:
        potion.name = new_name
    if new_description is not None:
        potion.description = new_description
    if new_regeneration is not None:
        potion.regeneration = new_regeneration
    if new_cost is not None:
        potion.cost = new_cost
    if new_type is not None:
        potion.type = new_type
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
