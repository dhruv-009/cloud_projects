from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)
#container1 functions and routes.

# @app.before_first_request
# def start():
#     banner = "B00947866"
#     ip = "172.10.20.2"

#     professor_app_url = 'https://fmdyn90ov7.execute-api.us-east-1.amazonaws.com/default/start'
#     payload = {'banner': banner, 'ip': ip}
#     response = requests.post(professor_app_url, json=payload)

#     return response.json(), response.status_code

@app.route('/store-file', methods=['POST'])
def store_file():
    input_data = request.get_json()

    if 'file' not in input_data or 'data' not in input_data:
        return jsonify({'file': None, 'error': 'Invalid JSON input.'}), 400

    file = input_data['file']
    data = input_data['data']

    try:
        with open("/etc/" + file, 'w') as f:
            lines = data.split('\n')
            for line in lines:
                if line.endswith('\\n'):
                    line = line[-1:]
                f.write(line)
                f.write('\n')

        return jsonify({'file': file, 'message': 'Success.'}), 200

    except Exception as e:
        return jsonify({'file': file, 'error': 'Error while storing the file to the storage.'}), 500

@app.route('/calculate', methods=['POST'])
def calculate():
    input_data = request.get_json()

    if 'file' not in input_data or input_data['file'] is None:
        return jsonify({'file': None,
                        'error': 'Invalid JSON input.'}), 400

    file = input_data['file']
    if not os.path.isfile(os.path.join("/etc", file)):
        return jsonify({'file': file,
                        'error': 'File not found.'}), 404

    container2_url = 'http://container2-service.default.svc.cluster.local:80/process'
    payload = {'file': file, 'product': input_data['product']}
    response = requests.post(container2_url, json=payload)

    return response.json(), response.status_code

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
