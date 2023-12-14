import os
import json
import boto3
import botocore
import logging
from src.urls3upload import url_assinada, url_assinada_post
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # Initialize the SSM client
    ssm = boto3.client('ssm')

    # Initialize the default response parameters
    code = 200
    data = None

    # Define the default headers for the response
    headers = {
        "Content-type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "*",
        "Access-Control-Allow-Headers": "*",
        "Accept": "*/*"
    }

    try:
        # Parse the event body
        logger.info(json.loads(event['body']))
        bucket_name = os.environ.get("S3_BUCKET_NAME", "bucket-live-124323")
        path = json.loads(event['body'])['s3KeyPath']
        metodo = json.loads(event['body'])['metodo']

        region = os.environ.get("REGION", "sa-east-1")
        
        if(metodo != "pre_signed_url_post"):
            data = url_assinada(bucket_name, path, 3600, metodo)
        else:
            data = url_assinada_post(bucket_name, path)
        print(data)


    except botocore.exceptions.ClientError as e:
        # Handle client errors from boto3 calls
        error = e.response['Error']
        logger.error(f'Erro tratado: {error}')
        code = error['Code']
        data = e.args[0]

    except Exception as e:
        # Handle non-client errors
        logger.error(f'Erro nao tratado: {e}')
        code = 500
        data = e

    print(data)

    # Prepare the final return
    retorno_final = retorno_funcao(code, data, headers)
    
    print(retorno_final)

    return retorno_final

def retorno_funcao(code, data, headers):
    return {
        "statusCode": code,
        "body": json.dumps({
            "data": data
        }),
        "headers": headers
    }#lesgo