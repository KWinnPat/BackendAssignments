from flask import jsonify, request
from flask_bcrypt import generate_password_hash

from db import db
from models.species import Species, species_schema
from util.reflection import populate_object
from lib.authenticate import authenticate, authenticate_return_auth

#CREATE
@authenticate_return_auth
def create_species(auth_info):
    post_data = request.form if request.form else request.get_json()

    new_species = Species.new_species_obj()
    if auth_info.user.force_rank == 'grand-master':
        populate_object(new_species, post_data)

        try:
            db.session.add(new_species)
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message": "unable to create record"}), 400

        return jsonify({"message": "species created", "result": species_schema.dump(new_species)}), 201
    return jsonify({"message": "unauthorized"}), 401

#READ
@authenticate
def get_species_by_id(species_id, auth_info):
    species_query = db.session.query(Species).filter(Species.species_id == species_id).first()
    return jsonify({"message": "species found", "result": species_schema.dump(species_query)}), 200