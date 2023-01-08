"""add last few columns in posts table

Revision ID: e8742932c51a
Revises: fc0f0fdd730f
Create Date: 2023-01-07 19:48:05.941092

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e8742932c51a'
down_revision = 'fc0f0fdd730f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), server_default='TRUE', nullable=True))
    op.add_column('posts', sa.Column('rating', sa.Integer(), server_default='0', nullable=True))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'rating')
    op.drop_column('posts', 'created_at')
    pass
