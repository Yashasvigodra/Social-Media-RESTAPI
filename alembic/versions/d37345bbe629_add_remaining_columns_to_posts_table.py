"""add remaining columns to posts table

Revision ID: d37345bbe629
Revises: 6ebdf67d7cde
Create Date: 2025-06-22 00:47:57.569287

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd37345bbe629'
down_revision: Union[str, Sequence[str], None] = '6ebdf67d7cde'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published',sa.Boolean(),nullable=False,server_default='TRUE'))
    op.add_column('posts',
                  sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')))

    pass


def downgrade() -> None:
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')

    pass
