from app.models import db, Order, User, environment, SCHEMA
from sqlalchemy.sql import text
from datetime import datetime, timedelta

def seed_orders():
    demo = User.query.filter_by(username='Demo').first()
    
    orders = [
        Order(
            user_id=demo.id,
            symbol='AAPL',
            order_type='market',
            side='buy',
            shares=10,
            status='filled',
            filled_price=175.50,
            filled_at=datetime.utcnow() - timedelta(days=5)
        ),
        Order(
            user_id=demo.id,
            symbol='GOOGL',
            order_type='limit',
            side='buy',
            shares=5,
            price=140.00,
            status='filled',
            filled_price=142.30,
            filled_at=datetime.utcnow() - timedelta(days=3)
        ),
        Order(
            user_id=demo.id,
            symbol='TSLA',
            order_type='market',
            side='buy',
            shares=15,
            status='pending'
        )
    ]
    
    for order in orders:
        db.session.add(order)
        
    db.session.commit()
    print('Orders seeded successfully!')

def undo_orders():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.orders RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM orders"))
    db.session.commit() 