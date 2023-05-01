import boto3
import os
import time

os.environ["AWS_ACCESS_KEY_ID"] = "test"
os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
os.environ["LOCALSTACK_HOSTNAME"] = "localhost"

sqs_client = boto3.client("sqs", endpoint_url="http://localhost:4566")
sns_client = boto3.client("sns", endpoint_url="http://localhost:4566")

sqs_queue = sqs_client.create_queue(QueueName="test_queue")
queue_url = sqs_queue["QueueUrl"]

queue_arn = f"arn:aws:sqs:{os.environ['AWS_DEFAULT_REGION']}:{os.environ['AWS_ACCESS_KEY_ID']}:test_queue"

sns_topic = sns_client.create_topic(Name="test_topic")
topic_arn = sns_topic["TopicArn"]

sns_client.subscribe(
    TopicArn=topic_arn,
    Protocol="sqs",
    Endpoint=queue_arn,
)

message = "Test message for SQS and SNS solution on LocalStack"
sns_client.publish(TopicArn=topic_arn, Message=message)

time.sleep(2)

received_messages = sqs_client.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=1)

if len(received_messages.get("Messages", [])) > 0:
    message_id = received_messages["Messages"][0]["MessageId"]
    print(f"Message successfully received with ID: {message_id}")
else:
    print("No messages received, test failed.")
