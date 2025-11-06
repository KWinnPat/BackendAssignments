from flask import Blueprint, request

import controllers

location = Blueprint('location', __name__)

# CREATE
@location.route('/location', methods=['POST'])
def create_location():
    return controllers.create_location()
# READ
@location.route('/location/<location_id>', methods=['GET'])
def get_location(location_id):
    return controllers.get_location_by_id(location_id)
# UPDATE
@location.route('/location/<location_id>', methods=['PUT'])
def update_location(location_id):
    return controllers.update_location_by_id(location_id)
# DELETE
@location.route('/location/delete/<location_id>', methods=['DELETE'])
def delete_location(location_id):
    return controllers.delete_location_by_id(location_id)