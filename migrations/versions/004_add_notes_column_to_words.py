"""add_notes_column_to_words

Revision ID: 004_notes
Revises: 003_word_category
Create Date: 2024-01-01 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '004_notes'
down_revision: Union[str, None] = '003_word_category'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('words', sa.Column('notes', sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column('words', 'notes')




Revision ID: 004_notes
Revises: 003_word_category
Create Date: 2024-01-01 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '004_notes'
down_revision: Union[str, None] = '003_word_category'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('words', sa.Column('notes', sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column('words', 'notes')




Revision ID: 004_notes
Revises: 003_word_category
Create Date: 2024-01-01 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '004_notes'
down_revision: Union[str, None] = '003_word_category'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('words', sa.Column('notes', sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column('words', 'notes')




