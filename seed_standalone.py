#!/usr/bin/env python3
"""
Standalone seed script for Encounter Spanish database
Can be run directly on Railway or locally with DATABASE_URL set
"""
import os
import sys
from sqlalchemy import create_engine, Column, String, Boolean, Integer, Text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("❌ ERROR: DATABASE_URL environment variable not set")
    sys.exit(1)

# Create engine and base
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Define models inline (simplified versions)
class Word(Base):
    __tablename__ = "words"
    id = Column(String, primary_key=True)
    spanish = Column(String, nullable=False)
    english = Column(String, nullable=False)

class Situation(Base):
    __tablename__ = "situations"
    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    order_index = Column(Integer, nullable=False)
    is_free = Column(Boolean, default=False, nullable=False)

class SituationWord(Base):
    __tablename__ = "situation_words"
    situation_id = Column(String, primary_key=True)
    word_id = Column(String, primary_key=True)
    position = Column(Integer, nullable=False)

# Seed data (same as before)
SEED_DATA = [
    ("Checking in at the Airport – 1", ["vuelo", "pasaporte", "maleta"], 1, True),
    ("Talking to the Mechanic – 1", ["coche", "problema", "reparar"], 2, True),
    ("Shopping – 1", ["comprar", "precio", "tienda"], 3, True),
    ("Small Talk – 1", ["hola", "cómo", "bien"], 4, True),
    ("Talking to Home Reno Contractor – 1", ["contratista", "obra", "precio"], 5, True),
    ("Card Not Working at Bank – 1", ["banco", "tarjeta", "problema"], 6, True),
    ("Card Not Working at Bank – 2", ["cuenta", "dinero", "sistema"], 7, True),
    ("ATM Not Dispensing Cash – 1", ["cajero", "efectivo", "número"], 8, True),
    ("Opening an Account – 1", ["contrato", "firma", "documento"], 9, True),
    ("Buying Medicine at Pharmacy – 1", ["farmacia", "medicina", "dolor"], 10, True),
    ("Headache or Fever – 1", ["cabeza", "fiebre", "cuerpo"], 11, True),
    ("Stomach Issue – 1", ["estómago", "agua", "pastilla"], 12, True),
    ("Prescription Pickup – 1", ["receta", "nombre", "seguro"], 13, True),
    ("Apartment Viewing – 1", ["apartamento", "llave", "precio"], 14, True),
    ("Rent and Deposit – 1", ["renta", "depósito", "mes"], 15, True),
    ("Package Delivery – 1", ["paquete", "edificio", "puerta"], 16, False),
    ("Giving Directions – 1", ["izquierda", "derecha", "calle"], 17, False),
    ("Finding an Address – 1", ["dirección", "número", "piso"], 18, False),
    ("Ordering Coffee – 1", ["café", "mesa", "cuenta"], 19, False),
    ("Reading the Menu – 1", ["menú", "comida", "bebida"], 20, False),
    ("Diet Restriction – 1", ["alergia", "carne", "pollo"], 21, False),
    ("Taking a Taxi – 1", ["taxi", "destino", "precio"], 22, False),
    ("Bus Ticket – 1", ["boleto", "estación", "asiento"], 23, False),
    ("Ride App Confusion – 1", ["conductor", "aplicación", "mapa"], 24, False),
    ("Grocery Store – 1", ["supermercado", "bolsa", "caja"], 25, False),
    ("Paying with Cash – 1", ["efectivo", "cambio", "recibo"], 26, False),
    ("Clothing Store – 1", ["talla", "camisa", "pantalón"], 27, False),
    ("WiFi Not Working – 1", ["internet", "conexión", "servicio"], 28, False),
    ("Phone Plan – 1", ["teléfono", "plan", "datos"], 29, False),
    ("Repair Technician Visit – 1", ["técnico", "problema", "sistema"], 30, False),
    ("Meeting a Neighbor – 1", ["vecino", "edificio", "ciudad"], 31, False),
    ("Small Talk at Event – 1", ["trabajo", "país", "tiempo"], 32, False),
    ("Invited to Dinner – 1", ["cena", "casa", "amigo"], 33, False),
    ("Chat with Carlos – 1", ["soy", "me llamo", "vivo"], 34, False),
    ("Chat with Alejandra – 1", ["quiero", "necesito", "busco"], 35, False),
    ("Chat with Diego – 1", ["tengo", "puedo", "hablo"], 36, False),
    ("Chat with Sofia – 1", ["voy", "pago", "traigo"], 37, False),
    ("Chat with Mateo – 1", ["hago", "uso", "trabajo"], 38, False),
    ("Chat with Camila – 1", ["ayer", "hoy", "mañana"], 39, False),
    ("Chat with Andrés – 1", ["aquí", "allí", "cerca"], 40, False),
    ("Chat with Valentina – 1", ["porque", "entonces", "pero"], 41, False),
    ("Chat with Luis – 1", ["primero", "después", "ahora"], 42, False),
    ("Chat with Mariana – 1", ["siempre", "nunca", "a veces"], 43, False),
    ("Chat with Javier – 1", ["más", "menos", "suficiente"], 44, False),
    ("Chat with Isabella – 1", ["conmigo", "contigo", "solo"], 45, False),
    ("Chat with Tomás – 1", ["antes", "tarde", "temprano"], 46, False),
    ("Chat with Daniela – 1", ["también", "todavía", "tampoco"], 47, False),
    ("Chat with Pablo – 1", ["fácil", "difícil", "importante"], 48, False),
    ("Chat with Lucía – 1", ["diferente", "igual", "nuevo"], 49, False),
    ("Chat with Martín – 1", ["mejor", "peor", "listo"], 50, False),
]

