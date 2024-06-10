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
        return create_author(json.loads(event['body']))
    elif event['httpMethod'] == 'GET':
        return read_author(event['queryStringParameters'])
    elif event['httpMethod'] == 'PUT':
        return update_author(json.loads(event['body']))
    elif event['httpMethod'] == 'DELETE':
        if event.get('resource') == '/authors/batch':
            return batch_delete_authors(json.loads(event['body']))
        else:
            return delete_author(event['queryStringParameters'])
    else:
        return {"statusCode": 400, "body": json.dumps({"message": "Unsupported method"})}

def create_author(payload):
    try:
        table.put_item(Item=payload)
        return {"statusCode": 200, "body": json.dumps(payload)}
    except ClientError as e:
        return {"statusCode": 500, "body": json.dumps({"message": str(e)})}

def read_author(payload):
    try:
        response = table.get_item(Key={'AuthorID': payload['AuthorID']})
        return {"statusCode": 200, "body": json.dumps(response.get('Item', {}))}
    except ClientError as e:
        return {"statusCode": 500, "body": json.dumps({"message": str(e)})}

def update_author(payload):
    try:
        key = {'AuthorID': payload['AuthorID']}
        update_expression = "set " + ", ".join([f"{k} = :{k}" for k in payload.keys() if k != 'AuthorID'])
        expression_attribute_values = {f":{k}": v for k, v in payload.items() if k != 'AuthorID'}
        response = table.update_item(
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW"
        )
        return {"statusCode": 200, "body": json.dumps(response['Attributes'])}
    except ClientError as e:
        return {"statusCode": 500, "body": json.dumps({"message": str(e)})}

def delete_author(payload):
    try:
        key = {'AuthorID': payload['AuthorID']}
        table.delete_item(Key=key)
        return {"statusCode": 200, "body": json.dumps(key)}
    except ClientError as e:
        return {"statusCode": 500, "body": json.dumps({"message": str(e)})}

def batch_delete_authors(payload):
    try:
        author_ids = payload.get('AuthorIDs', [])
        if not author_ids:
            return {"statusCode": 400, "body": json.dumps({"message": "No AuthorIDs provided"})}

        for author_id in author_ids:
            key = {'AuthorID': author_id}
            table.delete_item(Key=key)

        return {"statusCode": 200, "body": json.dumps({"message": "Authors deleted successfully"})}
    except ClientError as e:
        return {"statusCode": 500, "body": json.dumps({"message": str(e)})}

