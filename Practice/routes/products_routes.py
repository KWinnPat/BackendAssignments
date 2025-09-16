from flask import Blueprint

from controllers import products_controller

product = Blueprint('products', __name__)

@product.route('/products/<id>', methods=['GET'])
def read_products_by_id(id):
    return products_controller.read_products_by_id(id)
