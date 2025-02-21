from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import User, Portfolio, Transaction
from datetime import datetime

user_routes = Blueprint('account', __name__)

@user_routes.route('/')
@login_required
def get_account():
    """
    Get current user's account overview
    """
    portfolio = Portfolio.query.filter_by(user_id=current_user.id).first()
    
    return {
        'account_id': str(current_user.id),
        'buying_power': float(portfolio.buying_power),
        'cash_balance': float(portfolio.cash_balance),
        'portfolio_value': float(portfolio.total_value),
        'total_return': float(portfolio.total_return),
        'total_return_percentage': float(portfolio.return_percentage)
    }

@user_routes.route('/history')
@login_required
def get_account_history():
    """
    Get account's portfolio value history
    """
    interval = request.args.get('interval', '1D')
    
    # You'll need to implement the logic to get historical data
    # based on the interval parameter
    history = get_account_history(current_user.id, interval)
    
    return {
        'data_points': [{
            'timestamp': point.timestamp.isoformat(),
            'portfolio_value': float(point.value)
        } for point in history]
    }
