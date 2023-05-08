# make sure you have boto3, openapi, localstack and awscli installed as python libraries. (besides docker for localstack)

import os
import argparse
import openai
from src.apis.utils.chat_utils import localstack_architecture_to_be_evaluated

openai.api_key = ""

# Set environment variables for localstack
os.environ["AWS_ACCESS_KEY_ID"] = "test"
os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
os.environ["AWS_SESSION_TOKEN"] = "test"

def main(text):
    main_prompt=text
    first_iteration=0
    second_iteration=0

    while first_iteration<11:
        try:
            first_iteration+=1
            code_response_body = localstack_architecture_to_be_evaluated(main_prompt=main_prompt, text_prompt=text, iteration=first_iteration)
            print("Operation completed without errors.")
            break # If no exception is caught, exit the loop

        except Exception as error:
            print("Caught an error:", error)
            text=error

    while first_iteration>11 and second_iteration<11:
        try:
            second_iteration+=1
            code_response_body = localstack_architecture_to_be_evaluated(main_prompt=main_prompt, text_prompt=text, restart_gpt=True, iteration=first_iteration)
            print("Operation completed without errors.")
            break # If no exception is caught, exit the loop

        except Exception as error:
            print("Caught an error:", error)
            text=error

    print(f"Final code: {code_response_body}")

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Describe the AWS architecture that you want deploy on localstack:")
    parser.add_argument("text", type=str, help="Text to pass to the script")
    args = parser.parse_args()
    
    main(args.text)