"""
Add notes to MEDIUM complexity words in the database.
Simple 2-sentence explanations with examples.
"""
import sys
import os
from pathlib import Path

env_path = Path(__file__).parent.parent / '.env'
if env_path.exists():
    from dotenv import load_dotenv
    load_dotenv(env_path)

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Word

# MEDIUM complexity words with simple notes
WORD_NOTES = {
    # Accent marks change meaning
    "que": """Qué with an accent means "what" when asking questions. Que without an accent means "that" or "which" when connecting ideas.

¿Qué es esto? (What is this?)
El libro que leí (The book that I read)""",

    "qué": """Qué with an accent means "what" when asking questions. Que without an accent means "that" or "which" when connecting ideas.

¿Qué es esto? (What is this?)
El libro que leí (The book that I read)""",

    "cuando": """Cuándo with an accent means "when" in questions. Cuando without an accent means "when" as a connecting word.

¿Cuándo vienes? (When are you coming?)
Cuando llegué (When I arrived)""",

    "cuándo": """Cuándo with an accent means "when" in questions. Cuando without an accent means "when" as a connecting word.

¿Cuándo vienes? (When are you coming?)
Cuando llegué (When I arrived)""",

    "donde": """Dónde with an accent means "where" in questions. Donde without an accent means "where" as a connecting word.

¿Dónde está? (Where is it?)
La casa donde vivo (The house where I live)""",

    "dónde": """Dónde with an accent means "where" in questions. Donde without an accent means "where" as a connecting word.

¿Dónde está? (Where is it?)
La casa donde vivo (The house where I live)""",

    "cual": """Cuál with an accent means "which" in questions. Cual without an accent means "which" as a connecting word (formal).

¿Cuál prefieres? (Which do you prefer?)
El cual es mejor (Which one is better)""",

    "cuál": """Cuál with an accent means "which" in questions. Cual without an accent means "which" as a connecting word (formal).

¿Cuál prefieres? (Which do you prefer?)
El cual es mejor (Which one is better)""",

    "cuanto": """Cuánto with an accent means "how much" in questions. Cuanto without an accent means "as much as".

¿Cuánto cuesta? (How much does it cost?)
Tanto cuanto puedas (As much as you can)""",

    "cuánto": """Cuánto with an accent means "how much" in questions. Cuanto without an accent means "as much as".

¿Cuánto cuesta? (How much does it cost?)
Tanto cuanto puedas (As much as you can)""",

    "cuántos": """Cuántos with an accent means "how many" in questions. Always use the accent when asking.

¿Cuántos años tienes? (How many years do you have?)
¿Cuántos libros? (How many books?)""",

    "adónde": """Adónde means "where to" when asking about going somewhere. Always use the accent.

¿Adónde vas? (Where are you going to?)
¿Adónde vamos? (Where are we going to?)""",

    "porque": """Porque means "because" when explaining why. Porqué with an accent is a noun meaning "the reason why" (rare).

Vine porque quería (I came because I wanted)
No sé el porqué (I don't know the reason why)""",

    "porqué": """Porqué with an accent is a noun meaning "the reason why". Porque without an accent means "because".

No sé el porqué (I don't know the reason why)
Vine porque quería (I came because I wanted)""",

    "si": """Sí with an accent means "yes". Si without an accent means "if".

Sí, quiero (Yes, I want)
Si quieres, vamos (If you want, let's go)""",

    "sí": """Sí with an accent means "yes". Si without an accent means "if".

Sí, quiero (Yes, I want)
Si quieres, vamos (If you want, let's go)""",

    "mas": """Más with an accent means "more". Mas without an accent means "but" (very formal, rarely used).

Más grande (Bigger)
Mas no pudo (But he couldn't - formal)""",

    "más": """Más with an accent means "more". Mas without an accent means "but" (very formal, rarely used).

Más grande (Bigger)
Mas no pudo (But he couldn't - formal)""",

    "como": """Cómo with an accent means "how" in questions. Como without an accent means "like" or "as".

¿Cómo estás? (How are you?)
Como tú (Like you)""",

    "cómo": """Cómo with an accent means "how" in questions. Como without an accent means "like" or "as".

¿Cómo estás? (How are you?)
Como tú (Like you)""",

    # Two "to be"
    "ser": """Ser is used for things that don't change, like who you are or what something is. Estar is used for things that can change, like how you feel or where you are.

Soy médico (I am a doctor - permanent)
La comida es buena (The food is good - always good)""",

    "estar": """Estar is used for things that can change, like how you feel or where you are. Ser is used for things that don't change, like who you are.

Estoy cansado (I am tired - temporary)
La comida está buena (The food tastes good right now)""",

    # Two "for"
    "por": """Por is used for reasons, duration, or going through something. Para is used for purpose, destination, or deadlines.

Lo hice por ti (I did it for you - reason)
Por la mañana (During the morning)""",

    "para": """Para is used for purpose, destination, or deadlines. Por is used for reasons, duration, or going through something.

Es para ti (It's for you - destination)
Para mañana (By tomorrow - deadline)""",

    # Contractions
    "del": """Del is the only way to say "of the" or "from the" in Spanish. It's a contraction of "de" and "el".

La casa del profesor (The professor's house)
Vengo del banco (I come from the bank)""",

    "al": """Al is the only way to say "to the" in Spanish. It's a contraction of "a" and "el".

Voy al banco (I'm going to the bank)
Vamos al parque (We're going to the park)""",

    # "There is/are" forms
    "hay": """Hay means "there is" or "there are" right now. Había means "there was" or "there were" in the past.

Hay un problema (There is a problem)
Hay dos libros (There are two books)""",

    "había": """Había means "there was" or "there were" in the past. Hay means "there is" or "there are" right now.

Había un problema (There was a problem)
Había dos libros (There were two books)""",

    "habrá": """Habrá means "there will be" in the future. Hay means "there is" or "there are" right now.

Habrá un problema (There will be a problem)
Habrá dos libros (There will be two books)""",

    "habría": """Habría means "there would be" if something happened. Hay means "there is" or "there are" right now.

Habría un problema (There would be a problem)
Habría dos libros (There would be two books)""",

    # Time "ago"
    "hace": """Hace means "ago" when talking about time. It works backwards from English.

Hace dos días (Two days ago)
Hace una semana (One week ago)""",

    # Demonstratives
    "este": """Este means "this" for masculine things that are close to you. Esta means "this" for feminine things.

Este libro (This book - masculine)
Este niño (This boy)""",

    "esta": """Esta means "this" for feminine things that are close to you. Este means "this" for masculine things.

Esta casa (This house - feminine)
Esta niña (This girl)""",

    "esto": """Esto means "this" when you don't know what the thing is. Use este or esta when you know the thing.

¿Qué es esto? (What is this? - unknown thing)
Esto es bueno (This is good - unknown thing)""",

    "ese": """Ese means "that" for masculine things that are not close to you. Esa means "that" for feminine things.

Ese libro (That book - masculine)
Ese niño (That boy)""",

    "esa": """Esa means "that" for feminine things that are not close to you. Ese means "that" for masculine things.

Esa casa (That house - feminine)
Esa niña (That girl)""",

    "eso": """Eso means "that" when you don't know what the thing is. Use ese or esa when you know the thing.

¿Qué es eso? (What is that? - unknown thing)
Eso es bueno (That is good - unknown thing)""",

    # Possessives
    "mi": """Mi means "my" for one thing. Mis means "my" for more than one thing.

Mi casa (My house)
Mi libro (My book)""",

    "mis": """Mis means "my" for more than one thing. Mi means "my" for one thing.

Mis casas (My houses)
Mis libros (My books)""",

    "tu": """Tu means "your" for one thing. Tus means "your" for more than one thing.

Tu casa (Your house)
Tu libro (Your book)""",

    "tus": """Tus means "your" for more than one thing. Tu means "your" for one thing.

Tus casas (Your houses)
Tus libros (Your books)""",

    "su": """Su can mean "his", "her", "your", or "their" - you need context to know which one. Sus is the same but for more than one thing.

Su casa (His/her/your/their house - context tells you)
Su libro (His/her/your/their book)""",

    "sus": """Sus can mean "his", "her", "your", or "their" for more than one thing - you need context to know which one. Su is the same but for one thing.

Sus casas (His/her/your/their houses - context tells you)
Sus libros (His/her/your/their books)""",

    # Question vs relative
    "quien": """Quién with an accent means "who" in questions. Quien without an accent means "who" as a connecting word.

¿Quién es? (Who is it?)
La persona quien vino (The person who came)""",

    "quién": """Quién with an accent means "who" in questions. Quien without an accent means "who" as a connecting word.

¿Quién es? (Who is it?)
La persona quien vino (The person who came)""",

    # "De" multiple uses
    "de": """De can mean "of", "from", or show who owns something. It's very common and has many uses.

El libro de Juan (Juan's book - ownership)
Soy de México (I'm from Mexico - origin)
Casa de madera (Wooden house - material)""",

    # "Con" special forms
    "con": """Con means "with". Use conmigo for "with me" and contigo for "with you" - these are special forms.

Voy con él (I go with him)
Ven conmigo (Come with me - special form)""",

    "conmigo": """Conmigo means "with me" - it's a special form. You can't say "con yo", you must say "conmigo".

Ven conmigo (Come with me)
Voy conmigo (I go with me)""",

    "contigo": """Contigo means "with you" - it's a special form. You can't say "con tú", you must say "contigo".

Voy contigo (I go with you)
Ven contigo (Come with you)""",

    # Dual meanings
    "tiempo": """Tiempo can mean "time" or "weather". You need context to know which one.

No tengo tiempo (I don't have time)
¿Qué tiempo hace? (What's the weather like?)""",

    "mañana": """Mañana can mean "morning" or "tomorrow". You need context to know which one.

Por la mañana (In the morning)
Mañana voy (Tomorrow I go)""",
}

