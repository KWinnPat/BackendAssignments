from flask import jsonify, request
from db import db
from models.magical_school import Magical_Schools


# CREATE

def add_school():
    post_data = request.form if request.form else request.get_json()

    fields = ['school_name', 'location', 'founded_year', 'headmaster', 'active']
    required_fields = ['school_name', 'location']

    values = {}

    for field in fields:
        field_data = post_data.get(field)
       
        if field_data in required_fields and not field_data:
            return jsonify({"message": f'{field} is required'}), 400

        values[field] = field_data

    new_school = Magical_Schools(values['school_name'], values.get('location'), values.get('founded_year'), values.get('headmaster'))

    try:
        db.session.add(new_school)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create record"}), 400
    
    query = db.session.query(Magical_Schools).filter(Magical_Schools.school_name == values['school_name']).first()

    school = {
        "school_id": query.school_id,
        "school_name": query.school_name,
        "location": query.location,
        "founded_year": query.founded_year,
        "headmaster": query.headmaster,
    }

    return jsonify({"message": "school created", "result": school}), 200

# READ

def get_all_schools():
    query = db.session.query(Magical_Schools).all()

    print(query)

    school_list = []

    for school in query:
        school_dict = {
            'school_id': school.school_id,
            'school_name': school.school_name,
            'location': school.location,
            'founded_year': school.founded_year,
            'headmaster': school.headmaster
        }

        school_list.append(school_dict)

    return jsonify({"message": "schools found", "results": school_list}), 200


def get_school_by_id(school_id):
    query = db.session.query(Magical_Schools).filter(Magical_Schools.school_id == school_id).first()
    if not query:
        return jsonify({"message": f"school does not exist"}), 400

    school = {
        'school_id': query.school_id,
        'school_name': query.school_name,
        'location': query.location,
        'founded_year': query.founded_year,
        'headmaster': query.headmaster
    }

    return jsonify({"message": "school found", "result": school}), 200

# UPDATE

def update_school_by_id(school_id):
    post_data = request.form if request.form else request.get_json()
    query = db.session.query(Magical_Schools).filter(Magical_Schools.school_id == school_id).first()

    query.school_name = post_data.get("school_name", query.school_name)
    query.location = post_data.get("location", query.location)
    query.founded_year = post_data.get("founded_year", query.founded_year)
    query.headmaster = post_data.get("headmaster", query.headmaster)
    
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to update record"}), 400

    updated_school_query = db.session.query(Magical_Schools).filter(Magical_Schools.school_id == school_id).first()

    school = {
        'school_id': updated_school_query.school_id,
        'school_name': updated_school_query.school_name,
        'location': updated_school_query.location,
        'founded_year': updated_school_query.founded_year,
        'headmaster': updated_school_query.headmaster
    }

    return jsonify({"message": "school updated", "result": school}), 200
 
# DELETE
def delete_school_by_id(school_id):
    query = db.session.query(Magical_Schools).filter(Magical_Schools.school_id == school_id).first()
    if not query:
        return jsonify({"message": f"school does not exist"}), 400

    try:
        db.session.delete(query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": f"unable to delete record"}), 400

    return jsonify({"message": "school deleted"}), 200
