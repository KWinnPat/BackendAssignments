from flask import Blueprint, request

import controllers

hero = Blueprint('hero', __name__)

@hero.route('/hero', methods=['POST'])
def create_hero():
    return controllers.create_hero()
@hero.route('/hero-quest', methods=['POST'])
def assign_quest_to_hero():
    return controllers.assign_quest_to_hero()
@hero.route('/hero/<hero_id>', methods=['GET'])
def get_hero(hero_id):
    return controllers.get_hero_by_id(hero_id)
@hero.route('/heroes', methods=['GET'])
def get_heroes():
    return controllers.get_all_heroes()
@hero.route('/hero/<hero_id>/quests', methods=['GET'])
def get_hero_quests(hero_id):
    return controllers.get_hero_quests(hero_id)
@hero.route('/heroes/alive', methods=['GET'])
def get_alive_heroes():
    return controllers.get_alive_heroes()
@hero.route('/hero/<hero_id>', methods=['PUT'])
def update_hero(hero_id):
    return controllers.update_hero_by_id(hero_id)
@hero.route('/hero/delete/<hero_id>', methods=['DELETE'])
def delete_hero(hero_id):
    return controllers.delete_hero_by_id(hero_id)

