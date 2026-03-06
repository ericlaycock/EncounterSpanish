"""Add notes column to words

Revision ID: 004_notes
Revises: 003_word_category
Create Date: 2024-02-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '004_notes'
down_revision = '003_word_category'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('words', sa.Column('notes', sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column('words', 'notes')
