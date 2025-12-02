from flask import jsonify, request
from flask_bcrypt import generate_password_hash

from db import db
from models.master import Masters, master_schema, masters_schema
from models.user import Users
from util.reflection import populate_object
from lib.authenticate import authenticate, authenticate_return_auth

#CREATE
@authenticate_return_auth
def promote_to_master(auth_info):
    post_data = request.form if request.form else request.get_json()
    user_id = post_data.get('user_id')

    new_user = Masters.new_master_obj()
    if auth_info.user.force_rank == 'council' or auth_info.user.force_rank == 'grand-master':
        populate_object(new_user, post_data)

        new_user.password = generate_password_hash(new_user.password).decode('utf8')

        if user_id:
            user_query = db.session.query(Users).filter(Users.user_id == user_id).first()

            if user_query == None:
                return jsonify({"message": "user not found"}), 404

        try:
            db.session.add(new_user)
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message": "unable to create record"}), 400

        return jsonify({"message": "user created", "result": master_schema.dump(new_user)}), 201
    return jsonify({"message": "unauthorized"}), 401

#READ
@authenticate_return_auth
def get_all_masters(auth_info):
    query = db.session.query(Masters).all()
    if auth_info.user.force_rank != 'youngling':
        return jsonify({"message": "success", "result": masters_schema.dump(query)}), 200
    return jsonify({"message": "unauthorized"}), 401

#UPDATE
@authenticate_return_auth
def update_master_specialization(user_id, auth_info):
    query = db.session.query(Users).filter(Users.user_id == user_id).first()
    data = request.form if request.form else request.get_json()
    if auth_info.user.force_rank == 'council' or auth_info.user.force_rank == 'grand-master' or user_id == str(auth_info.user.user_id):
        populate_object(query, data)

        try:
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message": "unable to update record"}), 400

        return jsonify({"message": "user updated", "results": master_schema.dump(query)}), 200
    return jsonify({"message": "unauthorized"}), 401

#DELETE
@authenticate_return_auth
def delete_master_by_id(master_id, auth_info):
    query = db.session.query(Masters).filter(Masters.master_id == master_id).first()
    if auth_info.user.role == 'grand-master':
        if not query:
            return jsonify({"message": "master not found"}), 404
    
        try:
            db.session.delete(query)
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message": "unable to delete record"}), 400
    
        return jsonify({"message": "user deleted"}), 200
    return jsonify({"message": "unauthorized"}), 401