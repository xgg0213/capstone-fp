from flask.cli import AppGroup
from .seeds import seed_commands

def init_commands(app):
    """Initialize CLI commands"""
    app.cli.add_command(seed_commands) 