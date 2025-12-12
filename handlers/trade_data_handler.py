def get_latest_aggregated_trade_data(mdb, symbol, limit=1000):
    """Fetch trade data from MindsDB Binance integration"""
    binance_query = f"SELECT * FROM my_binance.aggregated_trade_data WHERE symbol='{symbol.upper()}' LIMIT {limit}"
    response = mdb.query(binance_query).fetch()
    try:
        return response.to_dict('records')
    except:
        return []