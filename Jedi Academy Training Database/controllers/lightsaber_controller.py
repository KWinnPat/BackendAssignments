from flask import jsonify, request
from flask_bcrypt import generate_password_hash

from db import db
from models.lightsaber import Lightsabers, lightsaber_schema, lightsabers_schema
from util.reflection import populate_object
from lib.authenticate import authenticate, authenticate_return_auth

#CREATE
@authenticate_return_auth
def create_lightsaber(auth_info):
    post_data = request.form if request.form else request.get_json()

    new_lightsaber = Lightsabers.new_lightsaber_obj()
    if auth_info.user.force_rank != 'youngling':
        populate_object(new_lightsaber, post_data)

        try:
            db.session.add(new_lightsaber)
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message": "unable to create record"}), 400

        return jsonify({"message": "lightsaber created", "result": lightsaber_schema.dump(new_lightsaber)}), 201
    return jsonify({"message": "unauthorized"}), 401

#READ
@authenticate
def get_lightsaber_by_owner_id(owner_id):
    lightsaber_query = db.session.query(Lightsabers).filter(Lightsabers.owner_id == owner_id).first()
    return jsonify({"message": "lightsaber found", "result": lightsaber_schema.dump(lightsaber_query)}), 200

#UPDATE
@authenticate_return_auth
def update_lightsaber_by_id(saber_id, auth_info):
    query = db.session.query(Lightsabers).filter(Lightsabers.saber_id == saber_id).first()
    data = request.form if request.form else request.get_json()
    if auth_info.user.user_id == query.owner_id:
        populate_object(query, data)

        try:
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message": "unable to update record"}), 400

        return jsonify({"message": "lightsaber updated", "results": lightsaber_schema.dump(query)}), 200
    return jsonify({"message": "unauthorized"}), 401

#DELETE
@authenticate_return_auth
def delete_lightsaber_by_id(saber_id, auth_info):
    query = db.session.query(Lightsabers).filter(Lightsabers.saber_id == saber_id).first()
    if auth_info.user.force_rank == 'council' or auth_info.user.force_rank == 'grand-master' or auth_info.user.user_id == query.owner_id:
        if not query:
            return jsonify({"message": "lightsaber not found"}), 404
    
        try:
            db.session.delete(query)
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message": "unable to delete record"}), 400
    
        return jsonify({"message": "lightsaber deleted"}), 200
    return jsonify({"message": "unauthorized"}), 401