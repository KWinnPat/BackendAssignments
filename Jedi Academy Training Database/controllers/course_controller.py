from flask import jsonify, request
from flask_bcrypt import generate_password_hash

from db import db
from models.course import Courses, course_schema, courses_schema
from models.padawan_course import PadawanCourses, padawan_course_schema, padawan_courses_schema
from util.reflection import populate_object
from lib.authenticate import authenticate, authenticate_return_auth

#CREATE
@authenticate_return_auth
def create_course(auth_info):
    post_data = request.form if request.form else request.get_json()
    instructor_id = post_data.get('instructor_id')

    new_course = Courses.new_course_obj()
    if auth_info.user.force_rank == 'grand-master':
        populate_object(new_course, post_data)

        try:
            db.session.add(new_course)
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message": "unable to create record"}), 400

        return jsonify({"message": "course created", "result": course_schema.dump(new_course)}), 201
    return jsonify({"message": "unauthorized"}), 401

#READ
@authenticate
def get_courses_by_difficulty(difficulty):
    course_query = db.session.query(Courses).filter(Courses.difficulty == difficulty).all()
    return jsonify({"message": "course found", "result": course_schema.dump(course_query)}), 200

#UPDATE
@authenticate_return_auth
def update_course_by_id(course_id, auth_info):
    query = db.session.query(Courses).filter(Courses.course_id == course_id).first()
    data = request.form if request.form else request.get_json()
    if auth_info.user.master_id == query.instructor_id or auth_info.user.force_rank == 'council' or auth_info.user.force_rank == 'grand-master':
        populate_object(query, data)

        try:
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message": "unable to update record"}), 400

        return jsonify({"message": "course updated", "results": course_schema.dump(query)}), 200
    return jsonify({"message": "unauthorized"}), 401

#DELETE
@authenticate_return_auth
def delete_course_by_id(course_id, auth_info):
    query = db.session.query(Courses).filter(Courses.course_id == course_id).first()
    if auth_info.user.master_id == query.instructor_id or auth_info.user.force_rank == 'council' or auth_info.user.force_rank == 'grand-master':
        if not query:
            return jsonify({"message": "course not found"}), 404
    
        try:
            db.session.delete(query)
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message": "unable to delete record"}), 400
    
        return jsonify({"message": "course deleted"}), 200
    return jsonify({"message": "unauthorized"}), 401