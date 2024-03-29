"""empty message

Revision ID: 504fe8bfd6f6
Revises: 170338268dd3
Create Date: 2020-04-14 15:46:37.722101

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '504fe8bfd6f6'
down_revision = '170338268dd3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('paymongo_payment_transactions', sa.Column('subscription_type_id', sa.Integer(), nullable=True))
    op.drop_constraint('paymongo_payment_transactions_ibfk_1', 'paymongo_payment_transactions', type_='foreignkey')
    op.create_foreign_key("subscription_type_id_fk", 'paymongo_payment_transactions', 'subscription_type', ['subscription_type_id'], ['id'], ondelete='CASCADE')
    op.drop_column('paymongo_payment_transactions', 'subscription_plan_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('paymongo_payment_transactions', sa.Column('subscription_plan_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_constraint("subscription_type_id_fk", 'paymongo_payment_transactions', type_='foreignkey')
    op.create_foreign_key('paymongo_payment_transactions_ibfk_1', 'paymongo_payment_transactions', 'subscription_plan', ['subscription_plan_id'], ['id'], ondelete='CASCADE')
    op.drop_column('paymongo_payment_transactions', 'subscription_type_id')
    # ### end Alembic commands ###
