from flask import Blueprint

import controllers

crystal = Blueprint('crystal', __name__)

@crystal.route('/crystal', methods=['POST'])
def create_crystal():
    return controllers.create_crystal()

@crystal.route('/crystals/<rarity_level>', methods=['GET'])
def get_crystals_by_rarity(rarity_level):
    return controllers.get_crystals_by_rarity(rarity_level)