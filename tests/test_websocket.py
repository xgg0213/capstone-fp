import asyncio
import pytest
from alpaca.data.live import StockDataStream
from alpaca.trading.client import TradingClient
from datetime import datetime
import pytz
import os
from dotenv import load_dotenv

@pytest.mark.asyncio
async def test_websocket():
    """Test WebSocket connection to Alpaca"""
    load_dotenv()
    
    api_key = os.getenv('ALPACA_API_KEY')
    secret_key = os.getenv('ALPACA_SECRET_KEY')
    
    print(f"Testing with API key: {api_key[:5]}...")
    
    # Check if market is open
    trading_client = TradingClient(api_key, secret_key, paper=True)
    clock = trading_client.get_clock()
    
    if not clock.is_open:
        next_open = clock.next_open.astimezone(pytz.timezone('America/New_York'))
        print(f"⚠️  Market is currently closed. Next open: {next_open}")
        print("Testing with delayed data...")
    
    # Flag to track if we received data
    received_data = False
    
    async def handle_quote(quote):
        nonlocal received_data
        received_data = True
        print(f"✅ Received quote: {quote.symbol} bid: ${quote.bid_price:.2f} ask: ${quote.ask_price:.2f}")
        
    async def handle_trade(trade):
        nonlocal received_data
        received_data = True
        print(f"✅ Received trade: {trade.symbol} @ ${trade.price:.2f}")
    
    try:
        client = StockDataStream(api_key, secret_key)
        
        # Subscribe to multiple active symbols
        symbols = ["SPY", "AAPL", "MSFT", "AMZN", "TSLA", "NVDA", "META", "GOOGL"]
        print(f"Subscribing to symbols: {', '.join(symbols)}")
        
        # Subscribe to both quotes and trades
        client.subscribe_quotes(handle_quote, *symbols)
        client.subscribe_trades(handle_trade, *symbols)
        
        print("Starting WebSocket connection...")
        print("Waiting for market data (30 seconds)...")
        
        # Run for 30 seconds or until we receive data
        try:
            await asyncio.wait_for(client._run_forever(), timeout=30.0)
        except asyncio.TimeoutError:
            print("❌ Timeout waiting for market data")
        except Exception as e:
            print(f"❌ Error during WebSocket operation: {e}")
        finally:
            await client.close()
        
        if not received_data:
            if not clock.is_open:
                pytest.skip("Market is closed - skipping test")
            else:
                assert False, "No market data received while market is open"
        
        return received_data
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        assert False, f"Test failed with error: {str(e)}"

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--capture=no"]) 