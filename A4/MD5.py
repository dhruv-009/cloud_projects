import hashlib
import requests

def lambda_handler(event, context):
    try:
        data = event
        value = data['value']
        hashed_value = hashlib.md5(value.encode('utf-8')).hexdigest()
        print(hashed_value)
        response = {
            "banner": "B00947866",
            "result": hashed_value,
            "arn": "arn:aws:lambda:us-east-1:982062056330:function:MD5",
            "action": "md5",
            "value": value
        }
        requests.post("https://v7qaxwoyrb.execute-api.us-east-1.amazonaws.com/default/end", json=response)

        return {
            "statusCode": 200,
            "body": response
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": "Error: " + str(e)
        }
