from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import db, Transaction, Symbol
from datetime import datetime

transaction_routes = Blueprint('transactions', __name__)

@transaction_routes.route('/')
@login_required
def get_transactions():
    """Get user's transaction history"""
    symbol_str = request.args.get('symbol')
    type_filter = request.args.get('type')  # buy or sell
    
    query = Transaction.query.filter_by(user_id=current_user.id)
    
    if symbol_str:
        # Find the symbol ID first
        symbol = Symbol.query.filter_by(symbol=symbol_str.upper()).first()
        if symbol:
            query = query.filter_by(symbol_id=symbol.id)
        else:
            # If symbol doesn't exist, return empty result
            return {'transactions': []}
            
    if type_filter:
        query = query.filter_by(type=type_filter.lower())
        
    transactions = query.order_by(Transaction.created_at.desc()).all()
    return {'transactions': [txn.to_dict() for txn in transactions]}

@transaction_routes.route('/stats')
@login_required
def get_transaction_stats():
    """Get transaction statistics"""
    symbol_str = request.args.get('symbol')
    if not symbol_str:
        return {'error': 'Symbol is required'}, 400
    
    # Find the symbol ID first
    symbol = Symbol.query.filter_by(symbol=symbol_str.upper()).first()
    if not symbol:
        return {'error': 'Symbol not found'}, 404
        
    transactions = Transaction.query.filter_by(
        user_id=current_user.id,
        symbol_id=symbol.id
    ).all()
    
    total_bought = sum(t.shares for t in transactions if t.type == 'buy')
    total_sold = sum(t.shares for t in transactions if t.type == 'sell')
    
    buy_amount = sum(t.shares * t.price for t in transactions if t.type == 'buy')
    sell_amount = sum(t.shares * t.price for t in transactions if t.type == 'sell')
    
    return {
        'symbol': symbol.symbol,
        'total_bought': float(total_bought),
        'total_sold': float(total_sold),
        'current_position': float(total_bought - total_sold),
        'average_buy_price': float(buy_amount / total_bought) if total_bought > 0 else 0,
        'average_sell_price': float(sell_amount / total_sold) if total_sold > 0 else 0,
        'realized_pl': float(sell_amount - (total_sold * (buy_amount / total_bought))) if total_bought > 0 else 0
    } 