"""create posts table

Revision ID: b80289d7b786
Revises: 
Create Date: 2024-05-01 11:53:46.444788

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b80289d7b786'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# run the commandes for the changes that we wanna to do
# alembic.sqlalchemy.org - DDL Internals = sa vad documentatia te upgarde/downgarde
def upgrade() -> None:
# creez tabelul cu numele columnulrilor si restul specificatiilor
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
    sa.Column('title', sa.String(), nullable=False))
    
    pass

# if we have any mistakes in the table we put the changes in this table to change the upgrade (rollingback)
def downgrade() -> None:
    op.drop_table('posts')

    pass
