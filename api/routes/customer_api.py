from datetime import datetime
from http import HTTPStatus
from flask import Blueprint, request
from flasgger import swag_from
from service.db_execute import execute_query_json
from utils.conversation_logging import write_conversation_log
from utils.error_logging import conversation_error

customer_api = Blueprint('customer_api', __name__)

@customer_api.get('/welcome')
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
    return 'Welcome api form customer_api', 200

# get customer details through account number
@customer_api.route('/customer/<account_number>', methods=['GET'])
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Customer details',
            'schema': {
                "account_number": "account_number",
            },
        }
    }
})
def get_customer_details(account_number):
    try:
        if request.method == 'GET':
            query = f"SELECT TOP(1) p.Name, p.EmailID, p.PhoneNumber from [PolicyD].[PrimaryInsured] as p JOIN [PolicyD].[PolicyDetails] AS pd ON pd.PolicyNumber = p.PolicyNumber where pd.AccountNumber='Z011330744';"
            customer_details = execute_query_json(sql_query=query)
            print(f"customer details 1--> {customer_details}")
            print(f"customer name -> {customer_details['data'][0]['Name']}")
            write_conversation_log(
                account_number=account_number,
                user_name=customer_details['data'][0]['Name'],
                session_id='sess_101',
                conversation_date_time=datetime.now(),
                conversation_prompt=f"fetching details of account number : {account_number}",
                conversation_intent="Customer details",
                conversation_response=customer_details,
                conversation_status=customer_details['status'],
                generated_sql=query,
                generated_sql_results=customer_details['data'],
                other_info="not required"
            )
            return customer_details, 200
        else:
            return {"message": "Method Not Allowed"}, HTTPStatus.METHOD_NOT_ALLOWED
    except Exception as e:
        print(f"Exception in get_customer_details --> {e}")
