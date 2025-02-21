from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import db, Transaction
from datetime import datetime

transaction_routes = Blueprint('transactions', __name__)

@transaction_routes.route('/')
@login_required
def get_transactions():
    """Get user's transaction history"""
    symbol = request.args.get('symbol')
    type = request.args.get('type')  # buy or sell
    
    query = Transaction.query.filter_by(user_id=current_user.id)
    
    if symbol:
        query = query.filter_by(symbol=symbol.upper())
    if type:
        query = query.filter_by(type=type.lower())
        
    transactions = query.order_by(Transaction.created_at.desc()).all()
    return {'transactions': [txn.to_dict() for txn in transactions]}

@transaction_routes.route('/stats')
@login_required
def get_transaction_stats():
    """Get transaction statistics"""
    symbol = request.args.get('symbol')
    if not symbol:
        return {'error': 'Symbol is required'}, 400
        
    symbol = symbol.upper()
    transactions = Transaction.query.filter_by(
        user_id=current_user.id,
        symbol=symbol
    ).all()
    
    total_bought = sum(t.shares for t in transactions if t.type == 'buy')
    total_sold = sum(t.shares for t in transactions if t.type == 'sell')
    
    buy_amount = sum(t.shares * t.price for t in transactions if t.type == 'buy')
    sell_amount = sum(t.shares * t.price for t in transactions if t.type == 'sell')
    
    return {
        'symbol': symbol,
        'total_bought': float(total_bought),
        'total_sold': float(total_sold),
        'current_position': float(total_bought - total_sold),
        'average_buy_price': float(buy_amount / total_bought) if total_bought > 0 else 0,
        'average_sell_price': float(sell_amount / total_sold) if total_sold > 0 else 0,
        'realized_pl': float(sell_amount - (total_sold * (buy_amount / total_bought))) if total_bought > 0 else 0
    } 