"""add content column to posts table

Revision ID: 216988cbfa04
Revises: 79e4d225ee00
Create Date: 2025-06-22 00:28:01.825760

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '216988cbfa04'
down_revision: Union[str, Sequence[str], None] = '79e4d225ee00'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
