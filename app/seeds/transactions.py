from app.models import db, Transaction, User, environment, SCHEMA
from sqlalchemy.sql import text
from datetime import datetime

def seed_transactions():
    # Get demo user
    demo = User.query.filter_by(username='Demo').first()
    
    # Create some initial transactions
    initial_transactions = [
        {
            'symbol': 'AAPL',
            'shares': 50,
            'price': 175.50,
            'type': 'buy'
        },
        {
            'symbol': 'MSFT',
            'shares': 30,
            'price': 325.75,
            'type': 'buy'
        },
        {
            'symbol': 'GOOGL',
            'shares': 20,
            'price': 135.25,
            'type': 'buy'
        },
        {
            'symbol': 'AAPL',
            'shares': 10,
            'price': 180.25,
            'type': 'sell'
        }
    ]

    for txn in initial_transactions:
        transaction = Transaction(
            user_id=demo.id,
            symbol=txn['symbol'],
            shares=txn['shares'],
            price=txn['price'],
            type=txn['type'],
            created_at=datetime.utcnow()
        )
        db.session.add(transaction)

    db.session.commit()
    print('Transactions seeded successfully!')

def undo_transactions():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.transactions RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM transactions"))
    db.session.commit()
    print('Transactions table cleared!') 