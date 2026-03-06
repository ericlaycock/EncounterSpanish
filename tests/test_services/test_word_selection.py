import uuid
from app.services.word_selection_service import select_words_for_situation, sort_words_encounter_first
from app.models import Word, UserWord


def test_select_words_for_situation(db, seed_data):
    user_id = uuid.uuid4()
    encounter_ids, high_freq_ids = select_words_for_situation(db, user_id, "banking_1")
    assert len(encounter_ids) == 3
    assert encounter_ids == ["enc_1", "enc_2", "enc_3"]
    assert len(high_freq_ids) == 2
    assert high_freq_ids[0] == "hf_1"  # lowest frequency_rank first


def test_select_words_skips_learned(db, seed_data):
    user_id = uuid.uuid4()
    # Mark hf_1 as learned
    db.add(UserWord(user_id=user_id, word_id="hf_1", seen_count=1))
    db.flush()
    _, high_freq_ids = select_words_for_situation(db, user_id, "banking_1")
    assert "hf_1" not in high_freq_ids
    assert high_freq_ids[0] == "hf_2"


def test_sort_words_encounter_first(db, seed_data):
    target_ids = ["enc_1", "enc_2", "enc_3", "hf_1", "hf_2"]
    words = db.query(Word).filter(Word.id.in_(target_ids)).all()
    sorted_words = sort_words_encounter_first(words, "banking_1", db, target_ids)
    sorted_ids = [w.id for w in sorted_words]
    # Encounter words should come first, in position order
    assert sorted_ids[:3] == ["enc_1", "enc_2", "enc_3"]
    # High freq words after
    assert set(sorted_ids[3:]) == {"hf_1", "hf_2"}
