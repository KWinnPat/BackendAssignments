from flask import Blueprint

import controllers

master = Blueprint('master', __name__)

@master.route('/master', methods=['POST'])
def promote_to_master():
    return controllers.promote_to_master()

@master.route('/masters', methods=['GET'])
def get_all_masters():
    return controllers.get_all_masters()

@master.route('/master/<master_id>', methods=['PUT'])
def update_master_specialization(master_id):
    return controllers.update_master_specialization(master_id)

@master.route('/master/<master_id>', methods=['DELETE'])
def delete_master_by_id(master_id):
    return controllers.delete_master_by_id(master_id)
