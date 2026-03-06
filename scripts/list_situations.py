#!/usr/bin/env python3
"""Script to list all situations in the database"""

import sys
import os

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
# Import directly from models.py to avoid import issues
import sys
import importlib.util
from pathlib import Path

# Load models.py directly
parent_dir = Path(__file__).parent.parent
models_py_path = parent_dir / "app" / "models.py"
spec = importlib.util.spec_from_file_location("app_models", str(models_py_path))
app_models = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app_models)
Situation = app_models.Situation


def list_all_situations():
    """List all situations from the database"""
    db = SessionLocal()
    try:
        # Query all situations ordered by order_index
        situations = db.query(Situation).order_by(Situation.order_index).all()
        
        if not situations:
            print("No situations found in the database.")
            return
        
        print(f"\n{'='*80}")
        print(f"Total Situations: {len(situations)}")
        print(f"{'='*80}\n")
        
        # Group by category for better readability
        categories = {}
        for situation in situations:
            if situation.category not in categories:
                categories[situation.category] = []
            categories[situation.category].append(situation)
        
        # Print by category
        for category in sorted(categories.keys()):
            print(f"\n📁 Category: {category.upper().replace('_', ' ')}")
            print(f"{'-'*80}")
            for situation in categories[category]:
                free_marker = "🆓" if situation.is_free else "🔒"
                print(f"  {free_marker} [{situation.id:30s}] {situation.title}")
                print(f"      Series: {situation.series_number}, Order: {situation.order_index}")
        
        # Summary by category
        print(f"\n{'='*80}")
        print("Summary by Category:")
        print(f"{'='*80}")
        for category in sorted(categories.keys()):
            count = len(categories[category])
            free_count = sum(1 for s in categories[category] if s.is_free)
            print(f"  {category:20s}: {count:3d} situations ({free_count} free, {count - free_count} premium)")
        
    except Exception as e:
        print(f"Error querying database: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    list_all_situations()

