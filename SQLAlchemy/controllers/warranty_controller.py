from flask import jsonify, request
from db import db
from models.warranty import Warranties


# CREATE
def add_warranty():
    post_data = request.form if request.form else request.get_json()

    fields = ['product_id', 'warranty_months']
    required_fields = ['product_id', 'warranty_months']

    values = {}

    for field in fields:
        field_data = post_data.get(field)
       
        if field_data in required_fields and not field_data:
            return jsonify({"message": f'{field} is required'}), 400

        values[field] = field_data

    try:
        values['warranty_months'] = int(values['warranty_months'])
    except (ValueError, TypeError):
        return jsonify({"message": "warranty_months must be a valid integer"}), 400

    new_warranty = Warranties(values['product_id'], values['warranty_months'])

    try:
        db.session.add(new_warranty)
        db.session.commit()
    # except:
    #     db.session.rollback()
    #     return jsonify({"message": "unable to create record"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error creating warranty: {str(e)}"}), 400

    query = db.session.query(Warranties).filter(Warranties.product_id == values['product_id']).first()

    warranty = {
        "warranty_id": query.warranty_id,
        "product_id": query.product_id,
        "warranty_months": query.warranty_months,
    }

    return jsonify({"message": "warranty created", "result": warranty}), 200
# READ

def get_all_warranties():
    query = db.session.query(Warranties).all()

    print(query)

    warranty_list = []

    for warranty in query:
        warranty_dict = {
            'warranty_id': warranty.warranty_id,
            'warranty_months': warranty.warranty_months,
            'product_id': warranty.product_id
        }

        warranty_list.append(warranty_dict)

    return jsonify({"message": "warranties found", "results": warranty_list}), 200


def get_warranty_by_id(warranty_id):
    query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()
    if not query:
        return jsonify({"message": f"warranty does not exist"}), 400

    warranty = {
        'warranty_id': query.warranty_id,
        'warranty_months': query.warranty_months,
        'product_id': query.product_id,
    }

    return jsonify({"message": "warranty found", "results": warranty}), 200

# UPDATE

def update_warranty_by_id(warranty_id):
    post_data = request.form if request.form else request.get_json()
    query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()
    
    query.product_id = post_data.get("product_id", query.product_id)
    query.warranty_months = post_data.get("warranty_months", query.warranty_months)
    
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to update record"}), 400

    updated_warranty_query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()

    warranty = {
        'warranty_id': updated_warranty_query.warranty_id,
        'warranty_months': updated_warranty_query.warranty_months,
        'product_id': updated_warranty_query.product_id,
    }

    return jsonify({"message": "warranty updated", "results": warranty}), 200

# DELETE
def delete_warranty_by_id(warranty_id):
    warranty_query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()

    if not warranty_query:
        return jsonify({"message": f"warranty by id {warranty_id} does not exist"}), 400    

    try:
        db.session.delete(warranty_query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete record"}), 400

    return jsonify({"message": "warranty deleted"}), 200