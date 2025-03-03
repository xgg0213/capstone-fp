from flask.cli import AppGroup
from .users import seed_users, undo_users
from .orders import seed_orders, undo_orders
from .portfolios import seed_portfolios, undo_portfolios
from .transactions import seed_transactions, undo_transactions
from .watchlists import seed_watchlists, undo_watchlists
from .symbols import seed_symbols, undo_symbols
# from .symbol_prices import seed_symbol_prices, undo_symbol_prices
from .symbol_prices import seed_symbol_prices, undo_symbol_prices
from .watchlist_symbols import seed_watchlist_symbols, undo_watchlist_symbols
from app.models.db import db, environment, SCHEMA

# Creates a seed group to hold our commands
# So we can type `flask seed --help`
seed_commands = AppGroup('seed')


# Creates the `flask seed all` command
@seed_commands.command('all')
def seed():
    if environment == 'production':
        # Before seeding, in reverse order
        undo_watchlist_symbols()  # Clear symbols before watchlists
        undo_watchlists()
        undo_transactions()
        undo_portfolios()
        undo_orders()
        undo_symbol_prices()
        undo_symbols()
        undo_users()
    
    seed_users()
    seed_symbols()
    seed_symbol_prices()
    seed_orders()
    seed_portfolios()
    seed_transactions()
    seed_watchlists()
    seed_watchlist_symbols()  # Seed symbols after watchlists


# Creates the `flask seed undo` command
@seed_commands.command('undo')
def undo():
    # Undo in reverse order of dependencies
    undo_watchlist_symbols()  # Clear symbols before watchlists
    undo_watchlists()
    undo_transactions()
    undo_portfolios()
    undo_orders()
    undo_symbol_prices()
    undo_symbols()
    undo_users()
