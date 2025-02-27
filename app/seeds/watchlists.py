from app.models import db, Watchlist, WatchlistSymbol, User, Symbol, environment, SCHEMA
from sqlalchemy.sql import text
from datetime import datetime

def seed_watchlists():
    # Get users and symbols first
    users = User.query.all()
    symbols = Symbol.query.all()

    # Create watchlists
    watchlists = [
        Watchlist(
            user_id=users[0].id,
            name="Tech Stocks"
        ),
        Watchlist(
            user_id=users[1].id,
            name="My Favorites"
        )
    ]

    for watchlist in watchlists:
        db.session.add(watchlist)
    
    db.session.commit()

    # Add symbols to watchlists
    watchlist_symbols = [
        WatchlistSymbol(
            watchlist_id=watchlists[0].id,
            symbol_id=symbols[0].id  # AAPL
        ),
        WatchlistSymbol(
            watchlist_id=watchlists[0].id,
            symbol_id=symbols[1].id  # GOOGL
        ),
        WatchlistSymbol(
            watchlist_id=watchlists[1].id,
            symbol_id=symbols[2].id  # MSFT
        )
    ]

    for ws in watchlist_symbols:
        db.session.add(ws)

    db.session.commit()

def undo_watchlists():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.watchlist_symbols RESTART IDENTITY CASCADE;")
        db.session.execute(f"TRUNCATE table {SCHEMA}.watchlists RESTART IDENTITY CASCADE;")
    else:
        db.session.execute("DELETE FROM watchlist_symbols")
        db.session.execute("DELETE FROM watchlists")
    
    db.session.commit()
    print('Watchlists table cleared!') 