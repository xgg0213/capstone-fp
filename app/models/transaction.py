from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime

class Transaction(db.Model):
    __tablename__ = 'transactions'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('orders.id')))
    symbol = db.Column(db.String(10), nullable=False)
    shares = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(4), nullable=False)  # buy, sell
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship('User', back_populates='transactions')
    order = db.relationship('Order', back_populates='transactions')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'order_id': self.order_id,
            'symbol': self.symbol,
            'shares': float(self.shares),
            'price': float(self.price),
            'type': self.type,
            'total': float(self.shares * self.price),
            'created_at': self.created_at.isoformat()
        } 