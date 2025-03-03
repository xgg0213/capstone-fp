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
    try:
        # Get user's portfolio
        portfolios = Portfolio.query.filter_by(user_id=current_user.id).all()
        
        if not portfolios:
            return {'portfolios': []}
            
        return {'portfolios': [portfolio.to_dict() for portfolio in portfolios]}
    except Exception as e:
        # Log the error
        print(f"Error in get_portfolio: {str(e)}")
        return {'error': 'An error occurred while fetching portfolio'}, 500

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
    try:
        data = request.get_json()
        amount = data.get('amount')
        
        if not amount:
            return {'errors': {'amount': 'Amount is required'}}, 400
            
        try:
            amount = Decimal(str(amount))
        except (ValueError, TypeError):
            return {'errors': {'amount': 'Invalid amount format'}}, 400
            
        user = User.query.get(current_user.id)
        if not user:
            return {'errors': {'user': 'User not found'}}, 404
            
        user.balance = float(Decimal(str(user.balance)) + amount)
        user.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return {'balance': user.balance}
    except Exception as e:
        db.session.rollback()
        print(f"Error in update_balance: {str(e)}")
        return {'errors': {'server': 'An error occurred'}}, 500 