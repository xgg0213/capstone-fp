from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime

class WatchlistSymbol(db.Model):
    __tablename__ = 'watchlist_symbols'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    watchlist_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('watchlists.id')), nullable=False)
    symbol_id = db.Column(db.Integer, db.ForeignKey('symbols.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    watchlist = db.relationship('Watchlist', back_populates='watchlist_symbols')
    symbol = db.relationship('Symbol', back_populates='watchlist_symbols')

    def to_dict(self):
        symbol_data = self.symbol.to_dict() if self.symbol else {}
        
        return {
            'id': self.id,
            'watchlist_id': self.watchlist_id,
            'symbol': symbol_data.get('symbol'),
            'company_name': symbol_data.get('company_name'),
            'current_price': float(symbol_data.get('current_price', 0)),
            'price_change_pct': float(symbol_data.get('price_change_pct', 0)),
            'created_at': self.created_at.isoformat()
        } 