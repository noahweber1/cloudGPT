<h1 align="center">
cloudGPT: One line to generate all cloud infrastructure ☁️
</h1>

<p align="center">
<img src="misc\cloud.png" alt="Jina NOW logo" width="250px">
</p>
<p align="center">
Use natural language to create a fully functional, tested and deployed cloud infrastructure with a single command!
</p>

<p align="center">
<a href="https://github.com/tiangolo/missing/actions?query=workflow%3ATest+event%3Apush+branch%3Amaster" target="_blank">
    <img src="https://img.shields.io/badge/platform-mac%20%7C%20linux%20%7C%20windows-blue" alt="Supported platforms">
</a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/tiangolo/fastapi" target="_blank">
    <img src="https://coverage-badge.samuelcolvin.workers.dev/tiangolo/fastapi.svg" alt="Coverage">
</a>
<a href="https://pypi.org/project/missing" target="_blank">
    <img src="https://img.shields.io/pypi/v/missing?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/missing" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/missing.svg?color=%2334D058" alt="Supported Python versions">
</a>
<a href="https://github.com/tiangolo/fastapi/actions?query=workflow%3ATest+event%3Apush+branch%3Amaster" target="_blank">
    <img src="https://github.com/tiangolo/fastapi/workflows/Test/badge.svg?event=push&branch=master" alt="Test">
</a>

<p align="center">
This project streamlines the creation and deployment of cloud infrastructure. 
Simply describe your problem using natural language, and the system will automatically build, test and deploy a cloud architecture based on your prompt.     
</p>

<p align="center">
Error messages are forwarded back to GPT4 recursively and the system self-corrects itself until it passes all tests and gets deployed.
</p>
    
Current capabilities:
   1. [✅] Test the proposed AWS architecture and deploy on a dev environement automatically. 🚀
   2. [✅] Test and deploy any cloud architecture with [Terraform](https://www.terraform.io/). ⚙️
   3. [✅] External memory with vector database - Pinecone (Optional configuration possibility). 🌲
   4. [✅] Deploy AWS architecture on [Localstack](https://localstack.cloud/) and test it there. 🏠

> ⚠️ Warning ⚠️ This project is in ALPHA developement and should NOT be used for direct deployments on the cloud. There are alot of security and monetary considerations.

## 📚 Table of Contents

1. [📋 Requirements](#requirements)
2. [🌐 Examples AWS](#examples-aws)
3. [⚙️ Examples Terraform](#examples-terraform)
4. [🏠 Examples localstack](#examples-localstack)
5. [🔧 Technical Explanation](#technical-explanation)
6. [🛠️ Task list](#task-list)
    
## Quickstart
    
## 📋 Requirements
- OpenAI key with access to GPT-4
- AWS Account
- [Optional] Pinecone access


### 1. Deploy AWS architecture on a dev environement directly in AWS and test it there.
    
    a) Install all the dependencies (as noted in requirements.txt)

    b) Create a dev environement in AWS. Preferably with budgets. (Agent will interact with the budgetalerts, see further development tickets at the page end.)

    c) Make sure that AWS Toolkit in VS Code is enabled, installed and connected to your dev environement.

    d) Make sure you define "AWS_ACCESS_KEY_ID" , "AWS_SECRET_ACCESS_KEY" and "AWS_DEFAULT_REGION" in the 'cloud_gpt_aws_cloudwatch.py' script.

    e) Insert the OpenAI credentials into 'cloud_gpt_aws_cloudwatch.py' script.

    f) Run the script: 'python cloud_gpt_aws_cloudwatch.py "create an s3 bucket and rds database and test that data is transferred between the two"'
    
### 2. Deploy AWS architecture on [localstack](https://localstack.cloud/) and test it there.

    a) Install all the dependencies (as noted in requirements.txt)

    b) Install localstack.

    c) Insert the OpenAI credentials into cloud_gpt_mvp.py and run it.

    
 _NOTE: The complexity of the solution is inherently tied to the number of tokens you GPT4 model can produce. Currently the 32k version is the most powerfull._   

