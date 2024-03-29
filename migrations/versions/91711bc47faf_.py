"""empty message

Revision ID: 91711bc47faf
Revises: 88ca65840f3b
Create Date: 2020-03-24 15:52:49.119391

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '91711bc47faf'
down_revision = '88ca65840f3b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('personal_information', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key("fk_personal_info", 'personal_information', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("fk_personal_info", 'personal_information', type_='foreignkey')
    op.drop_column('personal_information', 'user_id')
    # ### end Alembic commands ###
