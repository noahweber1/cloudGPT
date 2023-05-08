import boto3

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