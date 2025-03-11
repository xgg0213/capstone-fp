from app.models import db, Symbol
from sqlalchemy.sql import text
from app.models.db import SCHEMA, environment

def seed_symbols():

    # List of popular stock symbols with realistic data
    symbols = [
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
            'daily_high': 139.10,
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
            'current_price': 142.75,
            'daily_high': 143.80,
            'daily_low': 141.90,
            'daily_volume': 30500000,
            'price_change_pct': 0.45
        },
        {
            'symbol': 'TSLA',
            'company_name': 'Tesla Inc.',
            'current_price': 238.45,
            'daily_high': 242.10,
            'daily_low': 236.80,
            'daily_volume': 42300000,
            'price_change_pct': -1.20
        },
        {
            'symbol': 'NVDA',
            'company_name': 'NVIDIA Corporation',
            'current_price': 445.20,
            'daily_high': 448.75,
            'daily_low': 442.30,
            'daily_volume': 22500000,
            'price_change_pct': 2.35
        },
        {
            'symbol': 'META',
            'company_name': 'Meta Platforms Inc.',
            'current_price': 325.80,
            'daily_high': 328.50,
            'daily_low': 323.20,
            'daily_volume': 15800000,
            'price_change_pct': 1.85
        },
        {
            'symbol': 'NFLX',
            'company_name': 'Netflix Inc.',
            'current_price': 485.30,
            'daily_high': 488.50,
            'daily_low': 482.70,
            'daily_volume': 4200000,
            'price_change_pct': 1.45
        }
    ]

    # Create Symbol instances
    for symbol_data in symbols:
        symbol = Symbol(**symbol_data)
        db.session.add(symbol)
    
    db.session.commit()
    print('Symbols seeded successfully!')

def undo_symbols():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.symbols RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM symbols"))
    db.session.commit()
    print('Symbols table cleared!') 