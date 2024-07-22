import datetime
import uuid
from azure.cosmos import CosmosClient, exceptions
from dotenv import find_dotenv, load_dotenv
import os

# getting data from .env file
load_dotenv(find_dotenv())

# Connecting variable to the Cosmos DB
url = os.getenv('COSMOS_DB_URL')
key = os.getenv('COSMOS_DB_KEY')
# print(f"url -> {url} && key --> {key}")         #for debugging only

# Initialize the Cosmos client
client = CosmosClient(url, key)

# Define the database and container
database_name = os.getenv('COSMOS_DB_NAME')
container_name = os.getenv('COSMOS_DB_CONTAINER_NAME')

database = client.get_database_client(database_name)
container = database.get_container_client(container_name)

def write_conversation_log(account_number, user_name, session_id, conversation_date_time, conversation_prompt, conversation_intent,
                           conversation_response, conversation_status, generated_sql, generated_sql_results, other_info):
    try:
        # Create the document
        conversation_log = {
            'id': str(uuid.uuid4()), #f"{sessionId}-{user}",  # Unique identifier for the document
            'user': account_number,
            'userName': user_name,
            'sessionId': session_id,
            'convDateTime': conversation_date_time.isoformat(),
            'convPrompt': conversation_prompt,
            'convIntent': conversation_intent,
            'convResponse': conversation_response,
            'convStatus': conversation_status,
            'generatedSQL': generated_sql,
            'generatedSQLResults': generated_sql_results,
            'otherInfo': other_info
        }
        
        # Create the item in the container
        container.create_item(body=conversation_log)
        return "Success"
        
    except exceptions.CosmosResourceExistsError:
        return "Failure: A conversation log with the same ID already exists."
    except exceptions.CosmosHttpResponseError as e:
        return f"Failure: An error occurred - {e.message}"
    
# Example usage
# status = write_conversation_log(
#     account_number='12345',
#     userName='Amitabh Anand',
#     sessionId='session_12345',
#     convDateTime=datetime.datetime.now(),
#     convPrompt='How do I integrate Cosmos DB with Python?',
#     convIntent='IntegrationQuestion',
#     convResponse='You can use the azure-cosmos package...',
#     convStatus='Success',
#     generatedSQL=None,
#     generatedSQLResults=None,
#     otherInfo='No additional information'
# )
# print(status)