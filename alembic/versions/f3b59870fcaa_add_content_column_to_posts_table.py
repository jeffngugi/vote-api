"""add content column to posts table

Revision ID: f3b59870fcaa
Revises: 79fa349f3ce0
Create Date: 2024-11-25 11:03:50.582749

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f3b59870fcaa'
down_revision: Union[str, None] = '79fa349f3ce0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass