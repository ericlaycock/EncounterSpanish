"""
Script to check what's actually in the database
"""
import sys
import os
from pathlib import Path

# Set database URL from command line or use provided one
import sys
if len(sys.argv) > 1:
    os.environ['DATABASE_URL'] = sys.argv[1]

# Load .env file before importing app modules
env_path = Path(__file__).parent.parent / '.env'
if env_path.exists():
    from dotenv import load_dotenv
    load_dotenv(env_path)

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Word, Situation, SituationWord
from collections import Counter

def check_database():
    """Check database contents"""
    db: Session = SessionLocal()
    try:
        # Count words by category
        total_words = db.query(Word).count()
        encounter_words = db.query(Word).filter(Word.word_category == 'encounter').count()
        high_freq_words = db.query(Word).filter(Word.word_category == 'high_frequency').count()
        uncategorized_words = db.query(Word).filter(Word.word_category.is_(None)).count()
        
        # Count situations
        total_situations = db.query(Situation).count()
        
        # Count situation-word links
        total_links = db.query(SituationWord).count()
        
        # Count by category
        situation_categories = db.query(Situation.category).all()
        category_counts = Counter([cat[0] for cat in situation_categories])
        
        # Count unique encounter words
        unique_encounter_words = db.query(Word).filter(Word.word_category == 'encounter').distinct().count()
        
        # Count high-frequency words with ranks
        hf_with_ranks = db.query(Word).filter(
            Word.word_category == 'high_frequency',
            Word.frequency_rank.isnot(None)
        ).count()
        
        # Get some sample words
        sample_encounter = db.query(Word).filter(Word.word_category == 'encounter').limit(10).all()
        sample_hf = db.query(Word).filter(Word.word_category == 'high_frequency').order_by(Word.frequency_rank).limit(10).all()
        
        print("=" * 80)
        print("DATABASE CONTENTS CHECK")
        print("=" * 80)
        print()
        print(f"📊 WORDS TABLE:")
        print(f"   Total words: {total_words}")
        print(f"   - Encounter words: {encounter_words}")
        print(f"   - High-frequency words: {high_freq_words}")
        print(f"   - Uncategorized: {uncategorized_words}")
        print(f"   - Unique encounter words (distinct): {unique_encounter_words}")
        print(f"   - High-frequency with ranks: {hf_with_ranks}")
        print()
        print(f"📚 SITUATIONS TABLE:")
        print(f"   Total situations: {total_situations}")
        print()
        print(f"🔗 SITUATION_WORDS TABLE:")
        print(f"   Total links: {total_links}")
        if total_situations > 0:
            print(f"   Average words per situation: {total_links / total_situations:.2f}")
        print()
        print(f"📂 SITUATIONS BY CATEGORY:")
        for category, count in sorted(category_counts.items()):
            print(f"   - {category}: {count} encounters")
        print()
        
        # Expected counts
        expected_encounters = 10 * 50  # 10 categories × 50 encounters
        expected_encounter_words_min = expected_encounters * 3  # Minimum if no duplicates
        expected_high_freq = 1000
        
        print("=" * 80)
        print("EXPECTED vs ACTUAL:")
        print("=" * 80)
        print(f"Expected encounters: {expected_encounters}")
        print(f"Actual encounters: {total_situations}")
        print()
        print(f"Expected encounter words (min, if no duplicates): {expected_encounter_words_min}")
        print(f"Actual encounter words: {encounter_words}")
        print(f"Unique encounter words: {unique_encounter_words}")
        print()
        print(f"Expected high-frequency words: {expected_high_freq}")
        print(f"Actual high-frequency words: {high_freq_words}")
        print()
        
        # Sample words
        print("=" * 80)
        print("SAMPLE WORDS:")
        print("=" * 80)
        print("\nSample encounter words (first 10):")
        for word in sample_encounter:
            print(f"   - {word.spanish:25} → {word.english:35} (ID: {word.id})")
        
        print("\nSample high-frequency words (first 10 by rank):")
        for word in sample_hf:
            print(f"   - {word.spanish:25} → {word.english:35} (rank: {word.frequency_rank:4}, ID: {word.id})")
        
        # Check for duplicates
        print()
        print("=" * 80)
        print("DUPLICATE CHECK:")
        print("=" * 80)
        from sqlalchemy import func
        duplicate_spanish = db.query(Word.spanish, func.count(Word.id)).group_by(Word.spanish).having(func.count(Word.id) > 1).all()
        if duplicate_spanish:
            print(f"⚠️  Found {len(duplicate_spanish)} Spanish words with duplicate entries:")
            for spanish, count in duplicate_spanish[:10]:
                words = db.query(Word).filter(Word.spanish == spanish).all()
                print(f"   - '{spanish}': {count} entries (IDs: {[w.id for w in words]})")
        else:
            print("✅ No duplicate Spanish words found")
        
    finally:
        db.close()

