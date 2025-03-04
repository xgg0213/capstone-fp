from app.models import db, Transaction, User, Symbol, Order, environment, SCHEMA
from sqlalchemy.sql import text
from datetime import datetime

def seed_transactions():
    # Get users, symbols, and completed orders
    users = User.query.all()
    symbols = Symbol.query.all()
    completed_orders = Order.query.filter_by(status='completed').all()

    transactions = [
        Transaction(
            user_id=users[0].id,
            order_id=completed_orders[0].id,  # First completed order
            symbol_id=symbols[0].id,  # AAPL
            shares=100,
            price=175.50,
            type='buy'
        ),
        Transaction(
            user_id=users[0].id,
            order_id=completed_orders[1].id,  # Second completed order
            symbol_id=symbols[1].id,  # GOOGL
            shares=50,
            price=138.20,
            type='buy'
        ),
        Transaction(
            user_id=users[1].id,
            order_id=completed_orders[2].id,  # Third completed order
            symbol_id=symbols[2].id,  # MSFT
            shares=75,
            price=330.50,
            type='buy'
        )
    ]

    try:
        for transaction in transactions:
            db.session.add(transaction)
        db.session.commit()
        print('Transactions seeded successfully!')
    except Exception as e:
        db.session.rollback()
        print('Error seeding transactions:', str(e))
        raise e

def undo_transactions():
    # Because sqlite & psql
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.transactions RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM transactions"))
    db.session.commit()
    print('Transactions table cleared!') 