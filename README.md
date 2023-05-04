<h1 align="center">
cloudgpt: One line to generate all cloud infrastructure ☁️
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


This project streamlines the creation and deployment of cloud infrastructure. 
Simply describe your problem using natural language, and the system will automatically build, test and deploy the best cloud architecture.    

_NOTE: some features are still under heavy development, to test current version, see points 1. and 2. underneath._     
    
Current capabilities:
   1. [✅] Deploy AWS architecture on [localstack](https://localstack.cloud/) and test it there.
   2. [✅] Deploy AWS architecture on a dev environement directly in AWS and test it there.
    
## Quickstart
    
### Requirements
- OpenAI key with access to GPT-4

    
### 1. Deploy AWS architecture on [localstack](https://localstack.cloud/) and test it there.

    a) Install all the dependencies (as noted in requirements.txt)

    b) Install localstack.

    c) Insert the OpenAI credentials into cloud_gpt_mvp.py and run it.

### 2. Deploy AWS architecture on a dev environement directly in AWS and test it there.
    
    a) Install all the dependencies (as noted in requirements.txt)

    b) Create a dev environement in AWS. Preferably with budgets. (Agent will interact with the alerts, see further development tickets at the page end.)

    c) Make sure that AWS Toolkit in VS Code is enabled, installed and connected to your dev environement.

    d) Make sure you define "AWS_ACCESS_KEY_ID" , "AWS_SECRET_ACCESS_KEY", "AWS_DEFAULT_REGION" and "AWS_SESSION_TOKEN" in all GPT_AWS scripts.

    e) Insert the OpenAI credentials into cloud_gpt_aws_cloudwatch.py and run it.
    
 _NOTE: The complexity of the solution is inherently tied to the number of tokens you GPT4 model can produce. Currently the 32k version is the most powerfull.._   

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


## Examples


### SQS - SNS Architecture

```bash

gptdeploy generate --description "write me a sqs and sns solution and test it on localstack"
```


<img src="misc\sns_sqs.png" alt="First mistake AWS agent" heigth="150"/>

We first get a mistake because agent suggest following architecture:

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

## Technical Insights
The graphic below illustrates the process of creating the proposal architecture and deploying it to the cloud elaboration two different implementation strategies.

<img src="misc\cloud_gpt.png" alt="Workflow" />


1. Cloud GPT identifies a strategy and then interacts with the logs as it tries to deploy in the sandbox.
2. It tests each strategy until it finds one that works.
3. For each strategy, it generates a singular python file that creates the architecture.
4. Cloud GPT attempts to pass the autogenerated e2e test and produce 0 errors in the logs.
5. Once it finds a successful strategy, it deploys the architecture in the sandbox.
6. If it fails 10 times in a row, it moves on to the next completely different approach.
7. If it again fails here it provides the code to the last suggested solution without deployment. 



## 🛠️ Task list:

Task priorities are ordered (still missing):

1. Publish a python package abstracting the functionalities away.
2. Fine tune the GPT-4 on AWS + Boto3 code using [LoRA](https://adapterhub.ml/blog/2022/09/updates-in-adapter-transformers-v3-1/) like adapters.
3. Configure the agent to use budget alerts from the AWS dev environement.
4. Replace singular GPT endpoint with auto-gpt or baby agi. This can also help solve architecture diagramms and it could help with systematic sequential thinking.
5. Integration with langchain
6. Estimate the cost and stdout the estimate at every (successfull) iteration.
7. Integrate LMQL: LMQL is a programming language for language model interaction. This would allow better suggestions: https://lmql.ai/#wiki
8. add more examples to README.md
9. Integrate a vector database for better memory.


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
12. if the user runs cloudgpt without any arguments, show the help message
13. autoscaling enabled for cost saving
14. support for other large language models like Open Assistent
15. use cloudgpt list to show all deployments
16. cloudgpt delete to delete a deployment
17. cloudgpt update to update a deployment
18. Release workflow
