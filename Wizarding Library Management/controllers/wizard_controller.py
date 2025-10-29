from flask import jsonify, request
from db import db
from models.wizard import Wizards
from models.wizard_specialization import Wizard_Specializations


# CREATE

def add_wizard():
    post_data = request.form if request.form else request.get_json()

    fields = ['wizard_name', 'school_id', 'house', 'year_enrolled', 'magical_power_level', 'active']
    required_fields = ['wizard_name', 'school_id']

    values = {}

    for field in fields:
        field_data = post_data.get(field)
       
        if field_data in required_fields and not field_data:
            return jsonify({"message": f'{field} is required'}), 400

        values[field] = field_data

    new_wizard = Wizards(values['wizard_name'], values['school_id'], values['house'], values['year_enrolled'], values['magical_power_level'], values.get('active', True))

    try:
        db.session.add(new_wizard)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create record"}), 400
    
    query = db.session.query(Wizards).filter(Wizards.wizard_name == values['wizard_name']).first()

    wizard = {
        "wizard_id": query.wizard_id,
        "wizard_name": query.wizard_name,
        "school_id": query.school_id,
        "house": query.house,
        "year_enrolled": query.year_enrolled,
        "magical_power_level": query.magical_power_level,
        "active": query.active
    }

    return jsonify({"message": "wizard created", "result": wizard}), 200

def add_wizard_specialization():
    post_data = request.form if request.form else request.get_json()

    fields = ['wizard_id', 'spell_id', 'proficiency_level', 'date_learned']
    required_fields = ['wizard_id', 'spell_id']

    values = {}

    for field in fields:
        field_data = post_data.get(field)
       
        if field_data in required_fields and not field_data:
            return jsonify({"message": f'{field} is required'}), 400

        values[field] = field_data

    new_specialization = Wizard_Specializations(values['wizard_id'], values['spell_id'], values['proficiency_level'], values.get('date_learned'))

    try:
        db.session.add(new_specialization)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create record"}), 400
    
    query = db.session.query(Wizard_Specializations).filter(
        Wizard_Specializations.wizard_id == values['wizard_id'],
        Wizard_Specializations.spell_id == values['spell_id']
    ).first()

    specialization = {
        "wizard_id": query.wizard_id,
        "spell_id": query.spell_id,
        "proficiency_level": query.proficiency_level,
        "date_learned": query.date_learned
    }

    return jsonify({"message": "wizard specialization created", "result": specialization}), 200

# READ

def get_all_wizards():
    query = db.session.query(Wizards).all()

    print(query)

    wizard_list = []

    for wizard in query:
        wizard_dict = {
            'wizard_id': wizard.wizard_id,
            'wizard_name': wizard.wizard_name,
            'school_id': wizard.school_id,
            'house': wizard.house,
            'year_enrolled': wizard.year_enrolled,
            'magical_power_level': wizard.magical_power_level,
            'active': wizard.active
        }
        wizard_list.append(wizard_dict)

    return jsonify({"message": "all wizards retrieved", "result": wizard_list}), 200

def get_active_wizards():
    query = db.session.query(Wizards).filter(Wizards.active == True).all()

    print(query)

    wizard_list = []

    for wizard in query:
        wizard_dict = {
            'wizard_id': wizard.wizard_id,
            'wizard_name': wizard.wizard_name,
            'school_id': wizard.school_id,
            'house': wizard.house,
            'year_enrolled': wizard.year_enrolled,
            'magical_power_level': wizard.magical_power_level,
            'active': wizard.active
        }
        wizard_list.append(wizard_dict)

    return jsonify({"message": "active wizards retrieved", "result": wizard_list}), 200

def get_all_wizards_by_house(house):
    query = db.session.query(Wizards).filter(Wizards.house == house).all()

    print(query)

    wizard_list = []

    for wizard in query:
        wizard_dict = {
            'wizard_id': wizard.wizard_id,
            'wizard_name': wizard.wizard_name,
            'school_id': wizard.school_id,
            'house': wizard.house,
            'year_enrolled': wizard.year_enrolled,
            'magical_power_level': wizard.magical_power_level,
            'active': wizard.active
        }
        wizard_list.append(wizard_dict)

    return jsonify({"message": f"wizards from house {house} retrieved", "result": wizard_list}), 200

def get_wizard_by_id(wizard_id):
    query = db.session.query(Wizards).filter(Wizards.wizard_id == wizard_id).first()

    if not query:
        return jsonify({"message": "wizard not found"}), 404

    wizard = {
        'wizard_id': query.wizard_id,
        'wizard_name': query.wizard_name,
        'school_id': query.school_id,
        'house': query.house,
        'year_enrolled': query.year_enrolled,
        'magical_power_level': query.magical_power_level,
        'active': query.active
    }

    return jsonify({"message": "wizard found", "result": wizard}), 200

def get_all_wizards_by_power_level(magical_power_level):
    query = db.session.query(Wizards).filter(Wizards.magical_power_level >= magical_power_level).all()

    print(query)

    wizard_list = []

    for wizard in query:
        wizard_dict = {
            'wizard_id': wizard.wizard_id,
            'wizard_name': wizard.wizard_name,
            'school_id': wizard.school_id,
            'house': wizard.house,
            'year_enrolled': wizard.year_enrolled,
            'magical_power_level': wizard.magical_power_level,
            'active': wizard.active
        }
        wizard_list.append(wizard_dict)

    return jsonify({"message": f"wizards with magical power level >= {magical_power_level} retrieved", "result": wizard_list}), 200

# UPDATE

def update_wizard_by_id(wizard_id):
    put_data = request.form if request.form else request.get_json()

    fields = ['wizard_name', 'school_id', 'house', 'year_enrolled', 'magical_power_level', 'active']

    values = {}

    for field in fields:
        field_data = put_data.get(field)
        if field_data is not None:
            values[field] = field_data

    query = db.session.query(Wizards).filter(Wizards.wizard_id == wizard_id).first()

    if not query:
        return jsonify({"message": "wizard not found"}), 404

    for key, value in values.items():
        setattr(query, key, value)

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to update record"}), 400

    updated_wizard = {
        "wizard_id": query.wizard_id,
        "wizard_name": query.wizard_name,
        "school_id": query.school_id,
        "house": query.house,
        "year_enrolled": query.year_enrolled,
        "magical_power_level": query.magical_power_level,
        "active": query.active
    }

    return jsonify({"message": "wizard updated", "result": updated_wizard}), 200
 
# DELETE
def delete_wizard_by_id(wizard_id):
    query = db.session.query(Wizards).filter(Wizards.wizard_id == wizard_id).first()
    if not query:
        return jsonify({"message": f"wizard does not exist"}), 400

    try:
        db.session.delete(query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete record"}), 400

    return jsonify({"message": "wizard deleted"}), 200
