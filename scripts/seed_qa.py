#!/usr/bin/env python3
"""Seed QA database with minimal realistic data.

Run with: python scripts/seed_qa.py
Uses DATABASE_URL from environment (same as the app).
Idempotent: uses ON CONFLICT DO NOTHING.
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

engine = create_engine(settings.database_url, pool_pre_ping=True)
Session = sessionmaker(bind=engine)


def seed():
    db = Session()
    try:
        # --- Words: 20 encounter + 10 high frequency ---
        encounter_words = [
            ("enc_bank_1", "cuenta", "account"),
            ("enc_bank_2", "depositar", "to deposit"),
            ("enc_bank_3", "retirar", "to withdraw"),
            ("enc_bank_4", "transferencia", "transfer"),
            ("enc_bank_5", "saldo", "balance"),
            ("enc_bank_6", "prestamo", "loan"),
            ("enc_rest_1", "mesa", "table"),
            ("enc_rest_2", "menu", "menu"),
            ("enc_rest_3", "propina", "tip"),
            ("enc_rest_4", "cuenta", "bill/check"),
            ("enc_rest_5", "mesero", "waiter"),
            ("enc_rest_6", "reservacion", "reservation"),
            ("enc_air_1", "pasaporte", "passport"),
            ("enc_air_2", "equipaje", "luggage"),
            ("enc_air_3", "vuelo", "flight"),
            ("enc_groc_1", "carrito", "cart"),
            ("enc_groc_2", "cajero", "cashier"),
            ("enc_groc_3", "bolsa", "bag"),
            ("enc_mech_1", "llanta", "tire"),
            ("enc_mech_2", "aceite", "oil"),
        ]
        for wid, spanish, english in encounter_words:
            stmt = insert(Word).values(
                id=wid, spanish=spanish, english=english, word_category="encounter"
            ).on_conflict_do_nothing()
            db.execute(stmt)

        high_freq_words = [
            ("hf_1", "hola", "hello", 1),
            ("hf_2", "gracias", "thank you", 2),
            ("hf_3", "por favor", "please", 3),
            ("hf_4", "si", "yes", 4),
            ("hf_5", "no", "no", 5),
            ("hf_6", "bueno", "good", 6),
            ("hf_7", "donde", "where", 7),
            ("hf_8", "cuanto", "how much", 8),
            ("hf_9", "necesito", "I need", 9),
            ("hf_10", "quiero", "I want", 10),
        ]
        for wid, spanish, english, rank in high_freq_words:
            stmt = insert(Word).values(
                id=wid, spanish=spanish, english=english,
                word_category="high_frequency", frequency_rank=rank
            ).on_conflict_do_nothing()
            db.execute(stmt)

        # --- Situations: 2 categories x 3 each ---
        situations = [
            ("banking_1", "Opening a Bank Account", "banking", 1, 1, True),
            ("banking_2", "Wire Transfer", "banking", 2, 2, False),
            ("banking_3", "Currency Exchange", "banking", 3, 3, False),
            ("restaurant_1", "Ordering Food", "restaurant", 1, 4, True),
            ("restaurant_2", "Making a Reservation", "restaurant", 2, 5, False),
            ("restaurant_3", "Asking for the Bill", "restaurant", 3, 6, False),
        ]
        for sid, title, category, series, order, free in situations:
            stmt = insert(Situation).values(
                id=sid, title=title, category=category,
                series_number=series, order_index=order, is_free=free
            ).on_conflict_do_nothing()
            db.execute(stmt)

        # --- SituationWords: 3 encounter words per situation ---
        links = [
            ("banking_1", "enc_bank_1", 1), ("banking_1", "enc_bank_2", 2), ("banking_1", "enc_bank_3", 3),
            ("banking_2", "enc_bank_4", 1), ("banking_2", "enc_bank_5", 2), ("banking_2", "enc_bank_6", 3),
            ("banking_3", "enc_bank_1", 1), ("banking_3", "enc_bank_4", 2), ("banking_3", "enc_bank_5", 3),
            ("restaurant_1", "enc_rest_1", 1), ("restaurant_1", "enc_rest_2", 2), ("restaurant_1", "enc_rest_3", 3),
            ("restaurant_2", "enc_rest_4", 1), ("restaurant_2", "enc_rest_5", 2), ("restaurant_2", "enc_rest_6", 3),
            ("restaurant_3", "enc_rest_1", 1), ("restaurant_3", "enc_rest_4", 2), ("restaurant_3", "enc_rest_5", 3),
        ]
        for sit_id, word_id, pos in links:
            stmt = insert(SituationWord).values(
                situation_id=sit_id, word_id=word_id, position=pos
            ).on_conflict_do_nothing()
            db.execute(stmt)

        # --- Grammar situations + words ---
        from app.data.grammar_situations import GRAMMAR_SITUATIONS

        # Create grammar words (word_category='grammar')
        grammar_word_set = set()
        for sid, cfg in GRAMMAR_SITUATIONS.items():
            for word in cfg["word_workload"]:
                if word not in grammar_word_set:
                    grammar_word_set.add(word)
                    word_id = f"grammar_{word}"
                    stmt = insert(Word).values(
                        id=word_id, spanish=word, english=word,
                        word_category="grammar"
                    ).on_conflict_do_nothing()
                    db.execute(stmt)

        # Create grammar situation records and SituationWord links
        order_offset = 1000  # High order_index so they don't interfere with main situations
        for sid, cfg in GRAMMAR_SITUATIONS.items():
            stmt = insert(Situation).values(
                id=sid,
                title=cfg["title"],
                category="grammar",
                series_number=cfg["vocab_level"],
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
            selected_situation_categories=["banking"],
            dialect="mexico",
        ).on_conflict_do_nothing()
        db.execute(stmt)

        stmt = insert(Subscription).values(
            user_id=test_user_id, active=False
        ).on_conflict_do_nothing()
        db.execute(stmt)

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
