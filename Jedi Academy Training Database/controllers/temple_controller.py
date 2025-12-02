from flask import jsonify, request
from flask_bcrypt import generate_password_hash

from db import db
from models.temple import Temples, temple_schema, temples_schema
from util.reflection import populate_object
from lib.authenticate import authenticate, authenticate_return_auth

#CREATE
@authenticate_return_auth
def create_temple(auth_info):
    post_data = request.form if request.form else request.get_json()

    new_temple = Temples.new_temple_obj()
    if auth_info.user.force_rank == 'grand-master':
        populate_object(new_temple, post_data)

        try:
            db.session.add(new_temple)
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message": "unable to create record"}), 400

        return jsonify({"message": "temple created", "result": temple_schema.dump(new_temple)}), 201
    return jsonify({"message": "unauthorized"}), 401

#READ
@authenticate
def get_temple_by_id(temple_id, auth_info):
    temple_query = db.session.query(Temples).filter(Temples.temple_id == temple_id).first()
    return jsonify({"message": "temple found", "result": temple_schema.dump(temple_query)}), 200

#UPDATE
@authenticate_return_auth
def update_temple_by_id(temple_id, auth_info):
    query = db.session.query(Temples).filter(Temples.temple_id == temple_id).first()
    data = request.form if request.form else request.get_json()
    if auth_info.user.force_rank == 'grand-master':
        populate_object(query, data)

        try:
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message": "unable to update record"}), 400

        return jsonify({"message": "temple updated", "results": temple_schema.dump(query)}), 200
    return jsonify({"message": "unauthorized"}), 401

#DELETE
@authenticate_return_auth
def delete_temple_by_id(temple_id, auth_info):
    query = db.session.query(Temples).filter(Temples.temple_id == temple_id).first()
    if auth_info.user.role == 'grand-master':
        if not query:
            return jsonify({"message": "temple not found"}), 404
    
        try:
            db.session.delete(query)
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message": "unable to delete record"}), 400
    
        return jsonify({"message": "temple deleted"}), 200
    return jsonify({"message": "unauthorized"}), 401