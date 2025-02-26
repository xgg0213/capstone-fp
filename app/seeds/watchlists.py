from app.models import db, Watchlist, WatchlistSymbol, environment, SCHEMA
from sqlalchemy.sql import text
from datetime import datetime

def seed_watchlists():
    # First, create watchlists
    demo_watchlist = Watchlist(
        user_id=1,
        name='My First Watchlist'
    )

    demo_watchlist2 = Watchlist(
        user_id=1,
        name='Tech Stocks'
    )

    marnie_watchlist = Watchlist(
        user_id=2,
        name='Favorites'
    )

    db.session.add_all([demo_watchlist, demo_watchlist2, marnie_watchlist])
    db.session.commit()

    # Then, add symbols to watchlists
    demo_symbols = [
        WatchlistSymbol(
            watchlist_id=1,
            symbol='AAPL',
            company_name='Apple Inc.',
            current_price=175.50,
            price_change=1.25
        ),
        WatchlistSymbol(
            watchlist_id=1,
            symbol='MSFT',
            company_name='Microsoft Corporation',
            current_price=325.75,
            price_change=2.30
        ),
        WatchlistSymbol(
            watchlist_id=2,
            symbol='GOOGL',
            company_name='Alphabet Inc.',
            current_price=135.20,
            price_change=-0.75
        ),
        WatchlistSymbol(
            watchlist_id=2,
            symbol='META',
            company_name='Meta Platforms Inc.',
            current_price=292.50,
            price_change=1.80
        )
    ]

    marnie_symbols = [
        WatchlistSymbol(
            watchlist_id=3,
            symbol='TSLA',
            company_name='Tesla, Inc.',
            current_price=245.30,
            price_change=-1.20
        ),
        WatchlistSymbol(
            watchlist_id=3,
            symbol='NVDA',
            company_name='NVIDIA Corporation',
            current_price=420.15,
            price_change=3.45
        )
    ]

    db.session.add_all(demo_symbols + marnie_symbols)
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