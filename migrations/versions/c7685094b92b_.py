"""empty message

Revision ID: c7685094b92b
Revises: 03112e39a280
Create Date: 2018-02-20 15:33:22.818445

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7685094b92b'
down_revision = '03112e39a280'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('teachersub',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('userid', sa.Integer(), nullable=True),
    sa.Column('subjectid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['subjectid'], ['subject.id'], ),
    sa.ForeignKeyConstraint(['userid'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_index('ix_users_sub_id', table_name='users')
    op.drop_constraint('users_sub_id_fkey', 'users', type_='foreignkey')
    op.drop_column('users', 'sub_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('sub_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('users_sub_id_fkey', 'users', 'subject', ['sub_id'], ['id'])
    op.create_index('ix_users_sub_id', 'users', ['sub_id'], unique=False)
    op.drop_table('teachersub')
    # ### end Alembic commands ###
