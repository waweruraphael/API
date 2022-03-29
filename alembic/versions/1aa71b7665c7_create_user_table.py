"""create user table

Revision ID: 1aa71b7665c7
Revises: 8004dc8a4ae2
Create Date: 2022-03-28 08:37:24.495463

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1aa71b7665c7'
down_revision = '8004dc8a4ae2'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
        sa.Column('id',sa.Integer(),nullable=False,primary_key=True),
        sa.Column('email',sa.String(),nullable=False),
        sa.Column('password',sa.String(),nullable=False),
        sa.Column('created_at',sa.TIMESTAMP(timezone=True),
            nullable=False,server_default=sa.text('now()')),
        sa.UniqueConstraint('email') )


    pass


def downgrade():
    op.drop_table('users')
    pass
