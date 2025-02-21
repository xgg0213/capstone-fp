from flask import Blueprint, request
from app.models import Transaction, Order, Portfolio
from app.utils.auth import jwt_required
from sqlalchemy import desc

transaction_routes = Blueprint('transactions', __name__)

@transaction_routes.route('/', methods=['GET'])
@jwt_required
def get_transactions():
    """
    Get user's transaction history
    """
    # Get query parameters
    symbol = request.args.get('symbol')
    type = request.args.get('type')  # buy or sell
    limit = int(request.args.get('limit', 50))
    offset = int(request.args.get('offset', 0))
    
    # Build query
    query = Transaction.query.filter_by(user_id=g.user_id)
    
    if symbol:
        query = query.filter_by(symbol=symbol.upper())
    if type:
        query = query.filter_by(type=type.lower())
        
    # Get transactions
    transactions = query.order_by(desc(Transaction.timestamp))\
                       .offset(offset)\
                       .limit(limit)\
                       .all()
                       
    return {
        'transactions': [txn.to_dict() for txn in transactions]
    }

@transaction_routes.route('/stats', methods=['GET'])
@jwt_required
def get_transaction_stats():
    """
    Get transaction statistics for a symbol
    """
    symbol = request.args.get('symbol')
    if not symbol:
        return {'error': 'Symbol is required'}, 400
        
    symbol = symbol.upper()
    
    # Get all transactions for this symbol
    transactions = Transaction.query.filter_by(
        user_id=g.user_id,
        symbol=symbol
    ).all()
    
    # Calculate statistics
    total_bought = sum(t.quantity for t in transactions if t.type == 'buy')
    total_sold = sum(t.quantity for t in transactions if t.type == 'sell')
    current_position = total_bought - total_sold
    
    total_buy_amount = sum(t.total_amount for t in transactions if t.type == 'buy')
    total_sell_amount = sum(t.total_amount for t in transactions if t.type == 'sell')
    
    # Calculate average prices
    avg_buy_price = total_buy_amount / total_bought if total_bought > 0 else 0
    avg_sell_price = total_sell_amount / total_sold if total_sold > 0 else 0
    
    return {
        'symbol': symbol,
        'total_bought': float(total_bought),
        'total_sold': float(total_sold),
        'current_position': float(current_position),
        'average_buy_price': float(avg_buy_price),
        'average_sell_price': float(avg_sell_price),
        'total_buy_amount': float(total_buy_amount),
        'total_sell_amount': float(total_sell_amount)
    } 