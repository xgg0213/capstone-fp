from .db import db, environment, SCHEMA, add_prefix_for_prod

class WatchlistSymbol(db.Model):
    __tablename__ = 'watchlist_symbols'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    watchlist_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('watchlists.id')), nullable=False)
    symbol_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('symbols.id')), nullable=False)

    # Relationships
    watchlist = db.relationship('Watchlist', back_populates='watchlist_symbols')
    symbol = db.relationship('Symbol', primaryjoin="WatchlistSymbol.symbol_id==Symbol.id", back_populates='watchlist_symbols')

    def to_dict(self):
        return {
            'id': self.id,
            'watchlist_id': self.watchlist_id,
            'symbol_id': self.symbol_id
        } 