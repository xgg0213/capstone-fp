from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import db, Order, Transaction, Portfolio, User
from datetime import datetime

order_routes = Blueprint('orders', __name__)

@order_routes.route('/', methods=['POST'])
@login_required
def place_order():
    """Place a new order"""
    data = request.json
    
    # Validate order data
    required_fields = ['symbol', 'order_type', 'side', 'shares']
    if not all(field in data for field in required_fields):
        return {'error': 'Missing required fields'}, 400
        
    # Create new order
    order = Order(
        user_id=current_user.id,
        symbol=data['symbol'].upper(),
        order_type=data['order_type'],
        side=data['side'],
        shares=float(data['shares']),
        price=data.get('price'),
        status='pending'
    )
    
    db.session.add(order)
    db.session.commit()
    
    return order.to_dict()

@order_routes.route('/')
@login_required
def get_orders():
    """Get user's orders"""
    status = request.args.get('status')
    
    query = Order.query.filter_by(user_id=current_user.id)
    if status:
        query = query.filter_by(status=status)
        
    orders = query.order_by(Order.created_at.desc()).all()
    return {'orders': [order.to_dict() for order in orders]}

@order_routes.route('/<int:id>/cancel', methods=['POST'])
@login_required
def cancel_order(id):
    """Cancel a pending order"""
    order = Order.query.get(id)
    
    if not order or order.user_id != current_user.id:
        return {'error': 'Order not found'}, 404
        
    if order.status != 'pending':
        return {'error': 'Can only cancel pending orders'}, 400
        
    order.status = 'cancelled'
    db.session.commit()
    
    return order.to_dict()

@order_routes.route('/<int:order_id>/process', methods=['POST'])
@login_required
def process_order(order_id):
    """
    Process a pending order (Demo version)
    """
    order = Order.query.get(order_id)
    
    if not order:
        return {'errors': ['Order not found']}, 404
        
    if order.user_id != current_user.id:
        return {'errors': ['Unauthorized']}, 403
        
    if order.status != 'pending':
        return {'errors': ['Order is not pending']}, 400
    
    # For demo: use order price or default price
    market_price = order.price or 100.00
    
    # Update order status
    order.status = 'filled'
    order.filled_price = market_price
    order.filled_at = datetime.utcnow()
    
    # Update portfolio
    portfolio = Portfolio.query.filter_by(
        user_id=current_user.id,
        symbol=order.symbol
    ).first()
    
    if not portfolio:
        portfolio = Portfolio(
            user_id=current_user.id,
            symbol=order.symbol,
            shares=0
        )
        db.session.add(portfolio)
    
    # Update shares based on buy/sell
    if order.side == 'buy':
        portfolio.shares += order.shares
    else:  # sell
        portfolio.shares -= order.shares
    
    # Create transaction record
    transaction = Transaction(
        user_id=current_user.id,
        order_id=order.id,
        symbol=order.symbol,
        shares=order.shares,
        price=market_price,
        type=order.side
    )
    
    db.session.add(transaction)
    db.session.commit()
    
    return order.to_dict() 