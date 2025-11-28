from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required

from app.api.upload_helper import (
    allowed_file,
    get_unique_filename,
    upload_file_to_cloudinary,
)
from app.models import Sword, db

sword_routes = Blueprint('swords', __name__)


def _parse_decimal(field_name, value):
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        raise ValueError(f"{field_name} must be a number")


@sword_routes.route('/all')

def get_all_swords():
    """
    Get all swords.
    """
    swords = Sword.query.all()
    return jsonify({'swords': [sword.to_dict() for sword in swords]})


@sword_routes.route('/')
@login_required
def get_swords():
    """
    Get all swords for the logged-in user.
    """
    swords = Sword.query.filter_by(user_id=current_user.id).all()
    return jsonify({'swords': [sword.to_dict() for sword in swords]})


@sword_routes.route('/<int:id>')
def get_sword(id):
    """
    Get a sword by ID.
    """
    sword = Sword.query.filter_by(id=id).first()

    if not sword:
        return jsonify({'error': 'Sword not found'}), 404

    return jsonify(sword.to_dict())


@sword_routes.route('/', methods=['POST'])
@login_required
def create_sword():
    """
    Create a new sword for the logged-in user.
    """
    image = request.files.get("image")
    data = request.form if request.form else (request.get_json(silent=True) or {})

    if not image:
        return jsonify({'error': 'Sword image is required'}), 400
    if not allowed_file(image.filename):
        return jsonify({'error': 'File type not permitted'}), 400

    image.filename = get_unique_filename(image.filename)
    upload = upload_file_to_cloudinary(image)
    if "url" not in upload:
        return jsonify(upload), 400

    url = upload["url"]
    name = data.get("name")
    description = data.get("description")
    element = data.get("element")

    try:
        damage = _parse_decimal("damage", data.get("damage"))
        cost = _parse_decimal("cost", data.get("cost"))
        mana_cost = _parse_decimal("mana_cost", data.get("mana_cost"))
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    if not name:
        return jsonify({'error': 'Sword name is required'}), 400
    if not description:
        return jsonify({'error': 'Sword description is required'}), 400
    if not url:
        return jsonify({'error': 'Sword URL is required'}), 400
    if damage is None:
        return jsonify({'error': 'Sword damage is required'}), 400
    if cost is None:
        return jsonify({'error': 'Sword cost is required'}), 400
    if mana_cost is None:
        return jsonify({'error': 'Sword mana cost is required'}), 400
    if not element:
        return jsonify({'error': 'Sword element is required'}), 400

    # Check if the sword already exists for the user
    existing_sword = Sword.query.filter_by(user_id=current_user.id, name=name).first()
    if existing_sword:
        return jsonify({'error': 'Sword with this name already exists'}), 400
    # Create a new sword
    new_sword = Sword(user_id=current_user.id, url=url, name=name, description=description, damage=damage, cost=cost, mana_cost=mana_cost, element=element)
    db.session.add(new_sword)
    db.session.commit()

    return jsonify(new_sword.to_dict()), 201


@sword_routes.route('/<int:id>', methods=['PUT'])
@login_required
def update_sword(id):
    """
    Update a sword.
    """
    sword = Sword.query.filter_by(id=id, user_id=current_user.id).first()

    if not sword:
        return jsonify({'error': 'Sword not found'}), 404

    data = request.form if request.form else (request.get_json(silent=True) or {})
    image = request.files.get("image")

    if image:
        if not allowed_file(image.filename):
            return jsonify({'error': 'File type not permitted'}), 400
        image.filename = get_unique_filename(image.filename)
        upload = upload_file_to_cloudinary(image)
        if "url" not in upload:
            return jsonify(upload), 400
        sword.url = upload["url"]

    new_name = data.get('name')
    new_description = data.get('description')
    new_element = data.get('element')

    try:
        new_damage = (
            _parse_decimal("damage", data.get('damage')) if 'damage' in data else None
        )
        new_cost = _parse_decimal("cost", data.get('cost')) if 'cost' in data else None
        new_mana_cost = (
            _parse_decimal("mana_cost", data.get('mana_cost'))
            if 'mana_cost' in data
            else None
        )
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400


    if new_name is not None:
        sword.name = new_name
    if new_description is not None:
        sword.description = new_description
    if new_damage is not None:
        sword.damage = new_damage
    if new_cost is not None:
        sword.cost = new_cost
    if new_mana_cost is not None:
        sword.mana_cost = new_mana_cost
    if new_element is not None:
        sword.element = new_element
    # Check if the sword already exists for the user



    db.session.commit()
    return jsonify(sword.to_dict())


@sword_routes.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_sword(id):
    """
    Delete a user's sword.
    """
    sword = Sword.query.filter_by(id=id, user_id=current_user.id).first()

    if not sword:
        return jsonify({'error': 'Sword not found'}), 404

    db.session.delete(sword)
    db.session.commit()
    return jsonify({'message': 'Sword deleted successfully'})
