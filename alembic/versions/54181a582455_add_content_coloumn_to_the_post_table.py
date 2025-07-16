"""add content coloumn to the post table

Revision ID: 54181a582455
Revises: a3adf9b9e6b0
Create Date: 2025-07-16 09:56:27.479299

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '54181a582455'
down_revision: Union[str, Sequence[str], None] = 'a3adf9b9e6b0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",
        sa.Column("content", sa.String(), nullable=False, server_default=""))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
