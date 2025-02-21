from app.models import db, Transaction, User, Order, environment, SCHEMA
from sqlalchemy.sql import text
from datetime import datetime, timedelta

def seed_transactions():
    demo = User.query.filter_by(username='Demo').first()
    orders = Order.query.filter_by(user_id=demo.id).all()
    
    transactions = [
        Transaction(
            user_id=demo.id,
            order_id=orders[0].id,
            symbol='AAPL',
            shares=10,
            price=175.50,
            type='buy'
        ),
        Transaction(
            user_id=demo.id,
            order_id=orders[1].id,
            symbol='GOOGL',
            shares=5,
            price=142.30,
            type='buy'
        ),
        Transaction(
            user_id=demo.id,
            symbol='TSLA',
            shares=15,
            price=245.75,
            type='buy'
        )
    ]
    
    for transaction in transactions:
        db.session.add(transaction)
        
    db.session.commit()
    print('Transactions seeded successfully!')

def undo_transactions():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.transactions RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM transactions"))
    db.session.commit() 