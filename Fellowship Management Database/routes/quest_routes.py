from flask import Blueprint, request

import controllers

quest = Blueprint('quest', __name__)

@quest.route('/quest', methods=['POST'])
def create_quest():
    return controllers.create_quest()
@quest.route('/quest/<quest_id>', methods=['GET'])
def get_quest(quest_id):
    return controllers.get_quest_by_id(quest_id)
@quest.route('/quests/<difficulty_level>', methods=['GET'])
def get_quests(difficulty_level):
    return controllers.get_quests_by_difficulty(difficulty_level)
@quest.route('/quest/<quest_id>', methods=['PUT'])
def update_quest(quest_id):
    return controllers.update_quest_by_id(quest_id)
@quest.route('/quest/<quest_id>/complete', methods=['PUT'])
def complete_quest(quest_id):
    return controllers.set_quest_completed(quest_id)
@quest.route('/quest/delete/<quest_id>', methods=['DELETE'])
def delete_quest(quest_id):
    return controllers.delete_quest_by_id(quest_id)