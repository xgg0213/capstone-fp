from app.models import db, Symbol, SymbolPrice
from datetime import datetime, timedelta
from sqlalchemy.sql import text
from app.models.db import SCHEMA, environment

def seed_symbol_prices():
    # Clear existing price data
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.symbol_prices RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM symbol_prices"))
    db.session.commit()

    try:
        # Add historical price data
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        for symbol in Symbol.query.all():
            current_date = start_date
            base_price = symbol.current_price

            while current_date <= end_date:
                price = SymbolPrice(
                    symbol_id=symbol.id,
                    date=current_date,
                    open_price=base_price * 0.99,
                    close_price=base_price * 1.01,
                    high_price=base_price * 1.02,
                    low_price=base_price * 0.98,
                    volume=50000000
                )
                db.session.add(price)
                current_date += timedelta(days=1)
                base_price *= 1.001  # Slight upward trend

            db.session.commit()
        print('Symbol price history seeded successfully!')
    except Exception as e:
        db.session.rollback()
        print('Error seeding symbol prices:', str(e))
        raise e

def undo_symbol_prices():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.symbol_prices RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM symbol_prices"))
    db.session.commit()
    print('Symbol prices table cleared!') 