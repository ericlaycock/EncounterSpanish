"""Initial schema

Revision ID: 001_initial
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('password_hash', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_users_email', 'users', ['email'])

    # Create subscriptions table
    op.create_table(
        'subscriptions',
        sa.Column('user_id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('active', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('tier', sa.String(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
    )

    # Create words table
    op.create_table(
        'words',
        sa.Column('id', sa.String(), primary_key=True),
        sa.Column('spanish', sa.String(), nullable=False),
        sa.Column('english', sa.String(), nullable=False),
    )

    # Create situations table
    op.create_table(
        'situations',
        sa.Column('id', sa.String(), primary_key=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('order_index', sa.Integer(), nullable=False),
        sa.Column('is_free', sa.Boolean(), nullable=False, server_default='false'),
    )
    op.create_index('ix_situations_order_index', 'situations', ['order_index'])

    # Create situation_words table
    op.create_table(
        'situation_words',
        sa.Column('situation_id', sa.String(), primary_key=True),
        sa.Column('word_id', sa.String(), primary_key=True),
        sa.Column('position', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['situation_id'], ['situations.id']),
        sa.ForeignKeyConstraint(['word_id'], ['words.id']),
    )

    # Create user_words table
    op.create_table(
        'user_words',
        sa.Column('user_id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('word_id', sa.String(), primary_key=True),
        sa.Column('seen_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('typed_correct_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('spoken_correct_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('status', sa.String(), nullable=False, server_default='learning'),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.ForeignKeyConstraint(['word_id'], ['words.id']),
    )

    # Create user_situations table
    op.create_table(
        'user_situations',
        sa.Column('user_id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('situation_id', sa.String(), primary_key=True),
        sa.Column('started_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.ForeignKeyConstraint(['situation_id'], ['situations.id']),
    )

    # Create conversations table
    op.create_table(
        'conversations',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('situation_id', sa.String(), nullable=False),
        sa.Column('mode', sa.String(), nullable=False),
        sa.Column('target_word_ids', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('used_typed_word_ids', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default='[]'),
        sa.Column('used_spoken_word_ids', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default='[]'),
        sa.Column('status', sa.String(), nullable=False, server_default='active'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.ForeignKeyConstraint(['situation_id'], ['situations.id']),
    )
    op.create_index('ix_conversations_user_id', 'conversations', ['user_id'])


def downgrade() -> None:
    op.drop_index('ix_conversations_user_id', table_name='conversations')
    op.drop_table('conversations')
    op.drop_table('user_situations')
    op.drop_table('user_words')
    op.drop_table('situation_words')
    op.drop_index('ix_situations_order_index', table_name='situations')
    op.drop_table('situations')
    op.drop_table('words')
    op.drop_table('subscriptions')
    op.drop_index('ix_users_email', table_name='users')
    op.drop_table('users')

