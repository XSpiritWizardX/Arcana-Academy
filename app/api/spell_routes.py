from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required

from app.api.upload_helper import (
    allowed_file,
    get_unique_filename,
    upload_file_to_cloudinary,
)
from app.models import Spell, db

spell_routes = Blueprint('spells', __name__)


def _parse_decimal(field_name, value):
    """
    Convert incoming string/number to a float. Returns None when value is empty.
    Raises ValueError for invalid numeric inputs.
    """
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        raise ValueError(f"{field_name} must be a number")


@spell_routes.route('/all')
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
def get_spell(id):
    """
    Get a spell by ID.
    """
    spell = Spell.query.filter_by(id=id).first()

    if not spell:
        return jsonify({'error': 'Spell not found'}), 404

    return jsonify(spell.to_dict())


@spell_routes.route('/', methods=['POST'])
@login_required
def create_spell():
    """
    Create a new spell for the logged-in user.
    """
    image = request.files.get("image")
    data = request.form if request.form else (request.get_json(silent=True) or {})

    if not image:
        return jsonify({'error': 'Spell image is required'}), 400
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
        return jsonify({'error': 'Spell name is required'}), 400
    if not description:
        return jsonify({'error': 'Spell description is required'}), 400
    if damage is None:
        return jsonify({'error': 'Spell damage is required'}), 400
    if cost is None:
        return jsonify({'error': 'Spell cost is required'}), 400
    if mana_cost is None:
        return jsonify({'error': 'Spell mana cost is required'}), 400
    if not element:
        return jsonify({'error': 'Spell element is required'}), 400

    existing_spell = Spell.query.filter_by(user_id=current_user.id, name=name).first()
    if existing_spell:
        return jsonify({'error': 'Spell with this name already exists'}), 400

    new_spell = Spell(
        user_id=current_user.id,
        url=url,
        name=name,
        description=description,
        damage=damage,
        cost=cost,
        mana_cost=mana_cost,
        element=element,
    )
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

    data = request.form if request.form else (request.get_json(silent=True) or {})
    image = request.files.get("image")

    if image:
        if not allowed_file(image.filename):
            return jsonify({'error': 'File type not permitted'}), 400
        image.filename = get_unique_filename(image.filename)
        upload = upload_file_to_cloudinary(image)
        if "url" not in upload:
            return jsonify(upload), 400
        spell.url = upload["url"]

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
