from flask import jsonify, request
from db import db

from models.warranty import Warranties, warranty_schema, warranties_schema
from util.reflection import populate_object

# CREATE
def create_warranty():
    data = request.form if request.form else request.get_json()
    new_warranty = Warranties.new_warranty_obj()

    populate_object(new_warranty, data)

    try:
        db.session.add(new_warranty)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create record"}), 400

    return jsonify({"message": "warranty created", "results": warranty_schema.dump(new_warranty)}), 201

# READ
def get_warranty_by_id(warranty_id):
    query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()
    if not query:
        return jsonify({"message": "warranty not found"}), 404
    return jsonify({"results": warranty_schema.dump(query)}), 200



# UPDATE

def update_warranty_by_id(warranty_id):
    query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()
    data = request.form if request.form else request.get_json()

    populate_object(query, data)

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to update record"}), 400

    return jsonify({"message": "warranty updated", "results": warranty_schema.dump(query)}), 200

# DELETE

def delete_warranty_by_id(warranty_id):
    query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()
    if not query:
        return jsonify({"message": "warranty not found"}), 404

    try:
        db.session.delete(query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete record"}), 400

    return jsonify({"message": "warranty deleted"}), 200