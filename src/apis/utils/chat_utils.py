from typing import Any, Dict
import requests
import openai

VECTOR_DB_TOKEN=""

def query_database(query_prompt: str) -> Dict[str, Any]:
    """
    Query vector database to retrieve chunk with user's input questions.
    """
    url = "http://0.0.0.0:8000/query"
    headers = {
        "Content-Type": "application/json",
        "accept": "application/json",
        "Authorization": f"Bearer {VECTOR_DB_TOKEN}",
    }
    data = {"queries": [{"query": query_prompt, "top_k": 5}]}

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        result = response.json()
        # process the result
        return result
    else:
        raise ValueError(f"Error: {response.status_code} : {response.content}")

def aws_architecture_to_be_evaluated(text_prompt="write me a sqs and sns solution and test it on localstack", cloud_watch_logs="", restart_gpt=False, vector_db=False, iteration=1):

    meta_prompt = '''You are an autonomous agent called "assistant for AWS
    solution architecture" which act as an python function generator.
    These functions should encapsulate all of the boto3 code needed to
    deploy on the AWS. To accomplish the goal, you must follow following rules:

    Rules:
    1. As "assistant", you MUST response only in python code. No other
    text besides python code.
    2. You should take into account previous responses and the error
    messages you get in the process.
    3. The responses from "user" are the error messages of the action you
    performed. Use them to correct the solution.
    4. Write a small integration test inside of the script that showcases and proves
    solution was deployed.
    5. Do not use zip files as part of the solution.
    6. Try not to over-engineer the solution.
    7. Use boto3 to construct the solution.
    8. You can assume that "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY" and "AWS_DEFAULT_REGION" are already defined in the same named environement variables.
    9. The solution should be as short as possible.
    10. If needed you should define the neccessary ARN roles for any services.

    ''' #+ 'Additionally use the following cloud watch log messages to correct your response' + cloud_watch_logs
    
    messages=[]

    if vector_db:   
        chunks_response = query_database(text_prompt)
        chunks = []
        for result in chunks_response["results"]:
            for inner_result in result["results"]:
                chunks.append(inner_result["text"])
        messages.append(
        map(lambda chunk: {
            "role": "user",
            "content": chunk
        }, chunks))

    if iteration == 1:
        messages.append({"role": "system", "content": meta_prompt})
        messages.append({"role": "user", "content": str(text_prompt)})
    else:
        messages.append({"role": "user", "content": "Here is the error message:" +str(text_prompt)+ "This is the task to accomplish initially posed"+"create an s3 bucket and rds database and test that data is transferred between the two"})

    # CALL GPT4
    response = openai.ChatCompletion.create(
        model="gpt-4",
         messages=messages,
        )

    if restart_gpt:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            user="New session"
        )

    code_response_body=response["choices"][0]["message"]["content"].replace("python", "").replace("```","")
 
    #TODO unsafe, find better way to execute the returned strings
    exec(code_response_body, globals())

    return code_response_body
