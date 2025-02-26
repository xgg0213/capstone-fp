from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime

class WatchlistSymbol(db.Model):
    __tablename__ = 'watchlist_symbols'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    watchlist_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('watchlists.id')), nullable=False)
    symbol = db.Column(db.String(10), nullable=False)
    company_name = db.Column(db.String(100))
    current_price = db.Column(db.Float)
    price_change = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    watchlist = db.relationship('Watchlist', back_populates='symbols')

    def to_dict(self):
        return {
            'id': self.id,
            'symbol': self.symbol,
            'company_name': self.company_name,
            'current_price': self.current_price,
            'price_change': self.price_change,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 