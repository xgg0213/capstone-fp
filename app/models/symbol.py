from .db import db
from datetime import datetime

class Symbol(db.Model):
    __tablename__ = 'symbols'

    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False, unique=True)
    company_name = db.Column(db.String(255))
    current_price = db.Column(db.Numeric(10, 2), nullable=False)
    daily_high = db.Column(db.Numeric(10, 2))
    daily_low = db.Column(db.Numeric(10, 2))
    daily_volume = db.Column(db.Integer)
    price_change_pct = db.Column(db.Numeric(5, 2))
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Add relationships
    price_history = db.relationship('SymbolPrice', back_populates='symbol', order_by='desc(SymbolPrice.date)')
    portfolio_positions = db.relationship('Portfolio', back_populates='symbol')
    transactions = db.relationship('Transaction', back_populates='symbol')
    orders = db.relationship('Order', back_populates='symbol')
    watchlist_symbols = db.relationship('WatchlistSymbol', back_populates='symbol')

    def to_dict(self):
        # Get the latest price history
        latest_price = self.price_history[0] if self.price_history else None
        
        return {
            'id': self.id,
            'symbol': self.symbol,
            'company_name': self.company_name,
            'current_price': float(self.current_price) if self.current_price else None,
            'daily_high': float(self.daily_high) if self.daily_high else None,
            'daily_low': float(self.daily_low) if self.daily_low else None,
            'daily_volume': self.daily_volume,
            'price_change_pct': float(self.price_change_pct) if self.price_change_pct else None,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
            'price_history': [price.to_dict() for price in self.price_history[:30]]  # Last 30 days
        }

    def get_price_for_date(self, date):
        """Get the closing price for a specific date"""
        price_record = next(
            (price for price in self.price_history if price.date == date),
            None
        )
        return float(price_record.close_price) if price_record else None 

    @property
    def latest_price(self):
        """Get the most recent price data"""
        return self.price_history[0] if self.price_history else None

    def update_current_price(self):
        """Update current price from latest price history"""
        latest = self.latest_price
        if latest:
            self.current_price = latest.close_price
            self.daily_high = latest.high_price
            self.daily_low = latest.low_price
            self.daily_volume = latest.volume
            self.last_updated = datetime.utcnow()
            db.session.commit() 