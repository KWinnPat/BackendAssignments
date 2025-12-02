from flask import jsonify, request
from db import db

from models.warranty import Warranties, warranty_schema, warranties_schema
from util.reflection import populate_object
from lib.authenticate import authenticate, authenticate_return_auth

# CREATE
@authenticate_return_auth
def create_warranty(auth_info):
    data = request.form if request.form else request.get_json()
    new_warranty = Warranties.new_warranty_obj()
    if auth_info.user.role == 'super-admin':
        populate_object(new_warranty, data)

        try:
            db.session.add(new_warranty)
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message": "unable to create record"}), 400

        return jsonify({"message": "warranty created", "results": warranty_schema.dump(new_warranty)}), 201
    return jsonify({"message": "unauthorized"}), 401

# READ
@authenticate
def get_warranty_by_id(warranty_id):
    query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()
    if not query:
        return jsonify({"message": "warranty not found"}), 404
    return jsonify({"results": warranty_schema.dump(query)}), 200



# UPDATE
@authenticate_return_auth
def update_warranty_by_id(warranty_id, auth_info):
    query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()
    data = request.form if request.form else request.get_json()
    if auth_info.user.role == 'super-admin':
        populate_object(query, data)

        try:
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message": "unable to update record"}), 400

        return jsonify({"message": "warranty updated", "results": warranty_schema.dump(query)}), 200
    return jsonify({"message": "unauthorized"}), 401

# DELETE
@authenticate_return_auth
def delete_warranty_by_id(warranty_id, auth_info):
    query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()
    if auth_info.user.role == 'super-admin':
        if not query:
            return jsonify({"message": "warranty not found"}), 404
        try:
            db.session.delete(query)
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message": "unable to delete record"}), 400
    
        return jsonify({"message": "warranty deleted"}), 200
    return jsonify({"message": "unauthorized"}), 401