from app.models import db, Portfolio, User, environment, SCHEMA
from sqlalchemy.sql import text
from datetime import datetime

def seed_portfolios():
    demo = User.query.filter_by(username='Demo').first()
    
    portfolios = [
        Portfolio(
            user_id=demo.id,
            symbol='AAPL',
            shares=10,
            average_price=175.50
        ),
        Portfolio(
            user_id=demo.id,
            symbol='GOOGL',
            shares=5,
            average_price=142.30
        ),
        Portfolio(
            user_id=demo.id,
            symbol='TSLA',
            shares=15,
            average_price=245.75
        )
    ]
    
    for portfolio in portfolios:
        db.session.add(portfolio)
        
    db.session.commit()
    print('Portfolios seeded successfully!')

def undo_portfolios():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.portfolios RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM portfolios"))
    db.session.commit() 