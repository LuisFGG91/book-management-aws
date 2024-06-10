import boto3
import os
import json
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def handler(event, context):
    try:
        if event['httpMethod'] == 'POST':
            return create_genre(json.loads(event['body']))
        elif event['httpMethod'] == 'GET':
            return read_genre(event['queryStringParameters'])
        elif event['httpMethod'] == 'PUT':
            return update_genre(json.loads(event['body']))
        elif event['httpMethod'] == 'DELETE':
            return delete_genre(event['queryStringParameters'])
        else:
            return {"statusCode": 400, "body": json.dumps({"message": "Unsupported method"})}
    except KeyError:
        return {"statusCode": 400, "body": json.dumps({"message": "Missing required parameter"})}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"message": str(e)})}

def create_genre(payload):
    try:
        table.put_item(Item=payload)
        return {"statusCode": 200, "body": json.dumps(payload)}
    except ClientError as e:
        return {"statusCode": 500, "body": json.dumps({"message": str(e)})}

def read_genre(payload):
    try:
        response = table.get_item(Key={'GenreID': payload['GenreID']})
        return {"statusCode": 200, "body": json.dumps(response.get('Item', {}))}
    except ClientError as e:
        return {"statusCode": 500, "body": json.dumps({"message": str(e)})}

def update_genre(payload):
    try:
        key = {'GenreID': payload['GenreID']}
        update_expression = "set " + ", ".join([f"{k} = :{k}" for k in payload.keys() if k != 'GenreID'])
        expression_attribute_values = {f":{k}": v for k, v in payload.items() if k != 'GenreID'}
        response = table.update_item(
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW"
        )
        return {"statusCode": 200, "body": json.dumps(response['Attributes'])}
    except ClientError as e:
        return {"statusCode": 500, "body": json.dumps({"message": str(e)})}

def delete_genre(payload):
    try:
        key = {'GenreID': payload['GenreID']}
        table.delete_item(Key=key)
        return {"statusCode": 200, "body": json.dumps(key)}
    except ClientError as e:
        return {"statusCode": 500, "body": json.dumps({"message": str(e)})}

