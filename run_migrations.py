#!/usr/bin/env python3
"""Run database migrations"""
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from alembic.config import Config
    from alembic import command
    
    print("📦 Running database migrations...")
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
    print("✅ Database migrations complete!")
except Exception as e:
    print(f"❌ Migration error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