if __name__ == "__main__":
    check_database()



Script to check what's actually in the database
"""
import sys
import os
from pathlib import Path

# Set database URL from command line or use provided one
import sys
if len(sys.argv) > 1:
    os.environ['DATABASE_URL'] = sys.argv[1]

# Load .env file before importing app modules
env_path = Path(__file__).parent.parent / '.env'
if env_path.exists():
    from dotenv import load_dotenv
    load_dotenv(env_path)

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Word, Situation, SituationWord
from collections import Counter

def check_database():
    """Check database contents"""
    db: Session = SessionLocal()
    try:
        # Count words by category
        total_words = db.query(Word).count()
        encounter_words = db.query(Word).filter(Word.word_category == 'encounter').count()
        high_freq_words = db.query(Word).filter(Word.word_category == 'high_frequency').count()
        uncategorized_words = db.query(Word).filter(Word.word_category.is_(None)).count()
        
        # Count situations
        total_situations = db.query(Situation).count()
        
        # Count situation-word links
        total_links = db.query(SituationWord).count()
        
        # Count by category
        situation_categories = db.query(Situation.category).all()
        category_counts = Counter([cat[0] for cat in situation_categories])
        
        # Count unique encounter words
        unique_encounter_words = db.query(Word).filter(Word.word_category == 'encounter').distinct().count()
        
        # Count high-frequency words with ranks
        hf_with_ranks = db.query(Word).filter(
            Word.word_category == 'high_frequency',
            Word.frequency_rank.isnot(None)
        ).count()
        
        # Get some sample words
        sample_encounter = db.query(Word).filter(Word.word_category == 'encounter').limit(10).all()
        sample_hf = db.query(Word).filter(Word.word_category == 'high_frequency').order_by(Word.frequency_rank).limit(10).all()
        
        print("=" * 80)
        print("DATABASE CONTENTS CHECK")
        print("=" * 80)
        print()
        print(f"📊 WORDS TABLE:")
        print(f"   Total words: {total_words}")
        print(f"   - Encounter words: {encounter_words}")
        print(f"   - High-frequency words: {high_freq_words}")
        print(f"   - Uncategorized: {uncategorized_words}")
        print(f"   - Unique encounter words (distinct): {unique_encounter_words}")
        print(f"   - High-frequency with ranks: {hf_with_ranks}")
        print()
        print(f"📚 SITUATIONS TABLE:")
        print(f"   Total situations: {total_situations}")
        print()
        print(f"🔗 SITUATION_WORDS TABLE:")
        print(f"   Total links: {total_links}")
        if total_situations > 0:
            print(f"   Average words per situation: {total_links / total_situations:.2f}")
        print()
        print(f"📂 SITUATIONS BY CATEGORY:")
        for category, count in sorted(category_counts.items()):
            print(f"   - {category}: {count} encounters")
        print()
        
        # Expected counts
        expected_encounters = 10 * 50  # 10 categories × 50 encounters
        expected_encounter_words_min = expected_encounters * 3  # Minimum if no duplicates
        expected_high_freq = 1000
        
        print("=" * 80)
        print("EXPECTED vs ACTUAL:")
        print("=" * 80)
        print(f"Expected encounters: {expected_encounters}")
        print(f"Actual encounters: {total_situations}")
        print()
        print(f"Expected encounter words (min, if no duplicates): {expected_encounter_words_min}")
        print(f"Actual encounter words: {encounter_words}")
        print(f"Unique encounter words: {unique_encounter_words}")
        print()
        print(f"Expected high-frequency words: {expected_high_freq}")
        print(f"Actual high-frequency words: {high_freq_words}")
        print()
        
        # Sample words
        print("=" * 80)
        print("SAMPLE WORDS:")
        print("=" * 80)
        print("\nSample encounter words (first 10):")
        for word in sample_encounter:
            print(f"   - {word.spanish:25} → {word.english:35} (ID: {word.id})")
        
        print("\nSample high-frequency words (first 10 by rank):")
        for word in sample_hf:
            print(f"   - {word.spanish:25} → {word.english:35} (rank: {word.frequency_rank:4}, ID: {word.id})")
        
        # Check for duplicates
        print()
        print("=" * 80)
        print("DUPLICATE CHECK:")
        print("=" * 80)
        from sqlalchemy import func
        duplicate_spanish = db.query(Word.spanish, func.count(Word.id)).group_by(Word.spanish).having(func.count(Word.id) > 1).all()
        if duplicate_spanish:
            print(f"⚠️  Found {len(duplicate_spanish)} Spanish words with duplicate entries:")
            for spanish, count in duplicate_spanish[:10]:
                words = db.query(Word).filter(Word.spanish == spanish).all()
                print(f"   - '{spanish}': {count} entries (IDs: {[w.id for w in words]})")
        else:
            print("✅ No duplicate Spanish words found")
        
    finally:
        db.close()

if __name__ == "__main__":
    check_database()



Script to check what's actually in the database
"""
import sys
import os
from pathlib import Path

