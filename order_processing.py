import json
import boto3
import os

client = boto3.client('events')
EVENT_BUS_NAME = os.environ.get('EVENT_BUS_NAME', 'order-processing-bus')

def lambda_handler(event, context):
    body = json.loads(event.get('body', '{}'))
    order_id = body.get('order_id')
    customer_name = body.get('customer_name')
    items = body.get('items', [])
    event_detail = {
        'order_id': order_id,
        'customer_name': customer_name,
        'items': items,
        'total': body.get('total', 0)
    }
    response = client.put_events(Entries=[{
        'Source': 'com.orders.processor',
        'DetailType': 'OrderPlaced',
        'Detail': json.dumps(event_detail),
        'EventBusName': EVENT_BUS_NAME
    }])
    event_id = response['Entries'][0].get('EventId', '')
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Order placed', 'order_id': order_id, 'event_id': event_id})
    }
