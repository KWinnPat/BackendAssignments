from flask import jsonify, request
from db import db
from models.product import Products
from models.category import Categories


# CREATE
def add_product():
    post_data = request.form if request.form else request.get_json()

    fields = ['product_name', 'company_id', 'price', 'description', 'active']
    required_fields = ['product_name']

    values = {}

    for field in fields:
        field_data = post_data.get(field)
       
        if field_data in required_fields and not field_data:
            return jsonify({"message": f'{field} is required'}), 400

        values[field] = field_data

    new_product = Products(values['product_name'], values['description'], values['price'], values['company_id'], values.get('active', True))

    try:
        db.session.add(new_product)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create record"}), 400

    query = db.session.query(Products).filter(Products.product_name == values['product_name']).first()

    product = {
        "product_id": query.product_id,
        "product_name": query.product_name,
        "company_id": query.company_id,
        "price": query.price,
        "description": query.description,
        "active": query.active
    }

    return jsonify({"message": "product created", "result": product}), 200

def add_product_category():
    post_data = request.form if request.form else request.get_json()
    
    fields = ['product_id', 'category_id']
    required_fields = ['product_id', 'category_id']

    values = {}

    for field in fields:
        field_data = post_data.get(field)
        if field_data in required_fields and not field_data:
            return jsonify({"message": f'{field} is required'}), 400
        
        values[field] = field_data

    product_query = db.session.query(Products).filter(Products.product_id == values['product_id']).first()
    category_query = db.session.query(Categories).filter(Categories.category_id == values['category_id']).first()

    if product_query and category_query:
        product_query.categories.append(category_query)

        db.session.commit()

        categories_list = []

        for category in product_query.categories:
            categories_list.append({
                "category_id": category.category_id,
                "category_name": category.category_name
            })

        company_dict = {
            "company_id": product_query.company.company_id,
            "company_name": product_query.company.company_name
        }

        product = {
            'product_id': product_query.product_id,
            'product_name': product_query.product_name,
            'description': product_query.description,
            'price': product_query.price,
            'active': product_query.active,
            'company': company_dict,
            'categories': categories_list,
        }

    return jsonify({"message": "category added to product", "result": product}), 201


# READ
def get_all_products():
    query = db.session.query(Products).all()
    
    print(query)

    product_list = []

    for product in query:
        categories_list = []
        for category in product.categories:
            categories_list.append({
                "category_id": category.category_id,
                "category_name": category.category_name
            })

        company_dict = {
            'company_id': product.company.company_id,
            'company_name': product.company.company_name
        }

        if product.warranty:
            warranty_dict = {
                'warranty_id': product.warranty.warranty_id,
                'warranty_months': product.warranty.warranty_months
            }
        else:
            warranty_dict = {}

        product_dict = {
            'product_id': product.product_id,
            'product_name': product.product_name,
            'description': product.description,
            'price': product.price,
            'active': product.active,
            'company': company_dict,
            'warranty': warranty_dict,
            'categories': categories_list,
        }
        product_list.append(product_dict)

    return jsonify({"message": "products found", "result": product_list}), 200

def get_product_by_id(product_id):
    query = db.session.query(Products).filter(Products.product_id == product_id).first()
    if not query:
        return jsonify({"message": f"product does not exist"}), 400

    categories_list = []

    for category in query.categories:
        categories_list.append({
            "category_id": category.category_id,
            "category_name": category.category_name
        })

    company_dict = {
        'company_id': query.company.company_id,
        'company_name': query.company.company_name
    }

    if query.warranty:
        warranty_dict = {
            'warranty_id': query.warranty.warranty_id,
            'warranty_months': query.warranty.warranty_months
        }
    else:
        warranty_dict = {}

    product = {
        'product_id': query.product_id,
        'product_name': query.product_name,
        'description': query.description,
        'price': query.price,
        'active': query.active,
        'company': company_dict,
        'warranty': warranty_dict,
        'categories': categories_list,
    }

    return jsonify({"message": "product found", "result": product}), 200

def get_product_by_company_id(company_id):
    query = db.session.query(Products).filter(Products.company_id == company_id).first()
    if not query:
        return jsonify({"message": f"product does not exist"}), 400

    categories_list = []

    for category in query.categories:
        categories_list.append({
            "category_id": category.category_id,
            "category_name": category.category_name
        })

    company_dict = {
        'company_id': query.company.company_id,
        'company_name': query.company.company_name
    }

    if query.warranty:
        warranty_dict = {
            'warranty_id': query.warranty.warranty_id,
            'warranty_months': query.warranty.warranty_months
        }
    else:
        warranty_dict = {}

    product = {
        'product_id': query.product_id,
        'product_name': query.product_name,
        'description': query.description,
        'price': query.price,
        'active': query.active,
        'company': company_dict,
        'warranty': warranty_dict,
        'categories': categories_list,
    }

    return jsonify({"message": "product found", "result": product}), 200

def get_active_products():
    query = db.session.query(Products).filter(Products.active == True).all()
    
    print(query)

    product_list = []

    for product in query:
        categories_list = []
        print(product)
    

    for category in product.categories:
        categories_list.append({
            "category_id": category.category_id,
            "category_name": category.category_name
        })

    company_dict = {
        'company_id': product.company.company_id,
        'company_name': product.company.company_name
    }

    if product.warranty:
        warranty_dict = {
            'warranty_id': product.warranty.warranty_id,
            'warranty_months': product.warranty.warranty_months
        }
    else:
        warranty_dict = {}
            
        product_dict = {
            'product_id': product.product_id,
            'product_name': product.product_name,
            'description': product.description,
            'price': product.price,
            'active': product.active,
            'company': company_dict,
            'warranty': warranty_dict,
            'categories': categories_list,
        }

        product_list.append(product_dict)

    return jsonify({"message": "products found", "result": product_list}), 200
# UPDATE

def update_product_by_id(product_id):
    post_data = request.form if request.form else request.get_json()
    query = db.session.query(Products).filter(Products.product_id == product_id).first()
    
    query.product_name = post_data.get("product_name", query.product_name)
    query.description = post_data.get("description", query.description)
    query.price = post_data.get("price", query.price)
    query.active = post_data.get("active", query.active)
    query.company_id = post_data.get("company_id", query.company_id)
    
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to update record"}), 400

    updated_product_query = db.session.query(Products).filter(Products.product_id == product_id).first()

    product = {
        'product_id': updated_product_query.product_id,
        'product_name': updated_product_query.product_name,
        'company_id': updated_product_query.company_id,
        'price': updated_product_query.price,
        'description': updated_product_query.description,
        'active': updated_product_query.active
    }

    return jsonify({"message": "product updated", "results": product}), 200

# DELETE
def delete_product_by_id(product_id):
    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()

    if not product_query:
        return jsonify({"message": f"product by id {product_id} does not exist"}), 400    

    try:
        db.session.delete(product_query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete record"}), 400

    return jsonify({"message": "product deleted"}), 200