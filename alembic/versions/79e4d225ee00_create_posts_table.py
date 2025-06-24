"""create posts table

Revision ID: 79e4d225ee00
Revises: 
Create Date: 2025-06-22 00:10:50.330371

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import PrimaryKeyConstraint

# revision identifiers, used by Alembic.
revision: str = '79e4d225ee00'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts',sa.Column('id',sa.Integer(),nullable=False,primary_key=True),sa.Column('title' , sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
