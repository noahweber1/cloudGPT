import boto3
import os 

os.environ['AWS_DEFAULT_REGION'] = ''
os.environ['AWS_ACCESS_KEY_ID'] = ''
os.environ['AWS_SECRET_ACCESS_KEY'] = ''

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
