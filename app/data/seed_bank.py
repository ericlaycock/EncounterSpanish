"""Central seed bank — single source of truth for all word and situation data.

All encounter words, high-frequency words, situations, and their links
are defined here. Grammar situations are in grammar_situations.py.
The seed script (scripts/seed_qa.py) reads from this module.

Structure: _SUB_SITUATIONS defines compact word data as (spanish, english) tuples.
ENCOUNTER_WORDS, SITUATIONS, and SITUATION_WORDS are generated at import time.
"""

from app.data.hf_words import HIGH_FREQUENCY_WORDS  # noqa: F401 — re-exported

# --- Animation type display names (used by API and onboarding) ---

ANIMATION_NAMES = {
    "airport": "Airport",
    "banking": "Banking",
    "clothing": "Clothing Shopping",
    "internet": "Internet",
    "small_talk": "Small Talk",
    "contractor": "Home Renovation",
    "groceries": "Groceries",
    "mechanic": "Mechanic",
    "police": "Police Stop",
    "restaurant": "Eating Out",
}

# --- Compact sub-situation definitions ---
# Each sub-situation has 50 encounters × 3 words = 150 (spanish, english) tuples.
# Words progress from basic/essential (early encounters) to specialized (later).

_SUB_SITUATIONS = {
    "airport": [
        {
            "title": "Checking In",
            "goal": "Complete the airport check-in process with the airline agent",
            "word_prefix": "air",
            "words": [
                # Encounter 1-5 (basic essentials)
                ("pasaporte", "passport"), ("vuelo", "flight"), ("boleto", "ticket"),
                ("equipaje", "luggage"), ("mostrador", "counter"), ("agente", "agent"),
                ("asiento", "seat"), ("puerta", "gate"), ("terminal", "terminal"),
                ("maleta", "suitcase"), ("embarque", "boarding"), ("salida", "departure"),
                ("llegada", "arrival"), ("destino", "destination"), ("fila", "line/queue"),
                # Encounter 6-10
                ("ventanilla", "window seat"), ("pasillo", "aisle"), ("reserva", "reservation"),
                ("demora", "delay"), ("pantalla", "screen"), ("zona", "zone"),
                ("documento", "document"), ("identificación", "identification"), ("nacionalidad", "nationality"),
                ("seguridad", "security"), ("control", "checkpoint"), ("registro", "check-in"),
                ("directo", "direct"), ("escala", "layover"), ("conexión", "connection"),
                # Encounter 11-15
                ("confirmar", "to confirm"), ("imprimir", "to print"), ("escanear", "to scan"),
                ("disponible", "available"), ("asignado", "assigned"), ("seleccionar", "to select"),
                ("equipaje de mano", "carry-on"), ("etiqueta", "tag"), ("peso", "weight"),
                ("sobrepeso", "overweight"), ("límite", "limit"), ("restricción", "restriction"),
                ("facturar", "to check in luggage"), ("recibo", "receipt"), ("tarifa", "fare"),
                # Encounter 16-20
                ("aerolínea", "airline"), ("pasajero", "passenger"), ("tripulación", "crew"),
                ("primera clase", "first class"), ("económica", "economy"), ("preferente", "preferred"),
                ("ida", "one-way"), ("vuelta", "return"), ("redondo", "round-trip"),
                ("cinturón", "seatbelt"), ("abrocharse", "to fasten"), ("señal", "sign/signal"),
                ("cabina", "cabin"), ("compartimento", "compartment"), ("superior", "overhead"),
                # Encounter 21-25
                ("aterrizar", "to land"), ("despegar", "to take off"), ("pista", "runway"),
                ("auxiliar", "flight attendant"), ("servicio", "service"), ("asistencia", "assistance"),
                ("aduana", "customs"), ("declarar", "to declare"), ("inmigración", "immigration"),
                ("formulario", "form"), ("llenar", "to fill out"), ("firmar", "to sign"),
                ("recoger", "to pick up"), ("reclamo", "claim"), ("cinta", "conveyor belt"),
                # Encounter 26-30
                ("cancelación", "cancellation"), ("compensación", "compensation"), ("reembolso", "refund"),
                ("emergencia", "emergency"), ("chaleco", "vest"), ("oxígeno", "oxygen"),
                ("prohibido", "prohibited"), ("líquido", "liquid"), ("gel", "gel"),
                ("inspección", "inspection"), ("detector", "detector"), ("rayos", "x-rays"),
                ("electrónico", "electronic"), ("dispositivo", "device"), ("apagar", "to turn off"),
                # Encounter 31-35
                ("abordar", "to board"), ("llamada", "call/announcement"), ("final", "final"),
                ("retraso", "delay"), ("itinerario", "itinerary"), ("cambiar", "to change"),
                ("vacuna", "vaccine"), ("certificado", "certificate"), ("salud", "health"),
                ("horario", "schedule"), ("puntual", "on time"), ("hora", "hour/time"),
                ("clase ejecutiva", "business class"), ("reclinable", "reclining"), ("espacio", "space"),
                # Encounter 36-40
                ("frágil", "fragile"), ("especial", "special"), ("delicado", "delicate"),
                ("transbordo", "transfer"), ("mapa", "map"), ("información", "information"),
                ("sala de espera", "waiting room"), ("anuncio", "announcement"), ("altavoz", "loudspeaker"),
                ("moneda", "currency"), ("efectivo", "cash"), ("pagar", "to pay"),
                ("piloto", "pilot"), ("copiloto", "co-pilot"), ("torre", "tower"),
                # Encounter 41-45
                ("turbulencia", "turbulence"), ("altitud", "altitude"), ("presión", "pressure"),
                ("máscara", "mask"), ("instrucciones", "instructions"), ("cumplir", "to comply"),
                ("regulación", "regulation"), ("norma", "rule"), ("vigente", "in effect"),
                ("tránsito", "transit"), ("lounge", "lounge"), ("acceso", "access"),
                ("equipaje perdido", "lost luggage"), ("reporte", "report"), ("oficina", "office"),
                # Encounter 46-50
                ("sobrecargo", "surcharge"), ("cargo", "charge"), ("adicional", "additional"),
                ("visa", "visa"), ("sello", "stamp"), ("entrada", "entry"),
                ("zona franca", "duty-free zone"), ("tienda", "shop"), ("libre", "free/duty-free"),
                ("válido", "valid"), ("vencimiento", "expiration"), ("vigencia", "validity"),
                ("buen viaje", "have a good trip"), ("destino final", "final destination"), ("llegada segura", "safe arrival"),
            ],
        },
    ],
    "banking": [
        {
            "title": "Opening a Bank Account",
            "goal": "Open a bank account by providing your information to the teller",
            "word_prefix": "bank_open",
            "words": [
                # Encounter 1-5
                ("cuenta", "account"), ("banco", "bank"), ("abrir", "to open"),
                ("dinero", "money"), ("depositar", "to deposit"), ("saldo", "balance"),
                ("identificación", "identification"), ("documento", "document"), ("firma", "signature"),
                ("tarjeta", "card"), ("débito", "debit"), ("crédito", "credit"),
                ("ahorro", "savings"), ("corriente", "checking"), ("tipo", "type"),
                # Encounter 6-10
                ("cajero", "teller"), ("ventanilla", "service window"), ("turno", "turn/number"),
                ("formulario", "form"), ("llenar", "to fill out"), ("datos", "data/details"),
                ("nombre", "name"), ("dirección", "address"), ("teléfono", "phone number"),
                ("requisito", "requirement"), ("comprobante", "proof/receipt"), ("domicilio", "address/residence"),
                ("clave", "PIN/password"), ("contraseña", "password"), ("seguridad", "security"),
                # Encounter 11-15
                ("sucursal", "branch"), ("horario", "business hours"), ("atención", "service"),
                ("interés", "interest"), ("tasa", "rate"), ("porcentaje", "percentage"),
                ("plazo", "term/period"), ("fijo", "fixed"), ("variable", "variable"),
                ("comisión", "commission/fee"), ("cobrar", "to charge"), ("mensual", "monthly"),
                ("estado de cuenta", "account statement"), ("movimiento", "transaction"), ("consultar", "to check"),
                # Encounter 16-20
                ("transferencia", "transfer"), ("enviar", "to send"), ("recibir", "to receive"),
                ("beneficiario", "beneficiary"), ("autorizar", "to authorize"), ("confirmar", "to confirm"),
                ("retiro", "withdrawal"), ("retirar", "to withdraw"), ("efectivo", "cash"),
                ("cheque", "check"), ("chequera", "checkbook"), ("endosar", "to endorse"),
                ("banca en línea", "online banking"), ("aplicación", "app"), ("acceso", "access"),
                # Encounter 21-25
                ("préstamo", "loan"), ("solicitar", "to request"), ("aprobar", "to approve"),
                ("pago", "payment"), ("cuota", "installment"), ("vencimiento", "due date"),
                ("cancelar", "to cancel"), ("cerrar", "to close"), ("motivo", "reason"),
                ("extracto", "statement"), ("historial", "history"), ("registro", "record"),
                ("número de cuenta", "account number"), ("titular", "account holder"), ("cotitular", "co-holder"),
                # Encounter 26-30
                ("contrato", "contract"), ("cláusula", "clause"), ("leer", "to read"),
                ("cliente", "client"), ("nuevo", "new"), ("existente", "existing"),
                ("moneda", "currency"), ("nacional", "national"), ("extranjera", "foreign"),
                ("seguro", "insurance"), ("protección", "protection"), ("cobertura", "coverage"),
                ("notificación", "notification"), ("alerta", "alert"), ("mensaje", "message"),
                # Encounter 31-35
                ("sobregiro", "overdraft"), ("penalidad", "penalty"), ("recargo", "surcharge"),
                ("inversión", "investment"), ("fondo", "fund"), ("rendimiento", "yield/return"),
                ("fideicomiso", "trust"), ("patrimonio", "assets"), ("herencia", "inheritance"),
                ("poder notarial", "power of attorney"), ("apoderado", "authorized agent"), ("representante", "representative"),
                ("nómina", "payroll"), ("domiciliar", "to set up direct deposit"), ("automático", "automatic"),
                # Encounter 36-40
                ("auditoría", "audit"), ("verificar", "to verify"), ("cumplimiento", "compliance"),
                ("antigüedad", "seniority/age"), ("vigente", "current/valid"), ("renovar", "to renew"),
                ("sucursal principal", "main branch"), ("gerente", "manager"), ("cita", "appointment"),
                ("bóveda", "vault"), ("caja fuerte", "safe deposit box"), ("llave", "key"),
                ("impuesto", "tax"), ("retención", "withholding"), ("declaración", "declaration"),
                # Encounter 41-45
                ("cuenta conjunta", "joint account"), ("mancomunada", "joint/shared"), ("separada", "separate"),
                ("tarjeta adicional", "additional card"), ("límite", "limit"), ("aumentar", "to increase"),
                ("fraude", "fraud"), ("bloquear", "to block"), ("reportar", "to report"),
                ("token", "token"), ("autenticación", "authentication"), ("verificación", "verification"),
                ("divisa", "foreign currency"), ("cambio", "exchange"), ("cotización", "quote"),
                # Encounter 46-50
                ("corresponsal", "correspondent bank"), ("intermediario", "intermediary"), ("red", "network"),
                ("regulación", "regulation"), ("normativa", "policy"), ("cumplir", "to comply"),
                ("certificado", "certificate"), ("constancia", "proof/certificate"), ("sello", "stamp"),
                ("asesor", "advisor"), ("consultoría", "consulting"), ("planificación", "planning"),
                ("bienvenido", "welcome"), ("servicio al cliente", "customer service"), ("satisfacción", "satisfaction"),
            ],
        },
        {
            "title": "Wire Transfer",
            "goal": "Complete a wire transfer by giving the teller the recipient details",
            "word_prefix": "bank_wire",
            "words": [
                # Encounter 1-5
                ("transferencia", "transfer"), ("enviar", "to send"), ("dinero", "money"),
                ("cuenta", "account"), ("destino", "destination"), ("beneficiario", "beneficiary"),
                ("monto", "amount"), ("banco", "bank"), ("receptor", "receiving"),
                ("nombre", "name"), ("número", "number"), ("referencia", "reference"),
                ("confirmar", "to confirm"), ("datos", "data/details"), ("verificar", "to verify"),
                # Encounter 6-10
                ("comisión", "commission/fee"), ("costo", "cost"), ("cobrar", "to charge"),
                ("nacional", "domestic"), ("internacional", "international"), ("país", "country"),
                ("plazo", "timeframe"), ("inmediato", "immediate"), ("demora", "delay"),
                ("recibo", "receipt"), ("comprobante", "proof"), ("imprimir", "to print"),
                ("saldo", "balance"), ("disponible", "available"), ("suficiente", "sufficient"),
                # Encounter 11-15
                ("código SWIFT", "SWIFT code"), ("clave", "code/key"), ("interbancario", "interbank"),
                ("moneda", "currency"), ("dólar", "dollar"), ("peso", "peso"),
                ("tipo de cambio", "exchange rate"), ("conversión", "conversion"), ("equivalente", "equivalent"),
                ("formulario", "form"), ("llenar", "to fill out"), ("firmar", "to sign"),
                ("límite", "limit"), ("máximo", "maximum"), ("diario", "daily"),
                # Encounter 16-20
                ("programar", "to schedule"), ("fecha", "date"), ("recurrente", "recurring"),
                ("cancelar", "to cancel"), ("modificar", "to modify"), ("corregir", "to correct"),
                ("notificación", "notification"), ("correo", "email"), ("mensaje", "message"),
                ("seguridad", "security"), ("contraseña", "password"), ("autorizar", "to authorize"),
                ("origen", "origin"), ("emisor", "sender/issuer"), ("ordenante", "originator"),
                # Encounter 21-25
                ("acreditar", "to credit"), ("debitar", "to debit"), ("procesar", "to process"),
                ("estado", "status"), ("pendiente", "pending"), ("completado", "completed"),
                ("rastrear", "to track"), ("seguimiento", "tracking"), ("código", "code"),
                ("sucursal", "branch"), ("plaza", "city/location"), ("dirección", "address"),
                ("urgente", "urgent"), ("prioritario", "priority"), ("express", "express"),
                # Encounter 26-30
                ("regulación", "regulation"), ("normativa", "policy"), ("cumplir", "to comply"),
                ("retención", "withholding"), ("impuesto", "tax"), ("porcentaje", "percentage"),
                ("error", "error"), ("rechazar", "to reject"), ("motivo", "reason"),
                ("fondos", "funds"), ("insuficiente", "insufficient"), ("cubrir", "to cover"),
                ("lote", "batch"), ("múltiple", "multiple"), ("masivo", "bulk"),
                # Encounter 31-35
                ("corresponsal", "correspondent"), ("intermediario", "intermediary"), ("ruta", "route"),
                ("demora bancaria", "bank delay"), ("hábil", "business (day)"), ("calendario", "calendar"),
                ("reversar", "to reverse"), ("devolución", "return/refund"), ("original", "original"),
                ("duplicado", "duplicate"), ("detectar", "to detect"), ("prevenir", "to prevent"),
                ("IBAN", "IBAN"), ("cuenta CLABE", "CLABE account"), ("formato", "format"),
                # Encounter 36-40
                ("beneficiario final", "ultimate beneficiary"), ("propósito", "purpose"), ("concepto", "concept/description"),
                ("factura", "invoice"), ("pago", "payment"), ("proveedor", "supplier"),
                ("nómina", "payroll"), ("empleado", "employee"), ("salario", "salary"),
                ("alquiler", "rent"), ("hipoteca", "mortgage"), ("mensualidad", "monthly payment"),
                ("ahorro", "savings"), ("inversión", "investment"), ("portafolio", "portfolio"),
                # Encounter 41-45
                ("lavado de dinero", "money laundering"), ("prevención", "prevention"), ("declarar", "to declare"),
                ("tratado", "treaty"), ("bilateral", "bilateral"), ("acuerdo", "agreement"),
                ("auditoría", "audit"), ("registro", "record"), ("documentar", "to document"),
                ("digital", "digital"), ("electrónico", "electronic"), ("plataforma", "platform"),
                ("blockchain", "blockchain"), ("cripto", "crypto"), ("billetera digital", "digital wallet"),
                # Encounter 46-50
                ("fideicomiso", "trust"), ("fiduciario", "fiduciary"), ("garantía", "guarantee"),
                ("penalización", "penalty"), ("multa", "fine"), ("sanción", "sanction"),
                ("disputa", "dispute"), ("reclamo", "claim"), ("resolución", "resolution"),
                ("exitoso", "successful"), ("recibido", "received"), ("acreditado", "credited"),
                ("gracias", "thank you"), ("finalizar", "to finalize"), ("completar", "to complete"),
            ],
        },
        {
            "title": "Currency Exchange",
            "goal": "Exchange your currency by negotiating with the teller",
            "word_prefix": "bank_exchange",
            "words": [
                # Encounter 1-5
                ("cambiar", "to exchange"), ("dinero", "money"), ("moneda", "currency"),
                ("dólar", "dollar"), ("peso", "peso"), ("euro", "euro"),
                ("tipo de cambio", "exchange rate"), ("tasa", "rate"), ("hoy", "today"),
                ("comprar", "to buy"), ("vender", "to sell"), ("precio", "price"),
                ("efectivo", "cash"), ("billete", "banknote"), ("centavo", "cent/coin"),
                # Encounter 6-10
                ("comisión", "commission"), ("cobrar", "to charge"), ("gratis", "free"),
                ("casa de cambio", "exchange office"), ("ventanilla", "service window"), ("cajero", "cashier"),
                ("identificación", "identification"), ("pasaporte", "passport"), ("mostrar", "to show"),
                ("recibo", "receipt"), ("comprobante", "proof"), ("guardar", "to keep"),
                ("cantidad", "quantity/amount"), ("cuánto", "how much"), ("total", "total"),
                # Encounter 11-15
                ("mejor", "better"), ("peor", "worse"), ("comparar", "to compare"),
                ("oficial", "official"), ("paralelo", "parallel/unofficial"), ("mercado", "market"),
                ("subir", "to go up"), ("bajar", "to go down"), ("estable", "stable"),
                ("denominación", "denomination"), ("grande", "large"), ("pequeño", "small"),
                ("cambio exacto", "exact change"), ("suelto", "loose change"), ("feria", "small change"),
                # Encounter 16-20
                ("cheque de viajero", "traveler's check"), ("endosar", "to endorse"), ("canjear", "to cash/redeem"),
                ("límite", "limit"), ("máximo", "maximum"), ("mínimo", "minimum"),
                ("divisa", "foreign currency"), ("extranjera", "foreign"), ("local", "local"),
                ("negociar", "to negotiate"), ("ofrecer", "to offer"), ("aceptar", "to accept"),
                ("libra", "pound"), ("yen", "yen"), ("franco", "franc"),
                # Encounter 21-25
                ("fluctuar", "to fluctuate"), ("variación", "variation"), ("diferencia", "difference"),
                ("ganancia", "profit/gain"), ("pérdida", "loss"), ("margen", "margin"),
                ("certificado", "certificate"), ("documento", "document"), ("original", "original"),
                ("banco central", "central bank"), ("regulación", "regulation"), ("autorizar", "to authorize"),
                ("turista", "tourist"), ("viajero", "traveler"), ("residente", "resident"),
                # Encounter 26-30
                ("transferir", "to transfer"), ("cuenta", "account"), ("depositar", "to deposit"),
                ("tarjeta", "card"), ("débito", "debit"), ("crédito", "credit"),
                ("retiro", "withdrawal"), ("cajero automático", "ATM"), ("disponible", "available"),
                ("seguro", "safe/insurance"), ("proteger", "to protect"), ("cuidar", "to take care"),
                ("falsificado", "counterfeit"), ("detectar", "to detect"), ("auténtico", "authentic"),
                # Encounter 31-35
                ("cotización", "quotation"), ("consultar", "to check"), ("actualizar", "to update"),
                ("horario", "schedule"), ("abierto", "open"), ("cerrado", "closed"),
                ("remesa", "remittance"), ("enviar", "to send"), ("recibir", "to receive"),
                ("oro", "gold"), ("plata", "silver"), ("metal", "metal"),
                ("inflación", "inflation"), ("devaluación", "devaluation"), ("revaluación", "revaluation"),
                # Encounter 36-40
                ("spread", "spread"), ("diferencial", "differential"), ("porcentaje", "percentage"),
                ("cripto", "crypto"), ("bitcoin", "bitcoin"), ("digital", "digital"),
                ("declarar", "to declare"), ("impuesto", "tax"), ("exento", "exempt"),
                ("frontera", "border"), ("aduana", "customs"), ("límite de efectivo", "cash limit"),
                ("recargo", "surcharge"), ("penalización", "penalty"), ("multa", "fine"),
                # Encounter 41-45
                ("estafa", "scam"), ("fraude", "fraud"), ("reportar", "to report"),
                ("verificar", "to verify"), ("confirmar", "to confirm"), ("validar", "to validate"),
                ("reservar", "to reserve"), ("separar", "to set aside"), ("apartar", "to put aside"),
                ("giro", "money order"), ("postal", "postal"), ("telegráfico", "telegraphic"),
                ("paridad", "parity"), ("equilibrio", "equilibrium"), ("balanza", "balance"),
                # Encounter 46-50
                ("especulación", "speculation"), ("inversión", "investment"), ("riesgo", "risk"),
                ("cobertura", "hedging"), ("futuro", "futures"), ("derivado", "derivative"),
                ("regulador", "regulator"), ("supervisor", "supervisor"), ("cumplimiento", "compliance"),
                ("favorable", "favorable"), ("conveniente", "convenient"), ("ventajoso", "advantageous"),
                ("operación exitosa", "successful transaction"), ("satisfecho", "satisfied"), ("completo", "complete"),
            ],
        },
    ],
    "clothing": [
        {
            "title": "Finding the Right Size",
            "goal": "Find the right clothing size with help from the store clerk",
            "word_prefix": "cloth",
            "words": [
                # Encounter 1-5
                ("talla", "size"), ("probador", "fitting room"), ("descuento", "discount"),
                ("camisa", "shirt"), ("pantalón", "pants"), ("zapatos", "shoes"),
                ("precio", "price"), ("color", "color"), ("tienda", "store"),
                ("grande", "large"), ("pequeño", "small"), ("mediano", "medium"),
                ("buscar", "to look for"), ("encontrar", "to find"), ("necesitar", "to need"),
                # Encounter 6-10
                ("probarse", "to try on"), ("quedar", "to fit"), ("bien", "well"),
                ("ajustado", "tight"), ("flojo", "loose"), ("cómodo", "comfortable"),
                ("vestido", "dress"), ("falda", "skirt"), ("blusa", "blouse"),
                ("manga", "sleeve"), ("largo", "long"), ("corto", "short"),
                ("algodón", "cotton"), ("tela", "fabric"), ("material", "material"),
                # Encounter 11-15
                ("devolver", "to return"), ("cambiar", "to exchange"), ("recibo", "receipt"),
                ("rebaja", "sale/discount"), ("oferta", "offer/deal"), ("temporada", "season"),
                ("cremallera", "zipper"), ("botón", "button"), ("bolsillo", "pocket"),
                ("ancho", "wide"), ("estrecho", "narrow"), ("entallado", "fitted"),
                ("negro", "black"), ("blanco", "white"), ("azul", "blue"),
                # Encounter 16-20
                ("rojo", "red"), ("verde", "green"), ("gris", "gray"),
                ("estampado", "printed/patterned"), ("liso", "plain"), ("rayas", "stripes"),
                ("elegante", "elegant"), ("casual", "casual"), ("formal", "formal"),
                ("cinturón", "belt"), ("corbata", "tie"), ("pañuelo", "scarf/handkerchief"),
                ("marca", "brand"), ("calidad", "quality"), ("resistente", "durable"),
                # Encounter 21-25
                ("abrigo", "coat"), ("chaqueta", "jacket"), ("suéter", "sweater"),
                ("interior", "underwear"), ("calcetín", "sock"), ("media", "stocking"),
                ("tacón", "heel"), ("suela", "sole"), ("cuero", "leather"),
                ("joyería", "jewelry"), ("anillo", "ring"), ("collar", "necklace"),
                ("gafas", "glasses"), ("sombrero", "hat"), ("gorra", "cap"),
                # Encounter 26-30
                ("lavar", "to wash"), ("planchar", "to iron"), ("secar", "to dry"),
                ("coser", "to sew"), ("arreglar", "to alter/fix"), ("sastre", "tailor"),
                ("diseño", "design"), ("modelo", "model/style"), ("colección", "collection"),
                ("probador ocupado", "fitting room occupied"), ("esperar", "to wait"), ("disponible", "available"),
                ("talla única", "one size"), ("extra grande", "extra large"), ("extra pequeño", "extra small"),
                # Encounter 31-35
                ("seda", "silk"), ("lana", "wool"), ("lino", "linen"),
                ("poliéster", "polyester"), ("sintético", "synthetic"), ("elástico", "elastic/stretchy"),
                ("moda", "fashion"), ("tendencia", "trend"), ("estilo", "style"),
                ("traje", "suit"), ("esmoquin", "tuxedo"), ("chaleco", "vest"),
                ("impermeable", "waterproof"), ("térmico", "thermal"), ("ligero", "lightweight"),
                # Encounter 36-40
                ("bordado", "embroidered"), ("encaje", "lace"), ("flecos", "fringe"),
                ("solapa", "lapel"), ("puño", "cuff"), ("cuello", "collar/neck"),
                ("cierre", "fastener/closure"), ("broche", "clasp"), ("hebilla", "buckle"),
                ("planchado", "pressed"), ("arrugado", "wrinkled"), ("manchado", "stained"),
                ("guardarropa", "wardrobe"), ("percha", "hanger"), ("estante", "shelf"),
                # Encounter 41-45
                ("confección", "tailoring"), ("medida", "measurement"), ("cinta métrica", "measuring tape"),
                ("patronaje", "pattern-making"), ("molde", "pattern/mold"), ("cortar", "to cut"),
                ("exhibición", "display"), ("vitrina", "showcase"), ("maniquí", "mannequin"),
                ("exclusivo", "exclusive"), ("limitado", "limited"), ("edición", "edition"),
                ("ecológico", "eco-friendly"), ("sostenible", "sustainable"), ("reciclado", "recycled"),
                # Encounter 46-50
                ("alta costura", "haute couture"), ("pasarela", "runway"), ("diseñador", "designer"),
                ("personalizado", "customized"), ("único", "unique"), ("hecho a mano", "handmade"),
                ("garantía", "warranty"), ("política", "policy"), ("devolución", "return"),
                ("satisfecho", "satisfied"), ("perfecto", "perfect"), ("ideal", "ideal"),
                ("gracias", "thank you"), ("compra", "purchase"), ("bolsa", "bag"),
            ],
        },
    ],
    "contractor": [
        {
            "title": "Hiring a Plumber",
            "goal": "Hire a plumber by describing the problem and agreeing on a price",
            "word_prefix": "contr",
            "words": [
                # Encounter 1-5
                ("plomero", "plumber"), ("problema", "problem"), ("arreglar", "to fix"),
                ("agua", "water"), ("tubo", "pipe"), ("fuga", "leak"),
                ("baño", "bathroom"), ("cocina", "kitchen"), ("lavabo", "sink"),
                ("precio", "price"), ("costo", "cost"), ("presupuesto", "estimate/quote"),
                ("urgente", "urgent"), ("necesitar", "to need"), ("ayuda", "help"),
                # Encounter 6-10
                ("llave", "faucet/wrench"), ("grifo", "faucet/tap"), ("gotear", "to drip"),
                ("cañería", "plumbing/pipes"), ("drenaje", "drain"), ("tapado", "clogged"),
                ("reparar", "to repair"), ("instalar", "to install"), ("cambiar", "to replace"),
                ("material", "material"), ("pieza", "part/piece"), ("herramienta", "tool"),
                ("disponible", "available"), ("horario", "schedule"), ("cuándo", "when"),
                # Encounter 11-15
                ("inodoro", "toilet"), ("regadera", "shower"), ("tina", "bathtub"),
                ("calentador", "water heater"), ("tanque", "tank"), ("presión", "pressure"),
                ("roto", "broken"), ("dañado", "damaged"), ("viejo", "old"),
                ("nuevo", "new"), ("repuesto", "replacement part"), ("original", "original"),
                ("garantía", "warranty"), ("duración", "duration"), ("calidad", "quality"),
                # Encounter 16-20
                ("mano de obra", "labor"), ("hora", "hour"), ("cobrar", "to charge"),
                ("factura", "invoice"), ("pagar", "to pay"), ("efectivo", "cash"),
                ("tubería", "piping"), ("conexión", "connection"), ("junta", "joint/gasket"),
                ("válvula", "valve"), ("registro", "shutoff valve"), ("cerrar", "to close/shut"),
                ("nivel", "level"), ("medida", "measurement"), ("calcular", "to calculate"),
                # Encounter 21-25
                ("permiso", "permit"), ("licencia", "license"), ("certificado", "certificate"),
                ("experiencia", "experience"), ("años", "years"), ("recomendación", "recommendation"),
                ("desatascar", "to unclog"), ("destapador", "plunger"), ("sonda", "drain snake"),
                ("humedad", "humidity/moisture"), ("moho", "mold"), ("filtración", "seepage"),
                ("bomba", "pump"), ("motor", "motor"), ("eléctrico", "electric"),
                # Encounter 26-30
                ("contrato", "contract"), ("firmar", "to sign"), ("acuerdo", "agreement"),
                ("adelanto", "advance payment"), ("depósito", "deposit"), ("liquidar", "to settle/pay off"),
                ("sótano", "basement"), ("techo", "roof/ceiling"), ("pared", "wall"),
                ("excavación", "excavation"), ("zanja", "trench"), ("cavar", "to dig"),
                ("cobre", "copper"), ("PVC", "PVC"), ("galvanizado", "galvanized"),
                # Encounter 31-35
                ("sellador", "sealant"), ("cinta", "tape"), ("pegamento", "glue"),
                ("cortar", "to cut"), ("soldar", "to weld/solder"), ("unir", "to join"),
                ("inspección", "inspection"), ("revisar", "to check/inspect"), ("diagnóstico", "diagnosis"),
                ("cisterna", "cistern"), ("aljibe", "water tank"), ("tinaco", "rooftop tank"),
                ("residuo", "residue"), ("obstrucción", "obstruction"), ("limpiar", "to clean"),
                # Encounter 36-40
                ("emergencia", "emergency"), ("inundación", "flood"), ("daño", "damage"),
                ("seguro", "insurance"), ("cobertura", "coverage"), ("reclamar", "to claim"),
                ("calefacción", "heating"), ("radiador", "radiator"), ("termostato", "thermostat"),
                ("gas", "gas"), ("detector", "detector"), ("peligro", "danger"),
                ("ventilación", "ventilation"), ("extractor", "extractor fan"), ("ducto", "duct"),
                # Encounter 41-45
                ("purificador", "purifier"), ("filtro", "filter"), ("suavizador", "water softener"),
                ("riego", "irrigation"), ("manguera", "hose"), ("aspersor", "sprinkler"),
                ("fosa séptica", "septic tank"), ("drenaje pluvial", "storm drain"), ("alcantarilla", "sewer"),
                ("medidor", "meter"), ("consumo", "consumption"), ("lectura", "reading"),
                ("remodelación", "remodeling"), ("ampliación", "expansion"), ("diseño", "design"),
                # Encounter 46-50
                ("código", "code"), ("regulación", "regulation"), ("norma", "standard"),
                ("subcontratista", "subcontractor"), ("equipo", "team/equipment"), ("supervisor", "supervisor"),
                ("plazo", "deadline"), ("completar", "to complete"), ("terminar", "to finish"),
                ("recomendar", "to recommend"), ("referencia", "reference"), ("reseña", "review"),
                ("buen trabajo", "good job"), ("satisfecho", "satisfied"), ("agradecer", "to thank"),
            ],
        },
    ],
    "groceries": [
        {
            "title": "At the Supermarket",
            "goal": "Buy groceries by finding items and checking out",
            "word_prefix": "groc",
            "words": [
                # Encounter 1-5
                ("supermercado", "supermarket"), ("comprar", "to buy"), ("lista", "list"),
                ("fruta", "fruit"), ("verdura", "vegetable"), ("carne", "meat"),
                ("pan", "bread"), ("leche", "milk"), ("huevo", "egg"),
                ("precio", "price"), ("barato", "cheap"), ("caro", "expensive"),
                ("bolsa", "bag"), ("carrito", "cart"), ("canasta", "basket"),
                # Encounter 6-10
                ("pasillo", "aisle"), ("estante", "shelf"), ("sección", "section"),
                ("fresco", "fresh"), ("congelado", "frozen"), ("enlatado", "canned"),
                ("pollo", "chicken"), ("pescado", "fish"), ("cerdo", "pork"),
                ("arroz", "rice"), ("frijol", "bean"), ("pasta", "pasta"),
                ("aceite", "oil"), ("sal", "salt"), ("azúcar", "sugar"),
                # Encounter 11-15
                ("caja", "checkout/cashier"), ("pagar", "to pay"), ("cambio", "change"),
                ("oferta", "deal/offer"), ("descuento", "discount"), ("promoción", "promotion"),
                ("kilo", "kilogram"), ("gramo", "gram"), ("litro", "liter"),
                ("maduro", "ripe"), ("verde", "unripe/green"), ("podrido", "rotten"),
                ("orgánico", "organic"), ("natural", "natural"), ("integral", "whole grain"),
                # Encounter 16-20
                ("panadería", "bakery"), ("carnicería", "butcher shop"), ("pescadería", "fish counter"),
                ("lácteo", "dairy"), ("queso", "cheese"), ("yogur", "yogurt"),
                ("bebida", "drink"), ("jugo", "juice"), ("agua", "water"),
                ("galleta", "cookie/cracker"), ("cereal", "cereal"), ("chocolate", "chocolate"),
                ("condimento", "condiment"), ("salsa", "sauce"), ("vinagre", "vinegar"),
                # Encounter 21-25
                ("receta", "recipe"), ("ingrediente", "ingredient"), ("preparar", "to prepare"),
                ("marca", "brand"), ("genérico", "generic"), ("importado", "imported"),
                ("empaque", "packaging"), ("etiqueta", "label"), ("caducidad", "expiration"),
                ("refrigerador", "refrigerator section"), ("congelador", "freezer section"), ("ambiente", "room temperature"),
                ("limpieza", "cleaning"), ("detergente", "detergent"), ("jabón", "soap"),
                # Encounter 26-30
                ("papel", "paper"), ("servilleta", "napkin"), ("aluminio", "aluminum foil"),
                ("especia", "spice"), ("pimienta", "pepper"), ("canela", "cinnamon"),
                ("harina", "flour"), ("levadura", "yeast"), ("mantequilla", "butter"),
                ("nuez", "nut"), ("almendra", "almond"), ("cacahuate", "peanut"),
                ("fiambre", "deli meat"), ("jamón", "ham"), ("salchicha", "sausage"),
                # Encounter 31-35
                ("tomate", "tomato"), ("cebolla", "onion"), ("ajo", "garlic"),
                ("lechuga", "lettuce"), ("zanahoria", "carrot"), ("papa", "potato"),
                ("manzana", "apple"), ("plátano", "banana"), ("naranja", "orange"),
                ("limón", "lemon"), ("fresa", "strawberry"), ("uva", "grape"),
                ("atún", "tuna"), ("sardina", "sardine"), ("camarón", "shrimp"),
                # Encounter 36-40
                ("tortilla", "tortilla"), ("tostada", "toast/tostada"), ("crema", "cream/sour cream"),
                ("aguacate", "avocado"), ("chile", "chili pepper"), ("cilantro", "cilantro"),
                ("refresco", "soda"), ("cerveza", "beer"), ("vino", "wine"),
                ("pañal", "diaper"), ("toalla", "towel"), ("champú", "shampoo"),
                ("mascota", "pet"), ("alimento", "food/feed"), ("lata", "can"),
                # Encounter 41-45
                ("gourmet", "gourmet"), ("delicatessen", "delicatessen"), ("especialidad", "specialty"),
                ("libre de gluten", "gluten-free"), ("vegano", "vegan"), ("sin lactosa", "lactose-free"),
                ("peso", "weight"), ("báscula", "scale"), ("medir", "to measure"),
                ("empacador", "bagger"), ("acomodar", "to arrange"), ("separar", "to separate"),
                ("factura", "invoice"), ("ticket", "receipt"), ("fiscal", "tax-related"),
                # Encounter 46-50
                ("entrega", "delivery"), ("domicilio", "home address"), ("envío", "shipping"),
                ("estacionamiento", "parking lot"), ("entrada", "entrance"), ("salida", "exit"),
                ("horario", "schedule"), ("abierto", "open"), ("cerrado", "closed"),
                ("fidelidad", "loyalty"), ("puntos", "points"), ("membresía", "membership"),
                ("gracias", "thank you"), ("buen día", "good day"), ("volver", "to come back"),
            ],
        },
    ],
    "internet": [
        {
            "title": "Setting Up WiFi",
            "goal": "Set up your internet service by speaking with the technician",
            "word_prefix": "inet",
            "words": [
                # Encounter 1-5
                ("internet", "internet"), ("wifi", "WiFi"), ("conexión", "connection"),
                ("contraseña", "password"), ("red", "network"), ("señal", "signal"),
                ("router", "router"), ("cable", "cable"), ("enchufe", "plug/outlet"),
                ("rápido", "fast"), ("lento", "slow"), ("velocidad", "speed"),
                ("plan", "plan"), ("precio", "price"), ("mensual", "monthly"),
                # Encounter 6-10
                ("instalar", "to install"), ("técnico", "technician"), ("visita", "visit"),
                ("nombre de red", "network name"), ("cambiar", "to change"), ("configurar", "to configure"),
                ("conectar", "to connect"), ("desconectar", "to disconnect"), ("reiniciar", "to restart"),
                ("dispositivo", "device"), ("computadora", "computer"), ("celular", "cellphone"),
                ("funcionar", "to work/function"), ("problema", "problem"), ("solución", "solution"),
                # Encounter 11-15
                ("banda ancha", "broadband"), ("fibra óptica", "fiber optic"), ("megabits", "megabits"),
                ("descargar", "to download"), ("subir", "to upload"), ("datos", "data"),
                ("factura", "bill"), ("pagar", "to pay"), ("vencimiento", "due date"),
                ("servicio", "service"), ("atención", "customer care"), ("llamar", "to call"),
                ("modem", "modem"), ("antena", "antenna"), ("receptor", "receiver"),
                # Encounter 16-20
                ("cobertura", "coverage"), ("zona", "zone"), ("alcance", "range"),
                ("corte", "outage"), ("interrupción", "interruption"), ("restaurar", "to restore"),
                ("contrato", "contract"), ("permanencia", "commitment period"), ("cancelar", "to cancel"),
                ("actualizar", "to update/upgrade"), ("mejorar", "to improve"), ("paquete", "package"),
                ("televisión", "television"), ("teléfono", "telephone"), ("combo", "bundle"),
                # Encounter 21-25
                ("streaming", "streaming"), ("videollamada", "video call"), ("juego en línea", "online gaming"),
                ("límite", "limit"), ("ilimitado", "unlimited"), ("consumo", "usage"),
                ("seguridad", "security"), ("firewall", "firewall"), ("proteger", "to protect"),
                ("virus", "virus"), ("malware", "malware"), ("antivirus", "antivirus"),
                ("extensión", "extension/extender"), ("repetidor", "repeater"), ("amplificar", "to amplify"),
                # Encounter 26-30
                ("dirección IP", "IP address"), ("DNS", "DNS"), ("puerto", "port"),
                ("ethernet", "ethernet"), ("inalámbrico", "wireless"), ("bluetooth", "bluetooth"),
                ("latencia", "latency"), ("ping", "ping"), ("estabilidad", "stability"),
                ("asistencia técnica", "technical support"), ("soporte", "support"), ("ayuda", "help"),
                ("aplicación", "application"), ("navegador", "browser"), ("página web", "webpage"),
                # Encounter 31-35
                ("usuario", "username"), ("cuenta", "account"), ("registrar", "to register"),
                ("acceso", "access"), ("bloquear", "to block"), ("permitir", "to allow"),
                ("control parental", "parental controls"), ("filtro", "filter"), ("restricción", "restriction"),
                ("cámara", "camera"), ("monitor", "monitor"), ("vigilancia", "surveillance"),
                ("domótica", "home automation"), ("inteligente", "smart"), ("automatizar", "to automate"),
                # Encounter 36-40
                ("nube", "cloud"), ("almacenar", "to store"), ("respaldo", "backup"),
                ("impresora", "printer"), ("compartir", "to share"), ("acceso remoto", "remote access"),
                ("VPN", "VPN"), ("privacidad", "privacy"), ("encriptar", "to encrypt"),
                ("ancho de banda", "bandwidth"), ("saturado", "saturated"), ("optimizar", "to optimize"),
                ("proveedor", "provider"), ("competencia", "competition"), ("comparar", "to compare"),
                # Encounter 41-45
                ("instalación", "installation"), ("cableado", "wiring"), ("infraestructura", "infrastructure"),
                ("contratación", "hiring/contracting"), ("requisito", "requirement"), ("documento", "document"),
                ("migración", "migration"), ("portabilidad", "portability"), ("número", "number"),
                ("promoción", "promotion"), ("descuento", "discount"), ("oferta", "offer"),
                ("queja", "complaint"), ("reclamo", "claim"), ("resolver", "to resolve"),
                # Encounter 46-50
                ("medidor", "meter"), ("consumo real", "actual usage"), ("reporte", "report"),
                ("satelital", "satellite"), ("rural", "rural"), ("urbano", "urban"),
                ("mantenimiento", "maintenance"), ("actualización", "update"), ("programar", "to schedule"),
                ("satisfacción", "satisfaction"), ("calificación", "rating"), ("encuesta", "survey"),
                ("listo", "ready"), ("funcionando", "working"), ("perfecto", "perfect"),
            ],
        },
    ],
    "mechanic": [
        {
            "title": "Oil Change",
            "goal": "Get your car serviced by explaining what you need to the mechanic",
            "word_prefix": "mech",
            "words": [
                # Encounter 1-5
                ("aceite", "oil"), ("cambio", "change"), ("carro", "car"),
                ("motor", "engine"), ("taller", "workshop/garage"), ("mecánico", "mechanic"),
                ("revisar", "to check"), ("problema", "problem"), ("ruido", "noise"),
                ("freno", "brake"), ("llanta", "tire"), ("volante", "steering wheel"),
                ("gasolina", "gasoline"), ("tanque", "tank"), ("llenar", "to fill"),
                # Encounter 6-10
                ("filtro", "filter"), ("bujía", "spark plug"), ("batería", "battery"),
                ("luz", "light"), ("faro", "headlight"), ("direccional", "turn signal"),
                ("velocidad", "speed"), ("kilómetro", "kilometer"), ("milla", "mile"),
                ("arrancar", "to start"), ("apagar", "to turn off"), ("encender", "to turn on"),
                ("precio", "price"), ("costo", "cost"), ("presupuesto", "estimate"),
                # Encounter 11-15
                ("reparar", "to repair"), ("arreglar", "to fix"), ("cambiar", "to replace"),
                ("pieza", "part"), ("repuesto", "spare part"), ("original", "original/OEM"),
                ("garantía", "warranty"), ("duración", "duration"), ("meses", "months"),
                ("sintético", "synthetic"), ("convencional", "conventional"), ("viscosidad", "viscosity"),
                ("kilometraje", "mileage"), ("mantenimiento", "maintenance"), ("servicio", "service"),
                # Encounter 16-20
                ("transmisión", "transmission"), ("automático", "automatic"), ("manual", "manual"),
                ("embrague", "clutch"), ("pedal", "pedal"), ("palanca", "lever/shift"),
                ("radiador", "radiator"), ("refrigerante", "coolant"), ("temperatura", "temperature"),
                ("escape", "exhaust"), ("silenciador", "muffler"), ("tubo", "pipe"),
                ("suspensión", "suspension"), ("amortiguador", "shock absorber"), ("resorte", "spring"),
                # Encounter 21-25
                ("alineación", "alignment"), ("balanceo", "balancing"), ("rotación", "rotation"),
                ("correa", "belt"), ("cadena", "chain"), ("tensor", "tensioner"),
                ("alternador", "alternator"), ("generador", "generator"), ("eléctrico", "electrical"),
                ("fusible", "fuse"), ("cableado", "wiring"), ("cortocircuito", "short circuit"),
                ("aire acondicionado", "air conditioning"), ("compresor", "compressor"), ("freón", "freon/refrigerant"),
                # Encounter 26-30
                ("diagnóstico", "diagnostic"), ("computadora", "computer"), ("escáner", "scanner"),
                ("sensor", "sensor"), ("medidor", "gauge"), ("lectura", "reading"),
                ("oxidado", "rusted"), ("corroído", "corroded"), ("desgastado", "worn"),
                ("apretar", "to tighten"), ("aflojar", "to loosen"), ("torque", "torque"),
                ("gato", "jack"), ("llave", "wrench"), ("herramienta", "tool"),
                # Encounter 31-35
                ("aceite de motor", "engine oil"), ("nivel", "level"), ("dipstick", "dipstick"),
                ("junta", "gasket"), ("empaque", "seal"), ("sello", "seal"),
                ("bomba", "pump"), ("combustible", "fuel"), ("inyector", "injector"),
                ("carburador", "carburetor"), ("admisión", "intake"), ("válvula", "valve"),
                ("cigüeñal", "crankshaft"), ("pistón", "piston"), ("cilindro", "cylinder"),
                # Encounter 36-40
                ("turbo", "turbo"), ("sobrealimentador", "supercharger"), ("potencia", "horsepower"),
                ("catalizador", "catalytic converter"), ("emisión", "emission"), ("contaminación", "pollution"),
                ("freno de disco", "disc brake"), ("pastilla", "brake pad"), ("rotor", "rotor"),
                ("dirección hidráulica", "power steering"), ("fluido", "fluid"), ("manguera", "hose"),
                ("limpiaparabrisas", "windshield wiper"), ("parabrisas", "windshield"), ("cristal", "glass"),
                # Encounter 41-45
                ("tapicería", "upholstery"), ("vestidura", "seat cover"), ("piso", "floor/mat"),
                ("pintura", "paint"), ("abollar", "to dent"), ("rayar", "to scratch"),
                ("hojalatería", "body shop"), ("carrocería", "body/chassis"), ("soldar", "to weld"),
                ("seguro", "insurance"), ("cobertura", "coverage"), ("deducible", "deductible"),
                ("grúa", "tow truck"), ("remolcar", "to tow"), ("emergencia", "emergency"),
                # Encounter 46-50
                ("verificación", "inspection"), ("placa", "license plate"), ("registro", "registration"),
                ("híbrido", "hybrid"), ("ecológico", "eco-friendly"), ("recarga", "recharge"),
                ("tuning", "tuning"), ("modificar", "to modify"), ("personalizar", "to customize"),
                ("cita", "appointment"), ("programar", "to schedule"), ("disponible", "available"),
                ("listo", "ready"), ("recoger", "to pick up"), ("entregar", "to deliver"),
            ],
        },
    ],
    "police": [
        {
            "title": "Traffic Stop",
            "goal": "Handle a traffic stop by responding to the officer's questions",
            "word_prefix": "pol",
            "words": [
                # Encounter 1-5
                ("licencia", "license"), ("oficial", "officer"), ("documentos", "documents"),
                ("seguro", "insurance"), ("registro", "registration"), ("tarjeta", "card"),
                ("manejar", "to drive"), ("velocidad", "speed"), ("límite", "limit"),
                ("alto", "stop"), ("señal", "sign"), ("semáforo", "traffic light"),
                ("multa", "fine/ticket"), ("infracción", "violation"), ("pagar", "to pay"),
                # Encounter 6-10
                ("carro", "car"), ("placa", "license plate"), ("modelo", "model"),
                ("cinturón", "seatbelt"), ("abrochado", "fastened"), ("puesto", "on/wearing"),
                ("zona", "zone"), ("escolar", "school"), ("residencial", "residential"),
                ("derecho", "right"), ("obligación", "obligation"), ("ley", "law"),
                ("disculpe", "excuse me"), ("entender", "to understand"), ("explicar", "to explain"),
                # Encounter 11-15
                ("carretera", "highway"), ("autopista", "freeway"), ("calle", "street"),
                ("dirección", "direction"), ("sentido", "direction/way"), ("contrario", "opposite/wrong way"),
                ("cruce", "intersection"), ("esquina", "corner"), ("vuelta", "turn"),
                ("estacionar", "to park"), ("prohibido", "prohibited"), ("permitido", "allowed"),
                ("alcohol", "alcohol"), ("prueba", "test"), ("soplar", "to blow"),
                # Encounter 16-20
                ("accidente", "accident"), ("choque", "crash/collision"), ("daño", "damage"),
                ("ambulancia", "ambulance"), ("emergencia", "emergency"), ("herido", "injured"),
                ("testigo", "witness"), ("declaración", "statement"), ("nombre", "name"),
                ("celular", "cellphone"), ("distracción", "distraction"), ("sancionado", "penalized"),
                ("cinturón de seguridad", "seatbelt"), ("pasajero", "passenger"), ("menor", "minor"),
                # Encounter 21-25
                ("grúa", "tow truck"), ("remolcar", "to tow"), ("corralón", "impound lot"),
                ("radar", "radar"), ("cámara", "camera"), ("evidencia", "evidence"),
                ("advertencia", "warning"), ("primera vez", "first time"), ("perdón", "pardon"),
                ("carril", "lane"), ("rebasar", "to pass/overtake"), ("doble línea", "double line"),
                ("rotonda", "roundabout"), ("glorieta", "traffic circle"), ("ceder", "to yield"),
                # Encounter 26-30
                ("peatón", "pedestrian"), ("cruzar", "to cross"), ("paso", "crosswalk"),
                ("motocicleta", "motorcycle"), ("bicicleta", "bicycle"), ("ciclista", "cyclist"),
                ("retén", "checkpoint"), ("inspección", "inspection"), ("revisar", "to check"),
                ("licencia vencida", "expired license"), ("renovar", "to renew"), ("vigente", "valid/current"),
                ("extranjero", "foreigner"), ("turista", "tourist"), ("permiso", "permit"),
                # Encounter 31-35
                ("abogado", "lawyer"), ("defensa", "defense"), ("representante", "representative"),
                ("cargos", "charges"), ("grave", "serious"), ("leve", "minor"),
                ("comparecencia", "court appearance"), ("juzgado", "court"), ("fecha", "date"),
                ("imprudencia", "recklessness"), ("negligencia", "negligence"), ("responsabilidad", "responsibility"),
                ("recurso", "appeal"), ("impugnar", "to contest"), ("tribunal", "tribunal"),
                # Encounter 31-40
                ("arresto", "arrest"), ("detención", "detention"), ("esposas", "handcuffs"),
                ("patrulla", "patrol car"), ("sirena", "siren"), ("persecución", "pursuit"),
                ("registro vehicular", "vehicle search"), ("autorización", "authorization"), ("consentir", "to consent"),
                ("chaleco", "vest"), ("uniforme", "uniform"), ("insignia", "badge"),
                ("reporte", "report"), ("número de caso", "case number"), ("copia", "copy"),
                # Encounter 41-45
                ("soborno", "bribe"), ("corrupción", "corruption"), ("denunciar", "to report/denounce"),
                ("derechos", "rights"), ("silencio", "silence"), ("inocente", "innocent"),
                ("fianza", "bail"), ("liberación", "release"), ("custodia", "custody"),
                ("embajada", "embassy"), ("consulado", "consulate"), ("asistencia", "assistance"),
                ("traducción", "translation"), ("intérprete", "interpreter"), ("idioma", "language"),
                # Encounter 46-50
                ("protocolo", "protocol"), ("procedimiento", "procedure"), ("normativa", "regulation"),
                ("queja", "complaint"), ("asuntos internos", "internal affairs"), ("supervisión", "oversight"),
                ("antecedentes", "record/background"), ("historial", "history"), ("limpio", "clean"),
                ("cooperar", "to cooperate"), ("respetuoso", "respectful"), ("educado", "polite"),
                ("buenas noches", "good evening"), ("gracias", "thank you"), ("cuidado", "take care"),
            ],
        },
    ],
    "restaurant": [
        {
            "title": "Ordering Food",
            "goal": "Order a meal by communicating with the waiter",
            "word_prefix": "rest_order",
            "words": [
                # Encounter 1-5
                ("menú", "menu"), ("mesero", "waiter"), ("mesa", "table"),
                ("comida", "food"), ("bebida", "drink"), ("agua", "water"),
                ("pedir", "to order"), ("recomendar", "to recommend"), ("especial", "special"),
                ("entrada", "appetizer"), ("plato fuerte", "main course"), ("postre", "dessert"),
                ("pollo", "chicken"), ("carne", "meat/beef"), ("pescado", "fish"),
                # Encounter 6-10
                ("arroz", "rice"), ("ensalada", "salad"), ("sopa", "soup"),
                ("pan", "bread"), ("tortilla", "tortilla"), ("salsa", "sauce"),
                ("sal", "salt"), ("pimienta", "pepper"), ("limón", "lemon/lime"),
                ("picante", "spicy"), ("suave", "mild"), ("sabor", "flavor"),
                ("frío", "cold"), ("caliente", "hot"), ("tibio", "warm"),
                # Encounter 11-15
                ("cocinar", "to cook"), ("freír", "to fry"), ("asar", "to grill"),
                ("hervir", "to boil"), ("hornear", "to bake"), ("preparar", "to prepare"),
                ("vegetariano", "vegetarian"), ("alergia", "allergy"), ("ingrediente", "ingredient"),
                ("tenedor", "fork"), ("cuchillo", "knife"), ("cuchara", "spoon"),
                ("plato", "plate"), ("vaso", "glass"), ("servilleta", "napkin"),
                # Encounter 16-20
                ("taco", "taco"), ("enchilada", "enchilada"), ("burrito", "burrito"),
                ("guacamole", "guacamole"), ("frijoles", "beans"), ("queso", "cheese"),
                ("cerveza", "beer"), ("vino", "wine"), ("refresco", "soda"),
                ("jugo", "juice"), ("café", "coffee"), ("té", "tea"),
                ("porción", "portion"), ("grande", "large"), ("chico", "small"),
                # Encounter 21-25
                ("mariscos", "seafood"), ("camarón", "shrimp"), ("pulpo", "octopus"),
                ("cerdo", "pork"), ("cordero", "lamb"), ("res", "beef"),
                ("vegetales", "vegetables"), ("champiñón", "mushroom"), ("cebolla", "onion"),
                ("ajo", "garlic"), ("tomate", "tomato"), ("aguacate", "avocado"),
                ("chile", "chili"), ("jalapeño", "jalapeño"), ("habanero", "habanero"),
                # Encounter 26-30
                ("azúcar", "sugar"), ("miel", "honey"), ("crema", "cream"),
                ("mantequilla", "butter"), ("aceite", "oil"), ("vinagre", "vinegar"),
                ("delicioso", "delicious"), ("rico", "tasty"), ("sabroso", "flavorful"),
                ("fresco", "fresh"), ("casero", "homemade"), ("tradicional", "traditional"),
                ("dieta", "diet"), ("sin gluten", "gluten-free"), ("orgánico", "organic"),
                # Encounter 31-35
                ("ceviche", "ceviche"), ("mole", "mole"), ("tamales", "tamales"),
                ("mezcal", "mezcal"), ("tequila", "tequila"), ("margarita", "margarita"),
                ("antojito", "snack/appetizer"), ("quesadilla", "quesadilla"), ("tostada", "tostada"),
                ("sazón", "seasoning"), ("receta", "recipe"), ("chef", "chef"),
                ("parrilla", "grill"), ("horno", "oven"), ("sartén", "pan"),
                # Encounter 36-40
                ("maridaje", "pairing"), ("acompañamiento", "side dish"), ("guarnición", "garnish"),
                ("degustación", "tasting"), ("menú del día", "daily menu"), ("carta", "menu/wine list"),
                ("reservación", "reservation"), ("privado", "private"), ("terraza", "terrace"),
                ("propina", "tip"), ("servicio", "service"), ("excelente", "excellent"),
                ("comensal", "diner"), ("grupo", "group"), ("familiar", "family-style"),
                # Encounter 41-45
                ("vegano", "vegan"), ("crudo", "raw"), ("al vapor", "steamed"),
                ("ahumado", "smoked"), ("marinado", "marinated"), ("empanizado", "breaded"),
                ("fusión", "fusion"), ("contemporáneo", "contemporary"), ("gourmet", "gourmet"),
                ("bodega", "wine cellar"), ("cosecha", "harvest/vintage"), ("reserva", "reserve"),
                ("flambear", "to flambé"), ("gratinar", "to gratin"), ("reducción", "reduction"),
                # Encounter 46-50
                ("sommelier", "sommelier"), ("catador", "taster"), ("selección", "selection"),
                ("natural", "natural"), ("sustentable", "sustainable"), ("local", "local"),
                ("satisfecho", "satisfied"), ("lleno", "full"), ("suficiente", "enough"),
                ("memorable", "memorable"), ("felicitaciones", "congratulations"), ("al chef", "to the chef"),
                ("gracias", "thank you"), ("volver", "to come back"), ("favorito", "favorite"),
            ],
        },
        {
            "title": "Making a Reservation",
            "goal": "Make a restaurant reservation by calling or speaking with the host",
            "word_prefix": "rest_reserve",
            "words": [
                # Encounter 1-5
                ("reservación", "reservation"), ("mesa", "table"), ("personas", "people"),
                ("fecha", "date"), ("hora", "time"), ("noche", "evening/night"),
                ("nombre", "name"), ("teléfono", "phone"), ("confirmar", "to confirm"),
                ("disponible", "available"), ("lleno", "full"), ("esperar", "to wait"),
                ("hoy", "today"), ("mañana", "tomorrow"), ("fin de semana", "weekend"),
                # Encounter 6-10
                ("interior", "inside"), ("exterior", "outside"), ("terraza", "terrace"),
                ("ventana", "window"), ("esquina", "corner"), ("privado", "private"),
                ("grande", "large"), ("pequeño", "small"), ("íntimo", "intimate"),
                ("celebración", "celebration"), ("cumpleaños", "birthday"), ("aniversario", "anniversary"),
                ("grupo", "group"), ("pareja", "couple"), ("familia", "family"),
                # Encounter 11-15
                ("cancelar", "to cancel"), ("cambiar", "to change"), ("modificar", "to modify"),
                ("política", "policy"), ("anticipación", "advance notice"), ("penalidad", "penalty"),
                ("menú", "menu"), ("especial", "special"), ("temporada", "season"),
                ("horario", "schedule"), ("abierto", "open"), ("cerrado", "closed"),
                ("temprano", "early"), ("tarde", "late"), ("mediodía", "noon"),
                # Encounter 16-20
                ("alérgico", "allergic"), ("restricción", "restriction"), ("dieta", "diet"),
                ("silla alta", "high chair"), ("niño", "child"), ("accesible", "accessible"),
                ("estacionamiento", "parking"), ("valet", "valet"), ("cerca", "nearby"),
                ("recomendación", "recommendation"), ("popular", "popular"), ("favorito", "favorite"),
                ("código de vestimenta", "dress code"), ("elegante", "elegant"), ("casual", "casual"),
                # Encounter 21-25
                ("lista de espera", "waiting list"), ("turno", "turn"), ("notificar", "to notify"),
                ("garantizar", "to guarantee"), ("asegurar", "to ensure"), ("compromiso", "commitment"),
                ("decoración", "decoration"), ("ambiente", "atmosphere"), ("música", "music"),
                ("chef", "chef"), ("especialidad", "specialty"), ("cocina", "cuisine"),
                ("vista", "view"), ("jardín", "garden"), ("fuente", "fountain"),
                # Encounter 26-30
                ("evento", "event"), ("banquete", "banquet"), ("catering", "catering"),
                ("presupuesto", "budget"), ("precio", "price"), ("por persona", "per person"),
                ("menú fijo", "fixed menu"), ("degustación", "tasting"), ("maridaje", "pairing"),
                ("brindis", "toast"), ("champán", "champagne"), ("vino", "wine"),
                ("pastel", "cake"), ("velas", "candles"), ("sorpresa", "surprise"),
                # Encounter 31-35
                ("florista", "florist"), ("arreglo", "arrangement"), ("decorar", "to decorate"),
                ("fotógrafo", "photographer"), ("recuerdo", "memory/souvenir"), ("momento", "moment"),
                ("invitado", "guest"), ("invitación", "invitation"), ("confirmar asistencia", "to RSVP"),
                ("lugar", "place/venue"), ("salón", "hall/room"), ("capacidad", "capacity"),
                ("sonido", "sound"), ("micrófono", "microphone"), ("bocina", "speaker"),
                # Encounter 36-40
                ("iluminación", "lighting"), ("vela", "candle"), ("romántico", "romantic"),
                ("mantel", "tablecloth"), ("vajilla", "dinnerware"), ("cristalería", "glassware"),
                ("servicio completo", "full service"), ("autoservicio", "self-service"), ("buffet", "buffet"),
                ("coordinador", "coordinator"), ("organizar", "to organize"), ("planificar", "to plan"),
                ("contrato", "contract"), ("depósito", "deposit"), ("anticipo", "advance payment"),
                # Encounter 41-45
                ("regulación", "regulation"), ("aforo", "capacity limit"), ("norma", "rule"),
                ("comentario", "review/comment"), ("calificación", "rating"), ("reseña", "review"),
                ("aplicación", "app"), ("en línea", "online"), ("sitio web", "website"),
                ("descuento", "discount"), ("promoción", "promotion"), ("cupón", "coupon"),
                ("experiencia", "experience"), ("inolvidable", "unforgettable"), ("único", "unique"),
                # Encounter 46-50
                ("agradecimiento", "gratitude"), ("satisfacción", "satisfaction"), ("fidelidad", "loyalty"),
                ("tradición", "tradition"), ("costumbre", "custom"), ("cultura", "culture"),
                ("certificado", "certificate"), ("reconocimiento", "recognition"), ("premio", "award"),
                ("recomendado", "recommended"), ("destacado", "outstanding"), ("excepcional", "exceptional"),
                ("gracias", "thank you"), ("hasta pronto", "see you soon"), ("bienvenido", "welcome"),
            ],
        },
        {
            "title": "Asking for the Bill",
            "goal": "Ask for the bill, review the charges, and pay",
            "word_prefix": "rest_bill",
            "words": [
                # Encounter 1-5
                ("cuenta", "bill/check"), ("pagar", "to pay"), ("total", "total"),
                ("efectivo", "cash"), ("tarjeta", "card"), ("cambio", "change"),
                ("propina", "tip"), ("servicio", "service"), ("incluido", "included"),
                ("precio", "price"), ("cobrar", "to charge"), ("correcto", "correct"),
                ("recibo", "receipt"), ("factura", "invoice"), ("imprimir", "to print"),
                # Encounter 6-10
                ("dividir", "to split"), ("separar", "to separate"), ("cada uno", "each one"),
                ("error", "error"), ("equivocación", "mistake"), ("revisar", "to review"),
                ("bebida", "drink"), ("comida", "food"), ("extra", "extra"),
                ("impuesto", "tax"), ("IVA", "VAT/sales tax"), ("porcentaje", "percentage"),
                ("descuento", "discount"), ("promoción", "promotion"), ("cupón", "coupon"),
                # Encounter 11-15
                ("débito", "debit"), ("crédito", "credit"), ("terminal", "card terminal"),
                ("contactless", "contactless"), ("chip", "chip"), ("firma", "signature"),
                ("propina sugerida", "suggested tip"), ("voluntario", "voluntary"), ("obligatorio", "mandatory"),
                ("mesa", "table"), ("número", "number"), ("identificar", "to identify"),
                ("cerrar", "to close"), ("saldar", "to pay off"), ("liquidar", "to settle"),
                # Encounter 16-20
                ("desglose", "breakdown"), ("detalle", "detail"), ("concepto", "item/concept"),
                ("entrada", "appetizer"), ("plato fuerte", "main course"), ("postre", "dessert"),
                ("bebida alcohólica", "alcoholic drink"), ("sin alcohol", "non-alcoholic"), ("botella", "bottle"),
                ("copa", "glass/drink"), ("ronda", "round"), ("adicional", "additional"),
                ("cubierto", "cover charge"), ("cargo", "charge"), ("suplemento", "supplement"),
                # Encounter 21-25
                ("transferencia", "transfer"), ("aplicación", "app"), ("QR", "QR code"),
                ("voucher", "voucher"), ("vale", "voucher/coupon"), ("canjear", "to redeem"),
                ("puntos", "points"), ("recompensa", "reward"), ("acumular", "to accumulate"),
                ("moneda", "currency"), ("dólar", "dollar"), ("peso", "peso"),
                ("grupo", "group"), ("individual", "individual"), ("compartir", "to share"),
                # Encounter 26-30
                ("sobrar", "to be left over"), ("devolver", "to return"), ("sobrante", "leftover/surplus"),
                ("caja", "cash register"), ("cajero", "cashier"), ("mostrador", "counter"),
                ("recibo digital", "digital receipt"), ("correo", "email"), ("enviar", "to send"),
                ("fiscal", "fiscal/tax"), ("RFC", "tax ID"), ("datos fiscales", "tax details"),
                ("llevar", "to take away"), ("empacar", "to pack"), ("contenedor", "container"),
                # Encounter 31-35
                ("disputa", "dispute"), ("aclarar", "to clarify"), ("gerente", "manager"),
                ("doble cargo", "double charge"), ("cancelar", "to cancel"), ("reembolso", "refund"),
                ("comprobante", "proof"), ("transacción", "transaction"), ("autorización", "authorization"),
                ("plataforma", "platform"), ("en línea", "online"), ("reservación", "reservation"),
                ("membresía", "membership"), ("ventaja", "advantage"), ("beneficio", "benefit"),
                # Encounter 36-40
                ("regalo", "gift"), ("invitar", "to treat/invite"), ("cortesía", "courtesy/complimentary"),
                ("celebración", "celebration"), ("especial", "special"), ("ocasión", "occasion"),
                ("vino", "wine"), ("copa de vino", "glass of wine"), ("descorche", "corkage fee"),
                ("degustación", "tasting"), ("menú", "menu"), ("precio fijo", "fixed price"),
                ("todo incluido", "all-inclusive"), ("buffet", "buffet"), ("ilimitado", "unlimited"),
                # Encounter 41-45
                ("comisión", "commission"), ("cargo por servicio", "service charge"), ("automático", "automatic"),
                ("contabilidad", "accounting"), ("registro", "record"), ("archivos", "files"),
                ("reglamento", "regulation"), ("ley", "law"), ("consumidor", "consumer"),
                ("queja", "complaint"), ("sugerencia", "suggestion"), ("buzón", "mailbox/suggestion box"),
                ("deducible", "deductible"), ("gasto", "expense"), ("negocio", "business"),
                # Encounter 46-50
                ("satisfecho", "satisfied"), ("excelente", "excellent"), ("calidad", "quality"),
                ("agradecido", "grateful"), ("atención", "attention"), ("amable", "kind"),
                ("volver", "to come back"), ("recomendar", "to recommend"), ("favorito", "favorite"),
                ("despedida", "farewell"), ("buenas noches", "good evening"), ("hasta luego", "see you later"),
                ("gracias", "thank you"), ("buen provecho", "enjoy your meal"), ("felicidades", "congratulations"),
            ],
        },
    ],
    "small_talk": [
        {
            "title": "Meeting a Neighbor",
            "goal": "Have a friendly conversation with your new neighbor",
            "word_prefix": "talk",
            "words": [
                # Encounter 1-5
                ("hola", "hello"), ("vecino", "neighbor"), ("mucho gusto", "nice to meet you"),
                ("nombre", "name"), ("vivir", "to live"), ("casa", "house"),
                ("familia", "family"), ("trabajo", "work/job"), ("país", "country"),
                ("tiempo", "weather/time"), ("bonito", "nice/pretty"), ("tranquilo", "quiet/calm"),
                ("nuevo", "new"), ("mudarse", "to move"), ("barrio", "neighborhood"),
                # Encounter 6-10
                ("esposa", "wife"), ("esposo", "husband"), ("hijo", "son/child"),
                ("mascota", "pet"), ("perro", "dog"), ("gato", "cat"),
                ("jardín", "garden"), ("planta", "plant"), ("flor", "flower"),
                ("calle", "street"), ("parque", "park"), ("tienda", "store"),
                ("mañana", "morning"), ("tarde", "afternoon"), ("noche", "evening"),
                # Encounter 11-15
                ("cocinar", "to cook"), ("comida", "food"), ("receta", "recipe"),
                ("deporte", "sport"), ("caminar", "to walk"), ("correr", "to run"),
                ("música", "music"), ("película", "movie"), ("libro", "book"),
                ("fiesta", "party"), ("invitar", "to invite"), ("celebrar", "to celebrate"),
                ("ayudar", "to help"), ("favor", "favor"), ("necesitar", "to need"),
                # Encounter 16-20
                ("supermercado", "supermarket"), ("mercado", "market"), ("restaurante", "restaurant"),
                ("escuela", "school"), ("iglesia", "church"), ("hospital", "hospital"),
                ("taxi", "taxi"), ("autobús", "bus"), ("estación", "station"),
                ("seguro", "safe"), ("peligroso", "dangerous"), ("cuidado", "careful"),
                ("ruido", "noise"), ("silencio", "quiet"), ("respetar", "to respect"),
                # Encounter 21-25
                ("basura", "trash"), ("reciclar", "to recycle"), ("limpiar", "to clean"),
                ("estacionar", "to park"), ("carro", "car"), ("bicicleta", "bicycle"),
                ("llave", "key"), ("puerta", "door"), ("cerrar", "to close/lock"),
                ("electricidad", "electricity"), ("agua", "water"), ("gas", "gas"),
                ("internet", "internet"), ("señal", "signal"), ("compartir", "to share"),
                # Encounter 26-30
                ("reunión", "meeting/gathering"), ("comunidad", "community"), ("asociación", "association"),
                ("problema", "problem"), ("solución", "solution"), ("juntos", "together"),
                ("renta", "rent"), ("propietario", "landlord"), ("inquilino", "tenant"),
                ("mantenimiento", "maintenance"), ("reparar", "to repair"), ("reportar", "to report"),
                ("reglas", "rules"), ("convivencia", "coexistence"), ("acuerdo", "agreement"),
                # Encounter 31-35
                ("cumpleaños", "birthday"), ("regalo", "gift"), ("felicitar", "to congratulate"),
                ("vacaciones", "vacation"), ("viajar", "to travel"), ("playa", "beach"),
                ("tradición", "tradition"), ("costumbre", "custom"), ("cultura", "culture"),
                ("idioma", "language"), ("aprender", "to learn"), ("practicar", "to practice"),
                ("amable", "kind"), ("generoso", "generous"), ("simpático", "nice/friendly"),
                # Encounter 36-40
                ("consejo", "advice"), ("experiencia", "experience"), ("recomendación", "recommendation"),
                ("doctor", "doctor"), ("dentista", "dentist"), ("farmacia", "pharmacy"),
                ("clima", "climate"), ("calor", "heat"), ("frío", "cold"),
                ("lluvia", "rain"), ("sol", "sun"), ("nublado", "cloudy"),
                ("feriado", "holiday"), ("celebración", "celebration"), ("descanso", "rest"),
                # Encounter 41-45
                ("voluntario", "volunteer"), ("organización", "organization"), ("participar", "to participate"),
                ("nostalgia", "nostalgia"), ("extrañar", "to miss"), ("recuerdo", "memory"),
                ("jubilación", "retirement"), ("edad", "age"), ("joven", "young"),
                ("nieto", "grandchild"), ("abuelo", "grandfather"), ("generación", "generation"),
                ("fotografía", "photography"), ("álbum", "album"), ("momento", "moment"),
                # Encounter 46-50
                ("confianza", "trust"), ("amistad", "friendship"), ("respeto", "respect"),
                ("despedida", "farewell"), ("viaje", "trip"), ("suerte", "luck"),
                ("bienvenida", "welcome"), ("hogar", "home"), ("feliz", "happy"),
                ("agradecido", "grateful"), ("bendición", "blessing"), ("paz", "peace"),
                ("cuídate", "take care"), ("hasta luego", "see you later"), ("buena suerte", "good luck"),
            ],
        },
    ],
}

