"""add foreign key to posts table

Revision ID: fc0f0fdd730f
Revises: 51482d72f545
Create Date: 2023-01-07 19:41:42.285205

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc0f0fdd730f'
down_revision = '51482d72f545'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table='users', 
                            local_cols=['owner_id'], remote_cols=['id'],  ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
