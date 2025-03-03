from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime

class Symbol(db.Model):
    __tablename__ = 'symbols'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False, unique=True)
    company_name = db.Column(db.String(255), nullable=False)
    current_price = db.Column(db.Float, nullable=False)
    daily_high = db.Column(db.Float)
    daily_low = db.Column(db.Float)
    daily_volume = db.Column(db.BigInteger)
    price_change_pct = db.Column(db.Float)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    # Relationships
    price_history = db.relationship('SymbolPrice', back_populates='symbol', order_by='desc(SymbolPrice.date)', cascade='all, delete-orphan')
    portfolio_positions = db.relationship('Portfolio', back_populates='symbol', cascade='all, delete-orphan')
    transactions = db.relationship('Transaction', back_populates='symbol', cascade='all, delete-orphan')
    orders = db.relationship('Order', back_populates='symbol', cascade='all, delete-orphan')
    watchlist_symbols = db.relationship('WatchlistSymbol', back_populates='symbol', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'symbol': self.symbol,
            'company_name': self.company_name,
            'current_price': self.current_price,
            'daily_high': self.daily_high,
            'daily_low': self.daily_low,
            'daily_volume': self.daily_volume,
            'price_change_pct': self.price_change_pct,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
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
            self.updated_at = datetime.utcnow()
            db.session.commit() 