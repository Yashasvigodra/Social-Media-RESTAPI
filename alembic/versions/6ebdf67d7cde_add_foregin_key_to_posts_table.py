"""add foregin key to posts table

Revision ID: 6ebdf67d7cde
Revises: 8bd721429e6a
Create Date: 2025-06-22 00:40:44.764713

"""
from tkinter.constants import CASCADE
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6ebdf67d7cde'
down_revision: Union[str, Sequence[str], None] = '8bd721429e6a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table="posts", referent_table="users", local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name="posts")
    op.drop_column('posts','owner_id')
    pass
