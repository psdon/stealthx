"""empty message

Revision ID: d39ffb7252c5
Revises: 91711bc47faf
Create Date: 2020-03-26 09:15:40.024541

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd39ffb7252c5'
down_revision = '91711bc47faf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('session_token', sa.String(length=32), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'session_token')
    # ### end Alembic commands ###
