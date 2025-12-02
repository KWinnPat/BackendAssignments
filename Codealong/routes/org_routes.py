from flask import Blueprint

import controllers

orgs = Blueprint('orgs', __name__)

@orgs.route('/org', methods=['POST'])
def add_org_route():
    return controllers.add_org()

@orgs.route('/orgs', methods=['GET'])
def get_all_orgs_route():
    return controllers.get_all_orgs()

