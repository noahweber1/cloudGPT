import boto3

def create_s3_and_lambda_solution(bucket_name, function_name, lambda_role_arn, runtime, handler, region, aws_access_key_id, aws_secret_access_key):
    s3 = boto3.client('s3', region_name=region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    lambda_client = boto3.client('lambda', region_name=region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    # Create S3 bucket
    s3.create_bucket(Bucket=bucket_name)

    # Create Lambda function
    lambda_client.create_function(
        FunctionName=function_name,
        Runtime=runtime,
        Role=lambda_role_arn,
        Handler=handler,
        Code={
            'S3Bucket': bucket_name,
            'S3Key': 'lambda_function.py'
        }
    )

    return 'S3 and Lambda solution created successfully'


# Test the solution
test_bucket_name = 'test-bucket-name'
test_function_name = 'test-function-name'
test_lambda_role_arn = 'arn:aws:iam::123456789012:role/service-role/test-role'
test_runtime = 'python3.8'
test_handler = 'lambda_function.lambda_handler'
test_region = 'us-west-2'
test_aws_access_key_id = 'YOUR_AWS_ACCESS_KEY_ID'
test_aws_secret_access_key = 'YOUR_AWS_SECRET_ACCESS_KEY'

print(create_s3_and_lambda_solution(test_bucket_name, test_function_name, test_lambda_role_arn, test_runtime, test_handler, test_region, test_aws_access_key_id, test_aws_secret_access_key))
