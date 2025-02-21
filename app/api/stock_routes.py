from flask import Blueprint, request, jsonify
from app.utils.auth import jwt_required
from app.services.market_data_service import market_data_service
from flask import current_app
from datetime import datetime

stock_routes = Blueprint('stocks', __name__)

@stock_routes.route('/prices', methods=['GET'])
@jwt_required
def get_prices():
    """
    Get current prices for requested symbols
    """
    symbols = request.args.get('symbols', '').split(',')
    symbols = [s.strip().upper() for s in symbols if s.strip()]
    
    prices = {}
    for symbol in symbols:
        price_data = market_data_service.get_current_price(symbol)
        if price_data:
            prices[symbol] = price_data
            
    return jsonify(prices)

@stock_routes.route('/<symbol>/history', methods=['GET'])
@jwt_required
async def get_history(symbol):
    """Get historical price data for a symbol"""
    timeframe = request.args.get('timeframe', '1D')
    limit = int(request.args.get('limit', 100))
    
    data = await market_data_service.get_historical_data(
        symbol.upper(),
        timeframe=timeframe,
        limit=limit
    )
    
    return jsonify({
        'symbol': symbol.upper(),
        'timeframe': timeframe,
        'data': data
    })

@stock_routes.route('/subscribe', methods=['POST'])
@jwt_required
async def subscribe_symbol():
    """Add a new symbol to track"""
    symbol = request.json.get('symbol', '').upper()
    if not symbol:
        return {'error': 'Symbol is required'}, 400
        
    await market_data_service.add_symbol(symbol)
    return {'message': f'Successfully subscribed to {symbol}'}, 200

@stock_routes.route('/market-status')
def get_market_status():
    """Get current market status"""
    is_open = market_data_service.is_market_open()
    next_open = None
    
    if not is_open:
        clock = market_data_service.trading_client.get_clock()
        next_open = clock.next_open.isoformat()
        
    return jsonify({
        'is_open': is_open,
        'next_open': next_open,
        'server_time': datetime.now().isoformat()
    })

@stock_routes.route('/<symbol>/last-price')
def get_last_price(symbol):
    """Get last available price"""
    return jsonify(market_data_service.get_last_closing_price(symbol)) 