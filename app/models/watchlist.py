from .db import db, environment, SCHEMA, add_prefix_for_prod

class Watchlist(db.Model):
    __tablename__ = 'watchlists'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())

    # Relationships
    user = db.relationship('User', back_populates='watchlists')
    watchlist_symbols = db.relationship('WatchlistSymbol', back_populates='watchlist', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'symbols': [
                {
                    'id': ws.symbol.id,
                    'symbol': ws.symbol.symbol,
                    'company_name': ws.symbol.company_name,
                    'current_price': float(ws.symbol.current_price) if ws.symbol.current_price else None,
                    'price_change': float(ws.symbol.price_change_pct) if ws.symbol.price_change_pct else None
                } for ws in self.watchlist_symbols
            ],
            'created_at': self.created_at,
            'updated_at': self.updated_at
        } 