"""Initial migration with PostgreSQL

Revision ID: c610150352c6
Revises: 
Create Date: 2024-12-07 18:21:21.008593

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c610150352c6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('customers',
    sa.Column('id', sa.String(length=100), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('phone', sa.String(length=20), nullable=False),
    sa.Column('_password_hash', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone')
    )
    op.create_table('drivers',
    sa.Column('id', sa.String(length=100), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('phone', sa.String(length=20), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('car_type', sa.String(length=100), nullable=False),
    sa.Column('online', sa.Boolean(), nullable=True),
    sa.Column('latitude', sa.Float(), nullable=False),
    sa.Column('longitude', sa.Float(), nullable=False),
    sa.Column('_password_hash', sa.String(length=128), nullable=False),
    sa.Column('license_number', sa.String(length=100), nullable=False),
    sa.Column('id_number', sa.String(length=100), nullable=False),
    sa.Column('license_plate', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone')
    )
    op.create_table('orders',
    sa.Column('id', sa.String(length=100), nullable=False),
    sa.Column('vehicle_type', sa.String(length=50), nullable=False),
    sa.Column('distance', sa.Float(), nullable=False),
    sa.Column('loaders', sa.Integer(), nullable=False),
    sa.Column('loader_cost', sa.Float(), nullable=False),
    sa.Column('total_cost', sa.Float(), nullable=False),
    sa.Column('user_lat', sa.Float(), nullable=False),
    sa.Column('user_lng', sa.Float(), nullable=False),
    sa.Column('dest_lat', sa.Float(), nullable=False),
    sa.Column('dest_lng', sa.Float(), nullable=False),
    sa.Column('time', sa.String(length=100), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('driver_id', sa.String(length=100), nullable=True),
    sa.Column('customer_id', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ),
    sa.ForeignKeyConstraint(['driver_id'], ['drivers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vehicles',
    sa.Column('id', sa.String(length=100), nullable=False),
    sa.Column('body_type', sa.String(length=50), nullable=False),
    sa.Column('plate_no', sa.String(length=20), nullable=False),
    sa.Column('driver_id', sa.String(length=100), nullable=True),
    sa.Column('customer_id', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ),
    sa.ForeignKeyConstraint(['driver_id'], ['drivers.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('plate_no')
    )
    op.create_table('rides',
    sa.Column('id', sa.String(length=100), nullable=False),
    sa.Column('distance', sa.Float(), nullable=False),
    sa.Column('created_time', sa.DateTime(), nullable=True),
    sa.Column('loader_cost', sa.Float(), nullable=False),
    sa.Column('from_location', sa.String(length=100), nullable=False),
    sa.Column('to_location', sa.String(length=100), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('order_id', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ratings',
    sa.Column('id', sa.String(length=100), nullable=False),
    sa.Column('rating_score', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.String(length=100), nullable=True),
    sa.Column('ride_id', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.ForeignKeyConstraint(['ride_id'], ['rides.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ratings')
    op.drop_table('rides')
    op.drop_table('vehicles')
    op.drop_table('orders')
    op.drop_table('drivers')
    op.drop_table('customers')
    # ### end Alembic commands ###
