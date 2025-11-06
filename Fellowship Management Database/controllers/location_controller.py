from flask import jsonify, request
from db import db

from models.location import Locations, location_schema, locations_schema
from util.reflection import populate_object

# CREATE
def create_location():
    data = request.form if request.form else request.get_json()
    new_location = Locations.new_location_obj()

    populate_object(new_location, data)

    try:
        db.session.add(new_location)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create record"}), 400

    return jsonify({"message": "location created", "results": location_schema.dump(new_location)}), 201

# READ
def get_location_by_id(location_id):
    query = db.session.query(Locations).filter(Locations.location_id == location_id).first()
    if not query:
        return jsonify({"message": "location not found"}), 404
    return jsonify({"results": location_schema.dump(query)}), 200

# UPDATE
def update_location_by_id(location_id):
    query = db.session.query(Locations).filter(Locations.location_id == location_id).first()
    data = request.form if request.form else request.get_json()

    populate_object(query, data)

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to update record"}), 400

    return jsonify({"message": "location updated", "results": location_schema.dump(query)}), 200

# DELETE
def delete_location_by_id(location_id):
    query = db.session.query(Locations).filter(Locations.location_id == location_id).first()
    if not query:
        return jsonify({"message": "location not found"}), 404

    try:
        db.session.delete(query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete record"}), 400

    return jsonify({"message": "location deleted"}), 200