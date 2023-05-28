from flask import Flask, request, jsonify
import csv

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process():
    input_data = request.get_json()

    if 'file' not in input_data or input_data['file'] is None:
        return jsonify({'file': None,
                        'error': 'Invalid JSON input.'}), 400

    file = input_data['file']

    try:
        with open("/etc/"+file, newline='') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            total_sum = 0
            for row in csv_reader:
                if row['product'] == input_data['product']:
                    total_sum += int(row['amount'])
        return jsonify({'file': file,
                        'sum': total_sum}), 200

    except FileNotFoundError:
        return jsonify({'file': file,
                        'error': 'File not found.'}), 404

    except csv.Error:
        return jsonify({'file': file,
                        'error': 'Input file not in CSV format.'}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=7001, debug=True)
