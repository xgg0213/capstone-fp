from app import app
from app.models import db
from flask.cli import FlaskGroup

cli = FlaskGroup(app)

if __name__ == "__main__":
    cli() 