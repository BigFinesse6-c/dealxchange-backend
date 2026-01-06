"""add location column to listings

Revision ID: 2cab7e0a3fd8
Revises: 12953b77556f
Create Date: 2025-09-04 14:01:24.722535
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '2cab7e0a3fd8'
down_revision = '12953b77556f'
branch_labels = None
depends_on = None

def upgrade() -> None:
    """Upgrade schema."""
    # Add the location column to listings
    op.add_column('listings', sa.Column('location', sa.String(), nullable=True))

    # Optional: add an index for faster queries by location
    op.create_index(op.f('ix_listings_location'), 'listings', ['location'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Remove the index
    op.drop_index(op.f('ix_listings_location'), table_name='listings')

    # Drop the location column
    op.drop_column('listings', 'location')

