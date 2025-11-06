from flask import Blueprint, request

import controllers

realm = Blueprint('realm', __name__)
@realm.route('/realms', methods=['POST'])
def create_realm():
    return controllers.create_realm()
@realm.route('/realms/<realm_id>', methods=['GET'])
def get_realm(realm_id):
    return controllers.get_realm_by_id(realm_id)
@realm.route('/realms/<realm_id>', methods=['PUT'])
def update_realm(realm_id):
    return controllers.update_realm_by_id(realm_id)
@realm.route('/realms/delete/<realm_id>', methods=['DELETE'])
def delete_realm(realm_id):
    return controllers.delete_realm_by_id(realm_id)