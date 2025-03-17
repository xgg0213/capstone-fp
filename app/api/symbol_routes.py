from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.models import db, Symbol, SymbolPrice
from datetime import datetime

symbol_routes = Blueprint('symbols', __name__)

@symbol_routes.route('/')
@login_required
def get_symbols():
    symbols = Symbol.query.all()
    return jsonify({'symbols': [symbol.to_dict() for symbol in symbols]})

@symbol_routes.route('/<symbol>')
@login_required
def get_symbol(symbol):
    symbol_data = Symbol.query.filter(Symbol.symbol == symbol.upper()).first()
    if not symbol_data:
        return {'error': 'Symbol not found'}, 404
    return symbol_data.to_dict()

@symbol_routes.route('/', methods=['POST'])
@login_required
def create_symbol():
    data = request.json
    
    symbol = Symbol(
        symbol=data['symbol'].upper(),
        company_name=data.get('company_name'),
        current_price=data['current_price'],
        daily_high=data.get('daily_high'),
        daily_low=data.get('daily_low'),
        daily_volume=data.get('daily_volume'),
        price_change_pct=data.get('price_change_pct')
    )
    
    db.session.add(symbol)
    db.session.commit()
    
    return symbol.to_dict()

@symbol_routes.route('/<int:id>', methods=['PUT'])
@login_required
def update_symbol(id):
    symbol = Symbol.query.get(id)
    if not symbol:
        return {'error': 'Symbol not found'}, 404

    data = request.json
    
    if 'current_price' in data:
        symbol.current_price = data['current_price']
    if 'daily_high' in data:
        symbol.daily_high = data['daily_high']
    if 'daily_low' in data:
        symbol.daily_low = data['daily_low']
    if 'daily_volume' in data:
        symbol.daily_volume = data['daily_volume']
    if 'price_change_pct' in data:
        symbol.price_change_pct = data['price_change_pct']
    
    symbol.last_updated = datetime.utcnow()
    db.session.commit()
    
    return symbol.to_dict()

@symbol_routes.route('/<symbol>/prices')
@login_required
def get_symbol_prices(symbol):
    symbol_data = Symbol.query.filter(Symbol.symbol == symbol.upper()).first()
    if not symbol_data:
        return {'error': 'Symbol not found'}, 404
    
    return {'prices': [price.to_dict() for price in symbol_data.price_history]}

@symbol_routes.route('/<symbol>/prices', methods=['POST'])
@login_required
def add_symbol_price(symbol):
    symbol_data = Symbol.query.filter(Symbol.symbol == symbol.upper()).first()
    if not symbol_data:
        return {'error': 'Symbol not found'}, 404

    data = request.json
    
    # Check if price already exists for this date
    existing_price = SymbolPrice.query.filter_by(
        symbol_id=symbol_data.id,
        date=datetime.strptime(data['date'], '%Y-%m-%d').date()
    ).first()

    if existing_price:
        return {'error': 'Price already exists for this date'}, 400

    new_price = SymbolPrice(
        symbol_id=symbol_data.id,
        date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
        open_price=data['open'],
        close_price=data['close'],
        high_price=data['high'],
        low_price=data['low'],
        volume=data.get('volume')
    )

    db.session.add(new_price)
    db.session.commit()

    # Update current price in symbols table
    symbol_data.current_price = new_price.close_price
    symbol_data.daily_high = new_price.high_price
    symbol_data.daily_low = new_price.low_price
    symbol_data.daily_volume = new_price.volume
    symbol_data.last_updated = datetime.utcnow()
    db.session.commit()

    return new_price.to_dict()

@symbol_routes.route('/update-prices', methods=['POST'])
@login_required
def update_symbol_prices():
    """Update current prices for all symbols or specified symbols"""
    data = request.json
    symbols = data.get('symbols', [])  # Optional list of symbols to update
    
    if symbols:
        query = Symbol.query.filter(Symbol.symbol.in_([s.upper() for s in symbols]))
    else:
        query = Symbol.query.all()
    
    updated = []
    for symbol in query:
        symbol.update_current_price()
        updated.append(symbol.to_dict())
    
    return {'symbols': updated}

@symbol_routes.route('/<symbol>/prices/latest', methods=['POST'])
@login_required
def add_latest_price(symbol):
    """Add latest price and update symbol's current price"""
    symbol_data = Symbol.query.filter(Symbol.symbol == symbol.upper()).first()
    if not symbol_data:
        return {'error': 'Symbol not found'}, 404

    data = request.json
    today = datetime.now().date()
    
    # Create or update today's price
    existing_price = SymbolPrice.query.filter_by(
        symbol_id=symbol_data.id,
        date=today
    ).first()

    if existing_price:
        # Update existing price
        existing_price.close_price = data['close']
        existing_price.high_price = max(existing_price.high_price, data['high'])
        existing_price.low_price = min(existing_price.low_price, data['low'])
        existing_price.volume = data.get('volume', existing_price.volume)
        price = existing_price
    else:
        # Create new price
        price = SymbolPrice(
            symbol_id=symbol_data.id,
            date=today,
            open_price=data['open'],
            close_price=data['close'],
            high_price=data['high'],
            low_price=data['low'],
            volume=data.get('volume')
        )
        db.session.add(price)
    
    db.session.commit()
    
    # Update symbol's current price
    symbol_data.update_current_price()
    
    return price.to_dict()

def get_or_create_price(session, model, defaults=None, **kwargs):
    """Helper function to get or create a price record"""
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        params = dict((k, v) for k, v in kwargs.items())
        params.update(defaults or {})
        instance = model(**params)
        session.add(instance)
        return instance, True 