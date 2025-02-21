from flask import Blueprint, request, g
from app.models import db, Order
from app.forms import OrderForm
from app.utils.auth import jwt_required

trading_routes = Blueprint('trading', __name__)

@trading_routes.route('/orders', methods=['POST'])
@jwt_required
def place_order():
    """
    Place a new trade order (protected by both JWT and CSRF)
    """
    form = OrderForm()
    
    if form.validate_on_submit():
        # Validate order type and required fields
        if form.data['type'] == 'limit' and not form.data.get('limit_price'):
            return {'error': 'Limit price required for limit orders'}, 400
            
        order = Order(
            user_id=g.user_id,
            symbol=form.data['symbol'].upper(),
            order_type=form.data['type'],
            side=form.data['side'],
            quantity=form.data['quantity'],
            limit_price=form.data.get('limit_price'),
            status='pending'
        )
        
        db.session.add(order)
        db.session.commit()
        
        return {
            'order_id': str(order.id),
            'status': order.status,
            'created_at': order.created_at.isoformat()
        }, 201
        
    return {'error': 'Invalid order data', 'details': form.errors}, 400

@trading_routes.route('/orders', methods=['GET'])
@jwt_required
def get_orders():
    """
    Get user's orders with optional filters
    """
    status = request.args.get('status')
    limit = int(request.args.get('limit', 50))
    offset = int(request.args.get('offset', 0))
    
    query = Order.query.filter_by(user_id=g.user_id)
    
    if status:
        query = query.filter_by(status=status)
        
    orders = query.order_by(Order.created_at.desc())\
                 .offset(offset)\
                 .limit(limit)\
                 .all()
                 
    return {
        'orders': [order.to_dict() for order in orders]
    } 