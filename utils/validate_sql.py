import re
from service.db_execute import validate_sql_syntax

# To count the number of WHERE clauses
def count_where_clauses(sql_query):
    extracted_sql = ' '.join(sql_query.split()).lower()
    where_count = extracted_sql.count(' where ')
    return where_count

# To count the number of OR clauses
def count_or_clauses(sql_query):
    extracted_sql = ' '.join(sql_query.split()).lower()
    or_count = extracted_sql.count(' or ')
    return or_count

# To extract table names from JOINs
def extract_table_names(sql_query):
    tables = set()
    extracted_sql = sql_query.lower()

    from_pattern = r'\bfrom\s+(\w+\.\w+)\s+'
    from_matches = re.findall(from_pattern, extracted_sql)
    tables.update(from_matches)

    join_pattern = r'\bjoin\s+(\w+\.\w+)\s+on\b'
    join_matches = re.findall(join_pattern, extracted_sql)
    tables.update(join_matches)

    return list(tables)

# To extract table names along with aliases
def extract_table_names_with_aliases(sql_query):
    tables_with_aliases = []
    extracted_sql = sql_query.lower()

    from_pattern = r'\bfrom\s+(\w+\.\w+)(?:\s+as\s+(\w+))?\b'
    from_matches = re.findall(from_pattern, extracted_sql)
    tables_with_aliases.extend(from_matches)

    join_pattern = r'\bjoin\s+(\w+\.\w+)(?:\s+as\s+(\w+))?\s+on\b'
    join_matches = re.findall(join_pattern, extracted_sql)
    tables_with_aliases.extend(join_matches)

    return tables_with_aliases

# To format the table names with aliases
def format_table_aliases(table_aliases):
    return '; '.join([f"({table}, {alias})" for table, alias in table_aliases if alias]) if table_aliases else 'No table aliases found.'

# To extract join conditions on which the JOIN is happening
def extract_join_conditions(sql_query):
    join_conditions = []
    extracted_sql = sql_query.lower()

    join_pattern = r'\bjoin\s+(\w+\.\w+)\s*(?:as\s+\w+\s+)?on\s+([^ ]+\s*=\s*[^ ]+)'
    join_matches = re.findall(join_pattern, extracted_sql)
    
    for match in join_matches:
        join_conditions.append(match)
    
    return join_conditions

# To format join conditions on which the JOIN is happening
def format_join_condition(join_conditions):
    formatted_conditions = []
    for condition in join_conditions:
        formatted_conditions.append(condition[1])
    return '; '.join(formatted_conditions) if formatted_conditions else 'No join conditions found.'

# To provide JOIN_Status
def write_join_status(sql_query):
    join_conditions = extract_join_conditions(sql_query)
    if join_conditions:
        return "Available"
    else:
        return "Not Available"

# To validate WHERE clause based on AccountNumber
def validate_where_clause(sql_query, account_number):
    extracted_sql = ' '.join(sql_query.split()).lower()
    account_number_conditions = [
        f"accountnumber = '{account_number.lower()}'",
        f"accountnumber = {account_number.lower()}"
    ]
    for condition in account_number_conditions:
        if condition in extracted_sql:
            return True, f"WHERE Clause: AccountNumber found and verified {account_number}."
    return False, "AccountNumber not found."

# To validate OR clause through generated SQL after WHERE clause
def validate_or_clause(sql_query):
    extracted_sql = ' '.join(sql_query.split()).lower()
    where_position = extracted_sql.find(' where ')
    or_position = extracted_sql.find(' or ', where_position)

    if or_position > where_position:
        return False, "OR conditions are present after the WHERE clause."
    return True, "OR Clause: No OR Clause found after the WHERE clause."

# To validate JOIN conditions
def validate_join_conditions(sql_query):
    join_conditions = extract_join_conditions(sql_query)
    return join_conditions if join_conditions else []

# To validate SQL syntax
def validate_sql_syntax(sql_query):
    # Mock function to simulate SQL syntax validation
    # Replace with actual implementation or library call
    if "SELECT" in sql_query.upper():
        return True, "SQL syntax is correct."
    else:
        return False, "SQL syntax is incorrect."

# To validate the entire SQL query generated based on the above validations for syntax, WHERE, OR, JOIN
def validate_sql_query(sql_query, account_number):
    validation_messages = []

    # Validate SQL syntax
    syntax_valid, syntax_message = validate_sql_syntax(sql_query)
    validation_messages.append(syntax_message)

    if not syntax_valid:
        return False, validation_messages, []

    # Validate WHERE clause
    where_valid, where_message = validate_where_clause(sql_query, account_number)
    validation_messages.append(where_message)

    # Validate OR clause
    or_valid, or_message = validate_or_clause(sql_query)
    validation_messages.append(or_message)

    # Validate JOIN conditions
    join_conditions = validate_join_conditions(sql_query)
    if join_conditions:
        validation_messages.append("Join Conditions: Available.")
        join_condition_str = format_join_condition(join_conditions)
        validation_messages.append(f"Join Conditions Detail: {join_condition_str}")
    else:
        validation_messages.append("Join Conditions: Not Available.")

    overall_valid = syntax_valid and where_valid and or_valid
    return overall_valid, validation_messages, join_conditions
