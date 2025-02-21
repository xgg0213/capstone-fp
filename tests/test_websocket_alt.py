import asyncio
from alpaca.data.live import StockDataStream
import os
from dotenv import load_dotenv

async def test_websocket():
    load_dotenv()
    
    api_key = os.getenv('ALPACA_API_KEY')
    secret_key = os.getenv('ALPACA_SECRET_KEY')
    
    print(f"Testing with API key: {api_key[:5]}...")
    
    async def process_trade(trade):
        print(f"✅ Received trade: {trade.symbol} @ ${trade.price}")
        return True
    
    try:
        async with StockDataStream(api_key, secret_key) as stream:
            stream.subscribe_trades(process_trade, "AAPL")
            print("Waiting for trade data (30 seconds)...")
            
            try:
                await asyncio.wait_for(stream._run_forever(), timeout=30)
            except asyncio.TimeoutError:
                print("❌ Timeout waiting for trade data")
                return False
            except Exception as e:
                print(f"Error during stream: {e}")
                return False
                
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    try:
        success = asyncio.run(test_websocket())
        if success:
            print("✅ WebSocket test completed successfully!")
        else:
            print("❌ WebSocket test failed")
    except KeyboardInterrupt:
        print("Test stopped by user") 