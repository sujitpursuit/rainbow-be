import requests
from openpyxl import Workbook
import re
import time

def get_api_response(question, account_number):
    url = f"http://127.0.0.1:8090/api/v1/llm/enhance-results/{account_number}"
    headers = {'Content-Type': 'application/json'}
    payload = {'user_query': question}
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Status code returned: {response.status_code}")
    except requests.exceptions.RequestException as err:
        print(f"Error occurred: {err}")
        return {'error': str(err)}
    
    return None

def count_where_clauses(sql_query):
    if sql_query:
        extracted_sql = ' '.join(sql_query.split()).lower()
        return extracted_sql.count(' where ')
    return 0

def count_or_clauses(sql_query):
    if sql_query:
        extracted_sql = ' '.join(sql_query.split()).lower()
        return extracted_sql.count(' or ')
    return 0

def extract_table_names(sql_query):
    tables = set()
    if sql_query:
        extracted_sql = sql_query.lower()
        
        from_pattern = r'\bfrom\s+(\w+\.\w+)\s+'
        from_matches = re.findall(from_pattern, extracted_sql)
        tables.update(from_matches)
        
        join_pattern = r'\bjoin\s+(\w+\.\w+)\s+on\b'
        join_matches = re.findall(join_pattern, extracted_sql)
        tables.update(join_matches)
    
    return list(tables)

def extract_table_names_with_aliases(sql_query):
    tables_with_aliases = []
    if sql_query:
        extracted_sql = sql_query.lower()
        
        from_pattern = r'\bfrom\s+(\w+\.\w+)(?:\s+as\s+(\w+))?\b'
        from_matches = re.findall(from_pattern, extracted_sql)
        tables_with_aliases.extend(from_matches)
        
        join_pattern = r'\bjoin\s+(\w+\.\w+)(?:\s+as\s+(\w+))?\s+on\b'
        join_matches = re.findall(join_pattern, extracted_sql)
        tables_with_aliases.extend(join_matches)
    
    return tables_with_aliases

def format_table_aliases(table_aliases):
    return '; '.join([f"({table}, {alias})" for table, alias in table_aliases])

def extract_join_conditions(sql_query):
    join_conditions = []
    if sql_query:
        extracted_sql = sql_query.lower()
        
        join_pattern = r'\bjoin\s+(\w+\.\w+)\s*(?:as\s+\w+\s+)?on\s+([^ ]+\s*=\s*[^ ]+)'
        join_matches = re.findall(join_pattern, extracted_sql)
        
        for match in join_matches:
            join_conditions.append(match)
    
    return join_conditions

def format_join_condition(join_conditions):
    formatted_conditions = [condition[1] for condition in join_conditions]
    return '; '.join(formatted_conditions) if formatted_conditions else 'No join conditions found.'

def write_join_status(sql_query):
    join_conditions = extract_join_conditions(sql_query)
    return "Available" if join_conditions else "Not Available"

def validate_where_clause(sql_query, account_number):
    if sql_query:
        extracted_sql = ' '.join(sql_query.split()).lower()
        account_number_conditions = [
            f"accountnumber = '{account_number.lower()}'",
            f"accountnumber = {account_number.lower()}"
        ]
        for condition in account_number_conditions:
            if condition in extracted_sql:
                return True, f"WHERE Clause: AccountNumber found and verified {account_number}."
    return False, "AccountNumber not found."

def validate_or_clause(sql_query):
    if sql_query:
        extracted_sql = ' '.join(sql_query.split()).lower()
        where_position = extracted_sql.find(' where ')
        or_position = extracted_sql.find(' or ', where_position)
        
        if or_position > where_position:
            return False, "OR conditions are present after the WHERE clause."
    return True, "No OR Clause found after the WHERE clause."

def validate_join_conditions(sql_query):
    join_conditions = extract_join_conditions(sql_query)
    
    if join_conditions:
        return True, join_conditions
    
    return False, []

