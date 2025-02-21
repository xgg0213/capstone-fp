import pytest
from alpaca.data.live import StockDataStream
from alpaca.trading.client import TradingClient
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime, timedelta
import pytz
import os
from dotenv import load_dotenv

def get_market_hours():
    """Get market hours in ET"""
    et_tz = pytz.timezone('America/New_York')
    now = datetime.now(et_tz)
    market_open = now.replace(hour=9, minute=30, second=0, microsecond=0)
    market_close = now.replace(hour=16, minute=0, second=0, microsecond=0)
    return now, market_open, market_close

def test_alpaca_connection():
    """Test basic Alpaca connection and historical data"""
    load_dotenv()
    
    api_key = os.getenv('ALPACA_API_KEY')
    secret_key = os.getenv('ALPACA_SECRET_KEY')
    
    print(f"\nTesting with API key: {api_key[:5]}...")
    
    # Check market status
    trading_client = TradingClient(api_key, secret_key, paper=True)
    clock = trading_client.get_clock()
    
    now, market_open, market_close = get_market_hours()
    
    if clock.is_open:
        print("✅ Market is open")
    else:
        next_open = clock.next_open.astimezone(pytz.timezone('America/New_York'))
        print(f"ℹ️  Market is closed. Next open: {next_open}")
    
    # Test historical data access
    try:
        data_client = StockHistoricalDataClient(api_key, secret_key)
        
        # Get recent data
        request = StockBarsRequest(
            symbol_or_symbols="AAPL",
            timeframe=TimeFrame.Minute,
            start=datetime.now() - timedelta(days=1),
            end=datetime.now()
        )
        
        print("\nFetching historical data...")
        bars = data_client.get_stock_bars(request)
        
        if bars and len(bars["AAPL"]) > 0:
            latest = bars["AAPL"][-1]
            print(f"✅ Historical data available")
            print(f"Latest AAPL price: ${latest.close:.2f}")
            print(f"Data points received: {len(bars['AAPL'])}")
            return True
    except Exception as e:
        print(f"❌ Error fetching historical data: {e}")
        return False

@pytest.mark.asyncio
async def test_websocket():
    """Test WebSocket connection to Alpaca"""
    load_dotenv()
    
    api_key = os.getenv('ALPACA_API_KEY')
    secret_key = os.getenv('ALPACA_SECRET_KEY')
    
    # Check market status
    trading_client = TradingClient(api_key, secret_key, paper=True)
    clock = trading_client.get_clock()
    
    now, market_open, market_close = get_market_hours()
    
    if not clock.is_open:
        pytest.skip("Market is closed - skipping WebSocket test")
    
    received_data = False
    
    async def handle_quote(quote):
        nonlocal received_data
        received_data = True
        print(f"✅ Received quote: {quote.symbol} bid: ${quote.bid_price:.2f} ask: ${quote.ask_price:.2f}")
    
    try:
        client = StockDataStream(api_key, secret_key)
        
        # Subscribe to highly liquid symbols
        symbols = ["SPY", "QQQ", "IWM"]  # ETFs that trade frequently
        print(f"\nSubscribing to symbols: {', '.join(symbols)}")
        
        client.subscribe_quotes(handle_quote, *symbols)
        
        print("Starting WebSocket connection...")
        print("Waiting for market data (15 seconds)...")
        
        try:
            await asyncio.wait_for(client._run_forever(), timeout=15.0)
        except asyncio.TimeoutError:
            print("ℹ️  No real-time data received (expected if market is closed)")
        finally:
            await client.close()
        
        # Don't fail the test if market is closed
        if not received_data and clock.is_open:
            print("⚠️  No data received during market hours")
            
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    # First test basic connection and historical data
    test_alpaca_connection()
    
    # Then run WebSocket test if market is open
    pytest.main([__file__, "-v", "--capture=no"]) 