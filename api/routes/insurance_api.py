from http import HTTPStatus
from flask import Blueprint, request, jsonify
from flasgger import swag_from

from service.llm_response import generate_action_response_gemini

insurance_api = Blueprint('insurance_api', __name__)


@insurance_api.get('/welcome')
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

@insurance_api.route('/enhance-results/<account_number>', methods=['POST'])
def generate_actions_response(account_number):
    try:
        if request.method == 'POST':
            data = request.get_json()
            user_query = data['user_query']
            print(f"debugger_1 --> {user_query}")
            return generate_action_response_gemini(user_prompt=user_query, account_number=account_number), HTTPStatus.OK
        else:
            return {'message': 'HTTPStatus.METHOD_NOT_ALLOWED'}, HTTPStatus.METHOD_NOT_ALLOWED
    except Exception as e:
        return {'message': 'HTTPStatus.INTERNAL_SERVER_ERROR'}, HTTPStatus.INTERNAL_SERVER_ERROR
        