# --- Generate ENCOUNTER_WORDS, SITUATIONS, SITUATION_WORDS from compact data ---

ENCOUNTER_WORDS: dict[str, list[dict]] = {}
SITUATIONS: list[dict] = []
SITUATION_WORDS: list[dict] = []

# Order index base per animation_type (ensures globally unique order_index)
_ANIM_ORDER = list(_SUB_SITUATIONS.keys())

for category, sub_list in _SUB_SITUATIONS.items():
    category_words = []
    anim_base = _ANIM_ORDER.index(category) * 200  # 200 slots per animation type

    for sub_idx, sub in enumerate(sub_list):
        prefix = sub["word_prefix"]
        words = sub["words"]

        for enc_num in range(1, 51):
            # Word indices: 3 words per encounter
            base = (enc_num - 1) * 3
            w1 = words[base]
            w2 = words[base + 1]
            w3 = words[base + 2]

            # Each situation gets encounter_number 1-50 independently
            # Situation ID uses word_prefix for uniqueness (e.g., bank_open_1, bank_wire_1)
            situation_id = f"{prefix}_{enc_num}"

            # Encounter words
            for pos, (spanish, english) in enumerate([(w1[0], w1[1]), (w2[0], w2[1]), (w3[0], w3[1])], 1):
                word_id = f"enc_{prefix}_{(enc_num - 1) * 3 + pos:03d}"
                category_words.append({
                    "id": word_id,
                    "spanish": spanish,
                    "english": english,
                })
                SITUATION_WORDS.append({
                    "situation_id": situation_id,
                    "word_id": word_id,
                    "position": pos,
                })

            # Situation
            SITUATIONS.append({
                "id": situation_id,
                "title": sub["title"],
                "animation_type": category,
                "encounter_number": enc_num,
                "order_index": anim_base + sub_idx * 50 + enc_num,
                "is_free": enc_num <= 5,  # First 5 encounters per sub-situation are free
                "goal": sub["goal"],
            })

    ENCOUNTER_WORDS[category] = category_words
