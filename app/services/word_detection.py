import re
import unicodedata
from typing import List
from sqlalchemy.orm import Session
from app.models import Word


def normalize_text(text: str) -> str:
    """Normalize text: lowercase, remove punctuation, normalize accents"""
    # Lowercase
    text = text.lower()
    
    # Remove punctuation (keep spaces)
    text = re.sub(r'[^\w\s]', '', text)
    
    # Normalize accents (NFD decomposition, remove diacritics, recompose)
    text = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    
    return text


def detect_words_in_text(text: str, words: List[Word]) -> List[str]:
    """
    Detect which words/phrases appear in the given text.
    Returns list of word_ids that were detected.
    """
    normalized_text = normalize_text(text)
    detected_word_ids = []
    
    for word in words:
        # Normalize the Spanish word/phrase
        normalized_word = normalize_text(word.spanish)
        
        # Check if the normalized word appears as a substring
        if normalized_word in normalized_text:
            detected_word_ids.append(word.id)
    
    return detected_word_ids


def get_words_by_ids(db: Session, word_ids: List[str]) -> List[Word]:
    """Get Word objects by their IDs"""
    return db.query(Word).filter(Word.id.in_(word_ids)).all()



