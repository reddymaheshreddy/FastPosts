"""add left coloumns to post

Revision ID: 8ec94a5b7e00
Revises: dee637c4e9ed
Create Date: 2025-07-16 10:22:10.635327

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8ec94a5b7e00'
down_revision: Union[str, Sequence[str], None] = 'dee637c4e9ed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",
        sa.Column("published", sa.Boolean(), nullable=False, server_default="TRUE") ),
    op.add_column("posts",
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')))
    
    pass


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
