from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime

class Portfolio(db.Model):
    __tablename__ = 'portfolios'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')), nullable=False)
    symbol = db.Column(db.String(10), nullable=False)
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

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'symbol': self.symbol,
            'shares': float(self.shares),
            'average_price': float(self.average_price),
            # 'company_name': self.company_name,
            # 'current_price': float(self.current_price) if self.current_price else None,
            # 'day_change': float(self.day_change) if self.day_change else 0,
            # 'total_return': float(self.total_return) if self.total_return else 0,
            'market_value': float(self.shares * self.average_price),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 