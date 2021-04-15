import json
import random
import string

import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("ToDoTable")


def post_todo(event, context):
    body = json.loads(event.get("body"))
    todo = body.get("todo")
    todo_id = "".join(random.choices(string.ascii_letters + string.digits, k=12))

    item = {"todo_id": todo_id, "todo": todo}
    table.put_item(Item=item)

    response = {"statusCode": 200, "body": json.dumps(item)}

    return response


def get_todo(event, context):
    todo_id = event["pathParameters"]["todoId"]

    res = table.get_item(Key={"todo_id": todo_id})
    item = res["Item"]

    response = {"statusCode": 200, "body": json.dumps(item)}

    return response


def put_todo(event, context):
    todo_id = event["pathParameters"]["todoId"]
    body = json.loads(event.get("body"))
    todo = body.get("todo")

    item = {"todo_id": todo_id, "todo": todo}
    table.update_item(
        Key={"todo_id": todo_id},
        UpdateExpression="set todo=:todo",
        ExpressionAttributeValues={":todo": todo},
    )

    response = {"statusCode": 200, "body": json.dumps(item)}

    return response


def delete_todo(event, context):
    todo_id = event["pathParameters"]["todoId"]

    table.delete_item(Key={"todo_id": todo_id})

    response = {"statusCode": 200, "body": json.dumps({"todo_id": todo_id})}

    return response
