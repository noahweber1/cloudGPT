# make sure you have boto3, openapi, localstack and awscli installed as python libraries. (besides docker for localstack)

import os
import argparse
import openai
openai.api_key = "INSERT YOUR KEY"

# Set environment variables for localstack
os.environ["AWS_ACCESS_KEY_ID"] = "test"
os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
os.environ["AWS_SESSION_TOKEN"] = "test"

def local_stack_architecture_to_be_submitted(text_prompt="write me a sqs and sns solution and test it on localstack"):

    meta_prompt = '''You are an autonomous agent called "assistant for AWS
    solution architecture" which act as an python function generator.
    These functions should encapsulate all of the boto3 code needed to
    deploy on the localstack in one singular python function.
    To serve the request, you must follow following rules:

    Rules:
    1. As "assistant", you MUST response only in python code. No other
    text besides python code.
    2. You should take into account previous responses and the error
    messages you get in the process.
    3. The responses from "user" are the results of the action you
    performed. Use them to choose your next action.
    4. Write a small test inside of the script that showcases and proves
    solution was deployed.
    5. Do not use zip files as part of the solution.
    6. Try not to over-engineer the solution.
    7. Use boto3 to construct the solution.
    '''
    # CALL GPT
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
        {"role": "system", "content": meta_prompt},
        {"role": "user", "content": text_prompt},
        ]
    )
    #function_create_by_gpt = gpt.call(meta_prompt + text_prompt)
    #function_create_by_gpt()
    code_response_body=response["choices"][0]["message"]["content"]

    #TODO unsafe, find better way to execute the returned strings
    exec(code_response_body)

def main(text):
    while True:
        try:
            local_stack_architecture_to_be_submitted(text_prompt=text)
            print("Operation completed without errors.")
            break # If no exception is caught, exit the loop

        except ValueError as error:
            print("Caught an error:", error)
            text=error
    # Do something with the error message
    # For example, you can log the error or perform some other action

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Describe the AWS architecture that you want deploy on local stack.")
    parser.add_argument("text", type=str, help="Text to pass to the script")

    args = parser.parse_args()
    main(args.text)
