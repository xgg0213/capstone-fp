from .db import db
from datetime import datetime

class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    symbol = db.Column(db.String(10), nullable=False)
    type = db.Column(db.String(10), nullable=False)  # buy, sell
    quantity = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)  # quantity * price
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='transactions')
    order = db.relationship('Order', back_populates='transactions')

    def to_dict(self):
        return {
            'transaction_id': str(self.id),
            'order_id': str(self.order_id) if self.order_id else None,
            'symbol': self.symbol,
            'type': self.type,
            'quantity': float(self.quantity),
            'price': float(self.price),
            'total_amount': float(self.total_amount),
            'timestamp': self.timestamp.isoformat()
        } 