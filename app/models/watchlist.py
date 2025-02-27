from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime

class Watchlist(db.Model):
    __tablename__ = 'watchlists'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Update relationship name from 'symbols' to 'watchlist_symbols'
    watchlist_symbols = db.relationship('WatchlistSymbol', back_populates='watchlist', cascade='all, delete-orphan')
    user = db.relationship('User', back_populates='watchlists')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'symbols': [symbol.to_dict() for symbol in self.watchlist_symbols],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 