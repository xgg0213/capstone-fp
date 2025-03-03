from app.models import db, Watchlist
from sqlalchemy.sql import text
from app.models.db import SCHEMA, environment

def seed_watchlists():
    # Clear existing watchlists
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.watchlists RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM watchlists"))
    db.session.commit()

    try:
        # Create default watchlists for demo users
        watchlists = [
            Watchlist(
                user_id=1,  # Demo user
                name='My First Watchlist'
            ),
            Watchlist(
                user_id=2,  # Marnie
                name='Tech Stocks'
            )
        ]

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