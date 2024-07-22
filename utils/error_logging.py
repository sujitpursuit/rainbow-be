import datetime
from azure.cosmos import CosmosClient, exceptions
import uuid

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

def conversation_error(conversation_id, account_number, user_name, session_id, conversation_prompt, conversation_intent, error_message):
    try:
        # Create the document
        error_log = {
            'id': str(uuid.uuid4()), # Unique identifier for the document
            'convId': conversation_id,  
            'user': account_number,
            'userName': user_name,
            'sessionId': session_id,
            'convPrompt': conversation_prompt,
            'convIntent': conversation_intent,
            'errorMessage': error_message,
            'errorDateTime': datetime.datetime.now().isoformat()
        }
        
        # Create the item in the container
        container.create_item(body=error_log)
        return "Success"
        
    except exceptions.CosmosResourceExistsError:
        return "Failure: An error log with the same ID already exists."
    except exceptions.CosmosHttpResponseError as e:
        return f"Failure: An error occurred - {e.message}"

# Example usage
# status = conversation_error(
#     convId='error_12345',
#     user='12345',
#     userName='Amitabh Anand',
#     sessionId='session_12345',
#     convPrompt='How do I integrate Cosmos DB with Python?',
#     convIntent='IntegrationQuestion',
#     errorMessage='Timeout error while accessing Cosmos DB.'
# )

# print(status)