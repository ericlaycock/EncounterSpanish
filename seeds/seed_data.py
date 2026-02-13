"""
Seed data script for Encounter Spanish app.

This script creates:
- 55 situations with categories and series numbers
- Words and situation-word mappings (5 words per situation)

To run: python -m seeds.seed_data
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base, Word, Situation, SituationWord

# Create tables
Base.metadata.create_all(bind=engine)


# All 55 situations with categories and series numbers
SITUATIONS = [
    # ESSENTIAL SURVIVAL (1-5) - FREE
    {"id": "airport_checkin_1", "title": "Checking in at the Airport – 1", "order_index": 1, "is_free": True, "category": "airport", "series_number": 1},
    {"id": "mechanic_talk_1", "title": "Talking to the Mechanic – 1", "order_index": 2, "is_free": True, "category": "mechanic", "series_number": 1},
    {"id": "shopping_1", "title": "Shopping – 1", "order_index": 3, "is_free": True, "category": "shopping", "series_number": 1},
    {"id": "small_talk_1", "title": "Small Talk – 1", "order_index": 4, "is_free": True, "category": "small_talk", "series_number": 1},
    {"id": "contractor_reno_1", "title": "Talking to Home Reno Contractor – 1", "order_index": 5, "is_free": True, "category": "contractor", "series_number": 1},
    
    # BANK (6-9) - FREE
    {"id": "bank_card_1", "title": "Card Not Working at Bank – 1", "order_index": 6, "is_free": True, "category": "banking", "series_number": 1},
    {"id": "bank_card_2", "title": "Card Not Working at Bank – 2", "order_index": 7, "is_free": True, "category": "banking", "series_number": 2},
    {"id": "bank_atm_1", "title": "ATM Not Dispensing Cash – 1", "order_index": 8, "is_free": True, "category": "banking", "series_number": 3},
    {"id": "bank_account_1", "title": "Opening an Account – 1", "order_index": 9, "is_free": True, "category": "banking", "series_number": 4},
    
    # PHARMACY / HEALTH (10-13) - FREE
    {"id": "pharm_medicine_1", "title": "Buying Medicine at Pharmacy – 1", "order_index": 10, "is_free": True, "category": "pharmacy", "series_number": 1},
    {"id": "pharm_headache_1", "title": "Headache or Fever – 1", "order_index": 11, "is_free": True, "category": "pharmacy", "series_number": 2},
    {"id": "pharm_stomach_1", "title": "Stomach Issue – 1", "order_index": 12, "is_free": True, "category": "pharmacy", "series_number": 3},
    {"id": "pharm_prescription_1", "title": "Prescription Pickup – 1", "order_index": 13, "is_free": True, "category": "pharmacy", "series_number": 4},
    
    # APARTMENT / HOUSING (14-15) - FREE
    {"id": "apt_viewing_1", "title": "Apartment Viewing – 1", "order_index": 14, "is_free": True, "category": "apartment", "series_number": 1},
    {"id": "apt_rent_1", "title": "Rent and Deposit – 1", "order_index": 15, "is_free": True, "category": "apartment", "series_number": 2},
    
    # PREMIUM SITUATIONS (16-55)
    # APARTMENT / HOUSING (cont.) (16-17) - PREMIUM
    {"id": "apt_utilities_1", "title": "Utilities Question – 1", "order_index": 16, "is_free": False, "category": "apartment", "series_number": 3},
    {"id": "apt_appliance_1", "title": "Broken Appliance – 1", "order_index": 17, "is_free": False, "category": "apartment", "series_number": 4},
    
    # POLICE / DOCUMENTS (18-20) - PREMIUM
    {"id": "police_traffic_1", "title": "Traffic Stop – 1", "order_index": 18, "is_free": False, "category": "police", "series_number": 1},
    {"id": "police_passport_1", "title": "Passport Check – 1", "order_index": 19, "is_free": False, "category": "police", "series_number": 2},
    {"id": "police_fine_1", "title": "Receiving a Fine – 1", "order_index": 20, "is_free": False, "category": "police", "series_number": 3},
    
    # DELIVERY / DIRECTIONS (21-23) - PREMIUM
    {"id": "delivery_package_1", "title": "Package Delivery – 1", "order_index": 21, "is_free": False, "category": "delivery", "series_number": 1},
    {"id": "delivery_directions_1", "title": "Giving Directions – 1", "order_index": 22, "is_free": False, "category": "delivery", "series_number": 2},
    {"id": "delivery_address_1", "title": "Finding an Address – 1", "order_index": 23, "is_free": False, "category": "delivery", "series_number": 3},
    
    # RESTAURANT / FOOD (24-26) - PREMIUM
    {"id": "rest_coffee_1", "title": "Ordering Coffee – 1", "order_index": 24, "is_free": False, "category": "restaurant", "series_number": 1},
    {"id": "rest_menu_1", "title": "Reading the Menu – 1", "order_index": 25, "is_free": False, "category": "restaurant", "series_number": 2},
    {"id": "rest_diet_1", "title": "Diet Restriction – 1", "order_index": 26, "is_free": False, "category": "restaurant", "series_number": 3},
    
    # TRANSPORT (27-29) - PREMIUM
    {"id": "transport_taxi_1", "title": "Taking a Taxi – 1", "order_index": 27, "is_free": False, "category": "transport", "series_number": 1},
    {"id": "transport_bus_1", "title": "Bus Ticket – 1", "order_index": 28, "is_free": False, "category": "transport", "series_number": 2},
    {"id": "transport_ride_1", "title": "Ride App Confusion – 1", "order_index": 29, "is_free": False, "category": "transport", "series_number": 3},
    
    # SHOPPING (30-32) - PREMIUM
    {"id": "shop_grocery_1", "title": "Grocery Store – 1", "order_index": 30, "is_free": False, "category": "groceries", "series_number": 1},
    {"id": "shop_cash_1", "title": "Paying with Cash – 1", "order_index": 31, "is_free": False, "category": "shopping", "series_number": 2},
    {"id": "shop_clothing_1", "title": "Clothing Store – 1", "order_index": 32, "is_free": False, "category": "clothing", "series_number": 1},
    
    # INTERNET / SERVICES (33-35) - PREMIUM
    {"id": "internet_wifi_1", "title": "WiFi Not Working – 1", "order_index": 33, "is_free": False, "category": "internet", "series_number": 1},
    {"id": "internet_phone_1", "title": "Phone Plan – 1", "order_index": 34, "is_free": False, "category": "internet", "series_number": 2},
    {"id": "internet_repair_1", "title": "Repair Technician Visit – 1", "order_index": 35, "is_free": False, "category": "internet", "series_number": 3},
    
    # SOCIAL BASICS (36-38) - PREMIUM
    {"id": "social_neighbor_1", "title": "Meeting a Neighbor – 1", "order_index": 36, "is_free": False, "category": "social", "series_number": 1},
    {"id": "social_event_1", "title": "Small Talk at Event – 1", "order_index": 37, "is_free": False, "category": "social", "series_number": 2},
    {"id": "social_dinner_1", "title": "Invited to Dinner – 1", "order_index": 38, "is_free": False, "category": "social", "series_number": 3},
    
    # CHAT MODULES - VERBS (39-43) - PREMIUM
    {"id": "chat_carlos_1", "title": "Chat with Carlos – 1", "order_index": 39, "is_free": False, "category": "chat", "series_number": 1},
    {"id": "chat_alejandra_1", "title": "Chat with Alejandra – 1", "order_index": 40, "is_free": False, "category": "chat", "series_number": 2},
    {"id": "chat_diego_1", "title": "Chat with Diego – 1", "order_index": 41, "is_free": False, "category": "chat", "series_number": 3},
    {"id": "chat_sofia_1", "title": "Chat with Sofia – 1", "order_index": 42, "is_free": False, "category": "chat", "series_number": 4},
    {"id": "chat_mateo_1", "title": "Chat with Mateo – 1", "order_index": 43, "is_free": False, "category": "chat", "series_number": 5},
    
    # CHAT MODULES - TIME (44-46) - PREMIUM
    {"id": "chat_camila_1", "title": "Chat with Camila – 1", "order_index": 44, "is_free": False, "category": "chat", "series_number": 6},
    {"id": "chat_andres_1", "title": "Chat with Andrés – 1", "order_index": 45, "is_free": False, "category": "chat", "series_number": 7},
    {"id": "chat_valentina_1", "title": "Chat with Valentina – 1", "order_index": 46, "is_free": False, "category": "chat", "series_number": 8},
    
    # CHAT MODULES - CONNECTORS (47-49) - PREMIUM
    {"id": "chat_luis_1", "title": "Chat with Luis – 1", "order_index": 47, "is_free": False, "category": "chat", "series_number": 9},
    {"id": "chat_mariana_1", "title": "Chat with Mariana – 1", "order_index": 48, "is_free": False, "category": "chat", "series_number": 10},
    {"id": "chat_javier_1", "title": "Chat with Javier – 1", "order_index": 49, "is_free": False, "category": "chat", "series_number": 11},
    
    # CHAT MODULES - PRONOUNS/ADVERBS (50-52) - PREMIUM
    {"id": "chat_isabella_1", "title": "Chat with Isabella – 1", "order_index": 50, "is_free": False, "category": "chat", "series_number": 12},
    {"id": "chat_tomas_1", "title": "Chat with Tomás – 1", "order_index": 51, "is_free": False, "category": "chat", "series_number": 13},
    {"id": "chat_daniela_1", "title": "Chat with Daniela – 1", "order_index": 52, "is_free": False, "category": "chat", "series_number": 14},
    
    # CHAT MODULES - ADJECTIVES (53-55) - PREMIUM
    {"id": "chat_pablo_1", "title": "Chat with Pablo – 1", "order_index": 53, "is_free": False, "category": "chat", "series_number": 15},
    {"id": "chat_lucia_1", "title": "Chat with Lucía – 1", "order_index": 54, "is_free": False, "category": "chat", "series_number": 16},
    {"id": "chat_martin_1", "title": "Chat with Martín – 1", "order_index": 55, "is_free": False, "category": "chat", "series_number": 17},
]

# All words with their Spanish and English
WORDS = [
    # AIRPORT
    {"id": "w_vuelo", "spanish": "vuelo", "english": "flight"},
    {"id": "w_pasaporte", "spanish": "pasaporte", "english": "passport"},
    {"id": "w_maleta", "spanish": "maleta", "english": "suitcase"},
    {"id": "w_equipaje", "spanish": "equipaje", "english": "luggage"},
    {"id": "w_asiento_avion", "spanish": "asiento", "english": "seat"},
    {"id": "w_salida", "spanish": "salida", "english": "departure/gate"},
    
    # MECHANIC
    {"id": "w_coche", "spanish": "coche", "english": "car"},
    {"id": "w_reparar", "spanish": "reparar", "english": "to repair"},
    {"id": "w_taller", "spanish": "taller", "english": "workshop/garage"},
    {"id": "w_motor", "spanish": "motor", "english": "engine"},
    {"id": "w_ruido", "spanish": "ruido", "english": "noise"},
    {"id": "w_freno", "spanish": "freno", "english": "brake"},
    
    # SHOPPING (basic)
    {"id": "w_comprar", "spanish": "comprar", "english": "to buy"},
    {"id": "w_tienda", "spanish": "tienda", "english": "store"},
    {"id": "w_tarjeta_credito", "spanish": "tarjeta de crédito", "english": "credit card"},
    {"id": "w_precio", "spanish": "precio", "english": "price"},
    {"id": "w_cuenta", "spanish": "cuenta", "english": "account/bill"},
    
    # SMALL TALK
    {"id": "w_hola", "spanish": "hola", "english": "hello"},
    {"id": "w_como", "spanish": "cómo", "english": "how"},
    {"id": "w_bien", "spanish": "bien", "english": "well/good"},
    {"id": "w_gracias", "spanish": "gracias", "english": "thank you"},
    {"id": "w_por_favor", "spanish": "por favor", "english": "please"},
    {"id": "w_perdon", "spanish": "perdón", "english": "sorry"},
    
    # CONTRACTOR / HOME RENO
    {"id": "w_contratista", "spanish": "contratista", "english": "contractor"},
    {"id": "w_obra", "spanish": "obra", "english": "construction/work"},
    {"id": "w_material", "spanish": "material", "english": "material"},
    {"id": "w_fecha", "spanish": "fecha", "english": "date"},
    {"id": "w_presupuesto", "spanish": "presupuesto", "english": "budget/quote"},
    {"id": "w_terminar", "spanish": "terminar", "english": "to finish"},
    
    # BANK
    {"id": "w_banco", "spanish": "banco", "english": "bank"},
    {"id": "w_tarjeta", "spanish": "tarjeta", "english": "card"},
    {"id": "w_problema", "spanish": "problema", "english": "problem"},
    {"id": "w_dinero", "spanish": "dinero", "english": "money"},
    {"id": "w_sistema", "spanish": "sistema", "english": "system"},
    {"id": "w_cajero", "spanish": "cajero", "english": "ATM"},
    {"id": "w_efectivo", "spanish": "efectivo", "english": "cash"},
    {"id": "w_numero", "spanish": "número", "english": "number"},
    {"id": "w_contrato", "spanish": "contrato", "english": "contract"},
    {"id": "w_firma", "spanish": "firma", "english": "signature"},
    {"id": "w_documento", "spanish": "documento", "english": "document"},
    
    # PHARMACY / HEALTH
    {"id": "w_farmacia", "spanish": "farmacia", "english": "pharmacy"},
    {"id": "w_medicina", "spanish": "medicina", "english": "medicine"},
    {"id": "w_dolor", "spanish": "dolor", "english": "pain"},
    {"id": "w_cabeza", "spanish": "cabeza", "english": "head"},
    {"id": "w_fiebre", "spanish": "fiebre", "english": "fever"},
    {"id": "w_cuerpo", "spanish": "cuerpo", "english": "body"},
    {"id": "w_estomago", "spanish": "estómago", "english": "stomach"},
    {"id": "w_agua", "spanish": "agua", "english": "water"},
    {"id": "w_pastilla", "spanish": "pastilla", "english": "pill"},
    {"id": "w_receta", "spanish": "receta", "english": "prescription"},
    {"id": "w_nombre", "spanish": "nombre", "english": "name"},
    {"id": "w_seguro", "spanish": "seguro", "english": "insurance"},
    
    # APARTMENT / HOUSING
    {"id": "w_apartamento", "spanish": "apartamento", "english": "apartment"},
    {"id": "w_llave", "spanish": "llave", "english": "key"},
    {"id": "w_renta", "spanish": "renta", "english": "rent"},
    {"id": "w_deposito", "spanish": "depósito", "english": "deposit"},
    {"id": "w_mes", "spanish": "mes", "english": "month"},
    {"id": "w_luz", "spanish": "luz", "english": "light/electricity"},
    {"id": "w_gas", "spanish": "gas", "english": "gas"},
    {"id": "w_cocina", "spanish": "cocina", "english": "kitchen"},
    {"id": "w_bano", "spanish": "baño", "english": "bathroom"},
    
    # POLICE / DOCUMENTS
    {"id": "w_policia", "spanish": "policía", "english": "police"},
    {"id": "w_licencia", "spanish": "licencia", "english": "license"},
    {"id": "w_direccion", "spanish": "dirección", "english": "address"},
    {"id": "w_multa", "spanish": "multa", "english": "fine"},
    {"id": "w_vehiculo", "spanish": "vehículo", "english": "vehicle"},
    
    # DELIVERY / DIRECTIONS
    {"id": "w_paquete", "spanish": "paquete", "english": "package"},
    {"id": "w_edificio", "spanish": "edificio", "english": "building"},
    {"id": "w_puerta", "spanish": "puerta", "english": "door"},
    {"id": "w_izquierda", "spanish": "izquierda", "english": "left"},
    {"id": "w_derecha", "spanish": "derecha", "english": "right"},
    {"id": "w_calle", "spanish": "calle", "english": "street"},
    {"id": "w_piso", "spanish": "piso", "english": "floor"},
    
    # RESTAURANT / FOOD
    {"id": "w_cafe", "spanish": "café", "english": "coffee"},
    {"id": "w_mesa", "spanish": "mesa", "english": "table"},
    {"id": "w_menu", "spanish": "menú", "english": "menu"},
    {"id": "w_comida", "spanish": "comida", "english": "food"},
    {"id": "w_bebida", "spanish": "bebida", "english": "drink"},
    {"id": "w_alergia", "spanish": "alergia", "english": "allergy"},
    {"id": "w_carne", "spanish": "carne", "english": "meat"},
    {"id": "w_pollo", "spanish": "pollo", "english": "chicken"},
    
    # TRANSPORT
    {"id": "w_taxi", "spanish": "taxi", "english": "taxi"},
    {"id": "w_destino", "spanish": "destino", "english": "destination"},
    {"id": "w_boleto", "spanish": "boleto", "english": "ticket"},
    {"id": "w_estacion", "spanish": "estación", "english": "station"},
    {"id": "w_asiento", "spanish": "asiento", "english": "seat"},
    {"id": "w_conductor", "spanish": "conductor", "english": "driver"},
    {"id": "w_aplicacion", "spanish": "aplicación", "english": "app"},
    {"id": "w_mapa", "spanish": "mapa", "english": "map"},
    
    # SHOPPING
    {"id": "w_supermercado", "spanish": "supermercado", "english": "supermarket"},
    {"id": "w_bolsa", "spanish": "bolsa", "english": "bag"},
    {"id": "w_caja", "spanish": "caja", "english": "checkout/cash register"},
    {"id": "w_cambio", "spanish": "cambio", "english": "change"},
    {"id": "w_recibo", "spanish": "recibo", "english": "receipt"},
    {"id": "w_talla", "spanish": "talla", "english": "size"},
    {"id": "w_camisa", "spanish": "camisa", "english": "shirt"},
    {"id": "w_pantalon", "spanish": "pantalón", "english": "pants"},
    
    # INTERNET / SERVICES
    {"id": "w_internet", "spanish": "internet", "english": "internet"},
    {"id": "w_conexion", "spanish": "conexión", "english": "connection"},
    {"id": "w_servicio", "spanish": "servicio", "english": "service"},
    {"id": "w_telefono", "spanish": "teléfono", "english": "phone"},
    {"id": "w_plan", "spanish": "plan", "english": "plan"},
    {"id": "w_datos", "spanish": "datos", "english": "data"},
    {"id": "w_tecnico", "spanish": "técnico", "english": "technician"},
    
    # SOCIAL BASICS
    {"id": "w_vecino", "spanish": "vecino", "english": "neighbor"},
    {"id": "w_ciudad", "spanish": "ciudad", "english": "city"},
    {"id": "w_trabajo", "spanish": "trabajo", "english": "work"},
    {"id": "w_pais", "spanish": "país", "english": "country"},
    {"id": "w_tiempo", "spanish": "tiempo", "english": "time/weather"},
    {"id": "w_cena", "spanish": "cena", "english": "dinner"},
    {"id": "w_casa", "spanish": "casa", "english": "house"},
    {"id": "w_amigo", "spanish": "amigo", "english": "friend"},
    
    # CHAT MODULES - VERBS
    {"id": "w_soy", "spanish": "soy", "english": "I am"},
    {"id": "w_me_llamo", "spanish": "me llamo", "english": "my name is"},
    {"id": "w_vivo", "spanish": "vivo", "english": "I live"},
    {"id": "w_quiero", "spanish": "quiero", "english": "I want"},
    {"id": "w_necesito", "spanish": "necesito", "english": "I need"},
    {"id": "w_busco", "spanish": "busco", "english": "I'm looking for"},
    {"id": "w_tengo", "spanish": "tengo", "english": "I have"},
    {"id": "w_puedo", "spanish": "puedo", "english": "I can"},
    {"id": "w_hablo", "spanish": "hablo", "english": "I speak"},
    {"id": "w_voy", "spanish": "voy", "english": "I go"},
    {"id": "w_pago", "spanish": "pago", "english": "I pay"},
    {"id": "w_traigo", "spanish": "traigo", "english": "I bring"},
    {"id": "w_hago", "spanish": "hago", "english": "I do/make"},
    {"id": "w_uso", "spanish": "uso", "english": "I use"},
    
    # CHAT MODULES - TIME
    {"id": "w_ayer", "spanish": "ayer", "english": "yesterday"},
    {"id": "w_hoy", "spanish": "hoy", "english": "today"},
    {"id": "w_manana", "spanish": "mañana", "english": "tomorrow"},
    {"id": "w_aqui", "spanish": "aquí", "english": "here"},
    {"id": "w_alli", "spanish": "allí", "english": "there"},
    {"id": "w_cerca", "spanish": "cerca", "english": "near"},
    
    # CHAT MODULES - CONNECTORS
    {"id": "w_porque", "spanish": "porque", "english": "because"},
    {"id": "w_entonces", "spanish": "entonces", "english": "then"},
    {"id": "w_pero", "spanish": "pero", "english": "but"},
    {"id": "w_primero", "spanish": "primero", "english": "first"},
    {"id": "w_despues", "spanish": "después", "english": "after"},
    {"id": "w_ahora", "spanish": "ahora", "english": "now"},
    {"id": "w_siempre", "spanish": "siempre", "english": "always"},
    {"id": "w_nunca", "spanish": "nunca", "english": "never"},
    {"id": "w_veces", "spanish": "a veces", "english": "sometimes"},
    {"id": "w_mas", "spanish": "más", "english": "more"},
    {"id": "w_menos", "spanish": "menos", "english": "less"},
    {"id": "w_suficiente", "spanish": "suficiente", "english": "enough"},
    
    # CHAT MODULES - PRONOUNS/ADVERBS
    {"id": "w_conmigo", "spanish": "conmigo", "english": "with me"},
    {"id": "w_contigo", "spanish": "contigo", "english": "with you"},
    {"id": "w_solo", "spanish": "solo", "english": "alone/only"},
    {"id": "w_antes", "spanish": "antes", "english": "before"},
    {"id": "w_tarde", "spanish": "tarde", "english": "late"},
    {"id": "w_temprano", "spanish": "temprano", "english": "early"},
    {"id": "w_tambien", "spanish": "también", "english": "also"},
    {"id": "w_todavia", "spanish": "todavía", "english": "still"},
    {"id": "w_tampoco", "spanish": "tampoco", "english": "neither"},
    
    # CHAT MODULES - ADJECTIVES
    {"id": "w_facil", "spanish": "fácil", "english": "easy"},
    {"id": "w_dificil", "spanish": "difícil", "english": "difficult"},
    {"id": "w_importante", "spanish": "importante", "english": "important"},
    {"id": "w_diferente", "spanish": "diferente", "english": "different"},
    {"id": "w_igual", "spanish": "igual", "english": "same"},
    {"id": "w_nuevo", "spanish": "nuevo", "english": "new"},
    {"id": "w_mejor", "spanish": "mejor", "english": "better"},
    {"id": "w_peor", "spanish": "peor", "english": "worse"},
    {"id": "w_listo", "spanish": "listo", "english": "ready"},
]

# Situation-word mappings - NOW 5 WORDS PER SITUATION
SITUATION_WORDS = {
    # ESSENTIAL SURVIVAL (1-5)
    "airport_checkin_1": ["w_vuelo", "w_pasaporte", "w_maleta", "w_equipaje", "w_salida"],
    "mechanic_talk_1": ["w_coche", "w_problema", "w_reparar", "w_taller", "w_motor"],
    "shopping_1": ["w_comprar", "w_precio", "w_tienda", "w_tarjeta_credito", "w_cuenta"],
    "small_talk_1": ["w_hola", "w_como", "w_bien", "w_gracias", "w_por_favor"],
    "contractor_reno_1": ["w_contratista", "w_obra", "w_precio", "w_material", "w_fecha"],
    
    # BANK
    "bank_card_1": ["w_banco", "w_tarjeta", "w_problema", "w_cuenta", "w_dinero"],
    "bank_card_2": ["w_cuenta", "w_dinero", "w_sistema", "w_tarjeta", "w_banco"],
    "bank_atm_1": ["w_cajero", "w_efectivo", "w_numero", "w_tarjeta", "w_problema"],
    "bank_account_1": ["w_contrato", "w_firma", "w_documento", "w_banco", "w_cuenta"],
    
    # PHARMACY / HEALTH
    "pharm_medicine_1": ["w_farmacia", "w_medicina", "w_dolor", "w_pastilla", "w_nombre"],
    "pharm_headache_1": ["w_cabeza", "w_fiebre", "w_cuerpo", "w_dolor", "w_medicina"],
    "pharm_stomach_1": ["w_estomago", "w_agua", "w_pastilla", "w_dolor", "w_medicina"],
    "pharm_prescription_1": ["w_receta", "w_nombre", "w_seguro", "w_farmacia", "w_medicina"],
    
    # APARTMENT / HOUSING
    "apt_viewing_1": ["w_apartamento", "w_llave", "w_precio", "w_deposito", "w_mes"],
    "apt_rent_1": ["w_renta", "w_deposito", "w_mes", "w_contrato", "w_apartamento"],
    "apt_utilities_1": ["w_agua", "w_luz", "w_gas", "w_apartamento", "w_cuenta"],
    "apt_appliance_1": ["w_problema", "w_cocina", "w_bano", "w_apartamento", "w_reparar"],
    
    # POLICE / DOCUMENTS
    "police_traffic_1": ["w_policia", "w_licencia", "w_documento", "w_vehiculo", "w_problema"],
    "police_passport_1": ["w_pasaporte", "w_direccion", "w_numero", "w_documento", "w_nombre"],
    "police_fine_1": ["w_multa", "w_vehiculo", "w_problema", "w_policia", "w_documento"],
    
    # DELIVERY / DIRECTIONS
    "delivery_package_1": ["w_paquete", "w_edificio", "w_puerta", "w_direccion", "w_numero"],
    "delivery_directions_1": ["w_izquierda", "w_derecha", "w_calle", "w_edificio", "w_direccion"],
    "delivery_address_1": ["w_direccion", "w_numero", "w_piso", "w_edificio", "w_calle"],
    
    # RESTAURANT / FOOD
    "rest_coffee_1": ["w_cafe", "w_mesa", "w_cuenta", "w_precio", "w_por_favor"],
    "rest_menu_1": ["w_menu", "w_comida", "w_bebida", "w_precio", "w_cuenta"],
    "rest_diet_1": ["w_alergia", "w_carne", "w_pollo", "w_comida", "w_menu"],
    
    # TRANSPORT
    "transport_taxi_1": ["w_taxi", "w_destino", "w_precio", "w_direccion", "w_conductor"],
    "transport_bus_1": ["w_boleto", "w_estacion", "w_asiento", "w_destino", "w_precio"],
    "transport_ride_1": ["w_conductor", "w_aplicacion", "w_mapa", "w_destino", "w_direccion"],
    
    # SHOPPING
    "shop_grocery_1": ["w_supermercado", "w_bolsa", "w_caja", "w_precio", "w_recibo"],
    "shop_cash_1": ["w_efectivo", "w_cambio", "w_recibo", "w_precio", "w_caja"],
    "shop_clothing_1": ["w_talla", "w_camisa", "w_pantalon", "w_precio", "w_tienda"],
    
    # INTERNET / SERVICES
    "internet_wifi_1": ["w_internet", "w_conexion", "w_servicio", "w_problema", "w_tecnico"],
    "internet_phone_1": ["w_telefono", "w_plan", "w_datos", "w_servicio", "w_precio"],
    "internet_repair_1": ["w_tecnico", "w_problema", "w_sistema", "w_servicio", "w_fecha"],
    
    # SOCIAL BASICS
    "social_neighbor_1": ["w_vecino", "w_edificio", "w_ciudad", "w_hola", "w_nombre"],
    "social_event_1": ["w_trabajo", "w_pais", "w_tiempo", "w_hola", "w_como"],
    "social_dinner_1": ["w_cena", "w_casa", "w_amigo", "w_gracias", "w_comida"],
    
    # CHAT MODULES - VERBS
    "chat_carlos_1": ["w_soy", "w_me_llamo", "w_vivo", "w_hola", "w_como"],
    "chat_alejandra_1": ["w_quiero", "w_necesito", "w_busco", "w_por_favor", "w_gracias"],
    "chat_diego_1": ["w_tengo", "w_puedo", "w_hablo", "w_como", "w_bien"],
    "chat_sofia_1": ["w_voy", "w_pago", "w_traigo", "w_precio", "w_dinero"],
    "chat_mateo_1": ["w_hago", "w_uso", "w_trabajo", "w_como", "w_bien"],
    
    # CHAT MODULES - TIME
    "chat_camila_1": ["w_ayer", "w_hoy", "w_manana", "w_tiempo", "w_fecha"],
    "chat_andres_1": ["w_aqui", "w_alli", "w_cerca", "w_direccion", "w_lugar"],
    "chat_valentina_1": ["w_porque", "w_entonces", "w_pero", "w_como", "w_bien"],
    
    # CHAT MODULES - CONNECTORS
    "chat_luis_1": ["w_primero", "w_despues", "w_ahora", "w_tiempo", "w_fecha"],
    "chat_mariana_1": ["w_siempre", "w_nunca", "w_veces", "w_tiempo", "w_como"],
    "chat_javier_1": ["w_mas", "w_menos", "w_suficiente", "w_precio", "w_dinero"],
    
    # CHAT MODULES - PRONOUNS/ADVERBS
    "chat_isabella_1": ["w_conmigo", "w_contigo", "w_solo", "w_como", "w_bien"],
    "chat_tomas_1": ["w_antes", "w_tarde", "w_temprano", "w_tiempo", "w_fecha"],
    "chat_daniela_1": ["w_tambien", "w_todavia", "w_tampoco", "w_como", "w_bien"],
    
    # CHAT MODULES - ADJECTIVES
    "chat_pablo_1": ["w_facil", "w_dificil", "w_importante", "w_como", "w_bien"],
    "chat_lucia_1": ["w_diferente", "w_igual", "w_nuevo", "w_como", "w_bien"],
    "chat_martin_1": ["w_mejor", "w_peor", "w_listo", "w_como", "w_bien"],
}

# Add missing words for chat modules
WORDS.extend([
    {"id": "w_lugar", "spanish": "lugar", "english": "place"},
])


def seed_database():
    """Seed the database with situations and words"""
    db: Session = SessionLocal()
    
    try:
        # Delete in reverse order of foreign key dependencies
        print("🗑️ Clearing existing data...")
        from app.models import Conversation, UserSituation, UserWord
        db.query(SituationWord).delete()
        db.query(Conversation).delete()
        db.query(UserSituation).delete()
        db.query(UserWord).delete()
        db.query(Situation).delete()
        db.query(Word).delete()
        db.query(Subscription).delete()
        db.query(User).delete()
        db.commit()
        print("✅ Existing data cleared")
        
        # Upsert words (update if exists, insert if not)
        print("\n📝 Inserting/updating words...")
        words_created = 0
        words_updated = 0
        for word_data in WORDS:
            existing = db.query(Word).filter(Word.id == word_data['id']).first()
            if existing:
                existing.spanish = word_data['spanish']
                existing.english = word_data['english']
                words_updated += 1
            else:
                word = Word(**word_data)
                db.add(word)
                words_created += 1
            db.flush()
        db.commit()
        print(f"✅ Created {words_created} words, updated {words_updated} words")
        
        # Upsert situations
        print("\n📚 Inserting/updating situations...")
        situations_created = 0
        situations_updated = 0
        for situation_data in SITUATIONS:
            existing = db.query(Situation).filter(Situation.id == situation_data['id']).first()
            if existing:
                existing.title = situation_data['title']
                existing.order_index = situation_data['order_index']
                existing.is_free = situation_data['is_free']
                existing.category = situation_data['category']
                existing.series_number = situation_data['series_number']
                situations_updated += 1
            else:
                situation = Situation(**situation_data)
                db.add(situation)
                situations_created += 1
            db.flush()
        db.commit()
        print(f"✅ Created {situations_created} situations, updated {situations_updated} situations")
        
        # Link words to situations
        print("\n🔗 Linking words to situations...")
        total_links = 0
        for situation_id, word_list in SITUATION_WORDS.items():
            # Clear existing links for this situation before re-inserting
            db.query(SituationWord).filter(SituationWord.situation_id == situation_id).delete()
            db.flush()
            
            for position, word_id in enumerate(word_list, start=1):
                situation_word = SituationWord(
                    situation_id=situation_id,
                    word_id=word_id,
                    position=position
                )
                db.add(situation_word)
                total_links += 1
        db.commit()
        print(f"✅ Created {total_links} situation-word links")
        
        print("\n🎉 Database seed complete!")
        print(f"   - {len(WORDS)} words")
        print(f"   - {len(SITUATIONS)} situations")
        print(f"   - {total_links} situation-word links")
        print(f"   - {sum(1 for s in SITUATIONS if s['is_free'])} free situations")
        print(f"   - Average {total_links // len(SITUATIONS)} words per situation")
        
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
