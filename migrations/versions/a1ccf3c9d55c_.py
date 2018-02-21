"""empty message

Revision ID: a1ccf3c9d55c
Revises: 9fee462f4d5a
Create Date: 2018-02-21 19:53:11.582824

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1ccf3c9d55c'
down_revision = '9fee462f4d5a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_electives_semester_id', table_name='electives')
    op.drop_constraint('electives_semester_id_fkey', 'electives', type_='foreignkey')
    op.drop_column('electives', 'semester_id')
    op.add_column('semelect', sa.Column('electiveid', sa.Integer(), nullable=False))
    op.drop_constraint('semelect_streamid_fkey', 'semelect', type_='foreignkey')
    op.create_foreign_key(None, 'semelect', 'electives', ['electiveid'], ['id'], ondelete='CASCADE')
    op.drop_column('semelect', 'streamid')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('semelect', sa.Column('streamid', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'semelect', type_='foreignkey')
    op.create_foreign_key('semelect_streamid_fkey', 'semelect', 'streams', ['streamid'], ['id'], ondelete='CASCADE')
    op.drop_column('semelect', 'electiveid')
    op.add_column('electives', sa.Column('semester_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('electives_semester_id_fkey', 'electives', 'semester', ['semester_id'], ['id'])
    op.create_index('ix_electives_semester_id', 'electives', ['semester_id'], unique=False)
    # ### end Alembic commands ###
