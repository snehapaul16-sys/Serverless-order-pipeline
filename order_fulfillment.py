import json

def lambda_handler(event, context):
    detail = event.get('detail', {})
    order_id = detail.get('order_id')
    return {
        'statusCode': 200,
        'body': json.dumps({'order_id': order_id, 'status': 'FULFILLED'})
    }
