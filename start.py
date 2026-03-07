#!/usr/bin/env python3
"""Startup script that reads PORT from environment"""
import os
import sys
import subprocess
import uvicorn

# Ensure the app directory is in the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    # Run migrations before anything else if AUTO_MIGRATE is enabled
    if os.environ.get("AUTO_MIGRATE", "false").lower() == "true":
        print("Running database migrations...")
        subprocess.run([sys.executable, "-m", "alembic", "upgrade", "head"], check=True)

    # Run QA seed script if in QA environment (after migrations)
    if os.environ.get("ENVIRONMENT") == "qa":
        print("Running QA seed script...")
        subprocess.run([sys.executable, "scripts/seed_qa.py"], check=True)

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port
    )

