from app.models import db, Watchlist, User, environment, SCHEMA
from sqlalchemy.sql import text

def seed_watchlists():
    demo = User.query.filter_by(username='Demo').first()
    
    watchlists = [
        Watchlist(
            user_id=demo.id,
            name='Tech Stocks',
            symbols='AAPL,GOOGL,MSFT,META'
        ),
        Watchlist(
            user_id=demo.id,
            name='EV Stocks',
            symbols='TSLA,RIVN,LCID'
        ),
        Watchlist(
            user_id=demo.id,
            name='Crypto Stocks',
            symbols='COIN,MSTR,RIOT'
        )
    ]
    
    for watchlist in watchlists:
        db.session.add(watchlist)
        
    db.session.commit()
    print('Watchlists seeded successfully!')

def undo_watchlists():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.watchlists RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM watchlists"))
    db.session.commit() 