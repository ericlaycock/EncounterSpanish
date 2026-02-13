"""add_word_category_and_frequency_rank

Revision ID: 003
Revises: 002
Create Date: 2024-01-01 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '003_word_category'
down_revision: Union[str, None] = '002_onboarding'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('words', sa.Column('word_category', sa.String(), nullable=True))
    op.add_column('words', sa.Column('frequency_rank', sa.Integer(), nullable=True))
    op.create_index('ix_words_word_category', 'words', ['word_category'])


def downgrade() -> None:
    op.drop_index('ix_words_word_category', table_name='words')
    op.drop_column('words', 'frequency_rank')
    op.drop_column('words', 'word_category')

