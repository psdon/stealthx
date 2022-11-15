"""empty message

Revision ID: d52243a37098
Revises: 8e62e8e8638a
Create Date: 2019-12-20 08:23:00.320159

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd52243a37098'
down_revision = '8e62e8e8638a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('c_dat',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('data', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('c_dat')
    # ### end Alembic commands ###
