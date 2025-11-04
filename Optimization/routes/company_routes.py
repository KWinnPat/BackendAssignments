from flask import Blueprint, request

import controllers

company = Blueprint('company', __name__)

# CREATE
@company.route('/company', methods=['POST'])
def create_company():
    return controllers.create_company()

# READ
@company.route('/companies', methods=['GET'])
def get_companies():
    return controllers.get_all_companies()

@company.route('/company/<company_id>', methods=['GET'])
def get_company(company_id):
    return controllers.get_company_by_id(company_id)

# UPDATE
@company.route('/company/<company_id>', methods=['PUT'])
def update_company(company_id):
    return controllers.update_company_by_id(company_id)

# DELETE
@company.route('/company/delete/<company_id>', methods=['DELETE'])
def delete_company(company_id):
    return controllers.delete_company_by_id(company_id)