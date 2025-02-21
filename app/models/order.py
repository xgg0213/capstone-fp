from .db import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    symbol = db.Column(db.String(10), nullable=False)
    order_type = db.Column(db.String(10), nullable=False)  # market or limit
    side = db.Column(db.String(4), nullable=False)  # buy or sell
    quantity = db.Column(db.Float, nullable=False)
    limit_price = db.Column(db.Float)
    status = db.Column(db.String(10), nullable=False)  # pending, filled, cancelled
    filled_quantity = db.Column(db.Float, default=0)
    filled_price = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', back_populates='orders')
    transactions = db.relationship('Transaction', back_populates='order')

    def to_dict(self):
        return {
            'order_id': str(self.id),
            'symbol': self.symbol,
            'type': self.order_type,
            'side': self.side,
            'quantity': float(self.quantity),
            'status': self.status,
            'filled_quantity': float(self.filled_quantity) if self.filled_quantity else 0,
            'filled_price': float(self.filled_price) if self.filled_price else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def execute_transaction(self, quantity, price):
        """
        Execute a transaction for this order
        """
        from app.models import Transaction, Portfolio
        
        # Create transaction
        transaction = Transaction(
            user_id=self.user_id,
            order_id=self.id,
            symbol=self.symbol,
            type=self.side,
            quantity=quantity,
            price=price,
            total_amount=quantity * price
        )
        
        # Update order status
        self.filled_quantity += quantity
        self.filled_price = price
        
        if self.filled_quantity >= self.quantity:
            self.status = 'filled'
        else:
            self.status = 'partially_filled'
            
        # Update portfolio
        portfolio = Portfolio.query.filter_by(user_id=self.user_id).first()
        if self.side == 'buy':
            portfolio.cash_balance -= transaction.total_amount
        else:
            portfolio.cash_balance += transaction.total_amount
            
        db.session.add(transaction)
        db.session.add(self)
        db.session.add(portfolio)
        db.session.commit()
        
        return transaction 