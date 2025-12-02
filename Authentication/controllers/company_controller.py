from flask import jsonify, request
from db import db

from models.company import Companies, company_schema, companies_schema
from util.reflection import populate_object
from lib.authenticate import authenticate, authenticate_return_auth

# CREATE
def create_company():
    data = request.form if request.form else request.get_json()
    new_company = Companies.new_company_obj()

    populate_object(new_company, data)

    try:
        db.session.add(new_company)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create record"}), 400

    return jsonify({"message": "company created", "results": company_schema.dump(new_company)}), 201

# READ
@authenticate
def get_all_companies():
    query = db.session.query(Companies).all()
    return jsonify({"results": companies_schema.dump(query)}), 200

@authenticate_return_auth
def get_company_by_id(company_id, auth_info):
    query = db.session.query(Companies).filter(Companies.company_id == company_id).first()
    
    if auth_info.user.role ==  'super-admin' or company_id == str(auth_info.user.company_id):
        if not query:
            return jsonify({"message": "company not found"}), 404
        return jsonify({"results": company_schema.dump(query)}), 200

    return jsonify({"message": "unauthorized"}), 401


# UPDATE
@authenticate_return_auth
def update_company_by_id(company_id, auth_info):
    query = db.session.query(Companies).filter(Companies.company_id == company_id).first()
    data = request.form if request.form else request.get_json()
    if auth_info.user.role == 'super-admin':
        populate_object(query, data)

        try:
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message": "unable to update record"}), 400

        return jsonify({"message": "company updated", "results": company_schema.dump(query)}), 200
    return jsonify({"message": "unauthorized"}), 401

# DELETE
@authenticate_return_auth
def delete_company_by_id(company_id, auth_info):
    query = db.session.query(Companies).filter(Companies.company_id == company_id).first()
    if auth_info.user.role ==  'super-admin':
        if not query:
            return jsonify({"message": "company not found"}), 404

        try:
            db.session.delete(query)
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message": "unable to delete record"}), 400

        return jsonify({"message": "company deleted"}), 200
    return jsonify({"message": "unauthorized"}), 401