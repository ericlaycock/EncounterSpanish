"""Add dialect and quiz scores to users

Revision ID: 005_dialect_quiz
Revises: 004_add_notes_column_to_words
Create Date: 2024-02-15 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '005_dialect_quiz'
down_revision = '004_notes'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add dialect and quiz scores to users table
    op.add_column('users', sa.Column('dialect', sa.String(), nullable=True))
    op.add_column('users', sa.Column('grammar_score', sa.String(), nullable=True))
    op.add_column('users', sa.Column('vocab_score', sa.String(), nullable=True))
    
    # Change selected_situation_categories to single category (string instead of array)
    # We'll keep it as JSONB for now but change the API to accept single category


def downgrade() -> None:
    op.drop_column('users', 'vocab_score')
    op.drop_column('users', 'grammar_score')
    op.drop_column('users', 'dialect')

