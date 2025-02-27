from app.models import db, Symbol, SymbolPrice, environment, SCHEMA 
from datetime import datetime, timedelta

def seed_symbols():
    # Sample stock data
    stocks = [
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
            'daily_high': 139.00,
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
        },
        {
            'symbol': 'AMZN',
            'company_name': 'Amazon.com Inc.',
            'current_price': 145.80,
            'daily_high': 146.50,
            'daily_low': 145.20,
            'daily_volume': 35000000,
            'price_change_pct': 0.50
        }
    ]

    for stock_data in stocks:
        stock = Symbol(
            symbol=stock_data['symbol'],
            company_name=stock_data['company_name'],
            current_price=stock_data['current_price'],
            daily_high=stock_data['daily_high'],
            daily_low=stock_data['daily_low'],
            daily_volume=stock_data['daily_volume'],
            price_change_pct=stock_data['price_change_pct']
        )
        db.session.add(stock)
    
    db.session.commit()

    # Add price history for the last 30 days
    today = datetime.now().date()
    for stock in Symbol.query.all():
        base_price = float(stock.current_price)
        
        for days_ago in range(30, -1, -1):
            date = today - timedelta(days=days_ago)
            # Create some price variation
            variation = (30 - days_ago) * 0.001  # Slight upward trend
            daily_change = (hash(f"{stock.symbol}{date}") % 200 - 100) / 1000.0  # Random daily change
            
            close_price = base_price * (1 + variation + daily_change)
            high_price = close_price * 1.02
            low_price = close_price * 0.98
            open_price = (high_price + low_price) / 2

            price = SymbolPrice(
                symbol_id=stock.id,
                date=date,
                open_price=open_price,
                close_price=close_price,
                high_price=high_price,
                low_price=low_price,
                volume=stock.daily_volume * (0.8 + (hash(f"{stock.symbol}{date}") % 40) / 100.0)
            )
            db.session.add(price)
    
    db.session.commit()

def undo_symbols():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.symbol_prices RESTART IDENTITY CASCADE;")
        db.session.execute(f"TRUNCATE table {SCHEMA}.symbols RESTART IDENTITY CASCADE;")
    else:
        db.session.execute("DELETE FROM symbol_prices")
        db.session.execute("DELETE FROM symbols")
    
    db.session.commit() 