from app.models import db, Order, User, Symbol, environment, SCHEMA
from sqlalchemy.sql import text
from datetime import datetime, timedelta
import random

def seed_orders():
    # Get users and symbols first
    users = User.query.all()
    symbols = Symbol.query.all()
    
    if not users or not symbols:
        print("No users or symbols found. Make sure to seed users and symbols first.")
        return

    # Create sample orders
    orders = []
    
    # Add some completed buy orders for the first user
    for i, symbol in enumerate(symbols[:4]):  # First 4 symbols
        # Create orders with consistent dates for transaction matching
        days_ago = 30 - (i * 5)  # 30, 25, 20, 15 days ago
        order_date = datetime.now() - timedelta(days=days_ago)
        
        order = Order(
            user_id=users[0].id,
            symbol_id=symbol.id,
            shares=random.randint(10, 100),
            type='buy',
            status='completed',
            created_at=order_date,
            updated_at=order_date
        )
        orders.append(order)
    
    # Add some completed sell orders
    for i, symbol in enumerate(symbols[1:3]):  # 2nd and 3rd symbols
        # Create orders with consistent dates for transaction matching
        days_ago = 10 - (i * 5)  # 10, 5 days ago
        order_date = datetime.now() - timedelta(days=days_ago)
        
        order = Order(
            user_id=users[0].id,
            symbol_id=symbol.id,
            shares=random.randint(5, 20),
            type='sell',
            status='completed',
            created_at=order_date,
            updated_at=order_date
        )
        orders.append(order)
    
    # Add some pending orders
    for i, symbol in enumerate(symbols[2:5]):  # 3rd, 4th, and 5th symbols
        # Create orders with consistent dates
        days_ago = 3 - i  # 3, 2, 1 days ago
        order_date = datetime.now() - timedelta(days=days_ago)
        
        order = Order(
            user_id=users[0].id,
            symbol_id=symbol.id,
            shares=random.randint(5, 50),
            type=random.choice(['buy', 'sell']),
            status='pending',
            created_at=order_date,
            updated_at=order_date
        )
        orders.append(order)
    
    # Add a few orders for other users if there are any
    if len(users) > 1:
        for j, user in enumerate(users[1:]):
            for i, symbol in enumerate(random.sample(list(symbols), 2)):  # 2 random symbols
                # Create orders with consistent dates
                days_ago = 20 - (j * 5) - (i * 2)  # Spread out over time
                order_date = datetime.now() - timedelta(days=days_ago)
                
                order = Order(
                    user_id=user.id,
                    symbol_id=symbol.id,
                    shares=random.randint(10, 100),
                    type=random.choice(['buy', 'sell']),
                    status=random.choice(['completed', 'pending']),
                    created_at=order_date,
                    updated_at=order_date
                )
                orders.append(order)
    
    # Add all orders to the database
    for order in orders:
        db.session.add(order)

    db.session.commit()
    print(f"Added {len(orders)} orders to the database")

def undo_orders():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.orders RESTART IDENTITY CASCADE;")
    else:
        db.session.execute("DELETE FROM orders")
        
    db.session.commit()
    print('Orders table cleared!') 