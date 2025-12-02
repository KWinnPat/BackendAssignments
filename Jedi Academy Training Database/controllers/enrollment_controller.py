from flask import jsonify, request
from flask_bcrypt import generate_password_hash

from db import db
from models.padawan_course import PadawanCourses, padawan_course_schema, padawan_courses_schema
from util.reflection import populate_object
from lib.authenticate import authenticate, authenticate_return_auth

#CREATE
@authenticate_return_auth
def create_padawan_course(auth_info):
    post_data = request.form if request.form else request.get_json()

    new_padawan_course = PadawanCourses.new_padawan_course_obj()
    if auth_info.user.force_rank == 'master' or auth_info.user.force_rank == 'council' or auth_info.user.force_rank == 'grand-master':
        populate_object(new_padawan_course, post_data)

        try:
            db.session.add(new_padawan_course)
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message": "unable to create record"}), 400

        return jsonify({"message": "padawan course created", "result": padawan_course_schema.dump(new_padawan_course)}), 201
    return jsonify({"message": "unauthorized"}), 401

#DELETE
@authenticate
def delete_padawan_course_by_ids(padawan_id, course_id, auth_info):
    query = db.session.query(PadawanCourses).filter({(PadawanCourses.padawan_id == padawan_id) and (PadawanCourses.course_id == course_id)}).first()

    if not query:
        return jsonify({"message": "padawan course not found"}), 404

    try:
        db.session.delete(query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete record"}), 400

    return jsonify({"message": "padawan course deleted"}), 200
