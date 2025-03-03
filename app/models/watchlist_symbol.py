from .db import db, environment, SCHEMA, add_prefix_for_prod

class WatchlistSymbol(db.Model):
    __tablename__ = 'watchlist_symbols'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    watchlist_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('watchlists.id')), nullable=False)
    symbol_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('symbols.id')), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # Relationships
    watchlist = db.relationship('Watchlist', back_populates='watchlist_symbols')
    symbol = db.relationship('Symbol', back_populates='watchlist_symbols')

    # Add unique constraint to prevent duplicate symbols in a watchlist
    __table_args__ = (
        db.UniqueConstraint('watchlist_id', 'symbol_id', name='unique_watchlist_symbol'),
        {'schema': SCHEMA} if environment == "production" else None
    )

    def to_dict(self):
        return {
            'id': self.id,
            'watchlist_id': self.watchlist_id,
            'symbol_id': self.symbol_id,
            'created_at': self.created_at,
            'symbol': self.symbol.to_dict() if self.symbol else None
        } 