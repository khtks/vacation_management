"""add test column

Revision ID: 9379edc69e61
Revises: 
Create Date: 2020-01-17 16:52:52.357487

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9379edc69e61'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('test', sa.String(length=20), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'test')
    # ### end Alembic commands ###
