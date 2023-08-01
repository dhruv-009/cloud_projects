import boto3
import json

def lambda_handler(event, context):
    print(event)
    bucket_name = event['detail']['bucket']['name']
    object_key = event['detail']['object']['key']
    
    # Call AWS Rekognition to generate a caption for the image
    caption = generate_caption(bucket_name, object_key)
    
    # Store the caption result in the "caption-result" S3 bucket
    store_caption_result(bucket_name, object_key, caption)
    
    return event

def generate_caption(bucket, key):
    rekognition = boto3.client('rekognition')
    
    # Call DetectLabels API to get labels for the image
    response = rekognition.detect_labels(Image={'S3Object': {'Bucket': bucket, 'Name': key}})
    
    # Extract the first label as the caption
    if 'Labels' in response and len(response['Labels']) > 0:
        caption = response['Labels'][0]['Name']
    else:
        caption = "No caption found."
    
    return caption

def store_caption_result(bucket, key, caption):
    s3 = boto3.client('s3')
    result_bucket_name = "caption-result"
    result_object_key = f"{key.split('.')[0]}-caption.json"
    
    # Prepare the caption data as JSON
    caption_data = {
        "image": key,
        "caption": caption
    }
    s3.put_object(Bucket=result_bucket_name, Key=result_object_key, Body=json.dumps(caption_data))