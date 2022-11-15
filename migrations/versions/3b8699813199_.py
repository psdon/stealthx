"""empty message

Revision ID: 3b8699813199
Revises: b25c77ca8d93
Create Date: 2020-05-27 11:01:00.148556

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b8699813199'
down_revision = 'b25c77ca8d93'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('quest_chapter',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('num', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=45), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('video_url', sa.Text(), nullable=True),
    sa.Column('video_orig_filename', sa.Text(), nullable=True),
    sa.Column('quest_book_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(('quest_book_id', ), ['quest_book.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('quest',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('quest', sa.Text(), nullable=False),
    sa.Column('answer', sa.String(length=255), nullable=True),
    sa.Column('quest_chapter_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(("quest_chapter_id", ), ['quest_chapter.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('quest_book', sa.Column('code', sa.String(length=45), nullable=False))
    op.create_unique_constraint("quest_book_code_unique_constraint", 'quest_book', ['code'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("quest_book_code_unique_constraint", 'quest_book', type_='unique')
    op.drop_column('quest_book', 'code')
    op.drop_table('quest')
    op.drop_table('quest_chapter')
    # ### end Alembic commands ###