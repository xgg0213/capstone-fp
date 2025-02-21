from flask.cli import AppGroup
from .users import seed_users, undo_users
from .portfolios import seed_portfolios, undo_portfolios
from .orders import seed_orders, undo_orders
from .transactions import seed_transactions, undo_transactions
from .watchlists import seed_watchlists, undo_watchlists
from app.models.db import db, environment, SCHEMA

# Creates a seed group to hold our commands
# So we can type `flask seed --help`
seed_commands = AppGroup('seed')


# Creates the `flask seed all` command
@seed_commands.command('all')
def seed():
    if environment == 'production':
        # Before seeding in production, truncate all tables
        undo_watchlists()
        undo_transactions()
        undo_orders()
        undo_portfolios()
        undo_users()
        
    seed_users()
    seed_portfolios()
    seed_orders()
    seed_transactions()
    seed_watchlists()


# Creates the `flask seed undo` command
@seed_commands.command('undo')
def undo():
    # Undo in reverse order of dependencies
    undo_watchlists()
    undo_transactions()
    undo_orders()
    undo_portfolios()
    undo_users()
