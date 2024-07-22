from http import HTTPStatus
from flask import Blueprint, request
from flasgger import swag_from

policy_api = Blueprint('policy_api', __name__)

@policy_api.get('/policy')
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Welcome to the Flask Starter Kit',
            'schema': {
                "data": 'this is sample data',
                "summary": "this is summary"
            }
        }
    }
})
def welcome():
    """
    1 liner about the route
    A more detailed description of the endpoint
    ---
    """
    return 'Welcome to the Flask Starter Kit', 200