import pyodbc
import pandas as pd
from sqlalchemy.engine import URL, create_engine
from dotenv import load_dotenv, find_dotenv
from sqlalchemy import text
import os
import json as js

# getting credential from .env file
load_dotenv(find_dotenv())
server_name=os.getenv('DB_SERVER')
user_name=os.getenv('DB_USERNAME')
pwd=os.getenv('DB_PWD')
db_name=os.getenv('DB_NAME')
# print(f"serverName --> {server_name} \n user_name -> {user_name} \n password -> {pwd} \n db_name -> {db_name}") #for debugging only

# creating connection string
connection_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server_name};DATABASE={db_name};UID={user_name};PWD={pwd}'

# creating connection object
connection_url = URL.create(
    "mssql+pyodbc",
    query={"odbc_connect": connection_str}
)

# creating db engine
db_engine = create_engine(connection_url)

def validate_sql_syntax(sql_query):
    with db_engine.connect() as connection:
        try:
            connection.execute(text(sql_query))
            return True, "SQL syntax generated is correct."
        except Exception as e:
            return False, f"SQL syntax generated has error: {str(e)}"

# function for run sql
def execute_query_json(sql_query):
    with db_engine.begin() as db_eng:
        # print(type(sql_query))
        df = pd.read_sql(sql=sql_query, con=db_eng)
        pd.set_option('display.max_columns', None)
        data = df.to_json(indent=4, date_format='iso', index=False, orient='records')
        print(data)
        status = ''
        if data:
            status = 'SUCCESS'
        else:
            status = 'FAILED'
        response = {'data': js.loads(data), 'sql_query': sql_query.replace("\n", ' '), 'status': status}
    return response