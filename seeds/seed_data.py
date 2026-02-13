"""
Seed data script for Encounter Spanish app.

This script creates:
- 50 situations (first 15 are free, rest are premium)
- Words and situation-word mappings

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


# All 50 situations - first 15 are free, rest are premium
SITUATIONS = [
    # ESSENTIAL SURVIVAL (1-5) - FREE
    {"id": "airport_checkin_1", "title": "Checking in at the Airport – 1", "order_index": 1, "is_free": True},
    {"id": "mechanic_talk_1", "title": "Talking to the Mechanic – 1", "order_index": 2, "is_free": True},
    {"id": "shopping_1", "title": "Shopping – 1", "order_index": 3, "is_free": True},
    {"id": "small_talk_1", "title": "Small Talk – 1", "order_index": 4, "is_free": True},
    {"id": "contractor_reno_1", "title": "Talking to Home Reno Contractor – 1", "order_index": 5, "is_free": True},
    
    # BANK (6-9) - FREE
    {"id": "bank_card_1", "title": "Card Not Working at Bank – 1", "order_index": 6, "is_free": True},
    {"id": "bank_card_2", "title": "Card Not Working at Bank – 2", "order_index": 7, "is_free": True},
    {"id": "bank_atm_1", "title": "ATM Not Dispensing Cash – 1", "order_index": 8, "is_free": True},
    {"id": "bank_account_1", "title": "Opening an Account – 1", "order_index": 9, "is_free": True},
    
    # PHARMACY / HEALTH (10-13) - FREE
    {"id": "pharm_medicine_1", "title": "Buying Medicine at Pharmacy – 1", "order_index": 10, "is_free": True},
    {"id": "pharm_headache_1", "title": "Headache or Fever – 1", "order_index": 11, "is_free": True},
    {"id": "pharm_stomach_1", "title": "Stomach Issue – 1", "order_index": 12, "is_free": True},
    {"id": "pharm_prescription_1", "title": "Prescription Pickup – 1", "order_index": 13, "is_free": True},
    
    # APARTMENT / HOUSING (14-15) - FREE
    {"id": "apt_viewing_1", "title": "Apartment Viewing – 1", "order_index": 14, "is_free": True},
    {"id": "apt_rent_1", "title": "Rent and Deposit – 1", "order_index": 15, "is_free": True},
    
    # DELIVERY / DIRECTIONS (16-18) - PREMIUM
    {"id": "delivery_package_1", "title": "Package Delivery – 1", "order_index": 16, "is_free": False},
    {"id": "delivery_directions_1", "title": "Giving Directions – 1", "order_index": 17, "is_free": False},
    {"id": "delivery_address_1", "title": "Finding an Address – 1", "order_index": 18, "is_free": False},
    
    # RESTAURANT / FOOD (19-21) - PREMIUM
    {"id": "rest_coffee_1", "title": "Ordering Coffee – 1", "order_index": 19, "is_free": False},
    {"id": "rest_menu_1", "title": "Reading the Menu – 1", "order_index": 20, "is_free": False},
    {"id": "rest_diet_1", "title": "Diet Restriction – 1", "order_index": 21, "is_free": False},
    
    # TRANSPORT (22-24) - PREMIUM
    {"id": "transport_taxi_1", "title": "Taking a Taxi – 1", "order_index": 22, "is_free": False},
    {"id": "transport_bus_1", "title": "Bus Ticket – 1", "order_index": 23, "is_free": False},
    {"id": "transport_ride_1", "title": "Ride App Confusion – 1", "order_index": 24, "is_free": False},
    
    # SHOPPING (25-27) - PREMIUM
    {"id": "shop_grocery_1", "title": "Grocery Store – 1", "order_index": 25, "is_free": False},
    {"id": "shop_cash_1", "title": "Paying with Cash – 1", "order_index": 26, "is_free": False},
    {"id": "shop_clothing_1", "title": "Clothing Store – 1", "order_index": 27, "is_free": False},
    
    # INTERNET / SERVICES (28-30) - PREMIUM
    {"id": "internet_wifi_1", "title": "WiFi Not Working – 1", "order_index": 28, "is_free": False},
    {"id": "internet_phone_1", "title": "Phone Plan – 1", "order_index": 29, "is_free": False},
    {"id": "internet_repair_1", "title": "Repair Technician Visit – 1", "order_index": 30, "is_free": False},
    
    # SOCIAL BASICS (31-33) - PREMIUM
    {"id": "social_neighbor_1", "title": "Meeting a Neighbor – 1", "order_index": 31, "is_free": False},
    {"id": "social_event_1", "title": "Small Talk at Event – 1", "order_index": 32, "is_free": False},
    {"id": "social_dinner_1", "title": "Invited to Dinner – 1", "order_index": 33, "is_free": False},
    
    # CHAT MODULES - VERBS (34-38) - PREMIUM
    {"id": "chat_carlos_1", "title": "Chat with Carlos – 1", "order_index": 34, "is_free": False},
    {"id": "chat_alejandra_1", "title": "Chat with Alejandra – 1", "order_index": 35, "is_free": False},
    {"id": "chat_diego_1", "title": "Chat with Diego – 1", "order_index": 36, "is_free": False},
    {"id": "chat_sofia_1", "title": "Chat with Sofia – 1", "order_index": 37, "is_free": False},
    {"id": "chat_mateo_1", "title": "Chat with Mateo – 1", "order_index": 38, "is_free": False},
    
    # CHAT MODULES - TIME (39-41) - PREMIUM
    {"id": "chat_camila_1", "title": "Chat with Camila – 1", "order_index": 39, "is_free": False},
    {"id": "chat_andres_1", "title": "Chat with Andrés – 1", "order_index": 40, "is_free": False},
    {"id": "chat_valentina_1", "title": "Chat with Valentina – 1", "order_index": 41, "is_free": False},
    
    # CHAT MODULES - CONNECTORS (42-44) - PREMIUM
    {"id": "chat_luis_1", "title": "Chat with Luis – 1", "order_index": 42, "is_free": False},
    {"id": "chat_mariana_1", "title": "Chat with Mariana – 1", "order_index": 43, "is_free": False},
    {"id": "chat_javier_1", "title": "Chat with Javier – 1", "order_index": 44, "is_free": False},
    
    # CHAT MODULES - PRONOUNS/ADVERBS (45-47) - PREMIUM
    {"id": "chat_isabella_1", "title": "Chat with Isabella – 1", "order_index": 45, "is_free": False},
    {"id": "chat_tomas_1", "title": "Chat with Tomás – 1", "order_index": 46, "is_free": False},
    {"id": "chat_daniela_1", "title": "Chat with Daniela – 1", "order_index": 47, "is_free": False},
    
    # CHAT MODULES - ADJECTIVES (48-50) - PREMIUM
    {"id": "chat_pablo_1", "title": "Chat with Pablo – 1", "order_index": 48, "is_free": False},
    {"id": "chat_lucia_1", "title": "Chat with Lucía – 1", "order_index": 49, "is_free": False},
    {"id": "chat_martin_1", "title": "Chat with Martín – 1", "order_index": 50, "is_free": False},
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
    {"id": "w_cuenta", "spanish": "cuenta", "english": "account"},
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
    {"id": "w_precio", "spanish": "precio", "english": "price"},
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
    {"id": "w_pasaporte", "spanish": "pasaporte", "english": "passport"},
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

# Situation-word mappings
SITUATION_WORDS = {
    # ESSENTIAL SURVIVAL (1-5)
    "airport_checkin_1": ["w_vuelo", "w_pasaporte", "w_maleta"],
    "mechanic_talk_1": ["w_coche", "w_problema", "w_reparar"],
    "shopping_1": ["w_comprar", "w_precio", "w_tienda"],
    "small_talk_1": ["w_hola", "w_como", "w_bien"],
    "contractor_reno_1": ["w_contratista", "w_obra", "w_precio"],
    
    # BANK
    "bank_card_1": ["w_banco", "w_tarjeta", "w_problema"],
    "bank_card_2": ["w_cuenta", "w_dinero", "w_sistema"],
    "bank_atm_1": ["w_cajero", "w_efectivo", "w_numero"],
    "bank_account_1": ["w_contrato", "w_firma", "w_documento"],
    
    # PHARMACY / HEALTH
    "pharm_medicine_1": ["w_farmacia", "w_medicina", "w_dolor"],
    "pharm_headache_1": ["w_cabeza", "w_fiebre", "w_cuerpo"],
    "pharm_stomach_1": ["w_estomago", "w_agua", "w_pastilla"],
    "pharm_prescription_1": ["w_receta", "w_nombre", "w_seguro"],
    
    # APARTMENT / HOUSING
    "apt_viewing_1": ["w_apartamento", "w_llave", "w_precio"],
    "apt_rent_1": ["w_renta", "w_deposito", "w_mes"],
    "apt_utilities_1": ["w_agua", "w_luz", "w_gas"],
    "apt_appliance_1": ["w_problema", "w_cocina", "w_bano"],
    
    # POLICE / DOCUMENTS
    "police_traffic_1": ["w_policia", "w_licencia", "w_documento"],
    "police_passport_1": ["w_pasaporte", "w_direccion", "w_numero"],
    "police_fine_1": ["w_multa", "w_vehiculo", "w_problema"],
    
    # DELIVERY / DIRECTIONS
    "delivery_package_1": ["w_paquete", "w_edificio", "w_puerta"],
    "delivery_directions_1": ["w_izquierda", "w_derecha", "w_calle"],
    "delivery_address_1": ["w_direccion", "w_numero", "w_piso"],
    
    # RESTAURANT / FOOD
    "rest_coffee_1": ["w_cafe", "w_mesa", "w_cuenta"],
    "rest_menu_1": ["w_menu", "w_comida", "w_bebida"],
    "rest_diet_1": ["w_alergia", "w_carne", "w_pollo"],
    
    # TRANSPORT
    "transport_taxi_1": ["w_taxi", "w_destino", "w_precio"],
    "transport_bus_1": ["w_boleto", "w_estacion", "w_asiento"],
    "transport_ride_1": ["w_conductor", "w_aplicacion", "w_mapa"],
    
    # SHOPPING
    "shop_grocery_1": ["w_supermercado", "w_bolsa", "w_caja"],
    "shop_cash_1": ["w_efectivo", "w_cambio", "w_recibo"],
    "shop_clothing_1": ["w_talla", "w_camisa", "w_pantalon"],
    
    # INTERNET / SERVICES
    "internet_wifi_1": ["w_internet", "w_conexion", "w_servicio"],
    "internet_phone_1": ["w_telefono", "w_plan", "w_datos"],
    "internet_repair_1": ["w_tecnico", "w_problema", "w_sistema"],
    
    # SOCIAL BASICS
    "social_neighbor_1": ["w_vecino", "w_edificio", "w_ciudad"],
    "social_event_1": ["w_trabajo", "w_pais", "w_tiempo"],
    "social_dinner_1": ["w_cena", "w_casa", "w_amigo"],
    
    # CHAT MODULES - VERBS
    "chat_carlos_1": ["w_soy", "w_me_llamo", "w_vivo"],
    "chat_alejandra_1": ["w_quiero", "w_necesito", "w_busco"],
    "chat_diego_1": ["w_tengo", "w_puedo", "w_hablo"],
    "chat_sofia_1": ["w_voy", "w_pago", "w_traigo"],
    "chat_mateo_1": ["w_hago", "w_uso", "w_trabajo"],
    
    # CHAT MODULES - TIME
    "chat_camila_1": ["w_ayer", "w_hoy", "w_manana"],
    "chat_andres_1": ["w_aqui", "w_alli", "w_cerca"],
    "chat_valentina_1": ["w_porque", "w_entonces", "w_pero"],
    
    # CHAT MODULES - CONNECTORS
    "chat_luis_1": ["w_primero", "w_despues", "w_ahora"],
    "chat_mariana_1": ["w_siempre", "w_nunca", "w_veces"],
    "chat_javier_1": ["w_mas", "w_menos", "w_suficiente"],
    
    # CHAT MODULES - PRONOUNS/ADVERBS
    "chat_isabella_1": ["w_conmigo", "w_contigo", "w_solo"],
    "chat_tomas_1": ["w_antes", "w_tarde", "w_temprano"],
    "chat_daniela_1": ["w_tambien", "w_todavia", "w_tampoco"],
    
    # CHAT MODULES - ADJECTIVES
    "chat_pablo_1": ["w_facil", "w_dificil", "w_importante"],
    "chat_lucia_1": ["w_diferente", "w_igual", "w_nuevo"],
    "chat_martin_1": ["w_mejor", "w_peor", "w_listo"],
}


def seed_database():
    """Seed the database with situations and words"""
    db: Session = SessionLocal()
    
    try:
        # Upsert words (update if exists, insert if not) - process individually to avoid conflicts
        print("Inserting/updating words...")
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
            # Commit after each to avoid batch insert conflicts
            try:
                db.commit()
            except Exception as e:
                db.rollback()
                # If it's a duplicate, just update it
                existing = db.query(Word).filter(Word.id == word_data['id']).first()
                if existing:
                    existing.spanish = word_data['spanish']
                    existing.english = word_data['english']
                    db.commit()
                    words_updated += 1
                    if words_created > 0:
                        words_created -= 1
        print(f"Created {words_created} words, updated {words_updated} words")
        
        # Clear situation-word mappings and situations (but keep words)
        from app.models import Conversation, UserSituation, UserWord
        db.query(SituationWord).delete()
        db.query(Conversation).delete()  # Delete conversations first
        db.query(UserSituation).delete()  # Delete user situations
        db.query(Situation).delete()
        db.commit()
        
        # Insert situations
        print("Inserting situations...")
        for situation_data in SITUATIONS:
            situation = Situation(**situation_data)
            db.add(situation)
        db.commit()
        print(f"Inserted {len(SITUATIONS)} situations")
        
        # Insert situation-word mappings
        print("Inserting situation-word mappings...")
        total_mappings = 0
        for situation_id, word_ids in SITUATION_WORDS.items():
            for position, word_id in enumerate(word_ids, start=1):
                mapping = SituationWord(
                    situation_id=situation_id,
                    word_id=word_id,
                    position=position
                )
                db.add(mapping)
                total_mappings += 1
        db.commit()
        print(f"Inserted {total_mappings} situation-word mappings")
        
        print("✅ Seed data inserted successfully!")
        print(f"   - {len([s for s in SITUATIONS if s['is_free']])} free situations")
        print(f"   - {len([s for s in SITUATIONS if not s['is_free']])} premium situations")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
