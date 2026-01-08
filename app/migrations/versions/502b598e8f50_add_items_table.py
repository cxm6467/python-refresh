"""add items table

Revision ID: 502b598e8f50
Revises: 
Create Date: 2026-01-08 15:13:18.255306

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '502b598e8f50'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'store_managers',
        sa.Column('id', sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('name', sa.String(length=64), nullable=False),
        sa.Column('email', sa.String(length=320), nullable=False),
        sa.Column('password_hash', sa.String(), nullable=False)
    )

    op.create_table(
        'items',
        sa.Column('id', sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('name', sa.String(length=64), nullable=False),
        sa.Column('category', sa.String(length=32), nullable=False),
        sa.Column('price_usd', sa.Float(), nullable=False),
        sa.Column('in_stock', sa.Boolean(), nullable=False),
        sa.Column('store_manager_id', sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey('store_managers.id'), nullable=False),
    )




def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('items')
    op.drop_table('store_managers')
