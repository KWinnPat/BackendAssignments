from flask import Blueprint, request

import controllers

race = Blueprint('race', __name__)

@race.route('/race', methods=['POST'])
def create_race():
    return controllers.create_race()
@race.route('/race/<race_id>', methods=['GET'])
def get_race(race_id):
    return controllers.get_race_by_id(race_id)
@race.route('/races', methods=['GET'])
def get_races():
    return controllers.get_all_races()
@race.route('/race/<race_id>', methods=['PUT'])
def update_race(race_id):
    return controllers.update_race_by_id(race_id)
@race.route('/race/delete/<race_id>', methods=['DELETE'])
def delete_race(race_id):
    return controllers.delete_race_by_id(race_id) 