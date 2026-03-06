"""Add goal column to situations

Revision ID: 007_goal
Revises: 006_ai_requests
Create Date: 2024-12-20 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '007_goal'
down_revision = '006_ai_requests'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add goal column to situations table
    op.add_column('situations', sa.Column('goal', sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column('situations', 'goal')


