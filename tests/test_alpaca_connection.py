from alpaca.trading.client import TradingClient
from alpaca.data.historical import StockHistoricalDataClient
import os
from dotenv import load_dotenv

def test_alpaca_connection():
    load_dotenv()
    
    api_key = os.getenv('ALPACA_API_KEY')
    secret_key = os.getenv('ALPACA_SECRET_KEY')
    
    print("Testing Alpaca connection...")
    print(f"Using API key: {api_key[:5]}...{api_key[-5:]}")
    
    try:
        # Test trading client
        trading_client = TradingClient(api_key, secret_key, paper=True)
        account = trading_client.get_account()
        print("✅ Trading API connection successful")
        print(f"Account status: {account.status}")
        print(f"Buying power: ${account.buying_power}")
        
        # Test market data client
        data_client = StockHistoricalDataClient(api_key, secret_key)
        print("✅ Market Data API connection successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_alpaca_connection() 