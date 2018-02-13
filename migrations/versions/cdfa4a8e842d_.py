"""empty message

Revision ID: cdfa4a8e842d
Revises: b3d1d457f9fc
Create Date: 2018-02-10 07:08:27.876328

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cdfa4a8e842d'
down_revision = 'b3d1d457f9fc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('users_user_test_fkey', 'users', type_='foreignkey')
    op.drop_column('users', 'user_test')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('user_test', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('users_user_test_fkey', 'users', 'subject', ['user_test'], ['id'])
    # ### end Alembic commands ###
