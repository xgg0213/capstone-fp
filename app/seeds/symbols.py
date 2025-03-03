from app.models import db, Symbol
from sqlalchemy.sql import text
from app.models.db import SCHEMA, environment

def seed_symbols():
    # Clear existing symbols
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.symbols RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM symbols"))
    db.session.commit()

    # Sample symbols data
    symbols = [
        {
            'symbol': 'AAPL',
            'company_name': 'Apple Inc.',
            'current_price': 175.50,
            'daily_high': 176.20,
            'daily_low': 174.80,
            'daily_volume': 52000000,
            'price_change_pct': 0.75
        },
        {
            'symbol': 'GOOGL',
            'company_name': 'Alphabet Inc.',
            'current_price': 138.20,
            'daily_high': 139.10,
            'daily_low': 137.50,
            'daily_volume': 25000000,
            'price_change_pct': -0.25
        },
        {
            'symbol': 'MSFT',
            'company_name': 'Microsoft Corporation',
            'current_price': 330.50,
            'daily_high': 332.00,
            'daily_low': 329.80,
            'daily_volume': 18000000,
            'price_change_pct': 1.20
        }
    ]

    try:
        # Create Symbol instances
        for symbol_data in symbols:
            symbol = Symbol(**symbol_data)
            db.session.add(symbol)
        db.session.commit()
        print('Symbols seeded successfully!')
    except Exception as e:
        db.session.rollback()
        print('Error seeding symbols:', str(e))
        raise e

def undo_symbols():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.symbols RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM symbols"))
    db.session.commit()
    print('Symbols table cleared!') 