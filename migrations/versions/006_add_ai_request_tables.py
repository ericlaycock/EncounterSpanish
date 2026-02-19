"""Add AI request tables for LLM, STT, and TTS logging

Revision ID: 006_ai_requests
Revises: 005_dialect_quiz
Create Date: 2025-01-17 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '006_ai_requests'
down_revision = '005_dialect_quiz'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create llm_requests table
    op.create_table(
        'llm_requests',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('request_id', sa.String(), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('provider', sa.String(), nullable=False, server_default='openai'),
        sa.Column('model', sa.String(), nullable=False),
        sa.Column('prompt_version', sa.String(), nullable=False),
        sa.Column('agent_id', sa.String(), nullable=False),
        sa.Column('messages_json', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('response_json', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('temperature', sa.Float(), nullable=True),
        sa.Column('max_tokens', sa.Integer(), nullable=True),
        sa.Column('tokens_in', sa.Integer(), nullable=True),
        sa.Column('tokens_out', sa.Integer(), nullable=True),
        sa.Column('estimated_cost', sa.Float(), nullable=True),
        sa.Column('latency_ms', sa.Integer(), nullable=True),
        sa.Column('success', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('error_code', sa.String(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
    )
    op.create_index('ix_llm_requests_request_id', 'llm_requests', ['request_id'])
    op.create_index('ix_llm_requests_user_id', 'llm_requests', ['user_id'])
    op.create_index('ix_llm_requests_prompt_version', 'llm_requests', ['prompt_version'])
    op.create_index('ix_llm_requests_agent_id', 'llm_requests', ['agent_id'])
    op.create_index('ix_llm_requests_success', 'llm_requests', ['success'])
    
    # Create stt_requests table
    op.create_table(
        'stt_requests',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('request_id', sa.String(), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('provider', sa.String(), nullable=False, server_default='openai'),
        sa.Column('model', sa.String(), nullable=False),
        sa.Column('audio_sha256', sa.String(), nullable=True),
        sa.Column('audio_bytes', sa.Integer(), nullable=True),
        sa.Column('audio_format', sa.String(), nullable=True),
        sa.Column('language', sa.String(), nullable=True),
        sa.Column('latency_ms', sa.Integer(), nullable=True),
        sa.Column('success', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('error_code', sa.String(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('transcript_text', sa.Text(), nullable=True),
        sa.Column('output_json', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('estimated_cost', sa.Float(), nullable=True),
    )
    op.create_index('ix_stt_requests_request_id', 'stt_requests', ['request_id'])
    op.create_index('ix_stt_requests_user_id', 'stt_requests', ['user_id'])
    op.create_index('ix_stt_requests_success', 'stt_requests', ['success'])
    
    # Create tts_requests table
    op.create_table(
        'tts_requests',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('request_id', sa.String(), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('provider', sa.String(), nullable=False, server_default='openai'),
        sa.Column('model', sa.String(), nullable=False),
        sa.Column('voice', sa.String(), nullable=True),
        sa.Column('input_text_sha256', sa.String(), nullable=True),
        sa.Column('input_chars', sa.Integer(), nullable=True),
        sa.Column('latency_ms', sa.Integer(), nullable=True),
        sa.Column('success', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('error_code', sa.String(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('audio_bytes', sa.Integer(), nullable=True),
        sa.Column('output_format', sa.String(), nullable=True),
        sa.Column('audio_path', sa.String(), nullable=True),
        sa.Column('estimated_cost', sa.Float(), nullable=True),
    )
    op.create_index('ix_tts_requests_request_id', 'tts_requests', ['request_id'])
    op.create_index('ix_tts_requests_user_id', 'tts_requests', ['user_id'])
    op.create_index('ix_tts_requests_success', 'tts_requests', ['success'])


def downgrade() -> None:
    op.drop_index('ix_tts_requests_success', table_name='tts_requests')
    op.drop_index('ix_tts_requests_user_id', table_name='tts_requests')
    op.drop_index('ix_tts_requests_request_id', table_name='tts_requests')
    op.drop_table('tts_requests')
    
    op.drop_index('ix_stt_requests_success', table_name='stt_requests')
    op.drop_index('ix_stt_requests_user_id', table_name='stt_requests')
    op.drop_index('ix_stt_requests_request_id', table_name='stt_requests')
    op.drop_table('stt_requests')
    
    op.drop_index('ix_llm_requests_success', table_name='llm_requests')
    op.drop_index('ix_llm_requests_agent_id', table_name='llm_requests')
    op.drop_index('ix_llm_requests_prompt_version', table_name='llm_requests')
    op.drop_index('ix_llm_requests_user_id', table_name='llm_requests')
    op.drop_index('ix_llm_requests_request_id', table_name='llm_requests')
    op.drop_table('llm_requests')

