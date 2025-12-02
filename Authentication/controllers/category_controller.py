from flask import jsonify, request
from db import db

from models.category import Categories, category_schema, categories_schema
from util.reflection import populate_object
from lib.authenticate import authenticate, authenticate_return_auth

# CREATE
@authenticate_return_auth
def create_category(auth_info):
    data = request.form if request.form else request.get_json()
    new_category = Categories.new_category_obj()

    if auth_info.user.role == 'super-admin':
        populate_object(new_category, data)

        try:
            db.session.add(new_category)
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message": "unable to create record"}), 400
        
        return jsonify({"message": "category created", "results": category_schema.dump(new_category)}), 201
    
    return jsonify({"message": "unauthorized"}), 401
# READ
@authenticate
def get_all_categories():
    query = db.session.query(Categories).all()
    return jsonify({"results": categories_schema.dump(query)}), 200

@authenticate
def get_category_by_id(category_id):
    query = db.session.query(Categories).filter(Categories.category_id == category_id).first()
    if not query:
        return jsonify({"message": "category not found"}), 404
    return jsonify({"results": category_schema.dump(query)}), 200



# UPDATE
@authenticate_return_auth
def update_category_by_id(category_id, auth_info):
    query = db.session.query(Categories).filter(Categories.category_id == category_id).first()
    data = request.form if request.form else request.get_json()

    if auth_info.user.role == 'super-admin':

        populate_object(query, data)

        try:
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message": "unable to update record"}), 400

        return jsonify({"message": "category updated", "results": category_schema.dump(query)}), 200
    
    return jsonify({"message": "unauthorized"}), 401
# DELETE
@authenticate_return_auth
def delete_category_by_id(category_id, auth_info):
    query = db.session.query(Categories).filter(Categories.category_id == category_id).first()
    if auth_info.user.role == 'super-admin':
        if not query:
            return jsonify({"message": "category not found"}), 404

        try:
            db.session.delete(query)
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message": "unable to delete record"}), 400

        return jsonify({"message": "category deleted"}), 200
    return jsonify({"message": "unauthorized"}), 401