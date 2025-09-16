from flask import jsonify, request

from data import product_records

def read_products_by_id(id):
    for product in product_records:
        if product['product_id'] == int(id):
            return jsonify({"message": "product found", "results": product}), 200
    return jsonify({"message": f'Product with id {id} not found.'}), 400