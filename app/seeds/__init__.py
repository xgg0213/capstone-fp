from flask.cli import AppGroup
from .users import seed_users, undo_users
from .orders import seed_orders, undo_orders
from .portfolios import seed_portfolios, undo_portfolios
from .transactions import seed_transactions, undo_transactions
from .watchlists import seed_watchlists, undo_watchlists
from .symbols import seed_symbols, undo_symbols
from app.models.db import db, environment, SCHEMA

# Creates a seed group to hold our commands
# So we can type `flask seed --help`
seed_commands = AppGroup('seed')


# Creates the `flask seed all` command
@seed_commands.command('all')
def seed():
    if environment == 'production':
        # Before seeding, in reverse order
        undo_watchlists()
        undo_transactions()  # Transactions before orders
        undo_portfolios()
        undo_orders()       # Orders before symbols
        undo_symbols()
        undo_users()
    
    seed_users()
    seed_symbols()
    seed_orders()          # Orders before transactions
    seed_portfolios()
    seed_transactions()    # Transactions after orders
    seed_watchlists()


# Creates the `flask seed undo` command
@seed_commands.command('undo')
def undo():
    # Undo in reverse order of dependencies
    undo_watchlists()
    undo_transactions()
    undo_portfolios()
    undo_orders()
    undo_users()
    undo_symbols()
