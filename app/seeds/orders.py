from app.models import db, Order, environment, SCHEMA
from sqlalchemy.sql import text
from datetime import datetime, timedelta

def seed_orders():
    # Create orders for existing users (user_id 1, 2, 3)
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
            user_id=2,  # Marnie
            symbol='GOOGL',
            order_type='limit',
            side='buy',
            shares=5,
            price=140.00,  # Limit price
            status='pending'
        ),
        Order(
            user_id=3,  # Bobbie
            symbol='TSLA',
            order_type='market',
            side='buy',
            shares=15,
            status='pending'
        )
    ]
    
    try:
        for order in orders:
            db.session.add(order)
        db.session.commit()
        print('Orders seeded successfully!')
    except Exception as e:
        db.session.rollback()
        print('Error seeding orders:', str(e))
        raise e

def undo_orders():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.orders RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM orders"))
    db.session.commit()
    print('Orders table cleared!') 