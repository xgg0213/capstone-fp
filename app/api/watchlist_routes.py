from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import db, Watchlist, WatchlistSymbol, Symbol
from datetime import datetime

watchlist_routes = Blueprint('watchlist', __name__)

@watchlist_routes.route('/')
@login_required
def get_watchlists():
    """Get user's watchlists with symbols"""
    try:
        # Get all watchlists for the current user
        watchlists = Watchlist.query.filter_by(user_id=current_user.id).all()
        
        # Format the response
        return jsonify({
            'watchlists': [watchlist.to_dict() for watchlist in watchlists]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@watchlist_routes.route('/', methods=['POST'])
@login_required
def create_watchlist():
    """Create a new watchlist"""
    data = request.json
    
    if not data.get('name'):
        return jsonify({'error': 'Name is required'}), 400
        
    try:
        watchlist = Watchlist(
            user_id=current_user.id,
            name=data['name']
        )
        
        db.session.add(watchlist)
        db.session.commit()
        
        return jsonify(watchlist.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@watchlist_routes.route('/<int:id>/symbols', methods=['POST'])
@login_required
def add_symbol_to_watchlist(id):
    """Add a symbol to watchlist"""
    watchlist = Watchlist.query.get(id)
    
    if not watchlist or watchlist.user_id != current_user.id:
        return jsonify({'error': 'Watchlist not found'}), 404
        
    data = request.json
    symbol_str = data.get('symbol', '').upper()
    
    if not symbol_str:
        return jsonify({'error': 'Symbol is required'}), 400
        
    try:
        # Get the symbol from the database
        symbol = Symbol.query.filter_by(symbol=symbol_str).first()
        if not symbol:
            return jsonify({'error': 'Symbol not found'}), 404
            
        # Check if symbol already exists in watchlist
        existing = WatchlistSymbol.query.filter_by(
            watchlist_id=id,
            symbol_id=symbol.id
        ).first()
        
        if existing:
            return jsonify({'error': 'Symbol already in watchlist'}), 400
            
        # Add new symbol to watchlist
        watchlist_symbol = WatchlistSymbol(
            watchlist_id=id,
            symbol_id=symbol.id
        )
        
        db.session.add(watchlist_symbol)
        db.session.commit()
        
        return jsonify(watchlist.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@watchlist_routes.route('/<int:id>/symbols/<symbol>', methods=['DELETE'])
@login_required
def remove_symbol(id, symbol):
    """Remove a symbol from watchlist"""
    try:
        watchlist = Watchlist.query.get(id)
        
        if not watchlist or watchlist.user_id != current_user.id:
            return {'error': 'Watchlist not found'}, 404
            
        # First, find the Symbol object by its symbol string
        symbol_obj = Symbol.query.filter_by(symbol=symbol.upper()).first()
        
        if not symbol_obj:
            return {'error': 'Symbol not found'}, 404
            
        # Then find the WatchlistSymbol entry using watchlist_id and symbol_id
        symbol_to_remove = WatchlistSymbol.query.filter_by(
            watchlist_id=id,
            symbol_id=symbol_obj.id
        ).first()
        
        if not symbol_to_remove:
            return {'error': 'Symbol not in watchlist'}, 404
            
        db.session.delete(symbol_to_remove)
        db.session.commit()
            
        return watchlist.to_dict()
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500

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
    Add a symbol to user's default watchlist or create one if it doesn't exist
    """
    data = request.json
    symbol_str = data.get('symbol')
    
    if not symbol_str:
        return jsonify({'errors': ['Symbol is required']}), 400
    
    symbol_str = symbol_str.upper()
    
    try:
        # Get the symbol from the database
        symbol = Symbol.query.filter_by(symbol=symbol_str).first()
        if not symbol:
            return jsonify({'errors': ['Symbol not found']}), 404
        
        # Get or create default watchlist
        default_watchlist = Watchlist.query.filter_by(
            user_id=current_user.id,
            name='Default'
        ).first()
        
        if not default_watchlist:
            default_watchlist = Watchlist(
                user_id=current_user.id,
                name='Default'
            )
            db.session.add(default_watchlist)
            db.session.commit()
        
        # Check if symbol already exists in watchlist
        existing = WatchlistSymbol.query.filter_by(
            watchlist_id=default_watchlist.id,
            symbol_id=symbol.id
        ).first()
        
        if existing:
            return jsonify({'message': 'Symbol already in watchlist'}), 200
        
        # Add new symbol to watchlist
        watchlist_symbol = WatchlistSymbol(
            watchlist_id=default_watchlist.id,
            symbol_id=symbol.id
        )
        
        db.session.add(watchlist_symbol)
        db.session.commit()
        
        return jsonify({
            'message': 'Added to watchlist',
            'symbol': symbol_str,
            'watchlist': default_watchlist.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        print(f"Error adding to watchlist: {str(e)}")
        return jsonify({'errors': [str(e)]}), 500

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

@watchlist_routes.route('/<int:id>', methods=['PUT'])
@login_required
def update_watchlist(id):
    """Update watchlist name"""
    try:
        watchlist = Watchlist.query.get(id)
        
        if not watchlist or watchlist.user_id != current_user.id:
            return jsonify({'errors': ['Watchlist not found']}), 404
            
        data = request.json
        if not data or 'name' not in data:
            return jsonify({'errors': ['Name is required']}), 400
            
        name = data['name'].strip()
        if not name:
            return jsonify({'errors': ['Name cannot be empty']}), 400
            
        # Check if another watchlist with this name exists for the user
        existing_watchlist = Watchlist.query.filter(
            Watchlist.user_id == current_user.id,
            Watchlist.name == name,
            Watchlist.id != id
        ).first()
        
        if existing_watchlist:
            return jsonify({'errors': ['A watchlist with this name already exists']}), 400
            
        watchlist.name = name
        watchlist.updated_at = db.func.now()
        
        db.session.commit()
        return jsonify(watchlist.to_dict())
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'errors': [str(e)]}), 500

@watchlist_routes.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_watchlist(id):
    """Delete a watchlist"""
    try:
        watchlist = Watchlist.query.get(id)
        
        if not watchlist or watchlist.user_id != current_user.id:
            return jsonify({'errors': ['Watchlist not found']}), 404
            
        db.session.delete(watchlist)
        db.session.commit()
        
        return jsonify({'message': 'Watchlist deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'errors': [str(e)]}), 500 