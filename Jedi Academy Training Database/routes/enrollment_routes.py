from flask import Blueprint

import controllers

enrollment = Blueprint('enrollment', __name__)

@enrollment.route('/enrollment', methods=['POST'])
def create_padawan_course():
    return controllers.create_padawan_course()

@enrollment.route('/enrollment/<padawan_id>/<course_id>', methods=['DELETE'])
def delete_padawan_course_by_ids(padawan_id, course_id):
    return controllers.delete_padawan_course_by_ids(padawan_id, course_id)