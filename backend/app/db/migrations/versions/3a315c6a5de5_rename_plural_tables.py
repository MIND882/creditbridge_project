"""rename plural tables

Revision ID: 3a315c6a5de5
Revises: d7a2c4f8e1b9
Create Date: 2026-10-10 17:23:25.576800

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3a315c6a5de5'
down_revision: Union[str, Sequence[str], None] = 'd7a2c4f8e1b9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass  # renames were applied manually via SQL


def downgrade() -> None:
    pass