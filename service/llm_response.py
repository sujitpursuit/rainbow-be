from utils.conversation_logging import write_conversation_log
from utils.error_logging import conversation_error
from utils.rainbow_prompt import sql_prompt
import google.generativeai as genai
import json as js
from datetime import datetime
from service.db_execute import execute_query_json
import os
from dotenv import find_dotenv, load_dotenv

from utils.validate_sql import validate_sql_query

load_dotenv(find_dotenv())
api_key = os.getenv('GEMINI_API_KEY')

# safety measures for gemini LLM
safety_settings = [
    {
        "category": "HARM_CATEGORY_DANGEROUS",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]

# generating the SQL from LLM according to user asked question
def nl_sql_gemini(user_prompt: str):
    genai.configure(api_key=api_key)
    models  = genai.GenerativeModel('gemini-pro')
    prompt =  f"{sql_prompt} \n\n {user_prompt}"
    #print(f"Prompt sent to llm: {prompt}")
    response = models.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(temperature=0),
        safety_settings=safety_settings
    )
    return response.text

# eliminate the triple quotes of generated SQL
def parse_triple_quotes(in_str):
  start = in_str.find("```sql") + len("```sql\n")  
  end = in_str.rfind("```") 
  out_str = in_str[start:end].strip()
  return out_str

# generating the summary of results of generated SQL by LLM
def explain_result_gemini(sql_prompt, sql_result):
    user_prompt = f"""Summarize the results from the SQL query in less than or up to four sentences. 
    The result is an output from the following query: {sql_prompt}.
    Result: {sql_result}. 
    In the response, do not mention database-related words like SQL, rows, timestamps, etc."""

    models = genai.GenerativeModel('gemini-pro')
    response = models.generate_content(user_prompt, safety_settings=safety_settings)
    explanation = response.text
    return explanation

# generating the response by LLM according to the user_prompt and account 
def generate_response_gemini(user_prompt, account_number):
   requested_prompt = f"{user_prompt} where account number is {account_number}"
   generated_sql_by_llm = nl_sql_gemini(requested_prompt)
   runable_sql = parse_triple_quotes(generated_sql_by_llm)
   sql_result = execute_query_json(runable_sql)
   summary = explain_result_gemini(sql_prompt=user_prompt, sql_result=sql_result)
   return {'data': sql_result, 'summary': summary}

# generating the enhance response by LLM according to the user_prompt and account 
# def generate_action_response_gemini(user_prompt, account_number):
#     try: 
#         print(f"in the try block {user_prompt} and account number {account_number}")
#         requested_prompt = f"{user_prompt}. The account number should be {account_number}"
#         generated_sql_by_llm = nl_sql_gemini(requested_prompt)
#         runable_sql = parse_triple_quotes(generated_sql_by_llm)
#         # print(runable_sql)
#         # validation function for sql call here 
#         is_valid_sql = validate_sql_query(account_number=account_number, sql_query=runable_sql)
#         # is_valid_sql = True
#         # print(f"debugger_2 --> {is_valid_sql}")
        
