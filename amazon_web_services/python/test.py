import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event,context):

    print("HI")
    print(event)
    # event needs to contain bucket and key
    expiration=3600
    http_method='PUT'
    client_method='put_object'
    try:
        bucket=event['queryStringParameters']['bucket']
    except:
        bucket="yalty-dev-users"
    key=event['queryStringParameters']['key']
    print(bucket,key)
    s3 = boto3.client('s3')
    try:
        response = (s3.generate_presigned_url(ClientMethod=client_method, Params={'Bucket':bucket,'Key':key}, ExpiresIn=expiration, HttpMethod=http_method))
    except ClientError as e:
        logging.error(e)
        return {
        'statusCode': 400,
        'body': json.dumps(e)
        }

    # The response contains the presigned URL
    return {
    'statusCode': 200,
    'body': json.dumps(response)
    }