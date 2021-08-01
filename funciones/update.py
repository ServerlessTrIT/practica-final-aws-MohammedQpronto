import json
import time
import logging
import os

from funciones import decimalencoder
import boto3
dynamodb = boto3.resource('dynamodb')


def update(event, context):
    data = json.loads(event['body'])
    if 'Nombre' not in data or 'checked' not in data:
        logging.error("La validación ha fallado")
        raise Exception("No se ha podido actualizar.")
        return

    timestamp = int(time.time() * 1000)

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

  
    result = table.update_item(
        Key={
            'id': event['pathParameters']['id']
        },
        ExpressionAttributeNames={
          '#nombre': 'Nombre',
        },
        ExpressionAttributeValues={
          ':Nombre': data['Nombre'],
          ':checked': data['checked'],
          ':actualizado': timestamp,
        },
        UpdateExpression='SET #nombre = :Nombre, '
                         'checked = :checked, '
                         'actualizado = :actualizado',
        ReturnValues='ALL_NEW',
    )

    
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Attributes'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response
