"""post table foreign key

Revision ID: b9f3cb022efb
Revises: 1aa71b7665c7
Create Date: 2022-03-28 09:11:39.061071

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9f3cb022efb'
down_revision = '1aa71b7665c7'
branch_labels = None
depends_on = None


def upgrade():
    
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=False)),
    op.create_foreign_key('posts_users_fk',source_table='posts',
    referent_table="users", local_cols=['owner_id'],remote_cols=['id'],ondelete='CASCADE') 
    pass


def downgrade():
    op.drop_constraint('posts_owners_fk',table_name='posts')
    op.drop_column('posts','owner_id')
    pass
