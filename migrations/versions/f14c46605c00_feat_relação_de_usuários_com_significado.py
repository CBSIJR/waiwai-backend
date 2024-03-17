"""feat: relação de usuários com significado

Revision ID: f14c46605c00
Revises: fb4331e72d63
Create Date: 2024-03-17 18:05:46.195115

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f14c46605c00'
down_revision: Union[str, None] = 'fb4331e72d63'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
