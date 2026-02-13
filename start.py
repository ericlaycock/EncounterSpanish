#!/usr/bin/env python3
"""Startup script that reads PORT from environment"""
import os
import sys
import uvicorn

# Ensure the app directory is in the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port
    )

