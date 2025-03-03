FROM python:3.9.18-alpine3.18

RUN apk add build-base

RUN apk add postgresql-dev gcc python3-dev musl-dev

ARG FLASK_APP
ARG FLASK_ENV
ARG DATABASE_URL
ARG SCHEMA
ARG SECRET_KEY

WORKDIR /var/www

COPY requirements.txt .

RUN pip install -r requirements.txt
RUN pip install psycopg2

COPY . .

# Remove existing migrations and recreate them
RUN rm -rf migrations/
RUN python -c "from app.models.db import db, SCHEMA; from app import app; with app.app_context(): db.session.execute(f'DROP SCHEMA IF EXISTS {SCHEMA} CASCADE'); db.session.execute(f'CREATE SCHEMA IF NOT EXISTS {SCHEMA}'); db.session.commit()"

# Initialize migrations
RUN flask db init
RUN flask db migrate -m "initial migration"
RUN flask db upgrade
# RUN flask db upgrade
# RUN flask seed all
CMD gunicorn app:app