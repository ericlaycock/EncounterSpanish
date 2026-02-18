"""
Script to list all grammar-related words in the database.
Grammar words include: articles, pronouns, prepositions, conjunctions, common verbs, etc.
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
from app.database import SessionLocal
from app.models import Word

# Grammar word categories
GRAMMAR_CATEGORIES = {
    "articles": ["el", "la", "los", "las", "un", "una", "unos", "unas"],
    "pronouns": ["yo", "tú", "él", "ella", "nosotros", "nosotras", "vosotros", "vosotras", "ellos", "ellas",
                 "me", "te", "le", "nos", "os", "les", "lo", "la", "los", "las", "se"],
    "prepositions": ["a", "de", "en", "con", "por", "para", "sin", "sobre", "bajo", "entre", "hasta", "desde"],
    "conjunctions": ["y", "o", "pero", "porque", "que", "si", "cuando", "aunque", "mientras"],
    "common_verbs": ["ser", "estar", "tener", "hacer", "ir", "venir", "poder", "querer", "saber", "decir",
                     "dar", "ver", "haber", "pasar", "deber", "poner", "parecer", "quedar", "hablar",
                     "llevar", "dejar", "seguir", "encontrar", "llamar", "venir", "pensar", "salir",
                     "volver", "tomar", "contar", "conocer", "vivir", "sentir", "tratar", "mirar",
                     "esperar", "buscar", "existir", "entrar", "trabajar", "escribir", "perder",
                     "producir", "ocurrir", "entender", "pedir", "recibir", "recordar", "terminar",
                     "empezar", "acabar", "comenzar"],
    "question_words": ["qué", "cuál", "cuándo", "dónde", "cómo", "por qué", "quién", "cuánto"],
    "adverbs": ["muy", "más", "menos", "también", "tampoco", "siempre", "nunca", "ahora", "ya", "aún",
                "todavía", "aquí", "allí", "allá", "cerca", "lejos", "bien", "mal", "así", "entonces"],
    "possessive": ["mi", "tu", "su", "nuestro", "vuestro", "mío", "tuyo", "suyo"],
    "demonstrative": ["este", "esta", "estos", "estas", "ese", "esa", "esos", "esas", "aquel", "aquella",
                      "aquellos", "aquellas", "esto", "eso", "aquello"],
    "indefinite": ["algo", "alguien", "alguno", "alguna", "algunos", "algunas", "todo", "toda", "todos",
                   "todas", "cada", "otro", "otra", "otros", "otras", "mucho", "mucha", "muchos", "muchas",
                   "poco", "poca", "pocos", "pocas", "varios", "varias", "ninguno", "ninguna"],
    "phrases_with_grammar": ["del", "al", "porque", "me gusta", "te gusta", "le gusta", "nos gusta",
                             "os gusta", "les gusta", "mucho gusto", "por favor", "de nada"]
}

def get_all_words_from_db(db: Session):
    """Get all words from the database"""
    return db.query(Word).all()

def categorize_word(word: Word, grammar_categories: dict) -> list:
    """Categorize a word based on grammar categories"""
    spanish_lower = word.spanish.lower().strip()
    categories = []
    
    for category_name, words_list in grammar_categories.items():
        if spanish_lower in words_list:
            categories.append(category_name)
    
    return categories

def main():
    db: Session = SessionLocal()
    try:
        all_words = get_all_words_from_db(db)
        
        grammar_words = {}
        for word in all_words:
            categories = categorize_word(word, GRAMMAR_CATEGORIES)
            if categories:
                for cat in categories:
                    if cat not in grammar_words:
                        grammar_words[cat] = []
                    grammar_words[cat].append({
                        "id": word.id,
                        "spanish": word.spanish,
                        "english": word.english,
                        "category": word.word_category,
                        "frequency_rank": word.frequency_rank
                    })
        
        # Print results
        print("=" * 80)
        print("GRAMMAR-RELATED WORDS IN DATABASE")
        print("=" * 80)
        print()
        
        total_count = 0
        for category in sorted(grammar_words.keys()):
            words = grammar_words[category]
            print(f"\n{category.upper().replace('_', ' ')} ({len(words)} words):")
            print("-" * 80)
            for word in sorted(words, key=lambda x: x['spanish']):
                freq_info = f" (rank: {word['frequency_rank']})" if word['frequency_rank'] else ""
                cat_info = f" [{word['category']}]" if word['category'] else ""
                print(f"  • {word['spanish']:20} → {word['english']:30} {freq_info}{cat_info}")
                total_count += 1
        
        print()
        print("=" * 80)
        print(f"TOTAL GRAMMAR WORDS FOUND: {total_count}")
        print("=" * 80)
        
        # Also list words that might be grammar but aren't in our categories
        print("\n\nPOTENTIALLY MISSED GRAMMAR WORDS:")
        print("-" * 80)
        potential_grammar = []
        for word in all_words:
            spanish_lower = word.spanish.lower().strip()
            # Check for common patterns
            if (len(spanish_lower) <= 3 and 
                word.word_category == 'high_frequency' and
                spanish_lower not in [w for words_list in GRAMMAR_CATEGORIES.values() for w in words_list]):
                potential_grammar.append(word)
        
        for word in sorted(potential_grammar, key=lambda x: x.spanish):
            freq_info = f" (rank: {word.frequency_rank})" if word.frequency_rank else ""
            print(f"  • {word.spanish:20} → {word.english:30} {freq_info}")
        
    finally:
        db.close()

if __name__ == "__main__":
    main()



Script to list all grammar-related words in the database.
Grammar words include: articles, pronouns, prepositions, conjunctions, common verbs, etc.
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
from app.database import SessionLocal
from app.models import Word

# Grammar word categories
GRAMMAR_CATEGORIES = {
    "articles": ["el", "la", "los", "las", "un", "una", "unos", "unas"],
    "pronouns": ["yo", "tú", "él", "ella", "nosotros", "nosotras", "vosotros", "vosotras", "ellos", "ellas",
                 "me", "te", "le", "nos", "os", "les", "lo", "la", "los", "las", "se"],
    "prepositions": ["a", "de", "en", "con", "por", "para", "sin", "sobre", "bajo", "entre", "hasta", "desde"],
    "conjunctions": ["y", "o", "pero", "porque", "que", "si", "cuando", "aunque", "mientras"],
    "common_verbs": ["ser", "estar", "tener", "hacer", "ir", "venir", "poder", "querer", "saber", "decir",
                     "dar", "ver", "haber", "pasar", "deber", "poner", "parecer", "quedar", "hablar",
                     "llevar", "dejar", "seguir", "encontrar", "llamar", "venir", "pensar", "salir",
                     "volver", "tomar", "contar", "conocer", "vivir", "sentir", "tratar", "mirar",
                     "esperar", "buscar", "existir", "entrar", "trabajar", "escribir", "perder",
                     "producir", "ocurrir", "entender", "pedir", "recibir", "recordar", "terminar",
                     "empezar", "acabar", "comenzar"],
    "question_words": ["qué", "cuál", "cuándo", "dónde", "cómo", "por qué", "quién", "cuánto"],
    "adverbs": ["muy", "más", "menos", "también", "tampoco", "siempre", "nunca", "ahora", "ya", "aún",
                "todavía", "aquí", "allí", "allá", "cerca", "lejos", "bien", "mal", "así", "entonces"],
    "possessive": ["mi", "tu", "su", "nuestro", "vuestro", "mío", "tuyo", "suyo"],
    "demonstrative": ["este", "esta", "estos", "estas", "ese", "esa", "esos", "esas", "aquel", "aquella",
                      "aquellos", "aquellas", "esto", "eso", "aquello"],
    "indefinite": ["algo", "alguien", "alguno", "alguna", "algunos", "algunas", "todo", "toda", "todos",
                   "todas", "cada", "otro", "otra", "otros", "otras", "mucho", "mucha", "muchos", "muchas",
                   "poco", "poca", "pocos", "pocas", "varios", "varias", "ninguno", "ninguna"],
    "phrases_with_grammar": ["del", "al", "porque", "me gusta", "te gusta", "le gusta", "nos gusta",
                             "os gusta", "les gusta", "mucho gusto", "por favor", "de nada"]
}

def get_all_words_from_db(db: Session):
    """Get all words from the database"""
    return db.query(Word).all()

def categorize_word(word: Word, grammar_categories: dict) -> list:
    """Categorize a word based on grammar categories"""
    spanish_lower = word.spanish.lower().strip()
    categories = []
    
    for category_name, words_list in grammar_categories.items():
        if spanish_lower in words_list:
            categories.append(category_name)
    
    return categories

def main():
    db: Session = SessionLocal()
    try:
        all_words = get_all_words_from_db(db)
        
        grammar_words = {}
        for word in all_words:
            categories = categorize_word(word, GRAMMAR_CATEGORIES)
            if categories:
                for cat in categories:
                    if cat not in grammar_words:
                        grammar_words[cat] = []
                    grammar_words[cat].append({
                        "id": word.id,
                        "spanish": word.spanish,
                        "english": word.english,
                        "category": word.word_category,
                        "frequency_rank": word.frequency_rank
                    })
        
        # Print results
        print("=" * 80)
        print("GRAMMAR-RELATED WORDS IN DATABASE")
        print("=" * 80)
        print()
        
        total_count = 0
        for category in sorted(grammar_words.keys()):
            words = grammar_words[category]
            print(f"\n{category.upper().replace('_', ' ')} ({len(words)} words):")
            print("-" * 80)
            for word in sorted(words, key=lambda x: x['spanish']):
                freq_info = f" (rank: {word['frequency_rank']})" if word['frequency_rank'] else ""
                cat_info = f" [{word['category']}]" if word['category'] else ""
                print(f"  • {word['spanish']:20} → {word['english']:30} {freq_info}{cat_info}")
                total_count += 1
        
        print()
        print("=" * 80)
        print(f"TOTAL GRAMMAR WORDS FOUND: {total_count}")
        print("=" * 80)
        
        # Also list words that might be grammar but aren't in our categories
        print("\n\nPOTENTIALLY MISSED GRAMMAR WORDS:")
        print("-" * 80)
        potential_grammar = []
        for word in all_words:
            spanish_lower = word.spanish.lower().strip()
            # Check for common patterns
            if (len(spanish_lower) <= 3 and 
                word.word_category == 'high_frequency' and
                spanish_lower not in [w for words_list in GRAMMAR_CATEGORIES.values() for w in words_list]):
                potential_grammar.append(word)
        
        for word in sorted(potential_grammar, key=lambda x: x.spanish):
            freq_info = f" (rank: {word.frequency_rank})" if word.frequency_rank else ""
            print(f"  • {word.spanish:20} → {word.english:30} {freq_info}")
        
    finally:
        db.close()

if __name__ == "__main__":
    main()



Script to list all grammar-related words in the database.
Grammar words include: articles, pronouns, prepositions, conjunctions, common verbs, etc.
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
from app.database import SessionLocal
from app.models import Word

# Grammar word categories
GRAMMAR_CATEGORIES = {
    "articles": ["el", "la", "los", "las", "un", "una", "unos", "unas"],
    "pronouns": ["yo", "tú", "él", "ella", "nosotros", "nosotras", "vosotros", "vosotras", "ellos", "ellas",
                 "me", "te", "le", "nos", "os", "les", "lo", "la", "los", "las", "se"],
    "prepositions": ["a", "de", "en", "con", "por", "para", "sin", "sobre", "bajo", "entre", "hasta", "desde"],
    "conjunctions": ["y", "o", "pero", "porque", "que", "si", "cuando", "aunque", "mientras"],
    "common_verbs": ["ser", "estar", "tener", "hacer", "ir", "venir", "poder", "querer", "saber", "decir",
                     "dar", "ver", "haber", "pasar", "deber", "poner", "parecer", "quedar", "hablar",
                     "llevar", "dejar", "seguir", "encontrar", "llamar", "venir", "pensar", "salir",
                     "volver", "tomar", "contar", "conocer", "vivir", "sentir", "tratar", "mirar",
                     "esperar", "buscar", "existir", "entrar", "trabajar", "escribir", "perder",
                     "producir", "ocurrir", "entender", "pedir", "recibir", "recordar", "terminar",
                     "empezar", "acabar", "comenzar"],
    "question_words": ["qué", "cuál", "cuándo", "dónde", "cómo", "por qué", "quién", "cuánto"],
    "adverbs": ["muy", "más", "menos", "también", "tampoco", "siempre", "nunca", "ahora", "ya", "aún",
                "todavía", "aquí", "allí", "allá", "cerca", "lejos", "bien", "mal", "así", "entonces"],
    "possessive": ["mi", "tu", "su", "nuestro", "vuestro", "mío", "tuyo", "suyo"],
    "demonstrative": ["este", "esta", "estos", "estas", "ese", "esa", "esos", "esas", "aquel", "aquella",
                      "aquellos", "aquellas", "esto", "eso", "aquello"],
    "indefinite": ["algo", "alguien", "alguno", "alguna", "algunos", "algunas", "todo", "toda", "todos",
                   "todas", "cada", "otro", "otra", "otros", "otras", "mucho", "mucha", "muchos", "muchas",
                   "poco", "poca", "pocos", "pocas", "varios", "varias", "ninguno", "ninguna"],
    "phrases_with_grammar": ["del", "al", "porque", "me gusta", "te gusta", "le gusta", "nos gusta",
                             "os gusta", "les gusta", "mucho gusto", "por favor", "de nada"]
}

def get_all_words_from_db(db: Session):
    """Get all words from the database"""
    return db.query(Word).all()

def categorize_word(word: Word, grammar_categories: dict) -> list:
    """Categorize a word based on grammar categories"""
    spanish_lower = word.spanish.lower().strip()
    categories = []
    
    for category_name, words_list in grammar_categories.items():
        if spanish_lower in words_list:
            categories.append(category_name)
    
    return categories

def main():
    db: Session = SessionLocal()
    try:
        all_words = get_all_words_from_db(db)
        
        grammar_words = {}
        for word in all_words:
            categories = categorize_word(word, GRAMMAR_CATEGORIES)
            if categories:
                for cat in categories:
                    if cat not in grammar_words:
                        grammar_words[cat] = []
                    grammar_words[cat].append({
                        "id": word.id,
                        "spanish": word.spanish,
                        "english": word.english,
                        "category": word.word_category,
                        "frequency_rank": word.frequency_rank
                    })
        
        # Print results
        print("=" * 80)
        print("GRAMMAR-RELATED WORDS IN DATABASE")
        print("=" * 80)
        print()
        
        total_count = 0
        for category in sorted(grammar_words.keys()):
            words = grammar_words[category]
            print(f"\n{category.upper().replace('_', ' ')} ({len(words)} words):")
            print("-" * 80)
            for word in sorted(words, key=lambda x: x['spanish']):
                freq_info = f" (rank: {word['frequency_rank']})" if word['frequency_rank'] else ""
                cat_info = f" [{word['category']}]" if word['category'] else ""
                print(f"  • {word['spanish']:20} → {word['english']:30} {freq_info}{cat_info}")
                total_count += 1
        
        print()
        print("=" * 80)
        print(f"TOTAL GRAMMAR WORDS FOUND: {total_count}")
        print("=" * 80)
        
        # Also list words that might be grammar but aren't in our categories
        print("\n\nPOTENTIALLY MISSED GRAMMAR WORDS:")
        print("-" * 80)
        potential_grammar = []
        for word in all_words:
            spanish_lower = word.spanish.lower().strip()
            # Check for common patterns
            if (len(spanish_lower) <= 3 and 
                word.word_category == 'high_frequency' and
                spanish_lower not in [w for words_list in GRAMMAR_CATEGORIES.values() for w in words_list]):
                potential_grammar.append(word)
        
        for word in sorted(potential_grammar, key=lambda x: x.spanish):
            freq_info = f" (rank: {word.frequency_rank})" if word.frequency_rank else ""
            print(f"  • {word.spanish:20} → {word.english:30} {freq_info}")
        
    finally:
        db.close()

if __name__ == "__main__":
    main()



