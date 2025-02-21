from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime

class Order(db.Model):
    __tablename__ = 'orders'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')), nullable=False)
    symbol = db.Column(db.String(10), nullable=False)
    order_type = db.Column(db.String(10), nullable=False)  # 'market' or 'limit'
    side = db.Column(db.String(4), nullable=False)  # 'buy' or 'sell'
    shares = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float)  # Required for limit orders
    status = db.Column(db.String(10), nullable=False)  # 'pending', 'filled', 'cancelled'
    filled_price = db.Column(db.Float)  # Price at which order was filled
    filled_at = db.Column(db.DateTime)  # When the order was filled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = db.relationship('User', back_populates='orders')
    transactions = db.relationship('Transaction', back_populates='order', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'symbol': self.symbol,
            'order_type': self.order_type,
            'side': self.side,
            'shares': float(self.shares),  # Convert to float for JSON
            'price': float(self.price) if self.price else None,  # Handle None case
            'status': self.status,
            'filled_price': float(self.filled_price) if self.filled_price else None,
            'filled_at': self.filled_at.isoformat() if self.filled_at else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 