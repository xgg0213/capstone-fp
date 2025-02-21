import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'dev-jwt-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///dev.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CSRF_ENABLED = True
    WTF_CSRF_CHECK_DEFAULT = False  # We'll check CSRF manually for API routes
    JWT_ACCESS_TOKEN_EXPIRES = 24 * 60 * 60  # 24 hours in seconds 
    
    # Alpaca Configuration
    ALPACA_API_KEY = os.environ.get('ALPACA_API_KEY')
    ALPACA_SECRET_KEY = os.environ.get('ALPACA_SECRET_KEY')
    ALPACA_PAPER_TRADING = True  # Set to False for live trading
    ALPACA_BASE_URL = "https://paper-api.alpaca.markets" if ALPACA_PAPER_TRADING else "https://api.alpaca.markets" 