# Set database URL from command line or use provided one
import sys
if len(sys.argv) > 1:
    os.environ['DATABASE_URL'] = sys.argv[1]

# Load .env file before importing app modules
env_path = Path(__file__).parent.parent / '.env'
if env_path.exists():
    from dotenv import load_dotenv
    load_dotenv(env_path)

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Word, Situation, SituationWord
from collections import Counter

def check_database():
    """Check database contents"""
    db: Session = SessionLocal()
    try:
        # Count words by category
        total_words = db.query(Word).count()
        encounter_words = db.query(Word).filter(Word.word_category == 'encounter').count()
        high_freq_words = db.query(Word).filter(Word.word_category == 'high_frequency').count()
        uncategorized_words = db.query(Word).filter(Word.word_category.is_(None)).count()
        
        # Count situations
        total_situations = db.query(Situation).count()
        
        # Count situation-word links
        total_links = db.query(SituationWord).count()
        
        # Count by category
        situation_categories = db.query(Situation.category).all()
        category_counts = Counter([cat[0] for cat in situation_categories])
        
        # Count unique encounter words
        unique_encounter_words = db.query(Word).filter(Word.word_category == 'encounter').distinct().count()
        
        # Count high-frequency words with ranks
        hf_with_ranks = db.query(Word).filter(
            Word.word_category == 'high_frequency',
            Word.frequency_rank.isnot(None)
        ).count()
        
        # Get some sample words
        sample_encounter = db.query(Word).filter(Word.word_category == 'encounter').limit(10).all()
        sample_hf = db.query(Word).filter(Word.word_category == 'high_frequency').order_by(Word.frequency_rank).limit(10).all()
        
        print("=" * 80)
        print("DATABASE CONTENTS CHECK")
        print("=" * 80)
        print()
        print(f"📊 WORDS TABLE:")
        print(f"   Total words: {total_words}")
        print(f"   - Encounter words: {encounter_words}")
        print(f"   - High-frequency words: {high_freq_words}")
        print(f"   - Uncategorized: {uncategorized_words}")
        print(f"   - Unique encounter words (distinct): {unique_encounter_words}")
        print(f"   - High-frequency with ranks: {hf_with_ranks}")
        print()
        print(f"📚 SITUATIONS TABLE:")
        print(f"   Total situations: {total_situations}")
        print()
        print(f"🔗 SITUATION_WORDS TABLE:")
        print(f"   Total links: {total_links}")
        if total_situations > 0:
            print(f"   Average words per situation: {total_links / total_situations:.2f}")
        print()
        print(f"📂 SITUATIONS BY CATEGORY:")
        for category, count in sorted(category_counts.items()):
            print(f"   - {category}: {count} encounters")
        print()
        
        # Expected counts
        expected_encounters = 10 * 50  # 10 categories × 50 encounters
        expected_encounter_words_min = expected_encounters * 3  # Minimum if no duplicates
        expected_high_freq = 1000
        
        print("=" * 80)
        print("EXPECTED vs ACTUAL:")
        print("=" * 80)
        print(f"Expected encounters: {expected_encounters}")
        print(f"Actual encounters: {total_situations}")
        print()
        print(f"Expected encounter words (min, if no duplicates): {expected_encounter_words_min}")
        print(f"Actual encounter words: {encounter_words}")
        print(f"Unique encounter words: {unique_encounter_words}")
        print()
        print(f"Expected high-frequency words: {expected_high_freq}")
        print(f"Actual high-frequency words: {high_freq_words}")
        print()
        
        # Sample words
        print("=" * 80)
        print("SAMPLE WORDS:")
        print("=" * 80)
        print("\nSample encounter words (first 10):")
        for word in sample_encounter:
            print(f"   - {word.spanish:25} → {word.english:35} (ID: {word.id})")
        
        print("\nSample high-frequency words (first 10 by rank):")
        for word in sample_hf:
            print(f"   - {word.spanish:25} → {word.english:35} (rank: {word.frequency_rank:4}, ID: {word.id})")
        
        # Check for duplicates
        print()
        print("=" * 80)
        print("DUPLICATE CHECK:")
        print("=" * 80)
        from sqlalchemy import func
        duplicate_spanish = db.query(Word.spanish, func.count(Word.id)).group_by(Word.spanish).having(func.count(Word.id) > 1).all()
        if duplicate_spanish:
            print(f"⚠️  Found {len(duplicate_spanish)} Spanish words with duplicate entries:")
            for spanish, count in duplicate_spanish[:10]:
                words = db.query(Word).filter(Word.spanish == spanish).all()
                print(f"   - '{spanish}': {count} entries (IDs: {[w.id for w in words]})")
        else:
            print("✅ No duplicate Spanish words found")
        
    finally:
        db.close()

if __name__ == "__main__":
    check_database()



