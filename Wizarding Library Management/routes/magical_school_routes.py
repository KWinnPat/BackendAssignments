from flask import Blueprint

import controllers

school = Blueprint('magical_school', __name__)

@school.route('/school', methods=['POST'])
def add_school():
    return controllers.add_school()

@school.route('/schools', methods=['GET'])
def get_all_schools():
    return controllers.get_all_schools()

@school.route('/school/<school_id>', methods=['GET'])
def get_school_by_id(school_id):
    return controllers.get_school_by_id(school_id)

@school.route('/school/<school_id>', methods=['PUT'])
def update_school_by_id(school_id):
    return controllers.update_school_by_id(school_id)

@school.route('/school/delete/<school_id>', methods=['DELETE'])
def delete_school_by_id(school_id):
    return controllers.delete_school_by_id(school_id)