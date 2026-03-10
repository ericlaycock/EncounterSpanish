#!/usr/bin/env python3
"""Seed QA database with minimal realistic data.

Run with: python scripts/seed_qa.py
Uses DATABASE_URL from environment (same as the app).
Idempotent: uses ON CONFLICT DO UPDATE for encounter/situation data.

All word/situation data comes from app/data/seed_bank.py and
app/data/grammar_situations.py — never hardcoded here.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import insert
from app.config import settings
from app.models import Base, User, Subscription, Word, Situation, SituationWord
from app.auth import get_password_hash
from app.data.seed_bank import (
    HIGH_FREQUENCY_WORDS,
    ENCOUNTER_WORDS,
    SITUATIONS,
    SITUATION_WORDS,
)
from app.data.grammar_situations import GRAMMAR_SITUATIONS, GRAMMAR_WORD_TRANSLATIONS

engine = create_engine(settings.database_url, pool_pre_ping=True)
Session = sessionmaker(bind=engine)


def seed():
    db = Session()
    try:
        # --- Encounter words (upsert to fix stale data) ---
        for category_words in ENCOUNTER_WORDS.values():
            for w in category_words:
                stmt = insert(Word).values(
                    id=w["id"], spanish=w["spanish"], english=w["english"],
                    word_category="encounter"
                ).on_conflict_do_update(
                    index_elements=["id"],
                    set_={"spanish": w["spanish"], "english": w["english"]},
                )
                db.execute(stmt)

        # --- High-frequency words ---
        for w in HIGH_FREQUENCY_WORDS:
            stmt = insert(Word).values(
                id=w["id"], spanish=w["spanish"], english=w["english"],
                word_category="high_frequency", frequency_rank=w["frequency_rank"]
            ).on_conflict_do_nothing()
            db.execute(stmt)

        # --- Situations (upsert to fix stale data) ---
        for s in SITUATIONS:
            stmt = insert(Situation).values(**s).on_conflict_do_update(
                index_elements=["id"],
                set_={k: v for k, v in s.items() if k != "id"},
            )
            db.execute(stmt)

        # --- SituationWords (upsert to fix stale data) ---
        for link in SITUATION_WORDS:
            stmt = insert(SituationWord).values(**link).on_conflict_do_update(
                index_elements=["situation_id", "word_id"],
                set_={"position": link["position"]},
            )
            db.execute(stmt)

        # --- Grammar situations + words ---
        grammar_word_set = set()
        for sid, cfg in GRAMMAR_SITUATIONS.items():
            for word in cfg["word_workload"]:
                if word not in grammar_word_set:
                    grammar_word_set.add(word)
                    word_id = f"grammar_{word}"
                    english = GRAMMAR_WORD_TRANSLATIONS.get(word, word)
                    stmt = insert(Word).values(
                        id=word_id, spanish=word, english=english,
                        word_category="grammar"
                    ).on_conflict_do_update(
                        index_elements=["id"],
                        set_={"english": english, "spanish": word},
                    )
                    db.execute(stmt)

        order_offset = 1000
        for sid, cfg in GRAMMAR_SITUATIONS.items():
            stmt = insert(Situation).values(
                id=sid,
                title=cfg["title"],
                animation_type="grammar",
                encounter_number=cfg["vocab_level"],
                order_index=order_offset + cfg["vocab_level"],
                is_free=True,
                situation_type="grammar",
                vocab_level_required=cfg["vocab_level"],
                video_embed_id=cfg["video_embed_id"],
            ).on_conflict_do_nothing()
            db.execute(stmt)

            for pos, word in enumerate(cfg["word_workload"], 1):
                word_id = f"grammar_{word}"
                stmt = insert(SituationWord).values(
                    situation_id=sid, word_id=word_id, position=pos
                ).on_conflict_do_nothing()
                db.execute(stmt)

        # --- Test user ---
        password_hash = get_password_hash("testpassword123")
        test_user_id = "00000000-0000-0000-0000-000000000001"
        stmt = insert(User).values(
            id=test_user_id,
            email="qa@test.com",
            password_hash=password_hash,
            onboarding_completed=True,
            selected_animation_types=["banking"],
            dialect="mexico",
        ).on_conflict_do_nothing()
        db.execute(stmt)

        stmt = insert(Subscription).values(
            user_id=test_user_id, active=False
        ).on_conflict_do_nothing()
        db.execute(stmt)

        # --- Set admin flag for admin user ---
        db.execute(text(
            "UPDATE users SET is_admin = true WHERE email = 'ericlaycock44@gmail.com'"
        ))

        db.commit()
        print("QA seed data inserted successfully.")
    except Exception as e:
        db.rollback()
        print(f"Seed failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
