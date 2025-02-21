from app.models import db, Order, User, environment, SCHEMA
from sqlalchemy.sql import text
from datetime import datetime

def seed_orders():
    # Get demo user
    demo = User.query.filter_by(username='Demo').first()
    
    # Create some initial orders
    initial_orders = [
        {
            'symbol': 'TSLA',
            'shares': 10,
            'type': 'buy',
            'order_type': 'limit',
            'limit_price': 250.00,
            'status': 'pending'
        },
        {
            'symbol': 'META',
            'shares': 15,
            'type': 'buy',
            'order_type': 'market',
            'status': 'completed'
        },
        {
            'symbol': 'NVDA',
            'shares': 5,
            'type': 'sell',
            'order_type': 'stop',
            'stop_price': 450.00,
            'status': 'pending'
        }
    ]

    for order_data in initial_orders:
        order = Order(
            user_id=demo.id,
            symbol=order_data['symbol'],
            shares=order_data['shares'],
            type=order_data['type'],
            order_type=order_data['order_type'],
            status=order_data['status'],
            created_at=datetime.utcnow()
        )
        
        if 'limit_price' in order_data:
            order.limit_price = order_data['limit_price']
        if 'stop_price' in order_data:
            order.stop_price = order_data['stop_price']
            
        db.session.add(order)

    db.session.commit()
    print('Orders seeded successfully!')

def undo_orders():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.orders RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM orders"))
    db.session.commit()
    print('Orders table cleared!') 