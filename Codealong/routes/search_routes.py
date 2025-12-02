from flask import Blueprint

import controllers

search = Blueprint('search', __name__)

@search.route('/users/search', methods=['GET'])
def get_users_by_search_route():
    return controllers.get_users_by_search()