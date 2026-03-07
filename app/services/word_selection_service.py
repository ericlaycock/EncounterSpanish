from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from app.models import Word, Situation, SituationWord, UserWord
from typing import List, Set, Tuple


def get_learned_word_ids(db: Session, user_id) -> Set[str]:
    """Get set of word IDs the user has already encountered."""
    return {
        row[0] for row in
        db.query(UserWord.word_id).filter(UserWord.user_id == user_id).all()
    }


def select_words_for_grammar_situation(
    db: Session,
    situation_id: str,
) -> Tuple[List[str], List[str]]:
    """Select all words for a grammar situation (no high-freq onboarding).

    Returns (grammar_word_ids, []) — empty list for high-freq to match interface.
    """
    situation_words = db.query(SituationWord).filter(
        SituationWord.situation_id == situation_id
    ).order_by(SituationWord.position).all()
    grammar_word_ids = [sw.word_id for sw in situation_words]
    return grammar_word_ids, []


def select_words_for_situation(
    db: Session,
    user_id,
    situation_id: str,
    encounter_limit: int = 3,
    high_freq_limit: int = 2,
) -> Tuple[List[str], List[str]]:
    """Select encounter + high-frequency words for a situation.

    Returns (encounter_word_ids, high_freq_word_ids).
    For grammar situations, returns all grammar words with no high-freq.
    """
    situation = db.query(Situation).filter(Situation.id == situation_id).first()
    if situation and situation.situation_type == 'grammar':
        return select_words_for_grammar_situation(db, situation_id)

    situation_words = db.query(SituationWord).filter(
        SituationWord.situation_id == situation_id
    ).order_by(SituationWord.position).limit(encounter_limit).all()
    encounter_word_ids = [sw.word_id for sw in situation_words]

    learned_word_ids = get_learned_word_ids(db, user_id)

    high_freq_words = db.query(Word).filter(
        Word.word_category == "high_frequency",
        ~Word.id.in_(learned_word_ids) if learned_word_ids else True,
    ).order_by(Word.frequency_rank.asc().nullslast()).limit(high_freq_limit).all()
    high_freq_word_ids = [w.id for w in high_freq_words]

    return encounter_word_ids, high_freq_word_ids


def sort_words_encounter_first(
    words: List[Word],
    situation_id: str,
    db: Session,
    target_word_ids: List[str],
) -> List[Word]:
    """Sort words: encounter words by position first, then high-frequency."""
    word_dict = {w.id: w for w in words}
    situation_words = db.query(SituationWord).filter(
        SituationWord.situation_id == situation_id
    ).order_by(SituationWord.position).all()
    encounter_word_ids = {sw.word_id for sw in situation_words}

    sorted_encounter = [word_dict[sw.word_id] for sw in situation_words if sw.word_id in word_dict]
    sorted_high_freq = [word_dict[wid] for wid in target_word_ids if wid not in encounter_word_ids and wid in word_dict]

    return sorted_encounter + sorted_high_freq


def ensure_user_words(db: Session, user_id, words: List[Word]) -> None:
    """Create UserWord entries if they don't exist, increment seen_count."""
    for word in words:
        stmt = insert(UserWord).values(
            user_id=user_id,
            word_id=word.id,
            seen_count=1,
        ).on_conflict_do_update(
            index_elements=["user_id", "word_id"],
            set_={"seen_count": UserWord.seen_count + 1},
        )
        db.execute(stmt)
