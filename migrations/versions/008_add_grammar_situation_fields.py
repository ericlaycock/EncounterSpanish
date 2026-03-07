"""Add grammar situation fields to situations table

Revision ID: 008_grammar
Revises: 007_goal
Create Date: 2026-03-07 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '008_grammar'
down_revision = '007_goal'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('situations', sa.Column('situation_type', sa.String(), server_default='main', nullable=False))
    op.add_column('situations', sa.Column('vocab_level_required', sa.Integer(), nullable=True))
    op.add_column('situations', sa.Column('video_embed_id', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('situations', 'video_embed_id')
    op.drop_column('situations', 'vocab_level_required')
    op.drop_column('situations', 'situation_type')
