import grpc
from concurrent import futures
from flask import request
import requests
import computeandstorage_pb2
import computeandstorage_pb2_grpc
import boto3

class EC2OperationsServicer(computeandstorage_pb2_grpc.EC2OperationsServicer):
    def __init__(self):
        self.s3_bucket = 'elastic-storage-cloud'
        self.s3_base_url = f'https://elastic-storage-cloud.s3.amazonaws.com'
        self.s3_client = boto3.client('s3')

    # def Start(self, request, context):
    #     banner = request.banner
    #     ip = request.ip
    #     print("Received start request:")
    #     print("Banner:", banner)
    #     print("IP:", ip)

    #     payload = {
    #         "banner": "B00947866",
    #         "ip": "173.212.76.90"
    #     }
    #     response = requests.post(self.rob_app_url, json=payload)

    #     if response.status_code == 200:
    #         print("POST request to Rob's application successful")
    #     else:
    #         print("POST request to Rob's application failed")
    #         print(response.text)

    #     response = computeandstorage_pb2.StartResponse(success=True)
    #     return response

    def StoreData(self, request, context):
        data = request.data

        file_name = 'data.txt'
        s3_key = f'{self.s3_bucket}/{file_name}'

        self.s3_client.put_object(
            Bucket=self.s3_bucket,
            Key=file_name,
            Body=data
        )

        s3_uri = f'{self.s3_base_url}/{file_name}'
        print(s3_uri)
        return computeandstorage_pb2.StoreReply(s3uri=s3_uri)

    def AppendData(self, request, context):
        data = request.data
        file_name = 'data.txt'
        s3_key = f'{self.s3_bucket}/{file_name}'

        existing_data = self.s3_client.get_object(
            Bucket=self.s3_bucket,
            Key=file_name
        )['Body'].read().decode()

        appended_data = existing_data + data

        self.s3_client.put_object(
            Bucket=self.s3_bucket,
            Key=file_name,
            Body=appended_data
        )

        return computeandstorage_pb2.AppendReply()

    def DeleteFile(self, request, context):
        s3_uri = request.s3uri
        s3_key = s3_uri.replace(self.s3_base_url + '/', '')

        self.s3_client.delete_object(
            Bucket=self.s3_bucket,
            Key=s3_key
        )

        return computeandstorage_pb2.DeleteReply()
    
    def RunClient():
        channel = grpc.insecure_channel('localhost:50051')
        stub = computeandstorage_pb2_grpc.EC2OperationsStub(channel)

        data = request.get_json().get('data')

        store_data_request = computeandstorage_pb2.StoreRequest(
            data=data
        )

        store_data_response = stub.StoreData(store_data_request)

        s3_uri = ""
        if store_data_response.HasField('s3uri'):
            s3_uri = store_data_response.s3uri

        s3_uri = store_data_response.s3uri
        print("S3 URL:", s3_uri)

        append_data_request = computeandstorage_pb2.AppendRequest(
            data=data
        )

        append_data_response = stub.AppendData(append_data_request)

        if append_data_response.success:
            print("AppendData request successful")
        else:
            print("AppendData request failed")

        s3_uri = request.get_json().get('s3uri')

        delete_file_request = computeandstorage_pb2.DeleteRequest(
            s3uri=s3_uri
        )

        delete_file_response = stub.DeleteFile(delete_file_request)

        if delete_file_response.success:
            print("DeleteFile request successful")
        else:
            print("DeleteFile request failed")
    

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    computeandstorage_pb2_grpc.add_EC2OperationsServicer_to_server(EC2OperationsServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    payload = {
            "banner": "B00947866",
            "ip": "44.211.151.124:50051"
        }
    response = requests.post('http://54.173.209.76:9000/start', json=payload)

    if response:
        print("POST request to Rob's application successful")
    else:
        print("POST request to Rob's application failed")
    print(response.text)
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
