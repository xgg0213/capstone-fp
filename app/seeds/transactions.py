from app.models import db, Transaction, User, Symbol, Order, environment, SCHEMA
from sqlalchemy.sql import text
from datetime import datetime
import random

def seed_transactions():

    
    # Get completed orders
    completed_orders = Order.query.filter_by(status='completed').all()
    
    if not completed_orders:
        print("No completed orders found. Make sure to seed orders first.")
        return

    # Create transactions for all completed orders
    transactions = []
    for order in completed_orders:
        # Get the symbol for this order
        symbol = Symbol.query.get(order.symbol_id)
        if not symbol:
            print(f"Warning: Symbol with ID {order.symbol_id} not found for order {order.id}")
            continue
            
        # Create transaction with a price close to current price
        # Use a consistent price factor based on order ID for reproducibility
        random.seed(order.id)  # Set seed based on order ID for consistency
        price_factor = random.uniform(0.95, 1.05)
        transaction_price = symbol.current_price * price_factor
        
        # Create transaction with same date as order
        transaction = Transaction(
            user_id=order.user_id,
            order_id=order.id,
            symbol_id=order.symbol_id,
            shares=order.shares,
            price=transaction_price,
            type=order.type,
            created_at=order.created_at  # Use the same date as the order
        )
        
        transactions.append(transaction)
        db.session.add(transaction)
    
    db.session.commit()
    print(f'Added {len(transactions)} transactions to the database')

def undo_transactions():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.transactions RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM transactions"))
    db.session.commit()
    print('Transactions table cleared!') 