from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import db, Watchlist
from datetime import datetime

watchlist_routes = Blueprint('watchlists', __name__)

@watchlist_routes.route('/')
@login_required
def get_watchlists():
    """Get user's watchlists"""
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
        name=data['name'],
        symbols=','.join(data.get('symbols', []))
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
        
    symbol = request.json.get('symbol', '').upper()
    if not symbol:
        return {'error': 'Symbol is required'}, 400
        
    current_symbols = set(watchlist.symbols.split(',') if watchlist.symbols else [])
    current_symbols.add(symbol)
    watchlist.symbols = ','.join(current_symbols)
    
    db.session.commit()
    return watchlist.to_dict()

@watchlist_routes.route('/<int:id>/symbols/<symbol>', methods=['DELETE'])
@login_required
def remove_symbol(id, symbol):
    """Remove a symbol from watchlist"""
    watchlist = Watchlist.query.get(id)
    
    if not watchlist or watchlist.user_id != current_user.id:
        return {'error': 'Watchlist not found'}, 404
        
    current_symbols = set(watchlist.symbols.split(',') if watchlist.symbols else [])
    current_symbols.discard(symbol.upper())
    watchlist.symbols = ','.join(current_symbols)
    
    db.session.commit()
    return watchlist.to_dict() 