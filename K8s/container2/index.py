from flask import Flask, request, jsonify
import os
import csv

app = Flask(__name__)
#container2 functions.
@app.route('/process', methods=['POST'])
def process():
    input_data = request.get_json()

    if 'file' not in input_data or input_data['file'] is None:
        return jsonify({'file': None, 'error': 'Invalid JSON input.'}), 400

    file = input_data['file']
    total_sum = 0

    try:
        with open(os.path.join("/etc", file), 'r') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            lines = csvfile.readlines()
            if 'product' not in lines[0] or 'amount' not in lines[0]:
                return jsonify({'file': file, 'error': 'Input file not in CSV format.'}), 500
            lines = lines[1:]

            for line in lines:
                l = line.strip().split(",")
                if l[0].strip().lower() == input_data['product'].strip().lower():
                    total_sum = total_sum + int(l[-1])

        response = {'file': file, 'sum': str(total_sum)}
        return jsonify(response), 200

    except FileNotFoundError:
        response = {'file': file, 'error': 'File not found.'}
        return jsonify(response), 404

    except csv.Error:
        response = {'file': file, 'error': 'Input file not in CSV format.'}
        return jsonify(response), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=7001, debug=True)
