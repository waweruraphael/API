"""add columns to post table

Revision ID: 8004dc8a4ae2
Revises: 82bb995956c7
Create Date: 2022-03-28 08:24:20.397932

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8004dc8a4ae2'
down_revision = '82bb995956c7'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False)),
    op.add_column('posts',sa.Column('publish',sa.Boolean(),nullable=False,server_default='TRUE')),
      
    op.add_column('posts',sa.Column('created_at',sa.TIMESTAMP(timezone=True),
        nullable=False,server_default=sa.text('now()'))),
     
        
        
     
    pass


def downgrade():
    
    op.drop_column('posts','content')
    op.drop_column('posts','publish')
    op.drop_column('posts','created_at')
    
    pass
