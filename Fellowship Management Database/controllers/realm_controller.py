from flask import jsonify, request
from db import db

from models.realm import Realms, realm_schema, realms_schema
from util.reflection import populate_object

# CREATE
def create_realm():
    data = request.form if request.form else request.get_json()
    new_realm = Realms.new_realm_obj()

    populate_object(new_realm, data)

    try:
        db.session.add(new_realm)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create record"}), 400

    return jsonify({"message": "realm created", "results": realm_schema.dump(new_realm)}), 201

# READ
def get_realm_by_id(realm_id):
    query = db.session.query(Realms).filter(Realms.realm_id == realm_id).first()
    if not query:
        return jsonify({"message": "realm not found"}), 404
    return jsonify({"results": realm_schema.dump(query)}), 200

# UPDATE
def update_realm_by_id(realm_id):
    query = db.session.query(Realms).filter(Realms.realm_id == realm_id).first()
    data = request.form if request.form else request.get_json()

    populate_object(query, data)

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to update record"}), 400

    return jsonify({"message": "realm updated", "results": realm_schema.dump(query)}), 200

# DELETE
def delete_realm_by_id(realm_id):
    query = db.session.query(Realms).filter(Realms.realm_id == realm_id).first()
    if not query:
        return jsonify({"message": "realm not found"}), 404

    try:
        db.session.delete(query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete record"}), 400

    return jsonify({"message": "realm deleted"}), 200