#         if(is_valid_sql):
#             sql_result = execute_query_json(runable_sql)
#             print(f"sql_result -> {sql_result}")
#             print(f"type of sql_result -> {type(sql_result['data'])}")
#             enhance_result = enhance_policy_data(sql_result=sql_result, account_number=account_number)
#             summary = explain_result_gemini(sql_prompt=user_prompt, sql_result=sql_result)
#             return_object = {'response': enhance_result, 'summary':summary}
#             is_logged_saved = write_conversation_log(
#                 account_number=account_number,
#                 user_name='rakesh ranjan',
#                 session_id='sess_101',
#                 conversation_date_time=datetime.now(),
#                 conversation_prompt=user_prompt,
#                 conversation_intent='POLICY',
#                 conversation_response=return_object,
#                 conversation_status=sql_result['status'],
#                 generated_sql=sql_result['sql_query'],
#                 generated_sql_results=sql_result['data'],
#                 other_info='No additional Information'
#             )
#             # print(f"logged saved in cosmos db --> {is_logged_saved}")
#             return return_object
#         else:
#             return {'response': "Incorrect SQL", 'status': 'FAILED'}
#     except Exception as e:
#         print(f"Exception in generate_action_response_gemini --> {e}")
#         is_error_saved = conversation_error(
#             conversation_id='CVN_101',
#             account_number=account_number,
#             user_name='rakesh ranjan',
#             session_id='sess_101',
#             conversation_prompt=user_prompt,
#             conversation_intent='Policy',
#             conversation_response=e,
#         )
#         # print(f" is error saved --> {is_error_saved}")
def generate_action_response_gemini(user_prompt, account_number):
    start_time = datetime.now()
    try: 
        print(f"in the try block {user_prompt} and account number {account_number}")
        requested_prompt = f"{user_prompt}. The account number should be {account_number}"
        llm_start_time = datetime.now()
        generated_sql_by_llm = nl_sql_gemini(requested_prompt)
        llm_end_time = datetime.now()
        runable_sql = parse_triple_quotes(generated_sql_by_llm)

        # validation function for sql call here 
        is_valid_sql, validation_messages, join_conditions = validate_sql_query(sql_query=runable_sql, account_number=account_number)
        
        if is_valid_sql:
            sql_exec_start_time = datetime.now()
            sql_result = execute_query_json(runable_sql)
            sql_exec_end_time = datetime.now()
            
            print(f"sql_result -> {sql_result}")
            print(f"type of sql_result -> {type(sql_result['data'])}")
            enhance_start_time = datetime.now()
            enhance_result = enhance_policy_data(sql_result=sql_result, account_number=account_number)
            enhance_end_time = datetime.now()
            
            explain_start_time = datetime.now()
            summary = explain_result_gemini(sql_prompt=user_prompt, sql_result=sql_result)
            explain_end_time = datetime.now()
    
            return_object = {'response': enhance_result, 'summary': summary}
            end_time = datetime.now()
            
            is_logged_saved = write_conversation_log(
                account_number=account_number,
                user_name='rakesh ranjan',
                session_id='sess_101',
                conversation_date_time=datetime.now(),
                conversation_prompt=user_prompt,
                conversation_intent='POLICY',
                conversation_response=return_object,
                conversation_status=sql_result['status'],
                generated_sql=sql_result['sql_query'],
                generated_sql_results=sql_result['data'],
                other_info='No additional Information'
            )
            
            total_time_taken = end_time - start_time
            llm_time_taken = llm_end_time - llm_start_time
            sql_exec_time_taken = sql_exec_end_time - sql_exec_start_time
            enhance_time_taken = enhance_end_time - enhance_start_time
            explain_time_taken = explain_end_time - explain_start_time
            
            formatted_time = str(total_time_taken).split('.')[0]
            llm_time = str(llm_time_taken).split('.')[0]
            sql_exec_time = str(sql_exec_time_taken).split('.')[0]
            enhance_time = str(enhance_time_taken).split('.')[0]
            explain_time = str(explain_time_taken).split('.')[0]
            
            print(f"Total time taken: {formatted_time}")
            print(f"LLM time taken: {llm_time}")
            print(f"SQL execution time taken: {sql_exec_time}")
            print(f"EnhanceResult time taken: {enhance_time}")
            print(f"Explanation time taken: {explain_time}")
            return return_object
        else:
            return {'response': "Incorrect SQL", 'status': 'FAILED'}
            
    except Exception as e:
        print(f"Exception in generate_action_response_gemini --> {e}")
        is_error_saved = conversation_error(
            conversation_id='CVN_101',
            account_number=account_number,
            user_name='rakesh ranjan',
            session_id='sess_101',
            conversation_prompt=user_prompt,
            conversation_intent='Policy',
            error_message=str(e),
        )
        return {'response': 'Internal Server Error', 'status': 'FAILED'}





def enhance_policy_data(sql_result, account_number):
    sql_query = sql_result['sql_query']
    if 'SELECT' in sql_query and 'PolicyDetails' in sql_query:
        for policy in sql_result['data']:
            if policy.get('PolicyNumber') and policy.get('PremiumDue') is not None:
                policy_number = policy['PolicyNumber']
                premium_due = policy['PremiumDue']
                print(premium_due)
                policy['actions'] = create_dynamic_actions(policy_number=policy_number,premium_due=premium_due, account_number=account_number )
            else:
                return sql_result
    return sql_result

def create_dynamic_actions(policy_number, premium_due, account_number):
    actions = [
        {
			'label':'Pay',
			'url': f'https://zohosecurepay.com/checkout/45sm9zp-3rmtgxcc9el2bm/Invoice-Payment?amount={premium_due}',
		},
		{  
			'label':'Show more Details' ,
			'url': f'/api/v1/sql/policy-details/{policy_number}'
		},
		{ 
			'label':'Show Coverage',
			'url': f'/api/v1/sql/coverage-details/{policy_number}/{account_number}'
		}
    ]
    return actions
