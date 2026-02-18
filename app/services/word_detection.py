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
    Uses word boundary matching for better accuracy.
    """
    normalized_text = normalize_text(text)
    detected_word_ids = []
    
    for word in words:
        # Normalize the Spanish word/phrase
        normalized_word = normalize_text(word.spanish)
        
        # For multi-word phrases, check as substring
        # For single words, use word boundary matching
        if ' ' in normalized_word:
            # Multi-word phrase: check as substring
            if normalized_word in normalized_text:
                detected_word_ids.append(word.id)
        else:
            # Single word: use word boundary matching for accuracy
            # Check if word appears as whole word (not part of another word)
            import re
            pattern = r'\b' + re.escape(normalized_word) + r'\b'
            if re.search(pattern, normalized_text):
                detected_word_ids.append(word.id)
    
    return detected_word_ids


def get_words_by_ids(db: Session, word_ids: List[str]) -> List[Word]:
    """Get Word objects by their IDs"""
    return db.query(Word).filter(Word.id.in_(word_ids)).all()




    
    return detected_word_ids


def get_words_by_ids(db: Session, word_ids: List[str]) -> List[Word]:
    """Get Word objects by their IDs"""
    return db.query(Word).filter(Word.id.in_(word_ids)).all()




    
    return detected_word_ids


def get_words_by_ids(db: Session, word_ids: List[str]) -> List[Word]:
    """Get Word objects by their IDs"""
    return db.query(Word).filter(Word.id.in_(word_ids)).all()



