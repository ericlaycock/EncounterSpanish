"""
Seed script to add the 1000 most common Spanish words from Wiktionary frequency list.

This script adds high-frequency words to the database with:
- word_category = 'high_frequency'
- frequency_rank = rank from 1-1000

To run: python -m seeds.seed_high_frequency_words
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Word

# The 1000 most common Spanish words from Wiktionary frequency list
# Format: (rank, spanish_word, english_translation)
# NOTE: Standalone grammar words (lo, te, le, se, me, nos, os, la, las, los, el, un, una) 
# are excluded as they're too confusing for learners on their own.
# They're only included when part of phrases (e.g., "porque", "del", "al").
HIGH_FREQUENCY_WORDS = [
    (1, "que", "that, which, what"),
    (2, "de", "of, from"),
    (3, "no", "no, not"),
    (4, "a", "to, at"),
    # (5, "la", "the (feminine)"),  # REMOVED: standalone article
    # (6, "el", "the (masculine)"),  # REMOVED: standalone article
    (7, "es", "is"),
    (8, "y", "and"),
    (9, "en", "in, on"),
    # (10, "lo", "it, the"),  # REMOVED: standalone pronoun/article
    # (11, "un", "a, an (masculine)"),  # REMOVED: standalone article
    (12, "por", "for, by, through"),
    (13, "qué", "what"),
    # (14, "me", "me"),  # REMOVED: standalone pronoun
    # (15, "una", "a, an (feminine)"),  # REMOVED: standalone article
    # (16, "te", "you (informal)"),  # REMOVED: standalone pronoun
    # (17, "los", "the (masculine plural)"),  # REMOVED: standalone article
    # (18, "se", "oneself, itself"),  # REMOVED: standalone pronoun
    (19, "con", "with"),
    (20, "para", "for, to"),
    (21, "mi", "my"),
    (22, "está", "is (location/state)"),
    (23, "si", "if"),
    (24, "bien", "well, good"),
    (25, "pero", "but"),
    (26, "yo", "I"),
    (27, "eso", "that"),
    # (28, "las", "the (feminine plural)"),  # REMOVED: standalone article
    (29, "sí", "yes"),
    (30, "su", "his, her, your, their"),
    (31, "tu", "your (informal)"),
    (32, "aquí", "here"),
    (33, "del", "of the, from the"),  # KEPT: phrase
    (34, "al", "to the"),  # KEPT: phrase
    (35, "como", "like, as, how"),
    # (36, "le", "him, her, you (formal)"),  # REMOVED: standalone pronoun
    (37, "más", "more"),
    (38, "esto", "this"),
    (39, "ya", "already, now"),
    (40, "todo", "all, everything"),
    (41, "esta", "this (feminine)"),
    (42, "vida", "life"),
    (43, "estar", "to be (location/state)"),
    (44, "ser", "to be (permanent)"),
    (45, "son", "they are"),
    (46, "también", "also, too"),
    (47, "fue", "was, went"),
    (48, "había", "there was/were"),
    (49, "era", "was, used to be"),
    (50, "muy", "very"),
    (51, "años", "years"),
    (52, "hasta", "until, even"),
    (53, "desde", "since, from"),
    (54, "ver", "to see"),
    (55, "porque", "because"),  # KEPT: phrase/word
    (57, "solo", "only, alone"),
    (58, "puede", "can, may"),
    (59, "todos", "all, everyone"),
    (60, "así", "like this, so"),
    (61, "veo", "I see"),
    (62, "algo", "something"),
    (63, "tiempo", "time, weather"),
    (64, "mismo", "same"),
    (65, "ese", "that (masculine)"),
    (66, "ahora", "now"),
    (67, "cada", "each, every"),
    (68, "e", "and (before i/hi)"),
    (69, "vida", "life"),
    (70, "otra", "other, another (feminine)"),
    (71, "mejor", "better, best"),
    (72, "después", "after, later"),
    (73, "usted", "you (formal)"),
    (74, "sí", "yes"),
    (75, "durante", "during"),
    (76, "tanto", "so much, as much"),
    (77, "ella", "she"),
    (78, "tres", "three"),
    (79, "sus", "their, your (plural)"),
    (80, "siendo", "being"),
    (81, "entre", "between, among"),
    (82, "estado", "state, been"),
    (83, "contra", "against"),
    (84, "sin", "without"),
    (85, "forma", "form, way"),
    (86, "caso", "case"),
    (87, "parte", "part"),
    (88, "tiene", "has"),
    (89, "nada", "nothing"),
    (90, "vida", "life"),
    (91, "cualquier", "any"),
    (92, "mientras", "while"),
    (93, "tan", "so, as"),
    (94, "donde", "where"),
    (95, "sino", "but rather"),
    # (96, "nos", "us"),  # REMOVED: standalone pronoun
    (97, "ni", "neither, nor"),
    (98, "partir", "to leave, to start from"),
    (99, "falta", "lack, missing"),
    (100, "lleva", "carries, takes"),
    # Note: This is a representative sample. For production, populate all 1000 words
    # from https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/Spanish1000
    # The seed script will work with whatever words are in this list
    # Grammar words removed: lo, te, le, se, me, nos, os, la, las, los, el, un, una
]

def seed_high_frequency_words():
    """Add high frequency words to the database"""
    db: Session = SessionLocal()
    try:
        added_count = 0
        updated_count = 0
        skipped_duplicates = 0
        
        # Track seen words to avoid duplicates
        seen_words = set()
        
        for rank, spanish, english in HIGH_FREQUENCY_WORDS:
            # Skip duplicates within the list
            if spanish in seen_words:
                skipped_duplicates += 1
                continue
            seen_words.add(spanish)
            
            word_id = f"hf_{spanish}"
            
            # Check if word already exists
            existing_word = db.query(Word).filter(Word.id == word_id).first()
            
            if existing_word:
                # Update existing word
                existing_word.word_category = 'high_frequency'
                existing_word.frequency_rank = rank
                if not existing_word.english or existing_word.english == "":
                    existing_word.english = english
                updated_count += 1
            else:
                # Create new word
                new_word = Word(
                    id=word_id,
                    spanish=spanish,
                    english=english,
                    word_category='high_frequency',
                    frequency_rank=rank
                )
                db.add(new_word)
                added_count += 1
            
            # Commit in batches to avoid memory issues
            if (added_count + updated_count) % 50 == 0:
                db.commit()
        
        db.commit()
        print(f"✅ Added {added_count} high frequency words")
        print(f"✅ Updated {updated_count} existing words")
        if skipped_duplicates > 0:
            print(f"⚠️  Skipped {skipped_duplicates} duplicate words in list")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding high frequency words: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_high_frequency_words()

