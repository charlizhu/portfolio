import json
import uuid
import boto3
from botocore.config import Config

def lambda_handler(event, context):
    
    body = event['queryStringParameters']
    UserId = body['userid']
    # UserId = '0-629be520-c167-409d-99fd-c073e61f3a77'
    dynamodb = boto3.resource('dynamodb')
    game_state_table = dynamodb.Table('game_state')
    
    try:

        response = game_state_table.update_item(
            Key={
                'UserId': UserId
            },
            UpdateExpression="SET HasAvatar = :x",
            ExpressionAttributeValues={
                ':x': True
            },
            ReturnValues="UPDATED_NEW"
        )
    except Exception as e:
        print(e)
        return {
            'statusCode': 400,
            'body': json.dumps(str(e))
        }
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Processed')
    }