def add_notes_to_words():
    """Add notes to MEDIUM complexity words"""
    db: Session = SessionLocal()
    try:
        updated_count = 0
        not_found = []
        
        for spanish_word, note_text in WORD_NOTES.items():
            # Try to find the word (could be encounter or high-frequency)
            word = db.query(Word).filter(Word.spanish == spanish_word).first()
            
            if word:
                word.notes = note_text
                updated_count += 1
                print(f"✅ Updated: {spanish_word}")
            else:
                not_found.append(spanish_word)
        
        db.commit()
        print(f"\n✅ Updated {updated_count} words with notes")
        if not_found:
            print(f"⚠️  Not found in database: {', '.join(not_found)}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    add_notes_to_words()



Add notes to MEDIUM complexity words in the database.
Simple 2-sentence explanations with examples.
"""
import sys
import os
from pathlib import Path

env_path = Path(__file__).parent.parent / '.env'
if env_path.exists():
    from dotenv import load_dotenv
    load_dotenv(env_path)

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Word

# MEDIUM complexity words with simple notes
WORD_NOTES = {
    # Accent marks change meaning
    "que": """Qué with an accent means "what" when asking questions. Que without an accent means "that" or "which" when connecting ideas.

¿Qué es esto? (What is this?)
El libro que leí (The book that I read)""",

    "qué": """Qué with an accent means "what" when asking questions. Que without an accent means "that" or "which" when connecting ideas.

¿Qué es esto? (What is this?)
El libro que leí (The book that I read)""",

    "cuando": """Cuándo with an accent means "when" in questions. Cuando without an accent means "when" as a connecting word.

¿Cuándo vienes? (When are you coming?)
Cuando llegué (When I arrived)""",

    "cuándo": """Cuándo with an accent means "when" in questions. Cuando without an accent means "when" as a connecting word.

¿Cuándo vienes? (When are you coming?)
Cuando llegué (When I arrived)""",

    "donde": """Dónde with an accent means "where" in questions. Donde without an accent means "where" as a connecting word.

¿Dónde está? (Where is it?)
La casa donde vivo (The house where I live)""",

    "dónde": """Dónde with an accent means "where" in questions. Donde without an accent means "where" as a connecting word.

¿Dónde está? (Where is it?)
La casa donde vivo (The house where I live)""",

    "cual": """Cuál with an accent means "which" in questions. Cual without an accent means "which" as a connecting word (formal).

¿Cuál prefieres? (Which do you prefer?)
El cual es mejor (Which one is better)""",

    "cuál": """Cuál with an accent means "which" in questions. Cual without an accent means "which" as a connecting word (formal).

¿Cuál prefieres? (Which do you prefer?)
El cual es mejor (Which one is better)""",

    "cuanto": """Cuánto with an accent means "how much" in questions. Cuanto without an accent means "as much as".

¿Cuánto cuesta? (How much does it cost?)
Tanto cuanto puedas (As much as you can)""",

    "cuánto": """Cuánto with an accent means "how much" in questions. Cuanto without an accent means "as much as".

¿Cuánto cuesta? (How much does it cost?)
Tanto cuanto puedas (As much as you can)""",

    "cuántos": """Cuántos with an accent means "how many" in questions. Always use the accent when asking.

¿Cuántos años tienes? (How many years do you have?)
¿Cuántos libros? (How many books?)""",

    "adónde": """Adónde means "where to" when asking about going somewhere. Always use the accent.

¿Adónde vas? (Where are you going to?)
¿Adónde vamos? (Where are we going to?)""",

    "porque": """Porque means "because" when explaining why. Porqué with an accent is a noun meaning "the reason why" (rare).

Vine porque quería (I came because I wanted)
No sé el porqué (I don't know the reason why)""",

    "porqué": """Porqué with an accent is a noun meaning "the reason why". Porque without an accent means "because".

No sé el porqué (I don't know the reason why)
Vine porque quería (I came because I wanted)""",

    "si": """Sí with an accent means "yes". Si without an accent means "if".

Sí, quiero (Yes, I want)
Si quieres, vamos (If you want, let's go)""",

    "sí": """Sí with an accent means "yes". Si without an accent means "if".

Sí, quiero (Yes, I want)
Si quieres, vamos (If you want, let's go)""",

    "mas": """Más with an accent means "more". Mas without an accent means "but" (very formal, rarely used).

Más grande (Bigger)
Mas no pudo (But he couldn't - formal)""",

    "más": """Más with an accent means "more". Mas without an accent means "but" (very formal, rarely used).

Más grande (Bigger)
Mas no pudo (But he couldn't - formal)""",

    "como": """Cómo with an accent means "how" in questions. Como without an accent means "like" or "as".

¿Cómo estás? (How are you?)
Como tú (Like you)""",

    "cómo": """Cómo with an accent means "how" in questions. Como without an accent means "like" or "as".

¿Cómo estás? (How are you?)
Como tú (Like you)""",

    # Two "to be"
    "ser": """Ser is used for things that don't change, like who you are or what something is. Estar is used for things that can change, like how you feel or where you are.

Soy médico (I am a doctor - permanent)
La comida es buena (The food is good - always good)""",

    "estar": """Estar is used for things that can change, like how you feel or where you are. Ser is used for things that don't change, like who you are.

Estoy cansado (I am tired - temporary)
La comida está buena (The food tastes good right now)""",

    # Two "for"
    "por": """Por is used for reasons, duration, or going through something. Para is used for purpose, destination, or deadlines.

Lo hice por ti (I did it for you - reason)
Por la mañana (During the morning)""",

    "para": """Para is used for purpose, destination, or deadlines. Por is used for reasons, duration, or going through something.

Es para ti (It's for you - destination)
Para mañana (By tomorrow - deadline)""",

    # Contractions
    "del": """Del is the only way to say "of the" or "from the" in Spanish. It's a contraction of "de" and "el".

La casa del profesor (The professor's house)
Vengo del banco (I come from the bank)""",

    "al": """Al is the only way to say "to the" in Spanish. It's a contraction of "a" and "el".

Voy al banco (I'm going to the bank)
Vamos al parque (We're going to the park)""",

    # "There is/are" forms
    "hay": """Hay means "there is" or "there are" right now. Había means "there was" or "there were" in the past.

Hay un problema (There is a problem)
Hay dos libros (There are two books)""",

    "había": """Había means "there was" or "there were" in the past. Hay means "there is" or "there are" right now.

Había un problema (There was a problem)
Había dos libros (There were two books)""",

    "habrá": """Habrá means "there will be" in the future. Hay means "there is" or "there are" right now.

Habrá un problema (There will be a problem)
Habrá dos libros (There will be two books)""",

    "habría": """Habría means "there would be" if something happened. Hay means "there is" or "there are" right now.

Habría un problema (There would be a problem)
Habría dos libros (There would be two books)""",

    # Time "ago"
    "hace": """Hace means "ago" when talking about time. It works backwards from English.

Hace dos días (Two days ago)
Hace una semana (One week ago)""",

    # Demonstratives
    "este": """Este means "this" for masculine things that are close to you. Esta means "this" for feminine things.

Este libro (This book - masculine)
Este niño (This boy)""",

    "esta": """Esta means "this" for feminine things that are close to you. Este means "this" for masculine things.

Esta casa (This house - feminine)
Esta niña (This girl)""",

    "esto": """Esto means "this" when you don't know what the thing is. Use este or esta when you know the thing.

¿Qué es esto? (What is this? - unknown thing)
Esto es bueno (This is good - unknown thing)""",

    "ese": """Ese means "that" for masculine things that are not close to you. Esa means "that" for feminine things.

Ese libro (That book - masculine)
Ese niño (That boy)""",

    "esa": """Esa means "that" for feminine things that are not close to you. Ese means "that" for masculine things.

Esa casa (That house - feminine)
Esa niña (That girl)""",

    "eso": """Eso means "that" when you don't know what the thing is. Use ese or esa when you know the thing.

¿Qué es eso? (What is that? - unknown thing)
Eso es bueno (That is good - unknown thing)""",

    # Possessives
    "mi": """Mi means "my" for one thing. Mis means "my" for more than one thing.

Mi casa (My house)
Mi libro (My book)""",

    "mis": """Mis means "my" for more than one thing. Mi means "my" for one thing.

Mis casas (My houses)
Mis libros (My books)""",

    "tu": """Tu means "your" for one thing. Tus means "your" for more than one thing.

Tu casa (Your house)
Tu libro (Your book)""",

    "tus": """Tus means "your" for more than one thing. Tu means "your" for one thing.

Tus casas (Your houses)
Tus libros (Your books)""",

    "su": """Su can mean "his", "her", "your", or "their" - you need context to know which one. Sus is the same but for more than one thing.

Su casa (His/her/your/their house - context tells you)
Su libro (His/her/your/their book)""",

    "sus": """Sus can mean "his", "her", "your", or "their" for more than one thing - you need context to know which one. Su is the same but for one thing.

Sus casas (His/her/your/their houses - context tells you)
Sus libros (His/her/your/their books)""",

    # Question vs relative
    "quien": """Quién with an accent means "who" in questions. Quien without an accent means "who" as a connecting word.

¿Quién es? (Who is it?)
La persona quien vino (The person who came)""",

    "quién": """Quién with an accent means "who" in questions. Quien without an accent means "who" as a connecting word.

¿Quién es? (Who is it?)
La persona quien vino (The person who came)""",

    # "De" multiple uses
    "de": """De can mean "of", "from", or show who owns something. It's very common and has many uses.

El libro de Juan (Juan's book - ownership)
Soy de México (I'm from Mexico - origin)
Casa de madera (Wooden house - material)""",

    # "Con" special forms
    "con": """Con means "with". Use conmigo for "with me" and contigo for "with you" - these are special forms.

Voy con él (I go with him)
Ven conmigo (Come with me - special form)""",

    "conmigo": """Conmigo means "with me" - it's a special form. You can't say "con yo", you must say "conmigo".

Ven conmigo (Come with me)
Voy conmigo (I go with me)""",

    "contigo": """Contigo means "with you" - it's a special form. You can't say "con tú", you must say "contigo".

Voy contigo (I go with you)
Ven contigo (Come with you)""",

    # Dual meanings
    "tiempo": """Tiempo can mean "time" or "weather". You need context to know which one.

No tengo tiempo (I don't have time)
¿Qué tiempo hace? (What's the weather like?)""",

    "mañana": """Mañana can mean "morning" or "tomorrow". You need context to know which one.

Por la mañana (In the morning)
Mañana voy (Tomorrow I go)""",
}

def add_notes_to_words():
    """Add notes to MEDIUM complexity words"""
    db: Session = SessionLocal()
    try:
        updated_count = 0
        not_found = []
        
        for spanish_word, note_text in WORD_NOTES.items():
            # Try to find the word (could be encounter or high-frequency)
            word = db.query(Word).filter(Word.spanish == spanish_word).first()
            
            if word:
                word.notes = note_text
                updated_count += 1
                print(f"✅ Updated: {spanish_word}")
            else:
                not_found.append(spanish_word)
        
        db.commit()
        print(f"\n✅ Updated {updated_count} words with notes")
        if not_found:
            print(f"⚠️  Not found in database: {', '.join(not_found)}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    add_notes_to_words()



Add notes to MEDIUM complexity words in the database.
Simple 2-sentence explanations with examples.
"""
import sys
import os
from pathlib import Path

env_path = Path(__file__).parent.parent / '.env'
if env_path.exists():
    from dotenv import load_dotenv
    load_dotenv(env_path)

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Word

# MEDIUM complexity words with simple notes
WORD_NOTES = {
    # Accent marks change meaning
    "que": """Qué with an accent means "what" when asking questions. Que without an accent means "that" or "which" when connecting ideas.

¿Qué es esto? (What is this?)
El libro que leí (The book that I read)""",

    "qué": """Qué with an accent means "what" when asking questions. Que without an accent means "that" or "which" when connecting ideas.

¿Qué es esto? (What is this?)
El libro que leí (The book that I read)""",

    "cuando": """Cuándo with an accent means "when" in questions. Cuando without an accent means "when" as a connecting word.

¿Cuándo vienes? (When are you coming?)
Cuando llegué (When I arrived)""",

    "cuándo": """Cuándo with an accent means "when" in questions. Cuando without an accent means "when" as a connecting word.

¿Cuándo vienes? (When are you coming?)
Cuando llegué (When I arrived)""",

    "donde": """Dónde with an accent means "where" in questions. Donde without an accent means "where" as a connecting word.

¿Dónde está? (Where is it?)
La casa donde vivo (The house where I live)""",

    "dónde": """Dónde with an accent means "where" in questions. Donde without an accent means "where" as a connecting word.

¿Dónde está? (Where is it?)
La casa donde vivo (The house where I live)""",

    "cual": """Cuál with an accent means "which" in questions. Cual without an accent means "which" as a connecting word (formal).

¿Cuál prefieres? (Which do you prefer?)
El cual es mejor (Which one is better)""",

    "cuál": """Cuál with an accent means "which" in questions. Cual without an accent means "which" as a connecting word (formal).

¿Cuál prefieres? (Which do you prefer?)
El cual es mejor (Which one is better)""",

    "cuanto": """Cuánto with an accent means "how much" in questions. Cuanto without an accent means "as much as".

¿Cuánto cuesta? (How much does it cost?)
Tanto cuanto puedas (As much as you can)""",

    "cuánto": """Cuánto with an accent means "how much" in questions. Cuanto without an accent means "as much as".

¿Cuánto cuesta? (How much does it cost?)
Tanto cuanto puedas (As much as you can)""",

    "cuántos": """Cuántos with an accent means "how many" in questions. Always use the accent when asking.

¿Cuántos años tienes? (How many years do you have?)
¿Cuántos libros? (How many books?)""",

    "adónde": """Adónde means "where to" when asking about going somewhere. Always use the accent.

¿Adónde vas? (Where are you going to?)
¿Adónde vamos? (Where are we going to?)""",

    "porque": """Porque means "because" when explaining why. Porqué with an accent is a noun meaning "the reason why" (rare).

Vine porque quería (I came because I wanted)
No sé el porqué (I don't know the reason why)""",

    "porqué": """Porqué with an accent is a noun meaning "the reason why". Porque without an accent means "because".

No sé el porqué (I don't know the reason why)
Vine porque quería (I came because I wanted)""",

    "si": """Sí with an accent means "yes". Si without an accent means "if".

Sí, quiero (Yes, I want)
Si quieres, vamos (If you want, let's go)""",

    "sí": """Sí with an accent means "yes". Si without an accent means "if".

Sí, quiero (Yes, I want)
Si quieres, vamos (If you want, let's go)""",

    "mas": """Más with an accent means "more". Mas without an accent means "but" (very formal, rarely used).

Más grande (Bigger)
Mas no pudo (But he couldn't - formal)""",

    "más": """Más with an accent means "more". Mas without an accent means "but" (very formal, rarely used).

Más grande (Bigger)
Mas no pudo (But he couldn't - formal)""",

    "como": """Cómo with an accent means "how" in questions. Como without an accent means "like" or "as".

¿Cómo estás? (How are you?)
Como tú (Like you)""",

    "cómo": """Cómo with an accent means "how" in questions. Como without an accent means "like" or "as".

¿Cómo estás? (How are you?)
Como tú (Like you)""",

    # Two "to be"
    "ser": """Ser is used for things that don't change, like who you are or what something is. Estar is used for things that can change, like how you feel or where you are.

Soy médico (I am a doctor - permanent)
La comida es buena (The food is good - always good)""",

    "estar": """Estar is used for things that can change, like how you feel or where you are. Ser is used for things that don't change, like who you are.

Estoy cansado (I am tired - temporary)
La comida está buena (The food tastes good right now)""",

    # Two "for"
    "por": """Por is used for reasons, duration, or going through something. Para is used for purpose, destination, or deadlines.

Lo hice por ti (I did it for you - reason)
Por la mañana (During the morning)""",

    "para": """Para is used for purpose, destination, or deadlines. Por is used for reasons, duration, or going through something.

Es para ti (It's for you - destination)
Para mañana (By tomorrow - deadline)""",

    # Contractions
    "del": """Del is the only way to say "of the" or "from the" in Spanish. It's a contraction of "de" and "el".

La casa del profesor (The professor's house)
Vengo del banco (I come from the bank)""",

    "al": """Al is the only way to say "to the" in Spanish. It's a contraction of "a" and "el".

Voy al banco (I'm going to the bank)
Vamos al parque (We're going to the park)""",

    # "There is/are" forms
    "hay": """Hay means "there is" or "there are" right now. Había means "there was" or "there were" in the past.

Hay un problema (There is a problem)
Hay dos libros (There are two books)""",

    "había": """Había means "there was" or "there were" in the past. Hay means "there is" or "there are" right now.

Había un problema (There was a problem)
Había dos libros (There were two books)""",

    "habrá": """Habrá means "there will be" in the future. Hay means "there is" or "there are" right now.

Habrá un problema (There will be a problem)
Habrá dos libros (There will be two books)""",

    "habría": """Habría means "there would be" if something happened. Hay means "there is" or "there are" right now.

Habría un problema (There would be a problem)
Habría dos libros (There would be two books)""",

    # Time "ago"
    "hace": """Hace means "ago" when talking about time. It works backwards from English.

Hace dos días (Two days ago)
Hace una semana (One week ago)""",

    # Demonstratives
    "este": """Este means "this" for masculine things that are close to you. Esta means "this" for feminine things.

Este libro (This book - masculine)
Este niño (This boy)""",

    "esta": """Esta means "this" for feminine things that are close to you. Este means "this" for masculine things.

Esta casa (This house - feminine)
Esta niña (This girl)""",

    "esto": """Esto means "this" when you don't know what the thing is. Use este or esta when you know the thing.

¿Qué es esto? (What is this? - unknown thing)
Esto es bueno (This is good - unknown thing)""",

    "ese": """Ese means "that" for masculine things that are not close to you. Esa means "that" for feminine things.

Ese libro (That book - masculine)
Ese niño (That boy)""",

    "esa": """Esa means "that" for feminine things that are not close to you. Ese means "that" for masculine things.

Esa casa (That house - feminine)
Esa niña (That girl)""",

    "eso": """Eso means "that" when you don't know what the thing is. Use ese or esa when you know the thing.

¿Qué es eso? (What is that? - unknown thing)
Eso es bueno (That is good - unknown thing)""",

    # Possessives
    "mi": """Mi means "my" for one thing. Mis means "my" for more than one thing.

Mi casa (My house)
Mi libro (My book)""",

    "mis": """Mis means "my" for more than one thing. Mi means "my" for one thing.

Mis casas (My houses)
Mis libros (My books)""",

    "tu": """Tu means "your" for one thing. Tus means "your" for more than one thing.

Tu casa (Your house)
Tu libro (Your book)""",

    "tus": """Tus means "your" for more than one thing. Tu means "your" for one thing.

Tus casas (Your houses)
Tus libros (Your books)""",

    "su": """Su can mean "his", "her", "your", or "their" - you need context to know which one. Sus is the same but for more than one thing.

Su casa (His/her/your/their house - context tells you)
Su libro (His/her/your/their book)""",

    "sus": """Sus can mean "his", "her", "your", or "their" for more than one thing - you need context to know which one. Su is the same but for one thing.

Sus casas (His/her/your/their houses - context tells you)
Sus libros (His/her/your/their books)""",

    # Question vs relative
    "quien": """Quién with an accent means "who" in questions. Quien without an accent means "who" as a connecting word.

¿Quién es? (Who is it?)
La persona quien vino (The person who came)""",

    "quién": """Quién with an accent means "who" in questions. Quien without an accent means "who" as a connecting word.

¿Quién es? (Who is it?)
La persona quien vino (The person who came)""",

    # "De" multiple uses
    "de": """De can mean "of", "from", or show who owns something. It's very common and has many uses.

El libro de Juan (Juan's book - ownership)
Soy de México (I'm from Mexico - origin)
Casa de madera (Wooden house - material)""",

    # "Con" special forms
    "con": """Con means "with". Use conmigo for "with me" and contigo for "with you" - these are special forms.

Voy con él (I go with him)
Ven conmigo (Come with me - special form)""",

    "conmigo": """Conmigo means "with me" - it's a special form. You can't say "con yo", you must say "conmigo".

Ven conmigo (Come with me)
Voy conmigo (I go with me)""",

    "contigo": """Contigo means "with you" - it's a special form. You can't say "con tú", you must say "contigo".

Voy contigo (I go with you)
Ven contigo (Come with you)""",

    # Dual meanings
    "tiempo": """Tiempo can mean "time" or "weather". You need context to know which one.

No tengo tiempo (I don't have time)
¿Qué tiempo hace? (What's the weather like?)""",

    "mañana": """Mañana can mean "morning" or "tomorrow". You need context to know which one.

Por la mañana (In the morning)
Mañana voy (Tomorrow I go)""",
}

def add_notes_to_words():
    """Add notes to MEDIUM complexity words"""
    db: Session = SessionLocal()
    try:
        updated_count = 0
        not_found = []
        
        for spanish_word, note_text in WORD_NOTES.items():
            # Try to find the word (could be encounter or high-frequency)
            word = db.query(Word).filter(Word.spanish == spanish_word).first()
            
            if word:
                word.notes = note_text
                updated_count += 1
                print(f"✅ Updated: {spanish_word}")
            else:
                not_found.append(spanish_word)
        
        db.commit()
        print(f"\n✅ Updated {updated_count} words with notes")
        if not_found:
            print(f"⚠️  Not found in database: {', '.join(not_found)}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    add_notes_to_words()




