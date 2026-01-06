"""add image_urls column to listings

Revision ID: dd57aafe3eb1
Revises: 6661a91c9729
Create Date: 2026-01-05 18:25:04.405413

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as psql


# revision identifiers, used by Alembic.
revision: str = 'dd57aafe3eb1'
down_revision: Union[str, Sequence[str], None] = '6661a91c9729'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # Add image_urls column (JSONB) to listings table
    op.add_column(
        'listings',
        sa.Column('image_urls', psql.JSONB, nullable=True)
    )

def downgrade():
    # Remove the column if rolling back
    op.drop_column('listings', 'image_urls')
