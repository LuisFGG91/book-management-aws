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
        return create_book(json.loads(event['body']))
    elif event['httpMethod'] == 'GET':
        return read_book(event['queryStringParameters'])
    elif event['httpMethod'] == 'PUT':
        return update_book(json.loads(event['body']))
    elif event['httpMethod'] == 'DELETE':
        if event.get('resource') == '/books/batch':
            return batch_delete_books(json.loads(event['body']))
        else:
            return delete_book(event['queryStringParameters'])
    else:
        return {"statusCode": 400, "body": json.dumps({"message": "Unsupported method"})}

def create_book(payload):
    try:
        table.put_item(Item=payload)
        return {"statusCode": 200, "body": json.dumps(payload)}
    except ClientError as e:
        return {"statusCode": 500, "body": json.dumps({"message": str(e)})}

def read_book(payload):
    try:
        response = table.get_item(Key={'BookID': payload['BookID']})
        return {"statusCode": 200, "body": json.dumps(response.get('Item', {}))}
    except ClientError as e:
        return {"statusCode": 500, "body": json.dumps({"message": str(e)})}

def update_book(payload):
    try:
        key = {'BookID': payload['BookID']}
        update_expression = "set " + ", ".join([f"{k} = :{k}" for k in payload.keys() if k != 'BookID'])
        expression_attribute_values = {f":{k}": v for k, v in payload.items() if k != 'BookID'}
        response = table.update_item(
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW"
        )
        return {"statusCode": 200, "body": json.dumps(response['Attributes'])}
    except ClientError as e:
        return {"statusCode": 500, "body": json.dumps({"message": str(e)})}

def delete_book(payload):
    try:
        key = {'BookID': payload['BookID']}
        table.delete_item(Key=key)
        return {"statusCode": 200, "body": json.dumps(key)}
    except ClientError as e:
        return {"statusCode": 500, "body": json.dumps({"message": str(e)})}

def batch_delete_books(payload):
    try:
        book_ids = payload.get('BookIDs', [])
        if not book_ids:
            return {"statusCode": 400, "body": json.dumps({"message": "No BookIDs provided"})}

        for book_id in book_ids:
            key = {'BookID': book_id}
            table.delete_item(Key=key)

        return {"statusCode": 200, "body": json.dumps({"message": "Books deleted successfully"})}
    except ClientError as e:
        return {"statusCode": 500, "body": json.dumps({"message": str(e)})}