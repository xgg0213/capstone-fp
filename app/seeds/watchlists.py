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

    # Create demo watchlist
    demo_watchlist = Watchlist(
        user_id=1,  # Demo user
        name="My First Watchlist"
    )

    db.session.add(demo_watchlist)
    db.session.commit()

    # Add symbols to demo watchlist
    demo_symbols = [
        WatchlistSymbol(
            watchlist_id=demo_watchlist.id,
            symbol_id=symbols[0].id  # AAPL
        ),
        WatchlistSymbol(
            watchlist_id=demo_watchlist.id,
            symbol_id=symbols[1].id  # GOOGL
        )
    ]

    db.session.add_all(demo_symbols)
    db.session.commit()

def undo_watchlists():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.watchlist_symbols RESTART IDENTITY CASCADE;")
        db.session.execute(f"TRUNCATE table {SCHEMA}.watchlists RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM watchlist_symbols"))
        db.session.execute(text("DELETE FROM watchlists"))
        
    db.session.commit()
    print('Watchlists table cleared!') 