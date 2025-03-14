from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import db, Order, Transaction, Portfolio, User, Symbol
from datetime import datetime

order_routes = Blueprint('orders', __name__)

@order_routes.route('/', methods=['POST'])
@login_required
def place_order():
    """Place a new order"""
    try:
        data = request.json
        
        # Validate order data
        required_fields = ['symbol', 'shares', 'type']
        if not all(field in data for field in required_fields):
            return {'error': 'Missing required fields'}, 400
        
        # Find the symbol in the database
        symbol_obj = Symbol.query.filter_by(symbol=data['symbol'].upper()).first()
        if not symbol_obj:
            return {'error': f"Symbol {data['symbol']} not found"}, 404
        
        # Check if user has enough balance for buy orders
        if data['type'] == 'buy':
            user = User.query.get(current_user.id)
            order_total = float(data['shares']) * (data.get('price') or symbol_obj.current_price)
            if order_total > user.balance:
                return {'error': 'Insufficient funds'}, 400
        
        # Create new order
        order = Order(
            user_id=current_user.id,
            symbol_id=symbol_obj.id,
            shares=float(data['shares']),
            type=data['type'],
            status='pending'
        )
        
        db.session.add(order)
        db.session.commit()
        
        # Process the order immediately for demo purposes
        result = process_order_internal(order.id)
        if isinstance(result, tuple):
            return result
        
        return result.to_dict()
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500

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
    """Process a pending order (Demo version)"""
    result = process_order_internal(order_id)
    if isinstance(result, tuple):
        return result
    return result.to_dict()

def process_order_internal(order_id):
    """Internal function to process an order"""
    try:
        order = Order.query.get(order_id)
        
        if not order:
            return {'errors': ['Order not found']}, 404
            
        if order.user_id != current_user.id:
            return {'errors': ['Unauthorized']}, 403
            
        if order.status != 'pending':
            return {'errors': ['Order is not pending']}, 400
        
        # Get the symbol object
        symbol_obj = Symbol.query.get(order.symbol_id)
        if not symbol_obj:
            return {'errors': ['Symbol not found']}, 404
        
        # For demo: use current price from symbol
        market_price = symbol_obj.current_price
        if market_price is None or market_price <= 0:
            return {'errors': [f'Invalid market price for {symbol_obj.symbol}']}, 400
        
        # Update order status
        order.status = 'completed'
        
        # Update user balance for buy orders
        user = User.query.get(current_user.id)
        if not user:
            return {'errors': ['User not found']}, 404
        
        order_total = float(order.shares) * market_price
        
        if order.type == 'buy':
            if order_total > user.balance:
                return {'errors': ['Insufficient funds']}, 400
            user.balance -= order_total
        else:  # sell
            user.balance += order_total
        
        # Update portfolio
        try:
            portfolio = Portfolio.query.filter_by(
                user_id=current_user.id,
                symbol_id=order.symbol_id
            ).first()
            
            if not portfolio:
                portfolio = Portfolio(
                    user_id=current_user.id,
                    symbol_id=order.symbol_id,
                    shares=0,
                    average_price=market_price  # Set initial average price to current market price
                )
                db.session.add(portfolio)
            
            # Update shares based on buy/sell
            if order.type == 'buy':
                # Calculate new average price based on existing shares and new purchase
                if portfolio.shares > 0:
                    total_value = portfolio.shares * portfolio.average_price
                    new_value = order.shares * market_price
                    portfolio.average_price = (total_value + new_value) / (portfolio.shares + order.shares)
                else:
                    portfolio.average_price = market_price
                
                portfolio.shares += order.shares
            else:  # sell
                if portfolio.shares < order.shares:
                    return {'errors': ['Not enough shares to sell']}, 400
                portfolio.shares -= order.shares
                # Average price remains the same when selling
        except Exception as e:
            db.session.rollback()
            return {'errors': [f'Error updating portfolio: {str(e)}']}, 500
        
        # Create transaction record
        try:
            transaction = Transaction(
                user_id=current_user.id,
                order_id=order.id,
                symbol_id=order.symbol_id,
                shares=order.shares,
                price=market_price,
                type=order.type
            )
            
            db.session.add(transaction)
        except Exception as e:
            db.session.rollback()
            return {'errors': [f'Error creating transaction: {str(e)}']}, 500
        
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'errors': [f'Error committing changes: {str(e)}']}, 500
        
        return order
    except Exception as e:
        import traceback
        traceback.print_exc()
        db.session.rollback()
        return {'errors': [str(e)]}, 500 