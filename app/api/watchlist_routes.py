from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import db, Watchlist, WatchlistSymbol, Symbol
from datetime import datetime

watchlist_routes = Blueprint('watchlist', __name__)

@watchlist_routes.route('/')
@login_required
def get_watchlists():
    """Get user's watchlists with symbols"""
    watchlists = Watchlist.query.filter_by(user_id=current_user.id).all()
    return {'watchlists': [watchlist.to_dict() for watchlist in watchlists]}

@watchlist_routes.route('/', methods=['POST'])
@login_required
def create_watchlist():
    """Create a new watchlist"""
    data = request.json
    
    if not data.get('name'):
        return {'error': 'Name is required'}, 400
        
    watchlist = Watchlist(
        user_id=current_user.id,
        name=data['name']
    )
    
    db.session.add(watchlist)
    db.session.commit()
    
    return watchlist.to_dict()

@watchlist_routes.route('/<int:id>/symbols', methods=['POST'])
@login_required
def add_symbol(id):
    """Add a symbol to watchlist"""
    watchlist = Watchlist.query.get(id)
    
    if not watchlist or watchlist.user_id != current_user.id:
        return {'error': 'Watchlist not found'}, 404
        
    data = request.json
    symbol = data.get('symbol', '').upper()
    if not symbol:
        return {'error': 'Symbol is required'}, 400
        
    # Check if symbol already exists in watchlist
    existing = WatchlistSymbol.query.filter_by(
        watchlist_id=id, 
        symbol=symbol
    ).first()
    
    if existing:
        return {'error': 'Symbol already in watchlist'}, 400
        
    new_symbol = WatchlistSymbol(
        watchlist_id=id,
        symbol=symbol,
        company_name=data.get('company_name'),
        current_price=data.get('current_price'),
        price_change=data.get('price_change')
    )
    
    db.session.add(new_symbol)
    db.session.commit()
    return watchlist.to_dict()

@watchlist_routes.route('/<int:id>/symbols/<symbol>', methods=['DELETE'])
@login_required
def remove_symbol(id, symbol):
    """Remove a symbol from watchlist"""
    watchlist = Watchlist.query.get(id)
    
    if not watchlist or watchlist.user_id != current_user.id:
        return {'error': 'Watchlist not found'}, 404
        
    symbol_to_remove = WatchlistSymbol.query.filter_by(
        watchlist_id=id,
        symbol=symbol.upper()
    ).first()
    
    if symbol_to_remove:
        db.session.delete(symbol_to_remove)
        db.session.commit()
        
    return watchlist.to_dict()

@watchlist_routes.route('/<symbol>', methods=['GET'])
@login_required
def check_watchlist(symbol):
    """
    Check if a symbol is in user's watchlist
    """
    watchlist_item = Watchlist.query.filter_by(
        user_id=current_user.id,
        symbol=symbol.upper()
    ).first()
    
    return jsonify({
        'isWatched': watchlist_item is not None
    })

@watchlist_routes.route('', methods=['POST'])
@login_required
def add_to_watchlist():
    """
    Add a symbol to user's watchlist
    """
    data = request.json
    symbol = data.get('symbol')
    
    if not symbol:
        return jsonify({'errors': ['Symbol is required']}), 400
        
    # Check if already in watchlist
    existing = Watchlist.query.filter_by(
        user_id=current_user.id,
        symbol=symbol.upper()
    ).first()
    
    if existing:
        return jsonify({'errors': ['Symbol already in watchlist']}), 400
        
    watchlist_item = Watchlist(
        user_id=current_user.id,
        symbol=symbol.upper()
    )
    
    db.session.add(watchlist_item)
    db.session.commit()
    
    return jsonify({
        'message': 'Added to watchlist',
        'symbol': symbol.upper()
    })

@watchlist_routes.route('/<symbol>', methods=['DELETE'])
@login_required
def remove_from_watchlist(symbol):
    """
    Remove a symbol from user's watchlist
    """
    watchlist_item = Watchlist.query.filter_by(
        user_id=current_user.id,
        symbol=symbol.upper()
    ).first()
    
    if not watchlist_item:
        return jsonify({'errors': ['Symbol not in watchlist']}), 404
        
    db.session.delete(watchlist_item)
    db.session.commit()
    
    return jsonify({
        'message': 'Removed from watchlist',
        'symbol': symbol.upper()
    })

@watchlist_routes.route('/<symbol>/check', methods=['GET'])
@login_required
def check_watchlist_status(symbol):
    """
    Check if a symbol is in any of the user's watchlists
    """
    try:
        symbol_obj = Symbol.query.filter_by(symbol=symbol.upper()).first()
        if not symbol_obj:
            return jsonify({'isWatched': False})

        # Check if symbol exists in any of user's watchlists
        exists = WatchlistSymbol.query.join(Watchlist).filter(
            Watchlist.user_id == current_user.id,
            WatchlistSymbol.symbol_id == symbol_obj.id
        ).first()
        
        return jsonify({'isWatched': exists is not None})
    except Exception as e:
        return jsonify({'error': str(e)}), 500 