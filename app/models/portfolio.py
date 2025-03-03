from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime

class Portfolio(db.Model):
    __tablename__ = 'portfolios'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')), nullable=False)
    symbol_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('symbols.id')), nullable=False)
    shares = db.Column(db.Float, nullable=False, default=0)
    average_price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # company_name = db.Column(db.String(50))
    # current_price = db.Column(db.Float)
    # day_change = db.Column(db.Float)
    # total_return = db.Column(db.Float)

    # Relationships
    user = db.relationship('User', back_populates='portfolios')
    symbol = db.relationship('Symbol', back_populates='portfolio_positions')

    def to_dict(self):
        symbol_data = self.symbol.to_dict() if self.symbol else {}
        current_price = float(symbol_data.get('current_price', 0))
        price_change = float(symbol_data.get('price_change_pct', 0))
        
        # Calculate total return percentage
        total_return = ((current_price - self.average_price) / self.average_price * 100) if self.average_price > 0 else 0

        return {
            'id': self.id,
            'user_id': self.user_id,
            'symbol': symbol_data.get('symbol'),  # Get symbol string from Symbol model
            'company_name': symbol_data.get('company_name'),
            'shares': float(self.shares),
            'average_price': float(self.average_price),
            'current_price': current_price,
            'market_value': float(self.shares * current_price),
            'total_cost': float(self.shares * self.average_price),
            'total_return': float(total_return),
            'day_change': price_change,
            'unrealized_gain': float(self.shares * (current_price - self.average_price)),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 