def validate_sql_query(sql_query, account_number):
    validation_messages = []
    
    where_valid, where_message = validate_where_clause(sql_query, account_number)
    validation_messages.append(where_message)
    
    or_valid, or_message = validate_or_clause(sql_query)
    validation_messages.append(or_message)
    
    join_valid, join_conditions = validate_join_conditions(sql_query)
    if join_valid:
        validation_messages.append("Join conditions found.")
    else:
        validation_messages.append("No join conditions found.")
    
    overall_valid = where_valid and or_valid and join_valid
    return overall_valid, validation_messages, join_conditions

# Read from generated prompts file
with open('automated_prompts.txt', 'r') as file:
    lines = file.readlines()

questions = [re.sub(r'^\d+\.\s*', '', line.strip()) for line in lines if line.strip()]

# Store responses
results = []
account_number = 'Z011330744'

# Processing each question in a loop
for question in questions:
    response = get_api_response(question, account_number)
    
    print(f"Raw API Response: {response}")

    sql_query = 'N/A'

    if isinstance(response, dict) and 'response' in response:
        api_response = response['response']
        
        if isinstance(api_response, dict):
            sql_query = api_response.get('sql_query', 'N/A')
            data = api_response.get('data', 'Not Available')
            join_info = ''
            formatted_table_aliases = ''
            
            print(f"SQL Query: {sql_query}")
            print(f"Data: {data}")
            print(f"Type of data: {type(data)}")
            
            data_str = ', '.join([str(item) for item in data]) if isinstance(data, list) else str(data)
            
            try:
                overall_valid, validation_messages, join_conditions = validate_sql_query(sql_query, account_number)
                
                join_info = format_join_condition(join_conditions)
                tables_with_aliases = extract_table_names_with_aliases(sql_query)
                formatted_table_aliases = format_table_aliases(tables_with_aliases)
                
                results.append({
                    "question": question,
                    "sql_query": sql_query,
                    "data": data_str,
                    "summary": response.get('summary', 'No Summary'),
                    "status_code": api_response.get('status', 'N/A'),
                    "where_count": count_where_clauses(sql_query),
                    "or_clause": "Present" if count_or_clauses(sql_query) > 0 else "Not Present",
                    "join_status": write_join_status(sql_query),
                    "join_clause": join_info,
                    "table_aliases": formatted_table_aliases,
                    "validation_messages": ' | '.join(validation_messages)
                })
            except Exception as e:
                results.append({
                    "question": question,
                    "sql_query": sql_query,
                    "data": "Could not generate Data",
                    "summary": str(e),
                    "status_code": "Failed",
                    "where_count": count_where_clauses(sql_query),
                    "or_clause": "Not Present",
                    "join_status": "N/A",
                    "join_clause": "N/A",
                    "table_aliases": "N/A",
                    "validation_messages": str(e)
                })
        else:
            results.append({
                "question": question,
                "sql_query": 'N/A',
                "data": "Could not generate Data",
                "summary": "Unexpected response format",
                "status_code": "Failed",
                "where_count": "N/A",
                "or_clause": "Not Present",
                "join_status": "N/A",
                "join_clause": "N/A",
                "table_aliases": "N/A",
                "validation_messages": "Unexpected response format"
            })
    else:
        results.append({
            "question": question,
            "sql_query": 'N/A',
            "data": "Could not generate Data",
            "summary": response.get('error', 'No response'),
            "status_code": response.get('response', {}).get('status', 'Failed'),
            "where_count": "N/A",
            "or_clause": "Not Present",
            "join_status": "N/A",
            "join_clause": "N/A",
            "table_aliases": "N/A",
            "validation_messages": response.get('error', 'No response')
        })
    time.sleep(10)

response_workbook = Workbook()
sheet = response_workbook.active
sheet.title = "Responses"

headers = ["Question", "SQL Query", "Data", "Summary", "Status Code", "Where Count", "OR Clause", "Join Status", "Join Clause", "Table Aliases", "Validation Messages"]
sheet.append(headers)

for result in results:
    row = [
        result["question"],
        result["sql_query"],
        str(result["data"]),
        result["summary"],
        result["status_code"],
        result["where_count"],
        result["or_clause"],
        result["join_status"],
        result["join_clause"],
        result["table_aliases"],
        result["validation_messages"]
    ]
    sheet.append(row)

response_workbook.save("API_Responses.xlsx")
print("Results saved in API_Responses.xlsx")