### Installation (PyPi still missing)
```bash
pip install cloudgpt
cloudgpt configure --key <your openai api key>
```
If you set the environment variable `OPENAI_API_KEY`, the configuration step can be skipped.
Your api key must have access to gpt-4 to use this tool. 
We are working on a way to use gpt-3.5-turbo as well.

### Generate Infrastracture
```bash
cloudgpt generate --description "<description of your problem and potential solutions>"
```

The creation process should take between 5 and 15 minutes.

During this time, GPT iteratively builds your infrastructure until it finds a strategy that make your test scenario pass.

Be aware that the costs you have to pay for openai vary between $1.00 and $4.00 per infrastructure deployed (using GPT-4).

### Deploy Infrastracture
If you want to deploy your infrastructure to the cloud a [AWS account](https://aws.amazon.com/?nc1=h_ls) is required.

We will provide a tutorial how to set up a sandbox environment for the AWS.

```bash
cloudgpt deploy --infrastructure_path <path to infrastructure>
```

## 🌐 Examples AWS


### S3-RDS Architecture Example

```bash

gptdeploy generate --description "create an s3 bucket and rds database and test that data is transferred between the two"
```

or pass the "create an s3 bucket and rds database and test that data is transferred between the two" when calling the 'cloud_gpt_aws_cloud.py'

<img src="misc\s3_rds.png" alt="First mistake AWS agent" heigth="150"/>

We first get a mistake because agent suggests following architecture:

```python
import boto3
import os
from botocore.exceptions import ClientError


def create_s3_bucket(bucket_name):
    s3 = boto3.client('s3', aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                      aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
                      region_name=os.environ['AWS_DEFAULT_REGION'])

    try:
        s3.create_bucket(Bucket=bucket_name)
    except ClientError as e:
        print(e)


def create_rds_instance(instance_name, master_username, master_password):
    rds = boto3.client('rds', aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                       aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
                       region_name=os.environ['AWS_DEFAULT_REGION'])

    try:
        rds.create_db_instance(
            DBName=instance_name,
            AllocatedStorage=20,
            DBInstanceIdentifier=instance_name,
            Engine='mysql',
            MasterUsername=master_username,
            MasterUserPassword=master_password,
            DBInstanceClass='db.t2.micro',
            VpcSecurityGroupIds=[],
            AvailabilityZone=os.environ['AWS_DEFAULT_REGION'] + 'a'
        )
    except ClientError as e:
        print(e)


def test_data_transfer(bucket_name, instance_name, master_username, master_password):
    import pymysql
    import time

    s3 = boto3.resource('s3', aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
                        region_name=os.environ['AWS_DEFAULT_REGION'])

    rds = boto3.client('rds', aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                       aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
                       region_name=os.environ['AWS_DEFAULT_REGION'])

    try:
        s3.Object(bucket_name, 'test_data.txt').put(Body='Hello World!')
    except ClientError as e:
        print(e)

    instance = rds.describe_db_instances(DBInstanceIdentifier=instance_name)['DBInstances'][0]

    while instance['DBInstanceStatus'] != 'available':
        time.sleep(10)
        instance = rds.describe_db_instances(DBInstanceIdentifier=instance_name)['DBInstances'][0]

    try:
        connection = pymysql.connect(
            host=instance['Endpoint']['Address'],
            user=master_username,
            password=master_password,
            db=instance_name
        )

        with connection.cursor() as cursor:
            cursor.execute('CREATE TABLE IF NOT EXISTS test_data (id INT AUTO_INCREMENT PRIMARY KEY, content TEXT NOT NULL)')
            cursor.execute("INSERT INTO test_data (content) VALUES ('Hello World!')")
            connection.commit()

            cursor.execute('SELECT * FROM test_data')
            result = cursor.fetchone()

            assert result[1] == 'Hello World!'

            print('Data transfer test passed.')

    except pymysql.MySQLError as e:
        print(e)


def deploy_solution(bucket_name, instance_name, master_username, master_password):
    create_s3_bucket(bucket_name)
    create_rds_instance(instance_name, master_username, master_password)
    test_data_transfer(bucket_name, instance_name, master_username, master_password)


if __name__ == '__main__':
    deploy_solution('my-test-s3-bucket', 'my-test-rds-instance', 'myuser', 'mypassword')
```


<img src="misc\mistake_s3_rds.png" alt="First mistake AWS agent" heigth="150"/>

This mistake is fed back as input to the agent automatically, as a conversation point. Afterwards it self corrects and publishes exactly what was needed, passing the test.

```python
import boto3
import os
from botocore.exceptions import ClientError
import uuid


def create_s3_bucket(bucket_name):
    s3 = boto3.client('s3', aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                      aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
                      region_name=os.environ['AWS_DEFAULT_REGION'])

    try:
        s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': os.environ['AWS_DEFAULT_REGION']})
    except ClientError as e:
        print(e)


def create_rds_instance(instance_name, master_username, master_password):
    rds = boto3.client('rds', aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                       aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
                       region_name=os.environ['AWS_DEFAULT_REGION'])

    try:
        rds.create_db_instance(
            AllocatedStorage=20,
            DBInstanceIdentifier=instance_name,
            Engine='mysql',
            MasterUsername=master_username,
            MasterUserPassword=master_password,
            DBInstanceClass='db.t2.micro',
            VpcSecurityGroupIds=[],
            AvailabilityZone=os.environ['AWS_DEFAULT_REGION'] + 'a'
        )
    except ClientError as e:
        print(e)


def test_data_transfer(bucket_name, instance_name, master_username, master_password):
    import pymysql
    import time

    s3 = boto3.resource('s3', aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
                        region_name=os.environ['AWS_DEFAULT_REGION'])

    rds = boto3.client('rds', aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                       aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
                       region_name=os.environ['AWS_DEFAULT_REGION'])

    try:
        s3.Object(bucket_name, 'test_data.txt').put(Body='Hello World!')
    except ClientError as e:
        print(e)

    instance = rds.describe_db_instances(DBInstanceIdentifier=instance_name)['DBInstances'][0]

    while instance['DBInstanceStatus'] != 'available':
        time.sleep(10)
        instance = rds.describe_db_instances(DBInstanceIdentifier=instance_name)['DBInstances'][0]

    try:
        connection = pymysql.connect(
            host=instance['Endpoint']['Address'],
            user=master_username,
            password=master_password,
            db='mysql'
        )

        with connection.cursor() as cursor:
            cursor.execute('CREATE DATABASE IF NOT EXISTS test_db')
            cursor.execute('USE test_db')
            cursor.execute('CREATE TABLE IF NOT EXISTS test_data (id INT AUTO_INCREMENT PRIMARY KEY, content TEXT NOT NULL)')
            cursor.execute("INSERT INTO test_data (content) VALUES ('Hello World!')")
            connection.commit()

            cursor.execute('SELECT * FROM test_data')
            result = cursor.fetchone()

            assert result[1] == 'Hello World!'

            print('Data transfer test passed.')

    except pymysql.MySQLError as e:
        print(e)


def deploy_solution(bucket_name, instance_name, master_username, master_password):
    unique_id = str(uuid.uuid4())
    create_s3_bucket(bucket_name + '-' + unique_id)
    create_rds_instance(instance_name + '-' + unique_id, master_username, master_password)
    test_data_transfer(bucket_name + '-' + unique_id, instance_name + '-' + unique_id, master_username, master_password)


if __name__ == '__main__':
    deploy_solution('my-test-s3-bucket', 'my-test-rds-instance', 'myuser', 'mypassword')


```
<img src="misc\s3.png" alt="Sucess AWS agent" height="100" />
<img src="misc\rds.png" alt="Sucess AWS agent" height="100" />

<img src="misc\success_deployment.png" alt="Sucess AWS agent" height="150" />

### SQS-SNS Architecture Example

```bash

gptdeploy generate --description "create an SQS and SNS solution"
```

or pass the "create an SQS and SNS solution" when calling the 'cloud_gpt_aws_cloud.py'

<img src="misc\sns_sqs.png" alt="First mistake AWS agent" heigth="150"/>

We immediately get the correct solution:

```python
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
```

Confirmation of deployment:


<img src="misc\sqs_sns_aws.png" alt="First mistake AWS agent" heigth="150"/>

## 🏠 Examples localstack


### SQS-SNS Architecture Example

```bash

gptdeploy generate --description "write me a sqs and sns solution and test it on localstack"
```


<img src="misc\sns_sqs.png" alt="First mistake AWS agent" heigth="150"/>

We first get a mistake because agent suggests following architecture:

```python
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

sns_topic = sns_client.create_topic(Name="test_topic")
topic_arn = sns_topic["TopicArn"]

sns_client.subscribe(
    TopicArn=topic_arn,
    Protocol="sqs",
    Endpoint=f"{queue_url}",
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
```


<img src="misc\sns_sqs_mistake.png" alt="First mistake AWS agent" heigth="150"/>

This mistake is fed back as input to the agent automatically, as a conversation point. Afterwards it self corrects and publishes exactly what was needed, passing the test.

```python
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

```
<img src="misc\sns_sqs_no_mistake.png" alt="Sucess AWS agent" height="100" />




# Technical Explanation
The graphic below illustrates the process of creating the proposal architecture and deploying it to the cloud elaboration two different implementation strategies.

<img src="misc\cloud_gpt.png" alt="Workflow" />


1. Cloud GPT identifies a strategy and then interacts with the logs as it tries to deploy in the sandbox.
2. It tests each strategy until it finds one that works.
3. For each strategy, it generates a singular python file that creates the architecture.
4. Cloud GPT attempts to pass the autogenerated e2e test and produce 0 errors in the logs.
5. Once it finds a successful strategy, it deploys the architecture in the sandbox.
6. If it fails 10 times in a row, it moves on to the next completely different approach.
7. If it again fails here it provides the code to the last suggested solution without deployment. 



## 🛠️ Task list

Task priorities are ordered (still missing):

1. Publish a python package abstracting the functionalities away.
2. Fine tune the GPT-4 on AWS + Boto3 code using [LoRA](https://adapterhub.ml/blog/2022/09/updates-in-adapter-transformers-v3-1/) like adapters.
3. Configure the agent to use budget alerts from the AWS dev environement.
4. Replace singular GPT endpoint with auto-gpt or baby agi. This can also help solve architecture diagramms and it could help with systematic sequential thinking.
5. Integration with langchain
6. Estimate the cost and stdout the estimate at every (successfull) iteration.
7. Integrate LMQL: LMQL is a programming language for language model interaction. This would allow better suggestions: https://lmql.ai/#wiki
8. add more examples to README.md
9. Integrate [hatch](https://hatch.pypa.io/latest/install/) to manage the development environment and production build.
10. CI/CD on Github Actions.

Following are less-important, but needed tasks:

1. add video to README.md with super detailed explanations.
2. Deploy the solution automatically to the AWS cloud in a real, limited sanbox environment on the AWS (not through localstack)
3. Control the OpenAI spending
4. UI/In the browser
5. Go multi cloud not only AWS. Fine-tune on Terraform examples.
6. Fine-tune the GPT model to respond better to error messages from localstack.
7. Fine tune the GPT to make better suggestions (i.e. change temperature etc.)
8. Help localstack improve the support (5 stars) for more of the core services.
9. Integrate the possibility for Cloude (Anthropic AI)
10. check if windows and linux support works
11. support gpt3.5-turbo
12. if the user runs cloudGPT without any arguments, show the help message
13. autoscaling enabled for cost saving
14. support for other large language models like Open Assistent
15. use cloudGPT list to show all deployments
16. cloudGPT delete to delete a deployment
17. cloudGPT update to update a deployment
18. Release workflow
