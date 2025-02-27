from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime

class Transaction(db.Model):
    __tablename__ = 'transactions'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('orders.id')))
    symbol_id = db.Column(db.Integer, db.ForeignKey('symbols.id'), nullable=False)
    shares = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)  # Price at time of transaction
    type = db.Column(db.String(4), nullable=False)  # buy, sell
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship('User', back_populates='transactions')
    order = db.relationship('Order', back_populates='transactions')
    symbol = db.relationship('Symbol', back_populates='transactions')

    def to_dict(self):
        symbol_data = self.symbol.to_dict() if self.symbol else {}
        total = float(self.shares * self.price)
        
        # Calculate gain/loss for sell transactions
        gain_loss = None
        if self.type == 'sell':
            current_price = float(symbol_data.get('current_price', 0))
            gain_loss = float((self.price - current_price) * self.shares)

        return {
            'id': self.id,
            'user_id': self.user_id,
            'order_id': self.order_id,
            'symbol': symbol_data.get('symbol'),  # Get symbol string from Symbol model
            'company_name': symbol_data.get('company_name'),
            'shares': float(self.shares),
            'price': float(self.price),  # Historical price when transaction occurred
            'current_price': float(symbol_data.get('current_price', 0)),  # Current price from symbol
            'type': self.type,
            'total': total,
            'gain_loss': gain_loss,  # Only for sell transactions
            'created_at': self.created_at.isoformat()
        } 