"""add foreign key to ppost table

Revision ID: dee637c4e9ed
Revises: a4a9921dbb37
Create Date: 2025-07-16 10:16:20.710971

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dee637c4e9ed'
down_revision: Union[str, Sequence[str], None] = 'a4a9921dbb37'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",
        sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "post_users_fk", source_table="posts", referent_table="users",
        local_cols=["owner_id"], remote_cols=["id"], ondelete="CASCADE"
    )
    pass


def downgrade() -> None:
    op.drop_constraint("post_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
    pass
