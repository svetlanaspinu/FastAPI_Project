"""add foreign-key to posts table

Revision ID: ddd100a4b4c5
Revises: d6fac11da4ff
Create Date: 2024-05-02 09:45:16.353153

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ddd100a4b4c5'
down_revision: Union[str, None] = 'd6fac11da4ff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
# dupa ce am inserat comanda alembic revision -m "add foreign-key to posts table" pentru a lega tabelul users cu posts
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    # drop the fk
    op.drop_constraint('posts_users_fk', table_name='posts')
    # drop the column
    op.drop_column('posts', 'owner_id')
    pass
