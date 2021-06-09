import boto3
from django.http import JsonResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def test(request):
    return JsonResponse({'message': 'hello Daud'}, status=200)


def _parse_body(body):
    body_unicode = body.decode('utf-8')
    return json.loads(body_unicode)


@csrf_exempt
def connect(request):
    body = _parse_body(request.body)
    connection_id = body['connectionId']
    Connection.objects.create(connection_id=connection_id)
    return JsonResponse({'message': 'connect successfully'}, status=200,safe=False)



@csrf_exempt
def disconnect(request):
    body = _parse_body(request.body)
    connection_id = body['connectionId']
    Connection.objects.get(connection_id=connection_id).delete()

    return JsonResponse({'message': 'disconnect successfully'}, status=200,safe=False)


@csrf_exempt
def _send_to_connection(connection_id, data):
    gatewayapi = boto3.client("apigatewaymanagementapi", endpoint_url="https://jniw3bbhhi.execute-api.us-east-2.amazonaws.com/test/",
        region_name="us-east-2", aws_access_key_id="AKIA3HOOM6AGXFZYLJ5N", aws_secret_access_key="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")

    return gatewayapi.post_to_connection(ConnectionId=connection_id, Data=json.dumps(data).encode("utf-8"))


@csrf_exempt
def send_message(request):
    body = _parse_body(request.body)
    dict_body = dict(body)
    username = dict_body['body']['username']
    timestamp = dict_body['body']['timestamp']
    content = dict_body['body']['content']
    ChatMessage.objects.create(username=username, timestamp=timestamp, messages=content,)
    connections = Connection.objects.all()
    messages = {
        "username": username,
        "timestamp": timestamp,
        "messages": content
    }
    data = {"messages": [messages]}
    for connection in connections:
        _send_to_connection(connection.connection_id, data)

    return JsonResponse({"message": "message sent successfully"}, status=200, safe=False)


@csrf_exempt
def recent_messages(request):
    body = _parse_body(request.body)
    connections = [i.connection_id for i in Connection.objects.all()]
    message_list = [{'username':chat_message.username, 'content':chat_message.messages,
                     'timestamp':chat_message.timestamp} for chat_message in ChatMessage.objects.all()]
    data = {'messages': message_list}
    for connection_id in connections:
        _send_to_connection(connection_id, data)
    return JsonResponse({'message':'successfully sent'}, status=200,safe=False)


