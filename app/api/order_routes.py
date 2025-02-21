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