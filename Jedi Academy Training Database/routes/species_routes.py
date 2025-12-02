from flask import Blueprint

import controllers

species = Blueprint('species', __name__)

@species.route('/species', methods=['POST'])
def create_species():
    return controllers.create_species()

@species.route('/species/<species_id>', methods=['GET'])
def get_species_by_id(species_id):
    return controllers.get_species_by_id(species_id)
