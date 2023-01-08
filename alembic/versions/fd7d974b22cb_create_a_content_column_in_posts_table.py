"""create a content column in posts table

Revision ID: fd7d974b22cb
Revises: bef74816d525
Create Date: 2023-01-07 19:22:38.348433

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fd7d974b22cb'
down_revision = 'bef74816d525'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
