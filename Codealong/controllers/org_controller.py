from flask import jsonify, request

from db import db
from models.organization import Organizations, org_schema, orgs_schema
from util.reflection import populate_object
from lib.authenticate import authenticate, authenticate_return_auth

def add_org():
    post_data = request.form if request.form else request.get_json()

    new_org = Organizations.new_org_obj()

    populate_object(new_org, post_data)

    try:
        db.session.add(new_org)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create record"}), 400
    
    return jsonify({"message": "organization created", "result": org_schema.dump(new_org)}), 201

@authenticate_return_auth
def get_all_orgs(auth_info):
    if auth_info.user.role == 'super-admin':
        orgs_query = db.session.query(Organizations).all()

        return jsonify({"message": "success", "result": orgs_schema.dump(orgs_query)}), 200
    
    return jsonify({"message": "unauthorized"}), 401

