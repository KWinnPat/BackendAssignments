
from flask import Flask, jsonify, request
from data import product_records

app = Flask(__name__)

@app.route('/product/create', methods=['POST'])
def create_products():
    new_product = request.get_json()
    product_records.append(new_product)
    return jsonify({"message": "product created", "results": new_product}), 201

@app.route('/products', methods=['GET'])
def read_products():
    return jsonify({"message": "all products", "results": product_records}), 200

@app.route('/products/active', methods=['GET'])
def read_active_products():
    active_products = [product for product in product_records if product['active']]
    return jsonify({"message": "active products", "results": active_products}), 200

@app.route('/product/<id>', methods=['GET'])
def read_product_by_id(id):
    for product in product_records:
        if product['product_id'] == int(id):
            return jsonify({"message": "product found", "results": product}), 200
    return jsonify({"message": f'Product with id {id} not found.'}), 404

@app.route('/product/update/<id>', methods=['PUT'])
def update_products(id):
    updated_product = request.get_json()
    for index, product in enumerate(product_records):
        if product['product_id'] == int(id):
            product_records[index].update(updated_product)
            return jsonify({"message": "product updated", "results": product_records[index]}), 201
    return jsonify({"message": f'Product with id {id} not found.'}), 404

@app.route('/product/delete/<id>', methods=['DELETE'])
def delete_products(id):
    for index, product in enumerate(product_records):
        if product['product_id'] == int(id):
            deleted_product = product_records.pop(index)
            return jsonify({"message": "product deleted", "results": deleted_product}), 200
    return jsonify({"message": f'Product with id {id} not found.'}), 404

if __name__ == '__main__':
  app.run(port='8086', host='0.0.0.0')