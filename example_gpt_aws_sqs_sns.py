import os
import boto3
from botocore.exceptions import ClientError

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_DEFAULT_REGION = os.environ['AWS_DEFAULT_REGION']

def create_sqs_queue(queue_name):
    sqs_client = boto3.client('sqs', aws_access_key_id=AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                              region_name=AWS_DEFAULT_REGION)
    try:
        response = sqs_client.create_queue(QueueName=queue_name)
        return response['QueueUrl']
    except ClientError as e:
        print(e)
        return None

def create_sns_topic(topic_name):
    sns_client = boto3.client('sns', aws_access_key_id=AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                              region_name=AWS_DEFAULT_REGION)
    try:
        response = sns_client.create_topic(Name=topic_name)
        return response['TopicArn']
    except ClientError as e:
        print(e)
        return None

def subscribe_sqs_queue_to_sns_topic(queue_url, topic_arn):
    sqs_client = boto3.client('sqs', aws_access_key_id=AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                              region_name=AWS_DEFAULT_REGION)
    try:
        queue_arn = sqs_client.get_queue_attributes(QueueUrl=queue_url, AttributeNames=['QueueArn'])['Attributes']['QueueArn']
        sns_client = boto3.client('sns', aws_access_key_id=AWS_ACCESS_KEY_ID,
                                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                                  region_name=AWS_DEFAULT_REGION)
        response = sns_client.subscribe(TopicArn=topic_arn, Protocol='sqs', Endpoint=queue_arn)
        return response['SubscriptionArn']
    except ClientError as e:
        print(e)
        return None

def integration_test(queue_name, topic_name):
    queue_url = create_sqs_queue(queue_name)
    print(f"SQS Queue created: {queue_url}")

    topic_arn = create_sns_topic(topic_name)
    print(f"SNS Topic created: {topic_arn}")

    subscription_arn = subscribe_sqs_queue_to_sns_topic(queue_url, topic_arn)
    print(f"SQS Queue subscribed to SNS Topic: {subscription_arn}")

if __name__ == '__main__':
    integration_test(queue_name='test_queue', topic_name='test_topic')