WORD_TRANSLATIONS = {
    # New essential words
    "vuelo": "flight", "pasaporte": "passport", "maleta": "suitcase",
    "coche": "car", "reparar": "to repair",
    "comprar": "to buy", "tienda": "store",
    "hola": "hello", "cómo": "how", "bien": "well/good",
    "contratista": "contractor", "obra": "construction/work",
    # Existing words
    "banco": "bank", "tarjeta": "card", "problema": "problem",
    "cuenta": "account", "dinero": "money", "sistema": "system",
    "cajero": "ATM", "efectivo": "cash", "número": "number",
    "contrato": "contract", "firma": "signature", "documento": "document",
    "farmacia": "pharmacy", "medicina": "medicine", "dolor": "pain",
    "cabeza": "head", "fiebre": "fever", "cuerpo": "body",
    "estómago": "stomach", "agua": "water", "pastilla": "pill",
    "receta": "prescription", "nombre": "name", "seguro": "insurance",
    "apartamento": "apartment", "llave": "key", "precio": "price",
    "renta": "rent", "depósito": "deposit", "mes": "month",
    "luz": "light/electricity", "gas": "gas", "cocina": "kitchen",
    "baño": "bathroom", "policía": "police", "licencia": "license",
    "pasaporte": "passport", "dirección": "address", "multa": "fine/ticket",
    "vehículo": "vehicle", "paquete": "package", "edificio": "building",
    "puerta": "door", "izquierda": "left", "derecha": "right",
    "calle": "street", "piso": "floor", "café": "coffee",
    "mesa": "table", "menú": "menu", "comida": "food",
    "bebida": "drink", "alergia": "allergy", "carne": "meat",
    "pollo": "chicken", "taxi": "taxi", "destino": "destination",
    "boleto": "ticket", "estación": "station", "asiento": "seat",
    "conductor": "driver", "aplicación": "app", "mapa": "map",
    "supermercado": "supermarket", "bolsa": "bag", "caja": "checkout/cash register",
    "cambio": "change", "recibo": "receipt", "talla": "size",
    "camisa": "shirt", "pantalón": "pants", "internet": "internet",
    "conexión": "connection", "servicio": "service", "teléfono": "phone",
    "plan": "plan", "datos": "data", "técnico": "technician",
    "vecino": "neighbor", "ciudad": "city", "trabajo": "work",
    "país": "country", "tiempo": "time/weather", "cena": "dinner",
    "casa": "house", "amigo": "friend", "soy": "I am",
    "me llamo": "my name is", "vivo": "I live", "quiero": "I want",
    "necesito": "I need", "busco": "I'm looking for", "tengo": "I have",
    "puedo": "I can", "hablo": "I speak", "voy": "I go",
    "pago": "I pay", "traigo": "I bring", "hago": "I do/make",
    "uso": "I use", "ayer": "yesterday", "hoy": "today",
    "mañana": "tomorrow", "aquí": "here", "allí": "there",
    "cerca": "near", "porque": "because", "entonces": "then",
    "pero": "but", "primero": "first", "después": "after",
    "ahora": "now", "siempre": "always", "nunca": "never",
    "a veces": "sometimes", "más": "more", "menos": "less",
    "suficiente": "enough", "conmigo": "with me", "contigo": "with you",
    "solo": "alone/only", "antes": "before", "tarde": "late",
    "temprano": "early", "también": "also", "todavía": "still",
    "tampoco": "neither", "fácil": "easy", "difícil": "difficult",
    "importante": "important", "diferente": "different", "igual": "same",
    "nuevo": "new", "mejor": "better", "peor": "worse", "listo": "ready",
}

def seed_database():
    db = SessionLocal()
    try:
        print("🌱 Starting database seed...")
        
        # Create words
        print("📝 Creating words...")
        word_map = {}
        for spanish, english in WORD_TRANSLATIONS.items():
            word_id = f"w_{spanish.replace(' ', '_')}"
            existing = db.query(Word).filter(Word.id == word_id).first()
            if existing:
                word_map[spanish] = existing
            else:
                word = Word(id=word_id, spanish=spanish, english=english)
                db.add(word)
                word_map[spanish] = word
        db.commit()
        print(f"✅ Created {len(word_map)} words")
        
        # Create situations
        print("\n📚 Creating situations...")
        situation_map = {}
        for title, word_list, order_index, is_free in SEED_DATA:
            situation_id = str(order_index)  # Use just the number as ID
            existing = db.query(Situation).filter(Situation.id == situation_id).first()
            if existing:
                existing.title = title
                existing.order_index = order_index
                existing.is_free = is_free
                situation_map[order_index] = existing
            else:
                situation = Situation(id=situation_id, title=title, order_index=order_index, is_free=is_free)
                db.add(situation)
                situation_map[order_index] = situation
        db.commit()
        print(f"✅ Created {len(situation_map)} situations")
        
        # Link words to situations
        print("\n🔗 Linking words to situations...")
        total_links = 0
        for title, word_list, order_index, is_free in SEED_DATA:
            situation = situation_map[order_index]
            db.query(SituationWord).filter(SituationWord.situation_id == situation.id).delete()
            for position, spanish_word in enumerate(word_list, start=1):
                word = word_map[spanish_word]
                situation_word = SituationWord(
                    situation_id=situation.id,
                    word_id=word.id,
                    position=position
                )
                db.add(situation_word)
                total_links += 1
        db.commit()
        print(f"✅ Created {total_links} situation-word links")
        
        print("\n🎉 Database seed complete!")
        print(f"   - {len(word_map)} words")
        print(f"   - {len(situation_map)} situations")
        print(f"   - {total_links} situation-word links")
        print(f"   - {sum(1 for _, _, _, is_free in SEED_DATA if is_free)} free situations")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()

