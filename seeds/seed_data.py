"""
Seed data script for Encounter Spanish app.

This script creates:
- 50 situations (first 5 are free)
- Words and situation-word mappings

To run: python -m seeds.seed_data
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base, Word, Situation, SituationWord

# Create tables
Base.metadata.create_all(bind=engine)


# Placeholder data structure - replace with actual content
SITUATIONS = [
    # First 5 are free (order_index 1-5, is_free=True)
    {"id": "sit_001", "title": "At the Airport", "order_index": 1, "is_free": True},
    {"id": "sit_002", "title": "Checking into Hotel", "order_index": 2, "is_free": True},
    {"id": "sit_003", "title": "Ordering Coffee", "order_index": 3, "is_free": True},
    {"id": "sit_004", "title": "Asking for Directions", "order_index": 4, "is_free": True},
    {"id": "sit_005", "title": "At the Restaurant", "order_index": 5, "is_free": True},
    # Remaining 45 are paid (order_index 6-50, is_free=False)
    {"id": "sit_006", "title": "At the Bank", "order_index": 6, "is_free": False},
    {"id": "sit_007", "title": "Shopping for Groceries", "order_index": 7, "is_free": False},
    {"id": "sit_008", "title": "At the Pharmacy", "order_index": 8, "is_free": False},
    {"id": "sit_009", "title": "Taking a Taxi", "order_index": 9, "is_free": False},
    {"id": "sit_010", "title": "At the Doctor", "order_index": 10, "is_free": False},
    # Add remaining 40 situations here...
    # For now, creating placeholder entries
]

# Generate remaining placeholder situations
for i in range(11, 51):
    SITUATIONS.append({
        "id": f"sit_{i:03d}",
        "title": f"Situation {i}",
        "order_index": i,
        "is_free": False
    })

# Sample words - replace with actual words
WORDS = [
    {"id": "w_hola", "spanish": "hola", "english": "hello"},
    {"id": "w_gracias", "spanish": "gracias", "english": "thank you"},
    {"id": "w_por_favor", "spanish": "por favor", "english": "please"},
    {"id": "w_si", "spanish": "sí", "english": "yes"},
    {"id": "w_no", "spanish": "no", "english": "no"},
    {"id": "w_perdon", "spanish": "perdón", "english": "sorry"},
    {"id": "w_banco", "spanish": "banco", "english": "bank"},
    {"id": "w_hotel", "spanish": "hotel", "english": "hotel"},
    {"id": "w_aeropuerto", "spanish": "aeropuerto", "english": "airport"},
    {"id": "w_restaurante", "spanish": "restaurante", "english": "restaurant"},
    # Add more words as needed
]

# Situation-word mappings
# Format: {situation_id: [word_ids in order]}
SITUATION_WORDS = {
    "sit_001": ["w_hola", "w_gracias", "w_por_favor"],  # At the Airport
    "sit_002": ["w_hotel", "w_gracias", "w_por_favor"],  # Checking into Hotel
    "sit_003": ["w_por_favor", "w_gracias"],  # Ordering Coffee
    "sit_004": ["w_perdon", "w_gracias"],  # Asking for Directions
    "sit_005": ["w_restaurante", "w_por_favor", "w_gracias"],  # At the Restaurant
    "sit_006": ["w_banco", "w_por_favor"],  # At the Bank
    # Add mappings for remaining situations
}


def seed_database():
    """Seed the database with situations and words"""
    db: Session = SessionLocal()
    
    try:
        # Clear existing data (optional - comment out if you want to keep existing data)
        db.query(SituationWord).delete()
        db.query(Situation).delete()
        db.query(Word).delete()
        db.commit()
        
        # Insert words
        print("Inserting words...")
        for word_data in WORDS:
            word = Word(**word_data)
            db.add(word)
        db.commit()
        print(f"Inserted {len(WORDS)} words")
        
        # Insert situations
        print("Inserting situations...")
        for situation_data in SITUATIONS:
            situation = Situation(**situation_data)
            db.add(situation)
        db.commit()
        print(f"Inserted {len(SITUATIONS)} situations")
        
        # Insert situation-word mappings
        print("Inserting situation-word mappings...")
        total_mappings = 0
        for situation_id, word_ids in SITUATION_WORDS.items():
            for position, word_id in enumerate(word_ids, start=1):
                mapping = SituationWord(
                    situation_id=situation_id,
                    word_id=word_id,
                    position=position
                )
                db.add(mapping)
                total_mappings += 1
        db.commit()
        print(f"Inserted {total_mappings} situation-word mappings")
        
        print("Seed data inserted successfully!")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()



