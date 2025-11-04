from flask import jsonify, request
from db import db

from models.product import Products, product_schema, products_schema
from models.category import Categories, category_schema, categories_schema
from util.reflection import populate_object

# CREATE
def create_product():
    data = request.form if request.form else request.get_json()
    new_product = Products.new_product_obj()

    populate_object(new_product, data)

    try:
        db.session.add(new_product)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create record"}), 400

    return jsonify({"message": "product created", "results": product_schema.dump(new_product)}), 201

def create_product_category():
    post_data = request.form if request.form else request.get_json()
    
    product_id = post_data.get('product_id')
    category_id = post_data.get('category_id')

    product = db.session.query(Products).filter(Products.product_id == product_id).first()
    category = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if not product or not category:
        return jsonify({"message": "product or category not found"}), 404
    
    product.categories.append(category)

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create association"}), 400
    
    return jsonify({"message": "product added to category", "results": product_schema.dump(product)}), 201

# READ
def get_all_products():
    query = db.session.query(Products).all()
    return jsonify({"results": products_schema.dump(query)}), 200

def get_product_by_id(product_id):
    query = db.session.query(Products).filter(Products.product_id == product_id).first()
    if not query:
        return jsonify({"message": "product not found"}), 404
    return jsonify({"results": product_schema.dump(query)}), 200

def get_products_by_company_id(company_id):
    query = db.session.query(Products).filter(Products.company_id == company_id).all()
    if not query:
        return jsonify({"message": "products not found"}), 404
    return jsonify({"results": products_schema.dump(query)}), 200

def get_all_active_products():
    query = db.session.query(Products).filter(Products.is_active == True).all()
    return jsonify({"results": products_schema.dump(query)}), 200

# UPDATE

def update_product_by_id(product_id):
    query = db.session.query(Products).filter(Products.product_id == product_id).first()
    data = request.form if request.form else request.get_json()

    populate_object(query, data)

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to update record"}), 400

    return jsonify({"message": "product updated", "results": product_schema.dump(query)}), 200

# DELETE

def delete_product_by_id(product_id):
    query = db.session.query(Products).filter(Products.product_id == product_id).first()
    if not query:
        return jsonify({"message": "product not found"}), 404

    try:
        db.session.delete(query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete record"}), 400

    return jsonify({"message": "product deleted"}), 200