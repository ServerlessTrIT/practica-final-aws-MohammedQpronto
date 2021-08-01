import json
import logging
import os
import time
import uuid

import boto3
dynamodb = boto3.resource('dynamodb')


def create(event, context):
    data = json.loads(event['body'])
    if 'Nombre' not in data:
        logging.error("Se necesita un nombre")
        raise Exception("No se ha podido añadir a la bbdd.")
    
    timestamp = str(time.time())

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    item = {
        'id': str(uuid.uuid1()),
        'Nombre': data['Nombre'],
        'Creado': timestamp,
        'actualizado': timestamp,
        'Posicion': data['Posicion']
    }

    # write the todo to the database
    table.put_item(Item=item)

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(item)
    }

    return response
