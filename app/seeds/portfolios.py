from app.models import db, Portfolio, User
from sqlalchemy.sql import text
from datetime import datetime

def seed_portfolios():
    # Get demo user
    demo = User.query.filter_by(username='Demo').first()
    
    # Create some initial positions
    initial_positions = [
        {
            'symbol': 'AAPL',
            'shares': 50,
            'avg_price': 175.50
        },
        {
            'symbol': 'MSFT',
            'shares': 30,
            'avg_price': 325.75
        },
        {
            'symbol': 'GOOGL',
            'shares': 20,
            'avg_price': 135.25
        }
    ]

    for position in initial_positions:
        portfolio = Portfolio(
            user_id=demo.id,
            symbol=position['symbol'],
            shares=position['shares'],
            average_price=position['avg_price'],
            created_at=datetime.utcnow()
        )
        db.session.add(portfolio)

    db.session.commit()
    print('Portfolios seeded successfully!')

def undo_portfolios():
    db.session.execute(text("DELETE FROM portfolios"))
    db.session.commit()
    print('Portfolios table cleared!') 