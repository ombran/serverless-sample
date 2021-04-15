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
