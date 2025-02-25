from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import db, Portfolio, Transaction, User
from datetime import datetime
from decimal import Decimal

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

@portfolio_routes.route('', methods=['POST'])
@login_required
def update_balance():
    """
    Update user's balance
    """
    data = request.get_json()
    
    if 'amount' not in data:
        return {'errors': {'amount': 'Amount is required'}}, 400
        
    try:
        amount = Decimal(str(data['amount']))
        if amount <= 0:
            return {'errors': {'amount': 'Amount must be positive'}}, 400
            
        user = User.query.get(current_user.id)
        user.balance = user.balance + amount
        
        db.session.commit()
        return {'balance': float(user.balance)}
        
    except (ValueError, TypeError):
        return {'errors': {'amount': 'Invalid amount format'}}, 400
    except Exception as e:
        db.session.rollback()
        return {'errors': {'server': 'An error occurred'}}, 500 