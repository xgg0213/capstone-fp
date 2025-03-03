from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime
from sqlalchemy import event

class SymbolPrice(db.Model):
    __tablename__ = 'symbol_prices'

    if environment == "production":
        __table_args__ = (
            db.UniqueConstraint('symbol_id', 'date', name='unique_symbol_date'),
            {'schema': SCHEMA}
        )
    else:
        __table_args__ = (
            db.UniqueConstraint('symbol_id', 'date', name='unique_symbol_date'),
        )

    id = db.Column(db.Integer, primary_key=True)
    symbol_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('symbols.id')), nullable=False)
    date = db.Column(db.Date, nullable=False)
    open_price = db.Column(db.Float, nullable=False)
    close_price = db.Column(db.Float, nullable=False)
    high_price = db.Column(db.Float, nullable=False)
    low_price = db.Column(db.Float, nullable=False)
    volume = db.Column(db.BigInteger)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # Relationship
    symbol = db.relationship('Symbol', back_populates='price_history')

    def to_dict(self):
        return {
            'id': self.id,
            'symbol_id': self.symbol_id,
            'date': self.date.isoformat(),
            'open': self.open_price,
            'close': self.close_price,
            'high': self.high_price,
            'low': self.low_price,
            'volume': self.volume,
            'created_at': self.created_at.isoformat()
        }

    def update_symbol_current_price(self):
        """Update the associated symbol's current price data"""
        if self.symbol:
            self.symbol.current_price = self.close_price
            self.symbol.daily_high = self.high_price
            self.symbol.daily_low = self.low_price
            self.symbol.daily_volume = self.volume
            
            # Calculate price change percentage
            yesterday_price = SymbolPrice.query.filter(
                SymbolPrice.symbol_id == self.symbol_id,
                SymbolPrice.date < self.date
            ).order_by(SymbolPrice.date.desc()).first()
            
            if yesterday_price:
                price_change = ((self.close_price - yesterday_price.close_price) 
                              / yesterday_price.close_price * 100)
                self.symbol.price_change_pct = price_change
            
            self.symbol.last_updated = datetime.utcnow()

# SQLAlchemy event listeners
@event.listens_for(SymbolPrice, 'after_insert')
def update_symbol_on_insert(mapper, connection, target):
    target.update_symbol_current_price()

@event.listens_for(SymbolPrice, 'after_update')
def update_symbol_on_update(mapper, connection, target):
    target.update_symbol_current_price() 