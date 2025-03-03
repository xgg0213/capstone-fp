from flask.cli import AppGroup
from .users import seed_users, undo_users
from .symbols import seed_symbols, undo_symbols
from .symbol_prices import seed_symbol_prices, undo_symbol_prices
from .watchlists import seed_watchlists, undo_watchlists
from .watchlist_symbols import seed_watchlist_symbols, undo_watchlist_symbols
from .portfolios import seed_portfolios, undo_portfolios
from .orders import seed_orders, undo_orders
from .transactions import seed_transactions, undo_transactions
from app.models.db import db, environment, SCHEMA

# Creates a seed group to hold our commands
# So we can type `flask seed --help`
seed_commands = AppGroup('seed')

def setup_schema():
    """
    Sets up schema for production database
    """
    if environment == "production":
        db.session.execute(f'CREATE SCHEMA IF NOT EXISTS {SCHEMA}')
        db.session.commit()

def undo_tables():
    """Safely undo tables if they exist"""
    if environment == "production":
        try:
            db.session.execute(f'DROP SCHEMA IF EXISTS {SCHEMA} CASCADE')
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error dropping schema: {e}")
        
        # Recreate schema
        db.session.execute(f'CREATE SCHEMA IF NOT EXISTS {SCHEMA}')
        db.session.commit()

# Creates the `flask seed all` command
@seed_commands.command('all')
def seed():
    setup_schema()
    if environment == "production":
        # Instead of trying to truncate tables that might not exist,
        # just drop and recreate the schema
        undo_tables()

    # Seed in proper order based on dependencies
    seed_users()
    seed_symbols()
    seed_symbol_prices()
    seed_watchlists()
    seed_watchlist_symbols()
    seed_portfolios()
    seed_orders()
    seed_transactions()


# Creates the `flask seed undo` command
@seed_commands.command('undo')
def undo():
    if environment == "production":
        undo_tables()
    else:
        undo_transactions()
        undo_orders()
        undo_portfolios()
        undo_watchlist_symbols()
        undo_watchlists()
        undo_symbol_prices()
        undo_symbols()
        undo_users()
