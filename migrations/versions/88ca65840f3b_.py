"""empty message

Revision ID: 88ca65840f3b
Revises: ba42e32f9f0e
Create Date: 2020-03-24 15:25:50.600304

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '88ca65840f3b'
down_revision = 'ba42e32f9f0e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('personal_information',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=40), nullable=False),
    sa.Column('middle_name', sa.String(length=30), nullable=True),
    sa.Column('last_name', sa.String(length=30), nullable=False),
    sa.Column('mobile_number', sa.String(length=20), nullable=False),
    sa.Column('address_1', sa.String(length=50), nullable=False),
    sa.Column('address_2', sa.String(length=50), nullable=False),
    sa.Column('region', sa.String(length=50), nullable=False),
    sa.Column('city', sa.String(length=50), nullable=False),
    sa.Column('zip_code', sa.Integer(), nullable=False),
    sa.Column('country', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('personal_information')
    # ### end Alembic commands ###
