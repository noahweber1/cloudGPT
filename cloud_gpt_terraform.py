import os
import argparse
import openai
from src.utils.chat_utils import aws_architecture_to_be_evaluated
from src.utils.general_utils import collect_cloudwatch_logs

openai.api_key = ""

os.environ['AWS_DEFAULT_REGION'] = ''
os.environ['AWS_ACCESS_KEY_ID'] = ''
os.environ['AWS_SECRET_ACCESS_KEY'] = ''

def main(text):
    main_prompt=text
    first_iteration=0
    second_iteration=0

    while first_iteration<11:
        try:
            first_iteration+=1
            cloud_watch_logs = collect_cloudwatch_logs()
            code_response_body = aws_architecture_to_be_evaluated(main_prompt=main_prompt, text_prompt=text, cloud_watch_logs=cloud_watch_logs, iteration=first_iteration)
            print("Operation completed without errors.")
            break # If no exception is caught, exit the loop

        except Exception as error:
            print("Caught an error:", error)
            text=error

    while first_iteration>11 and second_iteration<11:
        try:
            second_iteration+=1
            cloud_watch_logs = collect_cloudwatch_logs()
            code_response_body = aws_architecture_to_be_evaluated(main_prompt=main_prompt, text_prompt=text, cloud_watch_logs=cloud_watch_logs, restart_gpt=True, iteration=first_iteration)
            print("Operation completed without errors.")
            break # If no exception is caught, exit the loop

        except Exception as error:
            print("Caught an error:", error)
            text=error

    print(f"Final code: {code_response_body}")

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Describe the AWS architecture that you want deploy on AWS:")
    parser.add_argument("text", type=str, help="Text to pass to the script")
    args = parser.parse_args()
    
    main(args.text)
