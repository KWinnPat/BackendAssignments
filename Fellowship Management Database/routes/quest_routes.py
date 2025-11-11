from flask import Blueprint, request

import controllers

quest = Blueprint('quest', __name__)

@quest.route('/quest', methods=['POST'])
def create_quest():
    return controllers.create_quest()
@quest.route('/quest/<quest_id>', methods=['GET'])
def get_quest(quest_id):
    return controllers.get_quest_by_id(quest_id)
@quest.route('/quests', methods=['GET'])
def get_quests():
    return controllers.get_quests_by_difficulty()
@quest.route('/quest/<quest_id>', methods=['PUT'])
def update_quest(quest_id):
    return controllers.update_quest_by_id(quest_id)
@quest.route('/quest/delete/<quest_id>', methods=['DELETE'])
def delete_quest(quest_id):
    return controllers.delete_quest_by_id(quest_id)