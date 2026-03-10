"""Rename category→animation_type, series_number→encounter_number, selected_situation_categories→selected_animation_types

Revision ID: 010_rename_fields
Revises: 009_is_admin
Create Date: 2026-03-09 00:00:00.000000

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '010_rename_fields'
down_revision = '009_is_admin'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Rename situations.category → situations.animation_type
    op.alter_column('situations', 'category', new_column_name='animation_type')
    op.drop_index('ix_situations_category', table_name='situations')
    op.create_index('ix_situations_animation_type', 'situations', ['animation_type'])

    # Rename situations.series_number → situations.encounter_number
    op.alter_column('situations', 'series_number', new_column_name='encounter_number')

    # Rename users.selected_situation_categories → users.selected_animation_types
    op.alter_column('users', 'selected_situation_categories', new_column_name='selected_animation_types')


def downgrade() -> None:
    op.alter_column('users', 'selected_animation_types', new_column_name='selected_situation_categories')
    op.alter_column('situations', 'encounter_number', new_column_name='series_number')
    op.drop_index('ix_situations_animation_type', table_name='situations')
    op.create_index('ix_situations_category', 'situations', ['animation_type'])
    op.alter_column('situations', 'animation_type', new_column_name='category')
