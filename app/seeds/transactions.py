from app.models import db, Transaction, environment, SCHEMA
from sqlalchemy.sql import text
from datetime import datetime, timedelta

def seed_transactions():
    transactions = [
        Transaction(
            user_id=1,  # Demo user
            order_id=1,  # AAPL order
            symbol='AAPL',
            shares=10,
            price=175.50,
            type='buy',
            created_at=datetime.utcnow() - timedelta(days=5)
        ),
        Transaction(
            user_id=2,  # Marnie
            order_id=2,  # GOOGL order
            symbol='GOOGL',
            shares=5,
            price=140.00,
            type='buy',
            created_at=datetime.utcnow() - timedelta(days=3)
        ),
        Transaction(
            user_id=3,  # Bobbie
            order_id=3,  # TSLA order
            symbol='TSLA',
            shares=15,
            price=100.00,
            type='buy',
            created_at=datetime.utcnow() - timedelta(days=1)
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
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.transactions RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM transactions"))
    db.session.commit()
    print('Transactions table cleared!') 