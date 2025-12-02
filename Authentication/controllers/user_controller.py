from flask import jsonify, request
from flask_bcrypt import generate_password_hash

from db import db
from models.user import Users, user_schema, users_schema
from models.company import Companies
from util.reflection import populate_object
from lib.authenticate import authenticate, authenticate_return_auth

def add_user():
    post_data = request.form if request.form else request.get_json()
    company_id = post_data.get('company_id')

    new_user = Users.new_user_obj()

    populate_object(new_user, post_data)

    new_user.password = generate_password_hash(new_user.password).decode('utf8')

    if company_id:
        company_query = db.session.query(Companies).filter(Companies.company_id == company_id).first()

        if company_query == None:
            return jsonify({"message": "company not found"}), 404

    try:
        db.session.add(new_user)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create record"}), 400
    
    return jsonify({"message": "user created", "result": user_schema.dump(new_user)}), 201

@authenticate
def get_all_users():
    users_query = db.session.query(Users).all()

    return jsonify({"message": "success", "result": users_schema.dump(users_query)}), 200

@authenticate_return_auth
def get_user_by_id(user_id, auth_info):
    user_query = db.session.query(Users).filter(Users.user_id == user_id).first()

    if auth_info.user.role == 'super-admin' or user_id == str(auth_info.user.user_id):
        return jsonify({"message": "user found", "result": user_schema.dump(user_query)}), 200
    
    return jsonify({"message": "unauthorized"}), 401


@authenticate_return_auth
def update_user_by_id(user_id, auth_info):
    query = db.session.query(Users).filter(Users.user_id == user_id).first()
    data = request.form if request.form else request.get_json()
    if auth_info.user.role == 'super-admin':
        populate_object(query, data)

        try:
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message": "unable to update record"}), 400

        return jsonify({"message": "user updated", "results": user_schema.dump(query)}), 200
    return jsonify({"message": "unauthorized"}), 401

@authenticate_return_auth
def delete_user_by_id(user_id, auth_info):
    query = db.session.query(Users).filter(Users.user_id == user_id).first()
    if auth_info.user.role == 'super-admin':
        if not query:
            return jsonify({"message": "user not found"}), 404
    
        try:
            db.session.delete(query)
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message": "unable to delete record"}), 400
    
        return jsonify({"message": "user deleted"}), 200
    return jsonify({"message": "unauthorized"}), 401