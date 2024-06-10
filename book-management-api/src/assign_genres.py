import boto3
import os
import json
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])
user_pool_id = os.environ['USER_POOL_ID']

def handler(event, context):
    try:
        user_id = event['requestContext']['authorizer']['claims']['sub']
    except KeyError:
        return {"statusCode": 401, "body": json.dumps({"message": "Unauthorized"})}

    if event['httpMethod'] == 'POST':
        return assign_genre_to_book(json.loads(event['body']))
    elif event['httpMethod'] == 'DELETE':
        return remove_genre_from_book(event['queryStringParameters'])
    else:
        return {"statusCode": 400, "body": json.dumps({"message": "Unsupported method"})}

def assign_genre_to_book(payload):
    try:
        table.put_item(Item=payload)
        return {"statusCode": 200, "body": json.dumps(payload)}
    except ClientError as e:
        return {"statusCode": 500, "body": json.dumps({"message": str(e)})}

def remove_genre_from_book(payload):
    key = {'BookID': payload['BookID'], 'GenreID': payload['GenreID']}
    try:
        table.delete_item(Key=key)
        return {"statusCode": 200, "body": json.dumps(key)}
    except ClientError as e:
        return {"statusCode": 500, "body": json.dumps({"message": str(e)})}

