from flask import Blueprint, request

import controllers

product = Blueprint('product', __name__)

# CREATE
@product.route('/product', methods=['POST'])
def create_product():
    return controllers.create_product()

@product.route('/product/category', methods=['POST'])
def create_product_category():
    return controllers.create_product_category()

# READ
@product.route('/products', methods=['GET'])
def get_products():
    return controllers.get_all_products()

@product.route('/products/active', methods=['GET'])
def get_active_products():
    return controllers.get_all_active_products()

@product.route('/product/<product_id>', methods=['GET'])
def get_product(product_id):
    return controllers.get_product_by_id(product_id)

@product.route('/products/company/<company_id>', methods=['GET'])
def get_products_by_company(company_id):
    return controllers.get_products_by_company_id(company_id)

# UPDATE
@product.route('/product/<product_id>', methods=['PUT'])
def update_product(product_id):
    return controllers.update_product_by_id(product_id)

# DELETE
@product.route('/product/delete/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    return controllers.delete_product_by_id(product_id)