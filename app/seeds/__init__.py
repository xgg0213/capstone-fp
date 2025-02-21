from flask.cli import AppGroup

# Create the group first
seed_commands = AppGroup('seed')

# Import the individual seed functions
from .users import seed_users, undo_users
from .portfolios import seed_portfolios, undo_portfolios
from .transactions import seed_transactions, undo_transactions
from .orders import seed_orders, undo_orders

# Define the seed commands
@seed_commands.command('all')
def seed():
    """Run all seed functions"""
    seed_users()
    seed_portfolios()
    seed_transactions()
    seed_orders()

@seed_commands.command('undo')
def undo():
    """Undo all seeds"""
    undo_orders()
    undo_transactions()
    undo_portfolios()
    undo_users()
