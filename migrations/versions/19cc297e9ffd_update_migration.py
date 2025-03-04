"""update migration

Revision ID: 19cc297e9ffd
Revises: 
Create Date: 2025-03-02 23:51:22.089581

"""

from alembic import op
import sqlalchemy as sa

import os
environment = os.getenv("FLASK_ENV")
SCHEMA = os.environ.get("SCHEMA")

# ffdc0a98111c, 3d50099a1157
# revision identifiers, used by Alembic.
revision = '19cc297e9ffd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('symbols',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('symbol', sa.String(length=10), nullable=False),
    sa.Column('company_name', sa.String(length=255), nullable=False),
    sa.Column('current_price', sa.Float(), nullable=False),
    sa.Column('daily_high', sa.Float(), nullable=True),
    sa.Column('daily_low', sa.Float(), nullable=True),
    sa.Column('daily_volume', sa.BigInteger(), nullable=True),
    sa.Column('price_change_pct', sa.Float(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('symbol')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=40), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('hashed_password', sa.String(length=255), nullable=False),
    sa.Column('balance', sa.Float(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('symbol_id', sa.Integer(), nullable=False),
    sa.Column('shares', sa.Float(), nullable=False),
    sa.Column('type', sa.String(length=4), nullable=False),
    sa.Column('status', sa.String(length=10), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['symbol_id'], ['symbols.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('portfolios',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('symbol_id', sa.Integer(), nullable=False),
    sa.Column('shares', sa.Float(), nullable=False),
    sa.Column('average_price', sa.Float(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['symbol_id'], ['symbols.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('symbol_prices',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('symbol_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('open_price', sa.Float(), nullable=False),
    sa.Column('close_price', sa.Float(), nullable=False),
    sa.Column('high_price', sa.Float(), nullable=False),
    sa.Column('low_price', sa.Float(), nullable=False),
    sa.Column('volume', sa.BigInteger(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.ForeignKeyConstraint(['symbol_id'], ['symbols.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('symbol_id', 'date', name='unique_symbol_date')
    )
    op.create_table('watchlists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('transactions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('symbol_id', sa.Integer(), nullable=False),
    sa.Column('shares', sa.Float(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('type', sa.String(length=4), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.ForeignKeyConstraint(['symbol_id'], ['symbols.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('watchlist_symbols',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('watchlist_id', sa.Integer(), nullable=False),
    sa.Column('symbol_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.ForeignKeyConstraint(['symbol_id'], ['symbols.id'], ),
    sa.ForeignKeyConstraint(['watchlist_id'], ['watchlists.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('watchlist_id', 'symbol_id', name='unique_watchlist_symbol')
    )
    # ### end Alembic commands ###

    # Ensure to mannually add this part to ensure Render deployment is successful, specific to this situation
    if environment == "production":
        op.execute(f"ALTER TABLE users SET SCHEMA {SCHEMA};")
        op.execute(f"ALTER TABLE orders SET SCHEMA {SCHEMA};")
        op.execute(f"ALTER TABLE portfolios SET SCHEMA {SCHEMA};")
        op.execute(f"ALTER TABLE symbols SET SCHEMA {SCHEMA};")
        op.execute(f"ALTER TABLE symbol_prices SET SCHEMA {SCHEMA};")
        op.execute(f"ALTER TABLE transactions SET SCHEMA {SCHEMA};")
        op.execute(f"ALTER TABLE watchlists SET SCHEMA {SCHEMA};")
        op.execute(f"ALTER TABLE watchlist_symbols SET SCHEMA {SCHEMA};")


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('watchlist_symbols')
    op.drop_table('transactions')
    op.drop_table('watchlists')
    op.drop_table('symbol_prices')
    op.drop_table('portfolios')
    op.drop_table('orders')
    op.drop_table('users')
    op.drop_table('symbols')
    # ### end Alembic commands ###
