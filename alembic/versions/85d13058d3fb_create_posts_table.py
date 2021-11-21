"""create posts table

Revision ID: 85d13058d3fb
Revises: 
Create Date: 2021-11-21 06:50:45.866916

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85d13058d3fb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():  # handle perubahan / creation table
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():  # hanle rollback table
    op.drop_table('posts')
    pass
