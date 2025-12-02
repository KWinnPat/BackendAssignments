from flask import Blueprint, request

import controllers

warranty = Blueprint('warranty', __name__)

# CREATE
@warranty.route('/warranty', methods=['POST'])
def create_warranty():
    return controllers.create_warranty()

# READ
@warranty.route('/warranty/<warranty_id>', methods=['GET'])
def get_warranty(warranty_id):
    return controllers.get_warranty_by_id(warranty_id)

# UPDATE
@warranty.route('/warranty/<warranty_id>', methods=['PUT'])
def update_warranty(warranty_id):
    return controllers.update_warranty_by_id(warranty_id)

# DELETE
@warranty.route('/warranty/delete/<warranty_id>', methods=['DELETE'])
def delete_warranty(warranty_id):
    return controllers.delete_warranty_by_id(warranty_id)
