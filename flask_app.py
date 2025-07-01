import os
from flask import Flask, jsonify
import json

app = Flask(__name__)

# Determine absolute path to the folder where app.py is
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'data.json')

@app.route('/api')
def get_data():
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error": "Data file not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Data file is not valid JSON"}), 500

if __name__ == '__main__':
    app.run(debug=True)
