from app.models import db, Symbol, SymbolPrice
from datetime import datetime, timedelta
from sqlalchemy.sql import text
from app.models.db import SCHEMA, environment
import random

def seed_symbol_prices():


    # Add historical price data for the last 30 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    # Simple patterns for different stocks
    # 1: Uptrend, -1: Downtrend, 0: Sideways
    patterns = {
        'AAPL': 1, 'MSFT': 1, 'GOOGL': 0, 'AMZN': 1, 
        'TSLA': -1, 'NVDA': 1, 'META': 0, 'NFLX': 1
    }
    
    # Volatility (higher = more volatile)
    volatility = {
        'AAPL': 0.015, 'MSFT': 0.012, 'GOOGL': 0.018, 'AMZN': 0.022,
        'TSLA': 0.035, 'NVDA': 0.028, 'META': 0.025, 'NFLX': 0.026
    }
    
    for symbol in Symbol.query.all():
        symbol_code = symbol.symbol
        current_date = start_date
        base_price = symbol.current_price * 0.9  # Start at 90% of current price
        
        # Get pattern and volatility for this symbol
        pattern = patterns.get(symbol_code, 0)
        vol = volatility.get(symbol_code, 0.015)
        
        # Generate 30 days of price history
        for day in range(30):
            current_date = start_date + timedelta(days=day)
            
            # Simple price movement based on pattern and volatility
            random_move = random.uniform(-vol, vol)
            if pattern == 1:  # Uptrend
                price_change = random_move + 0.002
            elif pattern == -1:  # Downtrend
                price_change = random_move - 0.002
            else:  # Sideways
                price_change = random_move
                
            # Calculate new price
            new_price = base_price * (1 + price_change)
            
            # Calculate daily high, low, open
            daily_range = new_price * vol
            daily_high = new_price + (daily_range * random.uniform(0.2, 0.5))
            daily_low = new_price - (daily_range * random.uniform(0.2, 0.5))
            daily_open = daily_low + (daily_high - daily_low) * random.uniform(0, 1)
            
            # Create price record
            price = SymbolPrice(
                symbol_id=symbol.id,
                date=current_date,
                open_price=daily_open,
                close_price=new_price,
                high_price=daily_high,
                low_price=daily_low,
                volume=int(symbol.daily_volume * random.uniform(0.8, 1.2))
            )
            
            db.session.add(price)
            
            # Update for next day
            base_price = new_price
        
    db.session.commit()
    print('Symbol price history seeded successfully!')

def undo_symbol_prices():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.symbol_prices RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM symbol_prices"))
    db.session.commit()
    print('Symbol prices table cleared!') 