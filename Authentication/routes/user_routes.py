from flask import Blueprint

import controllers
user = Blueprint('user', __name__)

@user.route('/user', methods=['POST'])
def add_user():
    return controllers.add_user()

@user.route('/users', methods=['GET'])
def get_all_users():
    return controllers.get_all_users()

@user.route('/user/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    return controllers.get_user_by_id(user_id)