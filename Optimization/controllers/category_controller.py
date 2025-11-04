from flask import jsonify, request
from db import db

from models.category import Categories, category_schema, categories_schema
from util.reflection import populate_object

# CREATE
def create_category():
    data = request.form if request.form else request.get_json()
    new_category = Categories.new_category_obj()

    populate_object(new_category, data)

    try:
        db.session.add(new_category)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create record"}), 400

    return jsonify({"message": "category created", "results": category_schema.dump(new_category)}), 201

# READ
def get_all_categories():
    query = db.session.query(Categories).all()
    return jsonify({"results": categories_schema.dump(query)}), 200

def get_category_by_id(category_id):
    query = db.session.query(Categories).filter(Categories.category_id == category_id).first()
    if not query:
        return jsonify({"message": "category not found"}), 404
    return jsonify({"results": category_schema.dump(query)}), 200



# UPDATE

def update_category_by_id(category_id):
    query = db.session.query(Categories).filter(Categories.category_id == category_id).first()
    data = request.form if request.form else request.get_json()

    populate_object(query, data)

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to update record"}), 400

    return jsonify({"message": "category updated", "results": category_schema.dump(query)}), 200

# DELETE

def delete_category_by_id(category_id):
    query = db.session.query(Categories).filter(Categories.category_id == category_id).first()
    if not query:
        return jsonify({"message": "category not found"}), 404

    try:
        db.session.delete(query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete record"}), 400

    return jsonify({"message": "category deleted"}), 200