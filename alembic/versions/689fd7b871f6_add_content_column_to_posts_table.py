"""add content column to posts table

Revision ID: 689fd7b871f6
Revises: b80289d7b786
Create Date: 2024-05-02 09:17:57.746680

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '689fd7b871f6'
down_revision: Union[str, None] = 'b80289d7b786'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
