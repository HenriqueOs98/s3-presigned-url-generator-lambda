import os
import boto3
from botocore.exceptions import ClientError

REGION = os.environ.get('REGION', "sa-east-1")

s3 =  boto3.client('s3', region_name = REGION, config = boto3.session.Config(signature_version='s3v4'))



# Function to generate a pre-signed URL for S3
def url_assinada(bucket_name, key, expires_in, tipo_evento):
    
    params = {
        'Bucket': bucket_name,
        'Key': key
    }
    try:


        # Generate the pre-signed URL
        response = s3.generate_presigned_url(
            ClientMethod=tipo_evento,
            Params=params,
            ExpiresIn=expires_in
        )
        return response
    except Exception as e:
        print(e)
        raise
    
def url_assinada_post(bucket_name, key,
                          fields=None, conditions=None, expiration=3600):
    """Generate a presigned URL S3 POST request to upload a file

    :param bucket_name: string
    :param object_name: string
    :param fields: Dictionary of prefilled form fields
    :param conditions: List of conditions to include in the policy
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Dictionary with the following keys:
        url: URL to post to
        fields: Dictionary of form fields and values to submit with the POST
    :return: None if error.
    """

    # Generate a presigned S3 POST URL
    try:
        response = s3.generate_presigned_post(bucket_name,
                                                     key,
                                                     Fields=fields,
                                                     Conditions=conditions,
                                                     ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None
    return response

    # The response contai