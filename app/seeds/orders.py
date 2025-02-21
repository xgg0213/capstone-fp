from app.models import db, Order, environment, SCHEMA
from sqlalchemy.sql import text
from datetime import datetime, timedelta

def seed_orders():
    orders = [
        Order(
            user_id=1,  # Demo user
            symbol='AAPL',
            order_type='market',
            side='buy',
            shares=10,
            status='filled',
            filled_price=175.50,
            filled_at=datetime.utcnow() - timedelta(days=5)
        ),
        Order(
            user_id=1,  # Demo user
            symbol='GOOGL',
            order_type='limit',
            side='buy',
            shares=5,
            price=140.00,  # Limit price
            status='pending'
        ),
        Order(
            user_id=1,  # Demo user
            symbol='TSLA',
            order_type='market',
            side='buy',
            shares=15,
            status='pending'
        ),
        # Add some orders for other users
        Order(
            user_id=2,  # Marnie
            symbol='MSFT',
            order_type='market',
            side='buy',
            shares=8,
            status='filled',
            filled_price=280.50,
            filled_at=datetime.utcnow() - timedelta(days=2)
        ),
        Order(
            user_id=3,  # Bobbie
            symbol='AMZN',
            order_type='limit',
            side='sell',
            shares=3,
            price=135.00,
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
    print('Orders table cleared!') 