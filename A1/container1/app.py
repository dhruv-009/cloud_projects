from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

@app.route('/calculate', methods=['POST'])
def calculate():
    input_data = request.get_json()

    if 'file' not in input_data or input_data['file'] is None:
        return jsonify({'file': None,
                        'error': 'Invalid JSON input.'}), 400

    file = input_data['file']
    print("abc")
    print(file)
    if not os.path.isfile("/etc/" + file):
        return jsonify({'file': file,
                        'error': 'File not found'}), 404

    container2_url = 'http://container2:7001/process'
    payload = {'file': file, 'product': input_data['product']}
    response = requests.post(container2_url, json=payload)

    return response.json(), response.status_code

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=6000, debug=True)