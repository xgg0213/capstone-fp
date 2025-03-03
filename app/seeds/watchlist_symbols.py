from app.models import db, WatchlistSymbol, Watchlist, Symbol
from sqlalchemy.sql import text
from app.models.db import SCHEMA, environment

def seed_watchlist_symbols():
    # Clear existing watchlist symbols
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.watchlist_symbols RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM watchlist_symbols"))
    db.session.commit()

    try:
        # Get demo user's watchlist and some symbols
        demo_watchlist = Watchlist.query.filter_by(user_id=1).first()
        aapl = Symbol.query.filter_by(symbol='AAPL').first()
        msft = Symbol.query.filter_by(symbol='MSFT').first()
        googl = Symbol.query.filter_by(symbol='GOOGL').first()

        # Create watchlist symbols
        watchlist_symbols = [
            WatchlistSymbol(
                watchlist_id=demo_watchlist.id,
                symbol_id=aapl.id
            ),
            WatchlistSymbol(
                watchlist_id=demo_watchlist.id,
                symbol_id=msft.id
            ),
            WatchlistSymbol(
                watchlist_id=demo_watchlist.id,
                symbol_id=googl.id
            )
        ]

        for watchlist_symbol in watchlist_symbols:
            db.session.add(watchlist_symbol)
        
        db.session.commit()
        print('Watchlist symbols seeded successfully!')
    except Exception as e:
        db.session.rollback()
        print('Error seeding watchlist symbols:', str(e))
        raise e

def undo_watchlist_symbols():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.watchlist_symbols RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM watchlist_symbols"))
    db.session.commit()
    print('Watchlist symbols table cleared!') 