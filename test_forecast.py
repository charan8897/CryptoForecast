import json
import mindsdb_sdk
from handlers.forecast_handler import get_or_create_recent_trade_data_view, forecast_next_symbol_prices

# Load config
with open('./config/mindsdb-config.json') as f:
    config = json.load(f)

with open('./config/model-config.json') as f:
    model_config = json.load(f)

# Connect
mdb = mindsdb_sdk.connect(url=config['host'])
print("✓ Connected to MindsDB")

# Test function 1
view_name = get_or_create_recent_trade_data_view(mdb, "btcusdt")
print(f"View name: {view_name}")

# Test function 2
model_name = model_config['btcusdt']
print(f"Model name: {model_name}")
predictions = forecast_next_symbol_prices(mdb, "btcusdt", model_name, limit=5)
print(f"Predictions: {predictions}")
