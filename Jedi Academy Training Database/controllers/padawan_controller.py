from flask import jsonify, request
from flask_bcrypt import generate_password_hash

from db import db
from models.padawan import Padawans, padawan_schema, padawans_schema
from models.master import Masters
from models.user import Users
from models.species import Species
from util.reflection import populate_object
from lib.authenticate import authenticate, authenticate_return_auth

#CREATE
@authenticate_return_auth
def add_new_padawan(auth_info):
    post_data = request.form if request.form else request.get_json()
    master_id = post_data.get('master_id')
    user_id = post_data.get('user_id')
    species_id = post_data.get('species_id')

    new_padawan = Padawans.new_padawan_obj()
    if auth_info.user.role == 'council' or auth_info.user.role == 'grand-master' or auth_info.user.role == 'master':
        populate_object(new_padawan, post_data)

        if master_id:
            master_query = db.session.query(Masters).filter(Masters.master_id == master_id).first()

            if master_query == None:
                return jsonify({"message": "master not found"}), 404

        if user_id:
            user_query = db.session.query(Users).filter(Users.user_id == user_id).first()

            if user_query == None:
                return jsonify({"message": "user not found"}), 404

        if species_id:
            species_query = db.session.query(Species).filter(Species.species_id == species_id).first()

            if species_query == None:
                return jsonify({"message": "species not found"}), 404

        try:
            db.session.add(new_padawan)
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message": "unable to create record"}), 400

        return jsonify({"message": "padawan created", "result": padawan_schema.dump(new_padawan)}), 201

    return jsonify({"message": "unauthorized"}), 401


#READ
@authenticate_return_auth
def get_all_padawans(auth_info):
    users_query = db.session.query(Padawans).all()

    return jsonify({"message": "success", "result": padawans_schema.dump(users_query)}), 200

def get_active_padawans():
    padawan_query = db.session.query(Users).filter(Users.force_rank == "padawan").filter(Users.is_active == True).all()
    
    return jsonify({"message": "user found", "result": padawans_schema.dump(padawan_query)}), 200

#UPDATE
@authenticate_return_auth
def update_padawan_training(user_id, auth_info):
    query = db.session.query(Padawans).filter(Padawans.user_id == user_id).first()
    data = request.form if request.form else request.get_json()
    if auth_info.user.role == 'council' or auth_info.user.role == 'grand-master' or Users.master_id == auth_info.user.master_id:
        populate_object(query, data)

        try:
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message": "unable to update record"}), 400

        return jsonify({"message": "user updated", "results": padawan_schema.dump(query)}), 200
    return jsonify({"message": "unauthorized"}), 401

@authenticate_return_auth
def promote_padawan(user_id, auth_info):
    query = db.session.query(Users).filter(Users.user_id == user_id).first()
    data = request.form if request.form else request.get_json()
    if auth_info.user.force_rank == 'council' or auth_info.user.force_rank == 'grand-master':
        populate_object(query, data)

        try:
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message": "unable to update record"}), 400

        return jsonify({"message": "user updated", "results": padawan_schema.dump(query)}), 200
    return jsonify({"message": "unauthorized"}), 401

#DELETE
@authenticate_return_auth
def delete_padawan_by_id(user_id, auth_info):
    query = db.session.query(Users).filter(Users.user_id == user_id).first()
    if auth_info.user.force_rank == 'council' or auth_info.user.role == 'grand-master':
        if not query:
            return jsonify({"message": "padawan not found"}), 404
    
        try:
            db.session.delete(query)
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message": "unable to delete record"}), 400
    
        return jsonify({"message": "padawan deleted"}), 200
    return jsonify({"message": "unauthorized"}), 401