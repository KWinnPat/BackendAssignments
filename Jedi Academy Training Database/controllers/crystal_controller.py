from flask import jsonify, request
from flask_bcrypt import generate_password_hash

from db import db
from models.crystal import Crystals, crystal_schema, crystals_schema
from util.reflection import populate_object
from lib.authenticate import authenticate, authenticate_return_auth

#CREATE
@authenticate_return_auth
def create_crystal(auth_info):
    post_data = request.form if request.form else request.get_json()

    new_crystal = Crystals.new_crystal_obj()
    if auth_info.user.force_rank == 'master' or auth_info.user.force_rank == 'council' or auth_info.user.force_rank == 'grand-master':
        populate_object(new_crystal, post_data)

        try:
            db.session.add(new_crystal)
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message": "unable to create record"}), 400

        return jsonify({"message": "crystal created", "result": crystal_schema.dump(new_crystal)}), 201
    return jsonify({"message": "unauthorized"}), 401

#READ
@authenticate_return_auth
def get_crystals_by_rarity(rarity_level, auth_info):
    query = db.session.query(Crystals).filter(Crystals.rarity_level == rarity_level).all()
    if auth_info.user.force_rank == 'master' or auth_info.user.force_rank == 'council' or auth_info.user.force_rank == 'grand-master':
        return jsonify({"message": "user found", "result": crystals_schema.dump(query)}), 200
    return jsonify({"message": "unauthorized"}), 401

