import os
import json
import logging
from pathlib import Path
from datetime import datetime
from flask_cors import CORS
from flask import Flask, jsonify, send_from_directory

logging.basicConfig(level=logging.INFO)
logger= logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

DIRECTORY = f"../portfolios"
today_date = datetime.now().strftime('%Y%m%d')

@app.route('/portfolioFiles', methods=['GET'])
def list_json_files():
    combined_portf_object = {}
    for file in os.listdir(DIRECTORY):
        if today_date in file:
            f = open(f'{DIRECTORY}/{file}','r')
            data = json.load(f)
            combined_portf_object[file] = data
    return combined_portf_object

# @app.route('/json-files/<filename>', methods=['GET'])
# def get_json_file(filename):
#     return send_from_directory(DIRECTORY, filename)

if __name__ == '__main__':
    app.run(port=3000, debug=True)
