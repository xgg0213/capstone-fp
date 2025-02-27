from app.models import db, Portfolio, User, Symbol, environment, SCHEMA
from datetime import datetime

def seed_portfolios():
    # Get users and symbols first
    users = User.query.all()
    symbols = Symbol.query.all()

    portfolios = [
        Portfolio(
            user_id=users[0].id,
            symbol_id=symbols[0].id,  # AAPL
            shares=100,
            average_price=175.50
        ),
        Portfolio(
            user_id=users[0].id,
            symbol_id=symbols[1].id,  # GOOGL
            shares=50,
            average_price=138.20
        ),
        Portfolio(
            user_id=users[1].id,
            symbol_id=symbols[2].id,  # MSFT
            shares=75,
            average_price=330.50
        )
    ]

    for portfolio in portfolios:
        db.session.add(portfolio)

    db.session.commit()

def undo_portfolios():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.portfolios RESTART IDENTITY CASCADE;")
    else:
        db.session.execute("DELETE FROM portfolios")
    
    db.session.commit() 