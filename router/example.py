from flask import Blueprint, request;

import api.api_example as API;

example_blueprints = Blueprint('example',__name__);

@example_blueprints.route('/test_get', methods=['GET'])
def test_get():
    return API.test_get();

@example_blueprints.route('/test_post', methods=['POST'])
def test_post():
    return API.test_post(request.get_json());