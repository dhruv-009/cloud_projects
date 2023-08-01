import boto3
import json

def lambda_handler(event, context):
    print(event)
    sns_message = json.loads(event['Records'][0]['Sns']['Message'])
    face_details = sns_message['Faces']
    facial_expression = infer_facial_expression(face_details)
    bucket_name = 'sentiment-result'
    object_key = 'face_detection_result.json'
    s3 = boto3.client('s3')
    s3.put_object(Bucket=bucket_name, Key=object_key, Body=json.dumps(facial_expression))
    return {
        'statusCode': 200,
        'body': facial_expression
    }

def infer_facial_expression(face_details):
    facial_expressions = []
    for face in face_details:
        # Extract the positions of mouth landmarks for each face
        mouth_left = face['Landmarks'][2]
        mouth_right = face['Landmarks'][3]
        mouth_width = abs(mouth_left['X'] - mouth_right['X'])
        smile_threshold = 0.2
        
        # If the mouth width is above the threshold, classify the person as smiling
        if mouth_width > smile_threshold:
            facial_expressions.append('Smiling')
        else:
            facial_expressions.append('Not Smiling')
    
    return facial_expressions