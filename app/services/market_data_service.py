import asyncio
import aiohttp
from datetime import datetime, timedelta
from flask import current_app
from .websocket_service import broadcast_price_update
from alpaca.data.live import StockDataStream
from alpaca.trading.client import TradingClient
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest, StockQuotesRequest
from alpaca.data.timeframe import TimeFrame
import pytz

class AlpacaMarketDataService:
    def __init__(self):
        self.prices = {}  # Cache of current prices
        self.previous_close = {}  # Cache of previous closing prices
        self.initialized = False
        self.last_closing_prices = {}  # Cache for closing prices
        
    def initialize(self):
        """Initialize Alpaca clients"""
        if self.initialized:
            return
            
        api_key = current_app.config['ALPACA_API_KEY']
        secret_key = current_app.config['ALPACA_SECRET_KEY']
        
        # Initialize clients
        self.trading_client = TradingClient(api_key, secret_key, paper=current_app.config['ALPACA_PAPER_TRADING'])
        self.data_stream = StockDataStream(api_key, secret_key)
        self.historical_client = StockHistoricalDataClient(api_key, secret_key)
        
        self.initialized = True
        
    async def connect_to_market_feed(self):
        """Connect to Alpaca's WebSocket feed"""
        self.initialize()
        
        # Initial symbols to track (you can add more)
        self.symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'NFLX']
        
        # Get previous closing prices
        await self.update_previous_close()
        
        # Subscribe to trade updates
        self.data_stream.subscribe_trades(self.handle_trade, *self.symbols)
        self.data_stream.subscribe_quotes(self.handle_quote, *self.symbols)
        
        # Start streaming
        await self.data_stream.run()
        
    async def handle_trade(self, trade):
        """Handle incoming trade data"""
        symbol = trade.symbol
        price = trade.price
        
        if symbol not in self.prices:
            self.prices[symbol] = {
                'price': price,
                'change': 0,
                'change_percent': 0,
                'volume': 0,
                'timestamp': None
            }
            
        prev_close = self.previous_close.get(symbol)
        if prev_close:
            change = price - prev_close
            change_percent = (change / prev_close) * 100
        else:
            change = 0
            change_percent = 0
            
        self.prices[symbol].update({
            'price': price,
            'change': change,
            'change_percent': change_percent,
            'timestamp': datetime.utcnow().isoformat()
        })
        
        broadcast_price_update(symbol, self.prices[symbol])
        
    async def handle_quote(self, quote):
        """Handle incoming quote data"""
        symbol = quote.symbol
        if symbol in self.prices:
            self.prices[symbol].update({
                'bid': quote.bid_price,
                'ask': quote.ask_price,
                'bid_size': quote.bid_size,
                'ask_size': quote.ask_size
            })
            
    async def update_previous_close(self):
        """Get previous day's closing prices"""
        end = datetime.now()
        start = end - timedelta(days=5)  # Get 5 days of data in case of holidays
        
        request = StockBarsRequest(
            symbol_or_symbols=self.symbols,
            timeframe=TimeFrame.Day,
            start=start,
            end=end
        )
        
        bars = self.historical_client.get_stock_bars(request)
        
        for symbol in self.symbols:
            if symbol in bars:
                symbol_bars = bars[symbol]
                if symbol_bars:
                    # Get the most recent closing price
                    self.previous_close[symbol] = symbol_bars[-1].close
                    
    async def get_historical_data(self, symbol, timeframe='1D', limit=100):
        """Get historical price data"""
        self.initialize()
        
        # Convert timeframe string to Alpaca TimeFrame
        timeframe_map = {
            '1D': TimeFrame.Day,
            '1H': TimeFrame.Hour,
            '15Min': TimeFrame.Minute(15),
            '5Min': TimeFrame.Minute(5),
            '1Min': TimeFrame.Minute
        }
        
        tf = timeframe_map.get(timeframe, TimeFrame.Day)
        end = datetime.now()
        start = end - timedelta(days=100)  # Adjust based on timeframe
        
        request = StockBarsRequest(
            symbol_or_symbols=symbol,
            timeframe=tf,
            start=start,
            end=end
        )
        
        bars = self.historical_client.get_stock_bars(request)
        
        return [
            {
                'timestamp': bar.timestamp.isoformat(),
                'open': bar.open,
                'high': bar.high,
                'low': bar.low,
                'close': bar.close,
                'volume': bar.volume
            }
            for bar in bars[symbol]
        ]
        
    def get_current_price(self, symbol):
        """Get current price from cache"""
        return self.prices.get(symbol)
        
    async def add_symbol(self, symbol):
        """Add a new symbol to track"""
        if symbol not in self.symbols:
            self.symbols.append(symbol)
            await self.update_previous_close()
            self.data_stream.subscribe_trades(self.handle_trade, symbol)
            self.data_stream.subscribe_quotes(self.handle_quote, symbol)

    async def handle_connection_error(self, error):
        """Handle connection errors"""
        print(f"Connection error: {error}")
        # Wait and try to reconnect
        await asyncio.sleep(5)
        try:
            await self.connect_to_market_feed()
        except Exception as e:
            await self.handle_connection_error(e)

    def is_market_open(self):
        """Check if market is currently open"""
        try:
            clock = self.trading_client.get_clock()
            return clock.is_open
        except:
            # Default to checking time if API fails
            et_time = datetime.now(pytz.timezone('America/New_York'))
            is_weekday = et_time.weekday() < 5
            is_market_hours = 9.5 <= et_time.hour + (et_time.minute/60) < 16
            return is_weekday and is_market_hours
            
    async def get_price(self, symbol):
        """Get price data based on market status"""
        if self.is_market_open():
            return self.get_current_price(symbol)
        else:
            return self.get_last_closing_price(symbol)
            
    async def update_closing_prices(self):
        """Cache closing prices when market closes"""
        for symbol in self.symbols:
            last_bar = await self.get_last_bar(symbol)
            if last_bar:
                self.last_closing_prices[symbol] = {
                    'price': last_bar.close,
                    'timestamp': last_bar.timestamp,
                    'market_closed': True
                }

market_data_service = AlpacaMarketDataService() 