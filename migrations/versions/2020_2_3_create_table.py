"""create table

Revision ID: e13528213bbc
Revises: 
Create Date: 2020-02-03 15:53:48.592792

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e13528213bbc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('remain_vacation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('google_id', sa.String(length=30), nullable=False),
    sa.Column('number_of_year', sa.Integer(), nullable=False),
    sa.Column('total_vacation', sa.Integer(), nullable=False),
    sa.Column('remain_vacation', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('used_vacation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('google_id', sa.String(length=30), nullable=False),
    sa.Column('start_date', sa.DateTime(), nullable=False),
    sa.Column('end_date', sa.DateTime(), nullable=False),
    sa.Column('type', sa.String(length=10), nullable=False),
    sa.Column('reference', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_info',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('google_id', sa.String(length=30), nullable=False),
    sa.Column('ko_name', sa.String(length=5), nullable=True),
    sa.Column('en_name', sa.String(length=10), nullable=False),
    sa.Column('entry_date', sa.DateTime(), nullable=True),
    sa.Column('admin', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_info')
    op.drop_table('used_vacation')
    op.drop_table('remain_vacation')
    # ### end Alembic commands ###
