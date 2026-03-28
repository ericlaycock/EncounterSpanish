"""Add daily_encounter_logs table

Revision ID: 014_daily_enc_log
Revises: 013_hint_count
Create Date: 2026-03-27 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = '014_daily_enc_log'
down_revision = '013_hint_count'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'daily_encounter_logs',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('situation_id', sa.String(), sa.ForeignKey('situations.id'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_daily_encounter_logs_user_created', 'daily_encounter_logs', ['user_id', 'created_at'])


def downgrade() -> None:
    op.drop_index('ix_daily_encounter_logs_user_created', table_name='daily_encounter_logs')
    op.drop_table('daily_encounter_logs')
