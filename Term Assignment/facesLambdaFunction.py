import boto3
import json

def lambda_handler(event, context):
    bucket_name = event['detail']['bucket']['name']
    object_key = event['detail']['object']['key']
    faces = detect_faces(bucket_name, object_key)
    result_file_key = f'{object_key.split(".")[0]}-faces.json'
    store_result_in_s3("faces-result", result_file_key, faces)
    return {
        'statusCode': 200,
        'body': {
            'Faces': faces
        }
    }

def detect_faces(bucket, key):
    rekognition = boto3.client('rekognition')
    
    # Call DetectFaces API to detect faces in the image
    response = rekognition.detect_faces(Image={'S3Object': {'Bucket': bucket, 'Name': key}})
    faces = response['FaceDetails']
    
    return faces

def store_result_in_s3(bucket, key, data):
    s3 = boto3.resource('s3')
    json_data = json.dumps(data, indent=2)
    s3.Object(bucket, key).put(Body=json_data)
    
# def publish_to_sns(topic_arn, message):
#     sns = boto3.client('sns')
#     response = sns.publish(TopicArn=topic_arn, Message=json.dumps(message))
#     return response