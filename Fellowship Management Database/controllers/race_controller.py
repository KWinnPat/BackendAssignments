from flask import jsonify, request
from db import db

from models.race import Races, race_schema, races_schema
from util.reflection import populate_object

# CREATE
def create_race():
    data = request.form if request.form else request.get_json()
    new_race = Races.new_race_obj()

    populate_object(new_race, data)

    try:
        db.session.add(new_race)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create record"}), 400
    
    return jsonify({"message": "race created", "results": race_schema.dump(new_race)}), 201

# READ
def get_all_races():
    query = db.session.query(Races).all()
    return jsonify({"results": races_schema.dump(query)}), 200 

def get_race_by_id(race_id):
    query = db.session.query(Races).filter(Races.race_id == race_id).first()
    if not query:
        return jsonify({"message": "race not found"}), 404
    return jsonify({"results": race_schema.dump(query)}), 200 

# UPDATE
def update_race_by_id(race_id):
    query = db.session.query(Races).filter(Races.race_id == race_id).first()
    data = request.form if request.form else request.get_json()

    populate_object(query, data)

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to update record"}), 400
    
    return jsonify({"message": "race updated", "results": race_schema.dump(query)}), 200

# DELETE
def delete_race_by_id(race_id):
    query = db.session.query(Races).filter(Races.race_id == race_id).first()
    if not query:
        return jsonify({"message": "race not found"}), 404
    
    try:
        db.session.delete(query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete record"}), 400
    
    return jsonify({"message": "race deleted"}), 200