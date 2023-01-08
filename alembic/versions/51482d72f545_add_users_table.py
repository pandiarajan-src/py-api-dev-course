"""add users table

Revision ID: 51482d72f545
Revises: fd7d974b22cb
Create Date: 2023-01-07 19:35:34.408190

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '51482d72f545'
down_revision = 'fd7d974b22cb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
