from alpaca.trading.client import TradingClient
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

def test_alpaca_connection():
    # Load environment variables
    load_dotenv()
    
    api_key = os.getenv('ALPACA_API_KEY')
    secret_key = os.getenv('ALPACA_SECRET_KEY')
    
    if not api_key or not secret_key:
        print("❌ Error: Alpaca keys not found in .env file")
        return False
        
    try:
        # Test trading client
        trading_client = TradingClient(api_key, secret_key, paper=True)
        account = trading_client.get_account()
        print("✅ Trading client connected successfully!")
        print(f"Account status: {account.status}")
        print(f"Buying power: ${account.buying_power}")
        
        # Test market data
        data_client = StockHistoricalDataClient(api_key, secret_key)
        request = StockBarsRequest(
            symbol_or_symbols="AAPL",
            timeframe=TimeFrame.Day,
            start=datetime.now() - timedelta(days=5),
            end=datetime.now()
        )
        bars = data_client.get_stock_bars(request)
        print("✅ Market data client connected successfully!")
        print(f"Got {len(bars['AAPL'])} bars for AAPL")
        
        return True
        
    except Exception as e:
        print(f"❌ Error connecting to Alpaca: {str(e)}")
        return False

if __name__ == "__main__":
    test_alpaca_connection() 