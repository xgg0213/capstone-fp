from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime

class Order(db.Model):
    __tablename__ = 'orders'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')), nullable=False)
    symbol_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('symbols.id')), nullable=False)
    shares = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(4), nullable=False)  # buy, sell
    status = db.Column(db.String(10), nullable=False, default='pending')  # pending, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = db.relationship('User', back_populates='orders')
    transactions = db.relationship('Transaction', back_populates='order')
    symbol = db.relationship('Symbol', back_populates='orders')

    def to_dict(self):
        symbol_data = self.symbol.to_dict() if self.symbol else {}
        
        return {
            'id': self.id,
            'user_id': self.user_id,
            'symbol': symbol_data.get('symbol'),
            'company_name': symbol_data.get('company_name'),
            'shares': float(self.shares),
            'type': self.type,
            'status': self.status,
            'current_price': float(symbol_data.get('current_price', 0)),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'transactions': [transaction.to_dict() for transaction in self.transactions]
        } 