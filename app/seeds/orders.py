from app.models import db, Order, User, Symbol, environment, SCHEMA
from sqlalchemy.sql import text
from datetime import datetime

def seed_orders():
    # Get users and symbols first
    users = User.query.all()
    symbols = Symbol.query.all()

    # Create sample orders - mix of completed and pending
    orders = [
        # Completed orders
        Order(
            user_id=users[0].id,
            symbol_id=symbols[0].id,  # AAPL
            shares=100,
            type='buy',
            status='completed'  # This will have a transaction
        ),
        Order(
            user_id=users[0].id,
            symbol_id=symbols[1].id,  # GOOGL
            shares=50,
            type='buy',
            status='completed'  # This will have a transaction
        ),
        Order(
            user_id=users[1].id,
            symbol_id=symbols[2].id,  # MSFT
            shares=75,
            type='buy',
            status='completed'  # This will have a transaction
        ),
        # Pending orders
        Order(
            user_id=users[0].id,
            symbol_id=symbols[0].id,  # AAPL
            shares=25,
            type='buy',
            status='pending'  # No transaction for this one
        ),
        Order(
            user_id=users[1].id,
            symbol_id=symbols[1].id,  # GOOGL
            shares=30,
            type='sell',
            status='pending'  # No transaction for this one
        )
    ]

    for order in orders:
        db.session.add(order)

    db.session.commit()

def undo_orders():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.orders RESTART IDENTITY CASCADE;")
    else:
        db.session.execute("DELETE FROM orders")
        
    db.session.commit()
    print('Orders table cleared!') 