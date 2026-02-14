"""Add onboarding fields

Revision ID: 002_onboarding
Revises: 001_initial
Create Date: 2024-01-15 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '002_onboarding'
down_revision = '001_initial'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add onboarding fields to users table
    op.add_column('users', sa.Column('onboarding_completed', sa.Boolean(), nullable=False, server_default='false'))
    op.add_column('users', sa.Column('selected_situation_categories', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    
    # Add category and series_number to situations table
    op.add_column('situations', sa.Column('category', sa.String(), nullable=True))
    op.add_column('situations', sa.Column('series_number', sa.Integer(), nullable=True))
    
    # Create index on category for faster queries
    op.create_index('ix_situations_category', 'situations', ['category'])


def downgrade() -> None:
    op.drop_index('ix_situations_category', table_name='situations')
    op.drop_column('situations', 'series_number')
    op.drop_column('situations', 'category')
    op.drop_column('users', 'selected_situation_categories')
    op.drop_column('users', 'onboarding_completed')




