"""add users table

Revision ID: 8bd721429e6a
Revises: 216988cbfa04
Create Date: 2025-06-22 00:33:06.612111

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8bd721429e6a'
down_revision: Union[str, Sequence[str], None] = '216988cbfa04'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id',sa.Integer(),nullable=False),
                    sa.Column('email',sa.String(),nullable=False),
                    sa.Column('password',sa.String(),nullable=False),
                    sa.Column('created_at',sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'),nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
