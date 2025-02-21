from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import db, Portfolio, Transaction
from datetime import datetime

portfolio_routes = Blueprint('portfolio', __name__)

@portfolio_routes.route('/')
@login_required
def get_portfolio():
    """Get user's portfolio positions"""
    positions = Portfolio.query.filter_by(user_id=current_user.id).all()
    return {'positions': [position.to_dict() for position in positions]}

@portfolio_routes.route('/history')
@login_required
def get_portfolio_history():
    """Get portfolio value history"""
    transactions = Transaction.query.filter_by(user_id=current_user.id)\
                                 .order_by(Transaction.created_at).all()
    
    # Calculate cumulative portfolio value over time
    history = []
    portfolio_value = 0
    
    for txn in transactions:
        if txn.type == 'buy':
            portfolio_value += txn.shares * txn.price
        else:
            portfolio_value -= txn.shares * txn.price
            
        history.append({
            'timestamp': txn.created_at.isoformat(),
            'value': portfolio_value
        })
    
    return {'history': history} 