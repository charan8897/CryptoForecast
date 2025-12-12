import json, argparse
from flask import Flask, request, send_from_directory, jsonify
import os
import mindsdb_sdk
from handlers.trade_data_handler import get_latest_aggregated_trade_data
from handlers.forecast_handler import forecast_next_symbol_prices

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
app = Flask(__name__, static_folder='public', static_url_path='')

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

connect_to_mindsdb()

# @app.route('/test')
# def test():
#     return jsonify({"status": "ok"})

@app.route('/trade-data/<symbol_id>')
def trade_data(symbol_id):
    limit = request.args.get('limit', 1000, type=int)
    if limit > 10000:
        return jsonify({"error": f"Limit {limit} exceeds max of 10000"}), 400
    
    data = get_latest_aggregated_trade_data(mdb, symbol_id, limit)
    return jsonify(data)

@app.route('/forecast/<symbol_id>')
def forecast(symbol_id):
    if symbol_id not in model_config:
        return jsonify({"error": f"Unsupported symbol {symbol_id}. No model available."}), 400
    
    model_name = model_config[symbol_id]
    predictions = forecast_next_symbol_prices(mdb, symbol_id, model_name)
    return jsonify(predictions)

if __name__ == '__main__':
    app.run(port=3000, debug=False)