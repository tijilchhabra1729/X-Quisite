"""empty message

Revision ID: 9c9bc19c9c99
Revises: 3705c096cf47
Create Date: 2020-08-12 22:38:54.336719

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c9bc19c9c99'
down_revision = '3705c096cf47'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('likes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('answerid', sa.Integer(), nullable=True),
    sa.Column('userid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['answerid'], ['answers.id'], ),
    sa.ForeignKeyConstraint(['userid'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('unlikes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('answerid', sa.Integer(), nullable=True),
    sa.Column('userid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['answerid'], ['answers.id'], ),
    sa.ForeignKeyConstraint(['userid'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('unlikes')
    op.drop_table('likes')
    # ### end Alembic commands ###