from flask import jsonify, request
from db import db
from models.spell import Spells


# CREATE

def add_spell():
    post_data = request.form if request.form else request.get_json()

    fields = ['spell_name', 'incantation', 'difficulty_level', 'spell_type', 'description']
    required_fields = ['spell_name']

    values = {}

    for field in fields:
        field_data = post_data.get(field)
       
        if field_data in required_fields and not field_data:
            return jsonify({"message": f'{field} is required'}), 400

        values[field] = field_data

    new_spell = Spells(values['spell_name'], values.get('incantation'), values.get('difficulty_level'), values.get('spell_type'), values.get('description'))

    try:
        db.session.add(new_spell)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create record"}), 400

    query = db.session.query(Spells).filter(Spells.spell_name == values['spell_name']).first()

    spell = {
        "spell_id": query.spell_id,
        "spell_name": query.spell_name,
        "incantation": query.incantation,
        "difficulty_level": query.difficulty_level,
        "spell_type": query.spell_type,
        "description": query.description
    }

    return jsonify({"message": "spell created", "result": spell}), 200

# READ

def get_all_spells():
    query = db.session.query(Spells).all()

    spell_list = []

    for spell in query:
        spell_dict = {
            'spell_id': spell.spell_id,
            'spell_name': spell.spell_name,
            'incantation': spell.incantation,
            'difficulty_level': spell.difficulty_level,
            'spell_type': spell.spell_type,
            'description': spell.description
        }

        spell_list.append(spell_dict)

    return jsonify({"message": "spells found", "results": spell_list}), 200


def get_spell_by_difficulty(difficulty_level):
    query = db.session.query(Spells).filter(Spells.difficulty_level == difficulty_level).all()

    if not query:
        return jsonify({"message": f"no spells found with difficulty level {difficulty_level}"}), 400

    spell_list = []

    for spell in query:
        spell_dict = {
            'spell_id': spell.spell_id,
            'spell_name': spell.spell_name,
            'incantation': spell.incantation,
            'difficulty_level': spell.difficulty_level,
            'spell_type': spell.spell_type,
            'description': spell.description
        }

        spell_list.append(spell_dict)

    return jsonify({"message": f"spells found with difficulty level {difficulty_level}", "results": spell_list}), 200

# UPDATE

def update_spell_by_id(spell_id):

    post_data = request.form if request.form else request.get_json()
    query = db.session.query(Spells).filter(Spells.spell_id == spell_id).first()

    if not query:
        return jsonify({"message": f"spell does not exist"}), 400

    query.spell_name = post_data.get("spell_name", query.spell_name)
    query.incantation = post_data.get("incantation", query.incantation)
    query.difficulty_level = post_data.get("difficulty_level", query.difficulty_level)
    query.spell_type = post_data.get("spell_type", query.spell_type)
    query.description = post_data.get("description", query.description)

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to update record"}), 400

    updated_spell_query = db.session.query(Spells).filter(Spells.spell_id == spell_id).first()

    spell = {
        'spell_id': updated_spell_query.spell_id,
        'spell_name': updated_spell_query.spell_name,
        'incantation': updated_spell_query.incantation,
        'difficulty_level': updated_spell_query.difficulty_level,
        'spell_type': updated_spell_query.spell_type,
        'description': updated_spell_query.description
    }

    return jsonify({"message": "spell updated", "result": spell}), 200
 
# DELETE
def delete_spell_by_id(spell_id):
    spell_query = db.session.query(Spells).filter(Spells.spell_id == spell_id).first()

    if not spell_query:
        return jsonify({"message": f"spell by id {spell_id} does not exist"}), 400    

    try:
        db.session.delete(spell_query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete record"}), 400

    return jsonify({"message": "spell deleted"}), 200
