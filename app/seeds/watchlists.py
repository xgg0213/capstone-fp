from app.models import db, Watchlist, environment, SCHEMA
from sqlalchemy.sql import text
from datetime import datetime

def seed_watchlists():
    watchlists = [
        Watchlist(
            user_id=1,  # Demo user
            name='Tech Stocks',
            symbols='AAPL,GOOGL,MSFT,TSLA'
        ),
        Watchlist(
            user_id=1,  # Demo user
            name='Finance',
            symbols='JPM,BAC,GS,MS'
        ),
        Watchlist(
            user_id=2,  # Marnie
            name='My Watchlist',
            symbols='AMZN,NFLX,META'
        ),
        Watchlist(
            user_id=3,  # Bobbie
            name='Favorites',
            symbols='NVDA,AMD,INTC'
        )
    ]

    try:
        for watchlist in watchlists:
            db.session.add(watchlist)
        db.session.commit()
        print('Watchlists seeded successfully!')
    except Exception as e:
        db.session.rollback()
        print('Error seeding watchlists:', str(e))
        raise e

def undo_watchlists():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.watchlists RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM watchlists"))
    db.session.commit()
    print('Watchlists table cleared!') 