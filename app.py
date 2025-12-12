import json, argparse
from flask import Flask, request, send_from_directory, jsonify
import os
import mindsdb_sdk
parser = argparse.ArgumentParser()
parser.add_argument(
    '-c', '--config-path',
    default='./config/mindsdb-config.json',
    help='Path to MindsDB config file'
)
parser.add_argument(
    '-m', '--model-config-path',
    default='./config/model-config.json',
    help='Path to model config file'
)
args = parser.parse_args()
with open(args.config_path) as f:
    mindsdb_config = json.load(f)

with open(args.model_config_path) as f:
    model_config = json.load(f)

print(f"MindsDB config loaded: {mindsdb_config}")
print(f"Model config loaded: {model_config}")

# MindsDB connection
mdb = None
def connect_to_mindsdb():
    global mdb
    try:
        mdb = mindsdb_sdk.connect(
            url=mindsdb_config['host']
        )
        print("✓ Connected to MindsDB")
    except Exception as e:
        print(f"✗ Failed to connect to MindsDB: {e}")
        exit(1)

app = Flask(__name__, static_folder='public', static_url_path='')
connect_to_mindsdb()

if __name__ == '__main__':
    app.run(port=3000, debug=True)
