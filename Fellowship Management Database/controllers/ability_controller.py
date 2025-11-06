from flask import jsonify, request
from db import db

from models.ability import Abilities, ability_schema, abilities_schema
from util.reflection import populate_object

# CREATE
def create_ability():
    data = request.form if request.form else request.get_json()
    new_ability = Abilities.new_ability_obj()

    populate_object(new_ability, data)

    try:
        db.session.add(new_ability)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create record"}), 400

    return jsonify({"message": "ability created", "results": ability_schema.dump(new_ability)}), 201

# UPDATE
def update_ability_by_id(ability_id):
    query = db.session.query(Abilities).filter(Abilities.ability_id == ability_id).first()
    data = request.form if request.form else request.get_json()

    populate_object(query, data)

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to update record"}), 400

    return jsonify({"message": "ability updated", "results": ability_schema.dump(query)}), 200

# DELETE
def delete_ability_by_id(ability_id):
    query = db.session.query(Abilities).filter(Abilities.ability_id == ability_id).first()
    if not query:
        return jsonify({"message": "ability not found"}), 404

    try:
        db.session.delete(query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete record"}), 400

    return jsonify({"message": "ability deleted"}), 200