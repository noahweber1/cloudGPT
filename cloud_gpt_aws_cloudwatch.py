import boto3
import os
import argparse
import openai
openai.api_key = ""

os.environ['AWS_DEFAULT_REGION'] = ''
os.environ['AWS_ACCESS_KEY_ID'] = ''
os.environ['AWS_SECRET_ACCESS_KEY'] = ''

def collect_cloudwatch_logs() -> str:
    # Create a CloudWatch Logs client
    client = boto3.client('logs')
    all_cloudwatchs_logs = ""
    
    # List log groups
    response = client.describe_log_groups()

    for log_group in response['logGroups']:
        log_group_name = log_group['logGroupName']
        print(f'Log group: {log_group_name}')

        # List log streams in the log group
        log_streams_response = client.describe_log_streams(logGroupName=log_group_name)
        for log_stream in log_streams_response['logStreams']:
            log_stream_name = log_stream['logStreamName']
            print(f'  Log stream: {log_stream_name}')

            # Get log events from the log stream
            log_events_response = client.get_log_events(logGroupName=log_group_name, logStreamName=log_stream_name)
            for log_event in log_events_response['events']:
                timestamp = log_event['timestamp']
                message = log_event['message']

                all_cloudwatchs_logs += f'Log event (timestamp: {timestamp}): {message}\n'
    
    return all_cloudwatchs_logs

def aws_architecture_to_be_evaluated(text_prompt="write me a sqs and sns solution and test it on localstack", cloud_watch_logs="", restart_gpt=False):

    meta_prompt = '''You are an autonomous agent called "assistant for AWS
    solution architecture" which act as an python function generator.
    These functions should encapsulate all of the boto3 code needed to
    deploy on the AWS in one singular python function.
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
    8. You have to specify
    ''' + 'Additionally use the following cloud watch log messages to correct your response' + cloud_watch_logs
    # CALL GPT, GPT-3.5 does not work as well currently.
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
        {"role": "system", "content": meta_prompt},
        {"role": "user", "content": text_prompt},
        ]
    )
    code_response_body=response["choices"][0]["message"]["content"]

    #TODO unsafe, find better way to execute the returned strings
    exec(code_response_body)

    return code_response_body

def main(text):

    first_iteration=0
    second_iteration=0

    while True and first_iteration<11:
        try:
            cloud_watch_logs = collect_cloudwatch_logs()
            aws_architecture_to_be_evaluated(text_prompt=text, cloud_watch_logs=cloud_watch_logs)
            print("Operation completed without errors.")
            break # If no exception is caught, exit the loop

        except ValueError as error:
            print("Caught an error:", error)
            text=error

    while True and second_iteration<10:
        try:
            cloud_watch_logs = collect_cloudwatch_logs()
            aws_architecture_to_be_evaluated(text_prompt=text, cloud_watch_logs=cloud_watch_logs, restart_gpt=True)
            print("Operation completed without errors.")
            break # If no exception is caught, exit the loop

        except ValueError as error:
            print("Caught an error:", error)
            text=error

    code_response_body= aws_architecture_to_be_evaluated(text_prompt=text, cloud_watch_logs=cloud_watch_logs, restart_gpt=False)

    print(f"Final code: {code_response_body}")

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Describe the AWS architecture that you want deploy on AWS:")
    parser.add_argument("text", type=str, help="Text to pass to the script")

    args = parser.parse_args()
    main(args.text)
