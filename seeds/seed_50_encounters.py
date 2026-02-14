"""
Seed script to generate 50 encounters per category with 3 words each.
This replaces the old seed_data.py structure.

Each encounter gets:
- 3 encounter-specific words
- When user starts encounter, system adds 2 highest frequency unlearned words
= 5 words total per encounter
"""
import sys
import os
from pathlib import Path

# Load .env file before importing app modules
env_path = Path(__file__).parent.parent / '.env'
if env_path.exists():
    from dotenv import load_dotenv
    load_dotenv(env_path)

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base, Word, Situation, SituationWord, User, Subscription, Conversation, UserSituation, UserWord

# Import the encounters data
from seeds.generate_50_encounters import ENCOUNTERS_BY_CATEGORY

# Create tables
Base.metadata.create_all(bind=engine)


def generate_all_encounters():
    """Generate all encounters from ENCOUNTERS_BY_CATEGORY"""
    all_situations = []
    all_words = []
    situation_word_mappings = {}
    
    word_id_counter = {}
    
    for category, encounters in ENCOUNTERS_BY_CATEGORY.items():
        for idx, encounter in enumerate(encounters, start=1):
            situation_id = f"{category}_{idx}"
            title = encounter["title"]
            words_list = encounter["words"]
            
            # Create situation
            all_situations.append({
                "id": situation_id,
                "title": title,
                "order_index": len(all_situations) + 1,
                "is_free": True,  # All encounters are free now
                "category": category,
                "series_number": idx
            })
            
            # Create words for this encounter
            encounter_word_ids = []
            for word_spanish in words_list:
                # Generate word ID
                word_base = word_spanish.replace(" ", "_").lower()
                if word_base not in word_id_counter:
                    word_id_counter[word_base] = 0
                word_id_counter[word_base] += 1
                
                word_id = f"w_{word_base}"
                if word_id_counter[word_base] > 1:
                    word_id = f"w_{word_base}_{word_id_counter[word_base]}"
                
                # Add word if not already in list
                if not any(w["id"] == word_id for w in all_words):
                    # Get English translation from dictionary
                    from seeds.word_translations import WORD_TRANSLATIONS
                    english = WORD_TRANSLATIONS.get(word_spanish, word_spanish.replace("_", " ").title())
                    all_words.append({
                        "id": word_id,
                        "spanish": word_spanish,
                        "english": english,
                        "word_category": "encounter"
                    })
                
                encounter_word_ids.append(word_id)
            
            # Map situation to words
            situation_word_mappings[situation_id] = encounter_word_ids
    
    return all_situations, all_words, situation_word_mappings


def seed_database():
    """Seed the database with 50 encounters per category"""
    db: Session = SessionLocal()
    
    try:
        # Generate all encounters
        print("Generating encounters...")
        all_situations, all_words, situation_word_mappings = generate_all_encounters()
        
        # Delete in reverse order of foreign key dependencies
        print("🗑️ Clearing existing data...")
        db.query(SituationWord).delete()
        db.query(Conversation).delete()
        db.query(UserSituation).delete()
        db.query(UserWord).delete()
        db.query(Situation).delete()
        db.query(Word).delete()
        db.query(Subscription).delete()
        db.query(User).delete()
        db.commit()
        print("✅ Existing data cleared")
        
        # Upsert words
        print(f"\n📝 Inserting/updating {len(all_words)} words...")
        words_created = 0
        words_updated = 0
        for word_data in all_words:
            existing = db.query(Word).filter(Word.id == word_data['id']).first()
            if existing:
                existing.spanish = word_data['spanish']
                existing.english = word_data['english']
                existing.word_category = 'encounter'
                words_updated += 1
            else:
                word = Word(**word_data)
                db.add(word)
                words_created += 1
            db.flush()
        db.commit()
        print(f"✅ Created {words_created} words, updated {words_updated} words")
        
        # Upsert situations
        print(f"\n📚 Inserting/updating {len(all_situations)} situations...")
        situations_created = 0
        situations_updated = 0
        for situation_data in all_situations:
            existing = db.query(Situation).filter(Situation.id == situation_data['id']).first()
            if existing:
                existing.title = situation_data['title']
                existing.order_index = situation_data['order_index']
                existing.is_free = True  # All free
                existing.category = situation_data['category']
                existing.series_number = situation_data['series_number']
                situations_updated += 1
            else:
                situation = Situation(**situation_data)
                db.add(situation)
                situations_created += 1
            db.flush()
        db.commit()
        print(f"✅ Created {situations_created} situations, updated {situations_updated} situations")
        
        # Link words to situations
        print(f"\n🔗 Linking words to situations...")
        total_links = 0
        for situation_id, word_list in situation_word_mappings.items():
            # Clear existing links
            db.query(SituationWord).filter(SituationWord.situation_id == situation_id).delete()
            db.flush()
            
            for position, word_id in enumerate(word_list, start=1):
                situation_word = SituationWord(
                    situation_id=situation_id,
                    word_id=word_id,
                    position=position
                )
                db.add(situation_word)
                total_links += 1
        db.commit()
        print(f"✅ Created {total_links} situation-word links")
        
        # Summary by category
        print("\n📊 Summary by category:")
        from collections import Counter
        category_counts = Counter(s['category'] for s in all_situations)
        for category, count in sorted(category_counts.items()):
            print(f"   - {category}: {count} encounters")
        
        print(f"\n🎉 Database seed complete!")
        print(f"   - {len(all_words)} words")
        print(f"   - {len(all_situations)} situations (all free)")
        print(f"   - {total_links} situation-word links")
        print(f"   - {len(category_counts)} categories")
        print(f"   - Average {total_links // len(all_situations) if all_situations else 0} words per encounter")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding database: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()

