from flask import Blueprint, request

import controllers

category = Blueprint('category', __name__) 

# CREATE
@category.route('/category', methods=['POST'])
def create_category():
    return controllers.create_category()

# READ
@category.route('/categories', methods=['GET'])
def get_categories():
    return controllers.get_all_categories()

@category.route('/category/<category_id>', methods=['GET'])
def get_category(category_id):
    return controllers.get_category_by_id(category_id)

# UPDATE
@category.route('/category/<category_id>', methods=['PUT'])
def update_category(category_id):
    return controllers.update_category_by_id(category_id)

# DELETE
@category.route('/category/delete/<category_id>', methods=['DELETE'])
def delete_category(category_id):
    return controllers.delete_category_by_id(category_id)
