def get_or_create_recent_trade_data_view(mdb, symbol):
    """Create or get recent trade data view"""
    view_name = f"recent_{symbol}_view"
    views = mdb.views.list()
    
    if any(v.name == view_name for v in views):
        return view_name
    
    view_select = f"SELECT * FROM my_binance.aggregated_trade_data WHERE symbol = '{symbol.upper()}'"
    mdb.views.create(view_name, view_select)
    return view_name

def forecast_next_symbol_prices(mdb, symbol, model_name, limit=10):
    """Get price predictions from ML model"""
    view_name = get_or_create_recent_trade_data_view(mdb, symbol)
    predict_query = f"SELECT m.* FROM {view_name} AS t JOIN mindsdb.{model_name} AS m WHERE m.open_time > LATEST LIMIT {limit}"
    response = mdb.query(predict_query).fetch()
    try:
        return response.to_dict('records')
    except:
        return []