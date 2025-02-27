from app.models import db, Portfolio, User, Symbol, environment, SCHEMA
from sqlalchemy.sql import text
from datetime import datetime

def seed_portfolios():
    # Get users and symbols first
    users = User.query.all()
    symbols = Symbol.query.all()

    portfolios = [
        Portfolio(
            user_id=users[0].id,  # Demo user
            symbol_id=symbols[0].id,  # AAPL
            shares=100,
            average_price=175.50
        ),
        Portfolio(
            user_id=users[0].id,  # Demo user
            symbol_id=symbols[1].id,  # GOOGL
            shares=50,
            average_price=138.20
        ),
        Portfolio(
            user_id=users[1].id,  # Marnie
            symbol_id=symbols[2].id,  # MSFT
            shares=75,
            average_price=330.50
        )
    ]

    try:
        for portfolio in portfolios:
            db.session.add(portfolio)
        db.session.commit()
        print('Portfolios seeded successfully!')
    except Exception as e:
        db.session.rollback()
        print('Error seeding portfolios:', str(e))
        raise e

def undo_portfolios():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.portfolios RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM portfolios"))
    
    db.session.commit()
    print('Portfolios table cleared!') 