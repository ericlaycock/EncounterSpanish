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
                ("abordaje", "boarding process"), ("vuelo", "flight"), ("boleto", "ticket"),
                ("aterrizaje", "landing"), ("mostrador", "counter"), ("agente", "agent"),
                ("asiento", "seat"), ("aéreo", "aerial"), ("terminal", "terminal"),
                ("maleta", "suitcase"), ("embarque", "boarding"), ("salida", "departure"),
                ("llegada", "arrival"), ("destino", "destination"), ("fila", "line/queue"),
                # Encounter 6-10
                ("ventanilla", "window seat"), ("vuelo directo", "direct flight"), ("reserva", "reservation"),
                ("demora", "delay"), ("tráfico aéreo", "air traffic"), ("zona", "zone"),
                ("documento", "document"), ("identificación", "identification"), ("nacionalidad", "nationality"),
                ("seguridad", "security"), ("azafata", "flight attendant"), ("registro", "check-in"),
                ("directo", "direct"), ("escala", "layover"), ("conexión", "connection"),
                # Encounter 11-15
                ("pase de abordar", "boarding pass"), ("imprimir", "to print"), ("escanear", "to scan"),
                ("disponible", "available"), ("asignado", "assigned"), ("seleccionar", "to select"),
                ("equipaje de mano", "carry-on"), ("hangar", "hangar"), ("plataforma", "platform"),
                ("sobrepeso", "overweight"), ("límite", "limit"), ("restricción", "restriction"),
                ("facturar", "to check in luggage"), ("despacho", "dispatch"), ("tarifa", "fare"),
                # Encounter 16-20
                ("aerolínea", "airline"), ("pasajero", "passenger"), ("tripulación", "crew"),
                ("primera clase", "first class"), ("económica", "economy"), ("preferente", "preferred"),
                ("ida", "one-way"), ("vuelta", "return"), ("redondo", "round-trip"),
                ("cinturón", "seatbelt"), ("abrocharse", "to fasten"), ("documentación", "documentation"),
                ("cabina", "cabin"), ("compartimento", "compartment"), ("superior", "overhead"),
                # Encounter 21-25
                ("aterrizar", "to land"), ("despegar", "to take off"), ("pista", "runway"),
                ("auxiliar", "flight attendant"), ("portaequipaje", "luggage rack"), ("asistencia", "assistance"),
                ("sobrevolado", "overflown"), ("declarar", "to declare"), ("inmigración", "immigration"),
                ("transatlántico", "transatlantic"), ("llenar", "to fill out"), ("firmar", "to sign"),
                ("recoger", "to pick up"), ("reclamo", "claim"), ("transcontinental", "transcontinental"),
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
                ("horario", "schedule"), ("puntual", "on time"), ("bienvenida a bordo", "welcome aboard"),
                ("clase ejecutiva", "business class"), ("reclinable", "reclining"), ("despegue", "takeoff"),
                # Encounter 36-40
                ("frágil", "fragile"), ("especial", "special"), ("delicado", "delicate"),
                ("transbordo", "transfer"), ("mapa", "map"), ("aduanal", "customs-related"),
                ("sala de espera", "waiting room"), ("anuncio", "announcement"), ("altavoz", "loudspeaker"),
                ("fumigación", "fumigation"), ("efectivo", "cash"), ("escáner corporal", "body scanner"),
                ("piloto", "pilot"), ("copiloto", "co-pilot"), ("banda transportadora", "conveyor belt"),
                # Encounter 41-45
                ("turbulencia", "turbulence"), ("altitud", "altitude"), ("presión", "pressure"),
                ("máscara", "mask"), ("instrucciones", "instructions"), ("recogida", "pickup/collection"),
                ("regulación", "regulation"), ("norma", "rule"), ("vigente", "in effect"),
                ("tránsito", "transit"), ("lounge", "lounge"), ("acceso", "access"),
                ("equipaje perdido", "lost luggage"), ("reporte", "report"), ("oficina", "office"),
                # Encounter 46-50
                ("sobrecargo", "surcharge"), ("cargo", "charge"), ("adicional", "additional"),
                ("pasarela", "jet bridge"), ("andén", "boarding platform"), ("entrada", "entry"),
                ("zona franca", "duty-free zone"), ("altoparlante", "speaker/PA"), ("taquilla", "ticket counter"),
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
                # Encounter 1-5 (basic essentials)
                ("apertura", "opening"), ("banco", "bank"), ("abrir", "to open"),
                ("depósito inicial", "initial deposit"), ("depositar", "to deposit"), ("saldo", "balance"),
                ("fondos", "funds"), ("boleta", "deposit slip"), ("giro", "money order"),
                ("tarjeta", "card"), ("débito", "debit"), ("crédito", "credit"),
                ("operación", "transaction"), ("corriente", "checking"), ("fiador", "guarantor"),
                # Encounter 6-10
                ("cajero", "teller"), ("aval", "endorser/guarantor"), ("turno", "turn/number"),
                ("garante", "guarantor"), ("cuentahabiente", "account holder"), ("datos", "data/details"),
                ("módulo", "service module"), ("dirección", "address"), ("teléfono", "phone number"),
                ("requisito", "requirement"), ("comprobante", "proof/receipt"), ("domicilio", "address/residence"),
                ("clave", "PIN/password"), ("contraseña", "password"), ("fila de espera", "waiting line"),
                # Encounter 11-15
                ("papelería", "paperwork"), ("cédula", "ID card"), ("acreditación", "accreditation"),
                ("huella digital", "fingerprint"), ("tasa", "rate"), ("porcentaje", "percentage"),
                ("plazo", "term/period"), ("fijo", "fixed"), ("variable", "variable"),
                ("comisión", "commission/fee"), ("cobrar", "to charge"), ("mensual", "monthly"),
                ("estado de cuenta", "account statement"), ("biométrico", "biometric"), ("consultar", "to check"),
                # Encounter 16-20
                ("transferencia", "transfer"), ("enviar", "to send"), ("código postal", "zip code"),
                ("beneficiario", "beneficiary"), ("autorizar", "to authorize"), ("RFC", "tax ID"),
                ("retiro", "withdrawal"), ("retirar", "to withdraw"), ("CURP", "national ID number"),
                ("cheque", "check"), ("chequera", "checkbook"), ("endosar", "to endorse"),
                ("banca en línea", "online banking"), ("aplicación", "app"), ("mancomunado", "joint"),
                # Encounter 21-25
                ("préstamo", "loan"), ("solicitar", "to request"), ("aprobar", "to approve"),
                ("pago", "payment"), ("cuota", "installment"), ("individual", "individual"),
                ("cancelar", "to cancel"), ("cerrar", "to close"), ("motivo", "reason"),
                ("extracto", "statement"), ("historial", "history"), ("persona física", "individual person"),
                ("número de cuenta", "account number"), ("titular", "account holder"), ("cotitular", "co-holder"),
                # Encounter 26-30
                ("dígito", "digit"), ("cláusula", "clause"), ("NIP", "PIN number"),
                ("cliente", "client"), ("cifrado", "encrypted"), ("existente", "existing"),
                ("ventanilla de cajas", "teller window"), ("lobby", "lobby"), ("extranjera", "foreign"),
                ("ejecutivo", "executive/officer"), ("protección", "protection"), ("cobertura", "coverage"),
                ("notificación", "notification"), ("alerta", "alert"), ("mensaje", "message"),
                # Encounter 31-35
                ("sobregiro", "overdraft"), ("penalidad", "penalty"), ("recargo", "surcharge"),
                ("asesoramiento", "advisory"), ("orientación", "guidance"), ("rendimiento", "yield/return"),
                ("fideicomiso", "trust"), ("patrimonio", "assets"), ("herencia", "inheritance"),
                ("poder notarial", "power of attorney"), ("apoderado", "authorized agent"), ("representante", "representative"),
                ("nómina", "payroll"), ("domiciliar", "to set up direct deposit"), ("automático", "automatic"),
                # Encounter 36-40
                ("auditoría", "audit"), ("verificar", "to verify"), ("cumplimiento", "compliance"),
                ("expedición", "issuance"), ("plástico", "card/plastic"), ("renovar", "to renew"),
                ("sucursal principal", "main branch"), ("gerente", "manager"), ("cita", "appointment"),
                ("bóveda", "vault"), ("caja fuerte", "safe deposit box"), ("estado financiero", "financial statement"),
                ("transacción", "transaction"), ("retención", "withholding"), ("declaración", "declaration"),
                # Encounter 41-45
                ("cuenta conjunta", "joint account"), ("mancomunada", "joint/shared"), ("separada", "separate"),
                ("tarjeta adicional", "additional card"), ("operación bancaria", "banking operation"), ("aumentar", "to increase"),
                ("fraude", "fraud"), ("bloquear", "to block"), ("reportar", "to report"),
                ("token", "token"), ("autenticación", "authentication"), ("verificación", "verification"),
                ("divisa", "foreign currency"), ("póliza", "policy"), ("cotización", "quote"),
                # Encounter 46-50
                ("corresponsal", "correspondent bank"), ("intermediario", "intermediary"), ("red", "network"),
                ("respaldo", "backing/support"), ("normativa", "policy"), ("activo", "asset"),
                ("cuentas por pagar", "accounts payable"), ("constancia", "proof/certificate"), ("rédito", "return/interest"),
                ("asesor", "advisor"), ("consultoría", "consulting"), ("planificación", "planning"),
                ("bienvenido", "welcome"), ("servicio al cliente", "customer service"), ("satisfacción", "satisfaction"),
            ],
        },
        {
            "title": "Wire Transfer",
            "goal": "Complete a wire transfer by giving the teller the recipient details",
            "word_prefix": "bank_wire",
            "words": [
                # Encounter 1-5 (basic essentials)
                ("giro bancario", "bank draft"), ("remesa", "remittance"), ("canalizar", "to channel"),
                ("depositante", "depositor"), ("receptor bancario", "bank receiver"), ("acreditado", "credited party"),
                ("monto", "amount"), ("cifra", "figure/amount"), ("receptor", "receiving"),
                ("institución", "institution"), ("girado", "drawn on"), ("referencia", "reference"),
                ("titular de cuenta", "account holder"), ("dígitos", "digits"), ("clave de rastreo", "tracking code"),
                # Encounter 6-10
                ("validar", "to validate"), ("costo", "cost"), ("información bancaria", "bank info"),
                ("cotejar", "to compare/verify"), ("descontar", "to deduct"), ("doméstico", "domestic"),
                ("foráneo", "foreign"), ("inmediato", "immediate"), ("nación", "nation"),
                ("lapso", "timespan"), ("instantáneo", "instant"), ("tardanza", "tardiness"),
                ("constancia de pago", "payment receipt"), ("justificante", "voucher"), ("suficiente", "sufficient"),
                # Encounter 11-15
                ("código SWIFT", "SWIFT code"), ("copiar", "to copy"), ("interbancario", "interbank"),
                ("bastante", "enough"), ("dólar", "dollar"), ("clave bancaria", "bank code"),
                ("tipo de cambio", "exchange rate"), ("conversión", "conversion"), ("equivalente", "equivalent"),
                ("llave interbancaria", "interbank key"), ("red bancaria", "bank network"), ("divisa extranjera", "foreign currency"),
                ("billete verde", "greenback"), ("máximo", "maximum"), ("moneda local", "local currency"),
                # Encounter 16-20
                ("programar", "to schedule"), ("fecha", "date"), ("recurrente", "recurring"),
                ("paridad cambiaria", "exchange parity"), ("modificar", "to modify"), ("corregir", "to correct"),
                ("tasa de cambio", "exchange rate"), ("equiparable", "comparable"), ("solicitud de envío", "send request"),
                ("rellenar", "to fill in"), ("rubricar", "to initial/sign"), ("tope", "cap"),
                ("origen", "origin"), ("emisor", "sender/issuer"), ("ordenante", "originator"),
                # Encounter 21-25
                ("acreditar", "to credit"), ("debitar", "to debit"), ("procesar", "to process"),
                ("cifra máxima", "maximum amount"), ("pendiente", "pending"), ("completado", "completed"),
                ("rastrear", "to track"), ("seguimiento", "tracking"), ("código", "code"),
                ("cotidiano", "daily/everyday"), ("plaza", "city/location"), ("agendar", "to schedule"),
                ("urgente", "urgent"), ("prioritario", "priority"), ("express", "express"),
                # Encounter 26-30
                ("anular", "to void"), ("editar", "to edit"), ("enmendar", "to amend"),
                ("aviso", "notice"), ("correo electrónico", "email"), ("texto", "text message"),
                ("error", "error"), ("rechazar", "to reject"), ("clave secreta", "secret code"),
                ("procedencia", "origin/source"), ("insuficiente", "insufficient"), ("cubrir", "to cover"),
                ("lote", "batch"), ("múltiple", "multiple"), ("masivo", "bulk"),
                # Encounter 31-35
                ("solicitante", "applicant"), ("abonar", "to credit"), ("ruta", "route"),
                ("demora bancaria", "bank delay"), ("hábil", "business (day)"), ("calendario", "calendar"),
                ("reversar", "to reverse"), ("devolución", "return/refund"), ("original", "original"),
                ("duplicado", "duplicate"), ("detectar", "to detect"), ("prevenir", "to prevent"),
                ("IBAN", "IBAN"), ("cuenta CLABE", "CLABE account"), ("formato", "format"),
                # Encounter 36-40
                ("beneficiario final", "ultimate beneficiary"), ("cargar", "to charge"), ("concepto", "concept/description"),
                ("tramitar", "to process"), ("en espera", "on hold"), ("proveedor", "supplier"),
                ("finalizado", "finalized"), ("empleado", "employee"), ("salario", "salary"),
                ("alquiler", "rent"), ("hipoteca", "mortgage"), ("mensualidad", "monthly payment"),
                ("localizar", "to locate"), ("monitorear", "to monitor"), ("portafolio", "portfolio"),
                # Encounter 41-45
                ("lavado de dinero", "money laundering"), ("prevención", "prevention"), ("referencia bancaria", "bank reference"),
                ("tratado", "treaty"), ("bilateral", "bilateral"), ("filial", "subsidiary"),
                ("domicilio bancario", "bank address"), ("apremiante", "pressing"), ("documentar", "to document"),
                ("digital", "digital"), ("preferencial", "preferential"), ("veloz", "fast"),
                ("blockchain", "blockchain"), ("cripto", "crypto"), ("billetera digital", "digital wallet"),
                # Encounter 46-50
                ("norma bancaria", "banking rule"), ("fiduciario", "fiduciary"), ("garantía", "guarantee"),
                ("penalización", "penalty"), ("reglamento", "rules"), ("sanción", "sanction"),
                ("disputa", "dispute"), ("acatar", "to comply with"), ("resolución", "resolution"),
                ("exitoso", "successful"), ("recibido", "received"), ("deducción", "deduction"),
                ("gracias", "thank you"), ("finalizar", "to finalize"), ("completar", "to complete"),
            ],
        },
        {
            "title": "Currency Exchange",
            "goal": "Exchange your currency by negotiating with the teller",
            "word_prefix": "bank_exchange",
            "words": [
                # Encounter 1-5 (basic essentials)
                ("trocar", "to barter"), ("capital", "capital/money"), ("dólar americano", "US dollar"),
                ("moneda mexicana", "Mexican currency"), ("moneda europea", "European currency"), ("euro", "euro"),
                ("cotización del día", "today's rate"), ("tarifa cambiaria", "exchange fee"), ("jornada", "trading day"),
                ("comprar", "to buy"), ("vender", "to sell"), ("adquirir", "to acquire"),
                ("enajenar", "to sell/dispose"), ("billete", "banknote"), ("centavo", "cent/coin"),
                # Encounter 6-10
                ("billetes", "banknotes/bills"), ("papel moneda", "paper money"), ("gratis", "free"),
                ("casa de cambio", "exchange office"), ("centésimo", "hundredth/cent"), ("cargo por cambio", "exchange charge"),
                ("sin cargo", "no charge"), ("bureau de cambio", "exchange bureau"), ("mostrar", "to show"),
                ("módulo cambiario", "exchange counter"), ("operador", "operator"), ("guardar", "to keep"),
                ("credencial", "credential"), ("cuánto", "how much"), ("documento de viaje", "travel document"),
                # Encounter 11-15
                ("exhibir", "to show/display"), ("peor", "worse"), ("comparar", "to compare"),
                ("boleta de cambio", "exchange slip"), ("paralelo", "parallel/unofficial"), ("conservar", "to keep/preserve"),
                ("subir", "to go up"), ("bajar", "to go down"), ("estable", "stable"),
                ("denominación", "denomination"), ("suma", "sum"), ("cuántos", "how many"),
                ("cambio exacto", "exact change"), ("suelto", "loose change"), ("feria", "small change"),
                # Encounter 16-20
                ("cheque de viajero", "traveler's check"), ("monto total", "total amount"), ("canjear", "to cash/redeem"),
                ("inferior", "worse/lower"), ("contrastar", "to contrast"), ("mínimo", "minimum"),
                ("autorizado", "authorized"), ("informal", "informal"), ("local", "local"),
                ("negociar", "to negotiate"), ("plaza cambiaria", "exchange market"), ("incrementar", "to increase"),
                ("libra", "pound"), ("yen", "yen"), ("franco", "franc"),
                # Encounter 21-25
                ("fluctuar", "to fluctuate"), ("variación", "variation"), ("diferencia", "difference"),
                ("disminuir", "to decrease"), ("pérdida", "loss"), ("margen", "margin"),
                ("constante", "constant"), ("billete grande", "large bill"), ("billete chico", "small bill"),
                ("banco central", "central bank"), ("billete menudo", "small denomination"), ("cambio justo", "fair change"),
                ("turista", "tourist"), ("viajero", "traveler"), ("residente", "resident"),
                # Encounter 26-30
                ("transferir", "to transfer"), ("moneda fraccionaria", "fractional currency"), ("vuelto", "change/remainder"),
                ("cheque viajero", "traveler's check"), ("cobrar cheque", "to cash a check"), ("máxima cantidad", "maximum quantity"),
                ("cantidad mínima", "minimum quantity"), ("cajero automático", "ATM"), ("moneda foránea", "foreign coin"),
                ("de fuera", "from abroad"), ("proteger", "to protect"), ("cuidar", "to take care"),
                ("falsificado", "counterfeit"), ("de aquí", "from here"), ("auténtico", "authentic"),
                # Encounter 31-35
                ("pactar", "to agree"), ("convenir", "to agree/suit"), ("actualizar", "to update"),
                ("libra esterlina", "pound sterling"), ("yen japonés", "Japanese yen"), ("cerrado", "closed"),
                ("franco suizo", "Swiss franc"), ("oscilar", "to oscillate"), ("movimiento cambiario", "exchange movement"),
                ("brecha", "gap"), ("utilidad", "profit/utility"), ("metal", "metal"),
                ("inflación", "inflation"), ("devaluación", "devaluation"), ("revaluación", "revaluation"),
                # Encounter 36-40
                ("spread", "spread"), ("diferencial", "differential"), ("quebranto", "loss/damage"),
                ("diferencia cambiaria", "exchange difference"), ("bitcoin", "bitcoin"), ("papel oficial", "official document"),
                ("copia original", "original copy"), ("banco emisor", "issuing bank"), ("exento", "exempt"),
                ("norma cambiaria", "exchange regulation"), ("facultar", "to authorize"), ("límite de efectivo", "cash limit"),
                ("visitante", "visitor"), ("habitante", "resident/inhabitant"), ("traspasar", "to transfer"),
                # Encounter 41-45
                ("cuenta destino", "destination account"), ("tarjeta bancaria", "bank card"), ("tarjeta de viaje", "travel card"),
                ("sacar dinero", "to withdraw"), ("dispensador", "dispenser"), ("accesible", "accessible"),
                ("reservar", "to reserve"), ("separar", "to set aside"), ("apartar", "to put aside"),
                ("resguardado", "safe/guarded"), ("postal", "postal"), ("telegráfico", "telegraphic"),
                ("paridad", "parity"), ("equilibrio", "equilibrium"), ("balanza", "balance"),
                # Encounter 46-50
                ("especulación", "speculation"), ("blindar", "to protect"), ("custodiar", "to guard"),
                ("billete falso", "counterfeit bill"), ("futuro", "futures"), ("derivado", "derivative"),
                ("regulador", "regulator"), ("supervisor", "supervisor"), ("legítimo", "legitimate"),
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
                # Encounter 1-5 (basic essentials)
                ("talla", "size"), ("probador", "fitting room"), ("descuento", "discount"),
                ("camisa", "shirt"), ("pantalón", "pants"), ("zapatos", "shoes"),
                ("prenda", "garment"), ("color", "color"), ("vestidor", "dressing room"),
                ("rebaja", "markdown"), ("playera", "t-shirt"), ("mediano", "medium"),
                ("buscar", "to look for"), ("bermuda", "shorts"), ("sandalia", "sandal"),
                # Encounter 6-10
                ("probarse", "to try on"), ("quedar", "to fit"), ("tono", "tone/shade"),
                ("ajustado", "tight"), ("flojo", "loose"), ("cómodo", "comfortable"),
                ("vestido", "dress"), ("falda", "skirt"), ("blusa", "blouse"),
                ("manga", "sleeve"), ("boutique", "boutique"), ("holgado", "roomy"),
                ("reducido", "small/reduced"), ("tela", "fabric"), ("intermedio", "medium/intermediate"),
                # Encounter 11-15
                ("devolver", "to return"), ("explorar", "to explore"), ("requerir", "to require"),
                ("medirse", "to try on (oneself)"), ("oferta", "offer/deal"), ("temporada", "season"),
                ("cremallera", "zipper"), ("botón", "button"), ("sentar", "to fit/suit"),
                ("ancho", "wide"), ("estrecho", "narrow"), ("entallado", "fitted"),
                ("adecuado", "suitable"), ("ceñido", "tight-fitting"), ("azul", "blue"),
                # Encounter 16-20
                ("agradable", "comfortable/pleasant"), ("maxi", "maxi dress"), ("gris", "gray"),
                ("estampado", "printed/patterned"), ("liso", "plain"), ("rayas", "stripes"),
                ("elegante", "elegant"), ("casual", "casual"), ("formal", "formal"),
                ("minifalda", "mini skirt"), ("corbata", "tie"), ("pañuelo", "scarf/handkerchief"),
                ("marca", "brand"), ("camiseta", "t-shirt/blouse"), ("resistente", "durable"),
                # Encounter 21-25
                ("abrigo", "coat"), ("chaqueta", "jacket"), ("suéter", "sweater"),
                ("puño largo", "long sleeve"), ("calcetín", "sock"), ("media", "stocking"),
                ("tacón", "heel"), ("suela", "sole"), ("extenso", "long/extended"),
                ("joyería", "jewelry"), ("anillo", "ring"), ("collar", "necklace"),
                ("gafas", "glasses"), ("sombrero", "hat"), ("gorra", "cap"),
                # Encounter 26-30
                ("lavar", "to wash"), ("planchar", "to iron"), ("secar", "to dry"),
                ("coser", "to sew"), ("arreglar", "to alter/fix"), ("sastre", "tailor"),
                ("diseño", "design"), ("breve", "short/brief"), ("colección", "collection"),
                ("probador ocupado", "fitting room occupied"), ("fibra de algodón", "cotton fiber"), ("tejido", "woven fabric"),
                ("talla única", "one size"), ("extra grande", "extra large"), ("extra pequeño", "extra small"),
                # Encounter 31-35
                ("componente", "component"), ("reintegrar", "to return/refund"), ("lino", "linen"),
                ("poliéster", "polyester"), ("sintético", "synthetic"), ("elástico", "elastic/stretchy"),
                ("moda", "fashion"), ("tendencia", "trend"), ("estilo", "style"),
                ("traje", "suit"), ("esmoquin", "tuxedo"), ("intercambiar", "to exchange"),
                ("impermeable", "waterproof"), ("térmico", "thermal"), ("ligero", "lightweight"),
                # Encounter 36-40
                ("bordado", "embroidered"), ("encaje", "lace"), ("flecos", "fringe"),
                ("solapa", "lapel"), ("puño", "cuff"), ("comprobante de compra", "proof of purchase"),
                ("cierre", "fastener/closure"), ("broche", "clasp"), ("hebilla", "buckle"),
                ("planchado", "pressed"), ("arrugado", "wrinkled"), ("manchado", "stained"),
                ("guardarropa", "wardrobe"), ("percha", "hanger"), ("liquidación", "clearance"),
                # Encounter 41-45
                ("confección", "tailoring"), ("ganga", "bargain"), ("cinta métrica", "measuring tape"),
                ("patronaje", "pattern-making"), ("molde", "pattern/mold"), ("cortar", "to cut"),
                ("exhibición", "display"), ("época de rebajas", "sale season"), ("maniquí", "mannequin"),
                ("exclusivo", "exclusive"), ("limitado", "limited"), ("edición", "edition"),
                ("ecológico", "eco-friendly"), ("sostenible", "sustainable"), ("reciclado", "recycled"),
                # Encounter 46-50
                ("alta costura", "haute couture"), ("cierre relámpago", "zipper"), ("diseñador", "designer"),
                ("personalizado", "customized"), ("ojal", "buttonhole"), ("hecho a mano", "handmade"),
                ("compartimiento", "compartment"), ("angosto", "narrow/tight"), ("a la medida", "tailored"),
                ("celeste", "sky blue"), ("perfecto", "perfect"), ("ideal", "ideal"),
                ("carmesí", "crimson"), ("compra", "purchase"), ("bolsa", "bag"),
            ],
        },
    ],
    "contractor": [
        {
            "title": "Hiring a Plumber",
            "goal": "Hire a plumber by describing the problem and agreeing on a price",
            "word_prefix": "contr",
            "words": [
                # Encounter 1-5 (basic essentials)
                ("plomero", "plumber"), ("fontanero", "plumber"), ("desperfecto", "defect"),
                ("componer", "to fix"), ("tubo", "pipe"), ("fuga", "leak"),
                ("conducto", "conduit"), ("goteo", "drip"), ("lavabo", "sink"),
                ("sanitario", "bathroom/toilet"), ("área de cocina", "kitchen area"), ("fregadero", "kitchen sink"),
                ("de emergencia", "emergency"), ("precisar", "to need"), ("ayuda", "help"),
                # Encounter 6-10
                ("socorro", "help/aid"), ("grifo de agua", "water tap"), ("gotear", "to drip"),
                ("cañería", "plumbing/pipes"), ("drenaje", "drain"), ("tapado", "clogged"),
                ("reparar", "to repair"), ("instalar", "to install"), ("canilla", "tap/spigot"),
                ("escurrir", "to drip/drain"), ("pieza", "part/piece"), ("red de tuberías", "pipe network"),
                ("desagüe", "drain"), ("obstruido", "blocked"), ("cuándo", "when"),
                # Encounter 11-15
                ("inodoro", "toilet"), ("regadera", "shower"), ("tina", "bathtub"),
                ("calentador", "water heater"), ("restaurar", "to restore"), ("montar", "to install/mount"),
                ("roto", "broken"), ("dañado", "damaged"), ("reemplazar", "to replace"),
                ("insumo", "supply"), ("utensilio", "utensil/tool"), ("agenda de trabajo", "work schedule"),
                ("en qué momento", "at what time"), ("duración", "duration"), ("excusado", "toilet"),
                # Encounter 16-20
                ("mano de obra", "labor"), ("ducha", "shower"), ("bañera", "bathtub"),
                ("boiler", "boiler"), ("depósito de agua", "water tank"), ("flujo", "flow"),
                ("averiado", "broken down"), ("maltratado", "damaged"), ("junta", "joint/gasket"),
                ("válvula", "valve"), ("recién comprado", "newly bought"), ("pieza de recambio", "replacement part"),
                ("de fábrica", "factory-made"), ("respaldo de producto", "product warranty"), ("calcular", "to calculate"),
                # Encounter 21-25
                ("permiso", "permit"), ("licencia", "license"), ("tiempo de vida", "lifespan"),
                ("grado", "grade/quality"), ("trabajo manual", "manual labor"), ("recomendación", "recommendation"),
                ("desatascar", "to unclog"), ("destapador", "plunger"), ("sonda", "drain snake"),
                ("humedad", "humidity/moisture"), ("moho", "mold"), ("filtración", "seepage"),
                ("bomba", "pump"), ("por hora", "per hour"), ("eléctrico", "electric"),
                # Encounter 26-30
                ("nota de cobro", "bill"), ("en billetes", "in cash"), ("sistema de tuberías", "pipe system"),
                ("adelanto", "advance payment"), ("enlace", "joint/link"), ("liquidar", "to settle/pay off"),
                ("sótano", "basement"), ("empaque", "gasket/seal"), ("llave de paso", "shutoff valve"),
                ("excavación", "excavation"), ("zanja", "trench"), ("cavar", "to dig"),
                ("control de agua", "water control"), ("PVC", "PVC"), ("galvanizado", "galvanized"),
                # Encounter 31-35
                ("sellador", "sealant"), ("sellar", "to seal"), ("altura", "height"),
                ("dimensión", "dimension"), ("soldar", "to weld/solder"), ("estimar", "to estimate"),
                ("autorización", "authorization"), ("revisar", "to check/inspect"), ("habilitación", "certification"),
                ("cisterna", "cistern"), ("aljibe", "water tank"), ("tinaco", "rooftop tank"),
                ("residuo", "residue"), ("obstrucción", "obstruction"), ("limpiar", "to clean"),
                # Encounter 36-40
                ("diploma", "diploma"), ("trayectoria", "track record"), ("daño", "damage"),
                ("antigüedad laboral", "work seniority"), ("referencia laboral", "job reference"), ("reclamar", "to claim"),
                ("calefacción", "heating"), ("radiador", "radiator"), ("termostato", "thermostat"),
                ("gas", "gas"), ("destapar", "to unclog"), ("sopapa", "plunger"),
                ("ventilación", "ventilation"), ("extractor", "extractor fan"), ("ducto", "duct"),
                # Encounter 41-45
                ("purificador", "purifier"), ("filtro", "filter"), ("suavizador", "water softener"),
                ("riego", "irrigation"), ("cable de drenaje", "drain cable"), ("aspersor", "sprinkler"),
                ("fosa séptica", "septic tank"), ("drenaje pluvial", "storm drain"), ("alcantarilla", "sewer"),
                ("medidor", "meter"), ("consumo", "consumption"), ("lectura", "reading"),
                ("remodelación", "remodeling"), ("ampliación", "expansion"), ("condensación", "condensation"),
                # Encounter 46-50
                ("hongo", "fungus"), ("infiltración", "infiltration"), ("bomba de agua", "water pump"),
                ("subcontratista", "subcontractor"), ("equipo", "team/equipment"), ("impulsor", "impeller"),
                ("de corriente", "electric-powered"), ("convenio", "contract/agreement"), ("terminar", "to finish"),
                ("recomendar", "to recommend"), ("pacto", "agreement/pact"), ("reseña", "review"),
                ("buen trabajo", "good job"), ("pago inicial", "initial payment"), ("agradecer", "to thank"),
            ],
        },
    ],
    "groceries": [
        {
            "title": "At the Supermarket",
            "goal": "Buy groceries by finding items and checking out",
            "word_prefix": "groc",
            "words": [
                # Encounter 1-5 (basic essentials)
                ("supermercado", "supermarket"), ("autoservicio", "self-service store"), ("lista", "list"),
                ("listado", "list/checklist"), ("fruta fresca", "fresh fruit"), ("vegetal", "vegetable"),
                ("res", "beef"), ("hogaza", "loaf of bread"), ("lácteo", "dairy"),
                ("blanquillo", "egg"), ("barato", "cheap"), ("caro", "expensive"),
                ("costoso", "expensive"), ("carrito", "cart"), ("canasta", "basket"),
                # Encounter 6-10
                ("funda", "bag"), ("carro de compras", "shopping cart"), ("sección", "section"),
                ("fresco", "fresh"), ("congelado", "frozen"), ("enlatado", "canned"),
                ("cesta", "basket"), ("corredor", "aisle/corridor"), ("anaquel", "shelf"),
                ("departamento", "department"), ("recién cortado", "freshly cut"), ("pasta", "pasta"),
                ("bajo cero", "frozen"), ("en conserva", "preserved"), ("pechuga", "chicken breast"),
                # Encounter 11-15
                ("caja", "checkout/cashier"), ("filete de pescado", "fish fillet"), ("lomo", "pork loin"),
                ("grano", "grain"), ("fideos", "noodles"), ("promoción", "promotion"),
                ("kilo", "kilogram"), ("gramo", "gram"), ("litro", "liter"),
                ("maduro", "ripe"), ("aceite de oliva", "olive oil"), ("podrido", "rotten"),
                ("orgánico", "organic"), ("sal de mesa", "table salt"), ("integral", "whole grain"),
                # Encounter 16-20
                ("panadería", "bakery"), ("carnicería", "butcher shop"), ("pescadería", "fish counter"),
                ("endulzante", "sweetener"), ("caja registradora", "cash register"), ("kilogramo", "kilogram"),
                ("bebida", "drink"), ("jugo", "juice"), ("medio kilo", "half kilo"),
                ("medio litro", "half liter"), ("cereal", "cereal"), ("chocolate", "chocolate"),
                ("condimento", "condiment"), ("salsa", "sauce"), ("en su punto", "ripe/ready"),
                # Encounter 21-25
                ("sin madurar", "unripe"), ("ingrediente", "ingredient"), ("preparar", "to prepare"),
                ("echado a perder", "spoiled"), ("genérico", "generic"), ("importado", "imported"),
                ("bio", "organic/bio"), ("sin procesar", "unprocessed"), ("caducidad", "expiration"),
                ("refrigerador", "refrigerator section"), ("congelador", "freezer section"), ("ambiente", "room temperature"),
                ("limpieza", "cleaning"), ("de grano entero", "whole grain"), ("horno de pan", "bread oven"),
                # Encounter 26-30
                ("local de carnes", "meat counter"), ("servilleta", "napkin"), ("aluminio", "aluminum foil"),
                ("especia", "spice"), ("mostrador de pescado", "fish counter"), ("canela", "cinnamon"),
                ("harina", "flour"), ("levadura", "yeast"), ("producto lácteo", "dairy product"),
                ("nuez", "nut"), ("almendra", "almond"), ("cacahuate", "peanut"),
                ("fiambre", "deli meat"), ("queso fresco", "fresh cheese"), ("salchicha", "sausage"),
                # Encounter 31-35
                ("yogur natural", "natural yogurt"), ("refresco", "soft drink"), ("ajo", "garlic"),
                ("jugo natural", "natural juice"), ("zanahoria", "carrot"), ("agua mineral", "mineral water"),
                ("bizcocho", "biscuit"), ("plátano", "banana"), ("golosina", "candy/sweet"),
                ("aderezo", "dressing"), ("fresa", "strawberry"), ("uva", "grape"),
                ("atún", "tuna"), ("sardina", "sardine"), ("salsa picante", "hot sauce"),
                # Encounter 36-40
                ("tortilla", "tortilla"), ("tostada", "toast/tostada"), ("crema", "cream/sour cream"),
                ("aceto", "vinegar"), ("chile", "chili pepper"), ("cilantro", "cilantro"),
                ("fórmula", "recipe/formula"), ("cerveza", "beer"), ("vino", "wine"),
                ("pañal", "diaper"), ("elaborar", "to prepare"), ("sello comercial", "brand/trademark"),
                ("mascota", "pet"), ("alimento", "food/feed"), ("lata", "can"),
                # Encounter 41-45
                ("gourmet", "gourmet"), ("delicatessen", "delicatessen"), ("especialidad", "specialty"),
                ("libre de gluten", "gluten-free"), ("vegano", "vegan"), ("sin lactosa", "lactose-free"),
                ("sin marca", "generic/unbranded"), ("báscula", "scale"), ("medir", "to measure"),
                ("empacador", "bagger"), ("acomodar", "to arrange"), ("traído de fuera", "imported"),
                ("envase", "container"), ("ticket", "receipt"), ("rótulo", "label"),
                # Encounter 46-50
                ("entrega", "delivery"), ("fecha de vencimiento", "expiration date"), ("zona refrigerada", "refrigerated zone"),
                ("estacionamiento", "parking lot"), ("zona de congelados", "frozen section"), ("temperatura ambiente", "room temp"),
                ("artículo de limpieza", "cleaning product"), ("limpiador", "cleaner"), ("barra de jabón", "bar of soap"),
                ("fidelidad", "loyalty"), ("puntos", "points"), ("membresía", "membership"),
                ("hoja de papel", "paper sheet"), ("buen día", "good day"), ("pañuelo de mesa", "table napkin"),
            ],
        },
    ],
    "internet": [
        {
            "title": "Setting Up WiFi",
            "goal": "Set up your internet service by speaking with the technician",
            "word_prefix": "inet",
            "words": [
                # Encounter 1-5 (basic essentials)
                ("internet", "internet"), ("wifi", "WiFi"), ("red inalámbrica", "wireless network"),
                ("wifi doméstico", "home WiFi"), ("clave de acceso", "access code"), ("red local", "local network"),
                ("router", "router"), ("cable", "cable"), ("intensidad", "signal strength"),
                ("enrutador", "router"), ("cable de red", "network cable"), ("tomacorriente", "outlet"),
                ("plan", "plan"), ("pausado", "slow"), ("rapidez", "speed"),
                # Encounter 6-10
                ("paquete de datos", "data plan"), ("cuota mensual", "monthly fee"), ("visita", "visit"),
                ("nombre de red", "network name"), ("colocar", "to install"), ("configurar", "to configure"),
                ("conectar", "to connect"), ("desconectar", "to disconnect"), ("reiniciar", "to restart"),
                ("especialista", "specialist"), ("cita de servicio", "service appointment"), ("SSID", "SSID"),
                ("funcionar", "to work/function"), ("renombrar", "to rename"), ("solución", "solution"),
                # Encounter 11-15
                ("banda ancha", "broadband"), ("fibra óptica", "fiber optic"), ("megabits", "megabits"),
                ("descargar", "to download"), ("ajustar", "to adjust"), ("enlazar", "to connect"),
                ("cortar enlace", "to disconnect"), ("rearrancar", "to restart"), ("aparato", "device"),
                ("portátil", "laptop"), ("teléfono móvil", "mobile phone"), ("operar", "to work/operate"),
                ("modem", "modem"), ("antena", "antenna"), ("inconveniente", "issue"),
                # Encounter 16-20
                ("conexión de alta velocidad", "high-speed connection"), ("cable óptico", "fiber optic cable"), ("alcance", "range"),
                ("corte", "outage"), ("interrupción", "interruption"), ("megabytes", "megabytes"),
                ("bajar archivos", "to download files"), ("permanencia", "commitment period"), ("cargar archivos", "to upload files"),
                ("fecha de pago", "payment date"), ("mejorar", "to improve"), ("soporte al cliente", "customer support"),
                ("televisión", "television"), ("comunicarse", "to communicate"), ("combo", "bundle"),
                # Encounter 21-25
                ("streaming", "streaming"), ("videollamada", "video call"), ("juego en línea", "online gaming"),
                ("módem", "modem"), ("ilimitado", "unlimited"), ("antena receptora", "receiving antenna"),
                ("decodificador", "decoder"), ("firewall", "firewall"), ("área de cobertura", "coverage area"),
                ("virus", "virus"), ("malware", "malware"), ("antivirus", "antivirus"),
                ("extensión", "extension/extender"), ("repetidor", "repeater"), ("amplificar", "to amplify"),
                # Encounter 26-30
                ("dirección IP", "IP address"), ("DNS", "DNS"), ("puerto", "port"),
                ("ethernet", "ethernet"), ("inalámbrico", "wireless"), ("bluetooth", "bluetooth"),
                ("latencia", "latency"), ("ping", "ping"), ("estabilidad", "stability"),
                ("asistencia técnica", "technical support"), ("soporte", "support"), ("extensión de señal", "signal range"),
                ("apagón", "outage"), ("navegador", "browser"), ("página web", "webpage"),
                # Encounter 31-35
                ("usuario", "username"), ("falla", "failure"), ("registrar", "to register"),
                ("restablecer", "to restore"), ("acuerdo de servicio", "service agreement"), ("periodo de permanencia", "commitment period"),
                ("control parental", "parental controls"), ("dar de baja", "to cancel"), ("renovar plan", "to upgrade plan"),
                ("cámara", "camera"), ("monitor", "monitor"), ("vigilancia", "surveillance"),
                ("domótica", "home automation"), ("inteligente", "smart"), ("automatizar", "to automate"),
                # Encounter 36-40
                ("optimizar", "to improve"), ("almacenar", "to store"), ("combo de servicios", "service bundle"),
                ("impresora", "printer"), ("compartir", "to share"), ("acceso remoto", "remote access"),
                ("VPN", "VPN"), ("privacidad", "privacy"), ("encriptar", "to encrypt"),
                ("ancho de banda", "bandwidth"), ("saturado", "saturated"), ("TV por cable", "cable TV"),
                ("línea fija", "landline"), ("competencia", "competition"), ("paquete triple", "triple bundle"),
                # Encounter 41-45
                ("instalación", "installation"), ("cableado", "wiring"), ("infraestructura", "infrastructure"),
                ("contratación", "hiring/contracting"), ("video en vivo", "live streaming"), ("llamada de video", "video call"),
                ("migración", "migration"), ("portabilidad", "portability"), ("juego en red", "online gaming"),
                ("tope de datos", "data cap"), ("sin tope", "unlimited"), ("uso de datos", "data usage"),
                ("queja", "complaint"), ("protección de red", "network security"), ("cortafuegos", "firewall"),
                # Encounter 46-50
                ("resguardar", "to protect"), ("consumo real", "actual usage"), ("programa malicioso", "malicious software"),
                ("satelital", "satellite"), ("rural", "rural"), ("urbano", "urban"),
                ("mantenimiento", "maintenance"), ("actualización", "update"), ("software dañino", "harmful software"),
                ("programa de protección", "protection software"), ("amplificador", "amplifier"), ("encuesta", "survey"),
                ("listo", "ready"), ("funcionando", "working"), ("repetidor de señal", "signal repeater"),
            ],
        },
    ],
    "mechanic": [
        {
            "title": "Oil Change",
            "goal": "Get your car serviced by explaining what you need to the mechanic",
            "word_prefix": "mech",
            "words": [
                # Encounter 1-5 (basic essentials)
                ("lubricante", "lubricant"), ("reemplazo", "replacement"), ("vehículo", "vehicle"),
                ("garage", "garage"), ("técnico automotriz", "auto technician"), ("inspeccionar", "to inspect"),
                ("sonido", "sound"), ("pastilla de freno", "brake pad"), ("neumático", "tire"),
                ("timón", "steering wheel"), ("combustible", "fuel"), ("abastecer", "to fill up"),
                ("purificador de aire", "air filter"), ("electrodo", "spark plug/electrode"), ("acumulador", "battery"),
                # Encounter 6-10
                ("foco delantero", "headlight"), ("bujía", "spark plug"), ("batería", "battery"),
                ("farol", "lamp"), ("faro", "headlight"), ("direccional", "turn signal"),
                ("intermitente", "blinker"), ("kilómetro", "kilometer"), ("milla", "mile"),
                ("arrancar", "to start"), ("kilómetros", "kilometers"), ("encender", "to turn on"),
                ("millas", "miles"), ("dar marcha", "to start"), ("desactivar", "to turn off"),
                # Encounter 11-15
                ("prender", "to turn on"), ("sustituir", "to replace"), ("refacción", "spare part"),
                ("de agencia", "OEM/dealer"), ("póliza de garantía", "warranty policy"), ("meses de cobertura", "months of coverage"),
                ("aceite sintético", "synthetic oil"), ("aceite convencional", "conventional oil"), ("meses", "months"),
                ("grado de viscosidad", "viscosity grade"), ("convencional", "conventional"), ("viscosidad", "viscosity"),
                ("kilometraje", "mileage"), ("recorrido", "mileage"), ("revisión periódica", "periodic maintenance"),
                # Encounter 16-20
                ("transmisión", "transmission"), ("atención vehicular", "vehicle service"), ("manual", "manual"),
                ("embrague", "clutch"), ("pedal", "pedal"), ("palanca", "lever/shift"),
                ("caja de velocidades", "gearbox"), ("refrigerante", "coolant"), ("temperatura", "temperature"),
                ("escape", "exhaust"), ("silenciador", "muffler"), ("transmisión automática", "automatic transmission"),
                ("suspensión", "suspension"), ("amortiguador", "shock absorber"), ("resorte", "spring"),
                # Encounter 21-25
                ("alineación", "alignment"), ("balanceo", "balancing"), ("rotación", "rotation"),
                ("correa", "belt"), ("transmisión manual", "manual transmission"), ("tensor", "tensioner"),
                ("alternador", "alternator"), ("generador", "generator"), ("disco de embrague", "clutch disc"),
                ("fusible", "fuse"), ("pedal de freno", "brake pedal"), ("cortocircuito", "short circuit"),
                ("aire acondicionado", "air conditioning"), ("compresor", "compressor"), ("freón", "freon/refrigerant"),
                # Encounter 26-30
                ("palanca de cambios", "gear shift"), ("enfriador", "cooler/radiator"), ("escáner", "scanner"),
                ("sensor", "sensor"), ("líquido refrigerante", "coolant fluid"), ("grado de calor", "temperature level"),
                ("oxidado", "rusted"), ("corroído", "corroded"), ("desgastado", "worn"),
                ("apretar", "to tighten"), ("aflojar", "to loosen"), ("torque", "torque"),
                ("tubo de escape", "exhaust pipe"), ("mofle", "muffler"), ("sistema de suspensión", "suspension system"),
                # Encounter 31-35
                ("aceite de motor", "engine oil"), ("absorbedor de impactos", "shock absorber"), ("dipstick", "dipstick"),
                ("espiral", "spring/coil"), ("alineado de llantas", "tire alignment"), ("equilibrar", "to balance"),
                ("rotación de llantas", "tire rotation"), ("banda", "belt"), ("inyector", "injector"),
                ("carburador", "carburetor"), ("admisión", "intake"), ("eslabón", "chain link"),
                ("cigüeñal", "crankshaft"), ("pistón", "piston"), ("cilindro", "cylinder"),
                # Encounter 36-40
                ("turbo", "turbo"), ("sobrealimentador", "supercharger"), ("potencia", "horsepower"),
                ("catalizador", "catalytic converter"), ("emisión", "emission"), ("contaminación", "pollution"),
                ("freno de disco", "disc brake"), ("polea tensora", "tensioner pulley"), ("rotor", "rotor"),
                ("dirección hidráulica", "power steering"), ("fluido", "fluid"), ("dínamo", "alternator/dynamo"),
                ("limpiaparabrisas", "windshield wiper"), ("generador eléctrico", "electric generator"), ("circuito eléctrico", "electrical circuit"),
                # Encounter 41-45
                ("tapicería", "upholstery"), ("vestidura", "seat cover"), ("fusible de seguridad", "safety fuse"),
                ("pintura", "paint"), ("abollar", "to dent"), ("rayar", "to scratch"),
                ("hojalatería", "body shop"), ("carrocería", "body/chassis"), ("arnés", "wiring harness"),
                ("falla eléctrica", "electrical fault"), ("climatización", "climate control"), ("deducible", "deductible"),
                ("compresor de aire", "air compressor"), ("remolcar", "to tow"), ("gas refrigerante", "refrigerant gas"),
                # Encounter 46-50
                ("prueba de diagnóstico", "diagnostic test"), ("placa", "license plate"), ("escáner automotriz", "automotive scanner"),
                ("híbrido", "hybrid"), ("equipo de cómputo", "computer equipment"), ("recarga", "recharge"),
                ("tuning", "tuning"), ("captador", "sensor"), ("personalizar", "to customize"),
                ("indicador", "gauge"), ("dato", "reading/data"), ("herrumbre", "rust"),
                ("corrosión", "corrosion"), ("gastado", "worn out"), ("soltar", "to loosen"),
            ],
        },
    ],
    "police": [
        {
            "title": "Traffic Stop",
            "goal": "Handle a traffic stop by responding to the officer's questions",
            "word_prefix": "pol",
            "words": [
                # Encounter 1-5 (basic essentials)
                ("permiso de conducir", "driver's license"), ("papeles", "papers"), ("documentos", "documents"),
                ("tarjeta de circulación", "vehicle registration"), ("conducir", "to drive"), ("pare", "stop"),
                ("letrero", "sign"), ("luz de tráfico", "traffic light"), ("matrícula", "license plate"),
                ("correa de seguridad", "safety belt"), ("colocado", "wearing"), ("área", "area"),
                ("zona escolar", "school zone"), ("infracción", "violation"), ("zona habitacional", "residential zone"),
                # Encounter 6-10
                ("facultad", "right"), ("perdone", "excuse me"), ("comprender", "to understand"),
                ("aclarar", "to explain"), ("abrochado", "fastened"), ("puesto", "on/wearing"),
                ("vía rápida", "highway"), ("escolar", "school"), ("residencial", "residential"),
                ("autovía", "freeway"), ("avenida", "avenue"), ("rumbo", "direction"),
                ("disculpe", "excuse me"), ("vía", "way/route"), ("sentido contrario", "wrong way"),
                # Encounter 11-15
                ("carretera", "highway"), ("intersección", "intersection"), ("curva", "curve"),
                ("aparcar", "to park"), ("sentido", "direction/way"), ("contrario", "opposite/wrong way"),
                ("no permitido", "not allowed"), ("bebida alcohólica", "alcoholic drink"), ("exhalar", "to exhale/blow"),
                ("estacionar", "to park"), ("colisión", "collision"), ("permitido", "allowed"),
                ("alcohol", "alcohol"), ("impacto", "impact"), ("soplar", "to blow"),
                # Encounter 16-20
                ("accidente", "accident"), ("servicio de emergencia", "emergency service"), ("situación de emergencia", "emergency situation"),
                ("ambulancia", "ambulance"), ("lesionado", "injured"), ("herido", "injured"),
                ("observador", "witness"), ("relato", "statement"), ("datos personales", "personal info"),
                ("falta de atención", "distraction"), ("distracción", "distraction"), ("sancionado", "penalized"),
                ("cinturón de seguridad", "seatbelt"), ("multado", "penalized"), ("menor", "minor"),
                # Encounter 21-25
                ("arnés de seguridad", "safety harness"), ("acompañante", "passenger"), ("corralón", "impound lot"),
                ("radar", "radar"), ("persona menor", "minor"), ("servicio de grúa", "tow truck"),
                ("advertencia", "warning"), ("primera vez", "first time"), ("perdón", "pardon"),
                ("carril", "lane"), ("rebasar", "to pass/overtake"), ("doble línea", "double line"),
                ("rotonda", "roundabout"), ("arrastrar", "to tow"), ("ceder", "to yield"),
                # Encounter 26-30
                ("peatón", "pedestrian"), ("cruzar", "to cross"), ("depósito vehicular", "impound lot"),
                ("motocicleta", "motorcycle"), ("detector de velocidad", "speed detector"), ("ciclista", "cyclist"),
                ("retén", "checkpoint"), ("cámara de vigilancia", "surveillance camera"), ("prueba fotográfica", "photographic evidence"),
                ("licencia vencida", "expired license"), ("amonestación", "warning"), ("primera ocasión", "first occasion"),
                ("extranjero", "foreigner"), ("disculpa", "apology/pardon"), ("carril de circulación", "traffic lane"),
                # Encounter 31-35
                ("adelantar", "to overtake"), ("defensa", "defense"), ("línea doble", "double line"),
                ("cargos", "charges"), ("grave", "serious"), ("leve", "minor"),
                ("comparecencia", "court appearance"), ("juzgado", "court"), ("redondel", "roundabout"),
                ("imprudencia", "recklessness"), ("negligencia", "negligence"), ("responsabilidad", "responsibility"),
                ("cruce circular", "traffic circle"), ("impugnar", "to contest"), ("tribunal", "tribunal"),
                # Encounter 36-40
                ("arresto", "arrest"), ("detención", "detention"), ("esposas", "handcuffs"),
                ("patrulla", "patrol car"), ("sirena", "siren"), ("persecución", "pursuit"),
                ("registro vehicular", "vehicle search"), ("dar paso", "to yield"), ("consentir", "to consent"),
                ("transeúnte", "pedestrian"), ("uniforme", "uniform"), ("insignia", "badge"),
                ("atravesar", "to cross"), ("número de caso", "case number"), ("copia", "copy"),
                # Encounter 41-45
                ("paso peatonal", "crosswalk"), ("corrupción", "corruption"), ("denunciar", "to report/denounce"),
                ("derechos", "rights"), ("moto", "motorcycle"), ("inocente", "innocent"),
                ("fianza", "bail"), ("liberación", "release"), ("custodia", "custody"),
                ("bici", "bicycle"), ("consulado", "consulate"), ("persona en bicicleta", "cyclist"),
                ("traducción", "translation"), ("intérprete", "interpreter"), ("idioma", "language"),
                # Encounter 46-50
                ("protocolo", "protocol"), ("procedimiento", "procedure"), ("puesto de control", "checkpoint"),
                ("revisión vehicular", "vehicle inspection"), ("asuntos internos", "internal affairs"), ("supervisión", "oversight"),
                ("antecedentes", "record/background"), ("examinar", "to check"), ("limpio", "clean"),
                ("cooperar", "to cooperate"), ("respetuoso", "respectful"), ("educado", "polite"),
                ("buenas noches", "good evening"), ("permiso vencido", "expired permit"), ("cuidado", "take care"),
            ],
        },
    ],
    "restaurant": [
        {
            "title": "Ordering Food",
            "goal": "Order a meal by communicating with the waiter",
            "word_prefix": "rest_order",
            "words": [
                # Encounter 1-5 (basic essentials)
                ("menú", "menu"), ("mesero", "waiter"), ("camarero", "waiter"),
                ("platillo", "dish"), ("trago", "drink"), ("jarra de agua", "water pitcher"),
                ("ordenar", "to order"), ("sugerir", "to suggest"), ("del día", "of the day"),
                ("primer plato", "appetizer/starter"), ("plato fuerte", "main course"), ("plato principal", "main dish"),
                ("bistec", "steak"), ("filete", "fish fillet"), ("guarnición de arroz", "rice side"),
                # Encounter 6-10
                ("verduras mixtas", "mixed salad"), ("caldo", "broth"), ("canasta de pan", "bread basket"),
                ("tortilla de harina", "flour tortilla"), ("salero", "salt shaker"), ("pimentero", "pepper shaker"),
                ("lima", "lime"), ("enchiloso", "spicy"), ("no picante", "mild"),
                ("picante", "spicy"), ("suave", "mild"), ("gusto", "taste"),
                ("frío", "cold"), ("caliente", "hot"), ("tibio", "warm"),
                # Encounter 11-15
                ("cocinar", "to cook"), ("freír", "to fry"), ("asar", "to grill"),
                ("hervir", "to boil"), ("hornear", "to bake"), ("ardiente", "hot/burning"),
                ("vegetariano", "vegetarian"), ("alergia", "allergy"), ("templado", "lukewarm"),
                ("guisar", "to cook"), ("saltear", "to sauté"), ("asar a la parrilla", "to grill"),
                ("cocer", "to boil"), ("gratinar", "to bake/gratin"), ("alistar", "to prepare"),
                # Encounter 16-20
                ("taco", "taco"), ("enchilada", "enchilada"), ("burrito", "burrito"),
                ("guacamole", "guacamole"), ("frijoles", "beans"), ("sin carne", "meatless"),
                ("intolerancia", "intolerance"), ("trinche", "fork"), ("cuchillo de mesa", "table knife"),
                ("cucharita", "teaspoon"), ("café", "coffee"), ("té", "tea"),
                ("porción", "portion"), ("loza", "plate/dish"), ("chico", "small"),
                # Encounter 21-25
                ("mariscos", "seafood"), ("copa de agua", "water glass"), ("pulpo", "octopus"),
                ("taco al pastor", "pastor taco"), ("cordero", "lamb"), ("enchilada suiza", "Swiss enchilada"),
                ("vegetales", "vegetables"), ("champiñón", "mushroom"), ("burrito de frijol", "bean burrito"),
                ("guacamole fresco", "fresh guacamole"), ("frijoles refritos", "refried beans"), ("queso fundido", "melted cheese"),
                ("cerveza de barril", "draft beer"), ("jalapeño", "jalapeño"), ("habanero", "habanero"),
                # Encounter 26-30
                ("copa de vino", "glass of wine"), ("agua de sabor", "flavored water"), ("jugo de naranja", "orange juice"),
                ("café americano", "American coffee"), ("té de manzanilla", "chamomile tea"), ("ración", "serving"),
                ("delicioso", "delicious"), ("rico", "tasty"), ("sabroso", "flavorful"),
                ("tamaño grande", "large size"), ("casero", "homemade"), ("tradicional", "traditional"),
                ("dieta", "diet"), ("sin gluten", "gluten-free"), ("tamaño chico", "small size"),
                # Encounter 31-35
                ("ceviche", "ceviche"), ("mole", "mole"), ("tamales", "tamales"),
                ("mezcal", "mezcal"), ("tequila", "tequila"), ("margarita", "margarita"),
                ("antojito", "snack/appetizer"), ("quesadilla", "quesadilla"), ("frutos del mar", "seafood"),
                ("sazón", "seasoning"), ("langostino", "prawn"), ("chef", "chef"),
                ("parrilla", "grill"), ("calamar", "squid"), ("borrego", "lamb"),
                # Encounter 36-40
                ("maridaje", "pairing"), ("acompañamiento", "side dish"), ("guarnición", "garnish"),
                ("degustación", "tasting"), ("menú del día", "daily menu"), ("corte de res", "beef cut"),
                ("reservación", "reservation"), ("privado", "private"), ("terraza", "terrace"),
                ("propina", "tip"), ("verdura de temporada", "seasonal vegetables"), ("excelente", "excellent"),
                ("comensal", "diner"), ("cebolla caramelizada", "caramelized onion"), ("familiar", "family-style"),
                # Encounter 41-45
                ("diente de ajo", "garlic clove"), ("crudo", "raw"), ("al vapor", "steamed"),
                ("ahumado", "smoked"), ("marinado", "marinated"), ("empanizado", "breaded"),
                ("fusión", "fusion"), ("contemporáneo", "contemporary"), ("jitomate", "tomato"),
                ("palta", "avocado"), ("chile serrano", "serrano chili"), ("chile poblano", "poblano chili"),
                ("flambear", "to flambé"), ("chile ancho", "ancho chili"), ("reducción", "reduction"),
                # Encounter 46-50
                ("sommelier", "sommelier"), ("catador", "taster"), ("selección", "selection"),
                ("piloncillo", "raw sugar"), ("sustentable", "sustainable"), ("néctar", "nectar/honey"),
                ("nata", "cream"), ("manteca", "lard/butter"), ("jugo de limón", "lemon juice"),
                ("memorable", "memorable"), ("felicitaciones", "congratulations"), ("al chef", "to the chef"),
                ("exquisito", "exquisite"), ("sazonado", "seasoned"), ("favorito", "favorite"),
            ],
        },
        {
            "title": "Making a Reservation",
            "goal": "Make a restaurant reservation by calling or speaking with the host",
            "word_prefix": "rest_reserve",
            "words": [
                # Encounter 1-5 (basic essentials)
                ("reserva de mesa", "table reservation"), ("lugar para sentarse", "seating"), ("comensales", "diners/guests"),
                ("por la noche", "in the evening"), ("apellido", "last name"), ("número de contacto", "contact number"),
                ("ratificar", "to confirm"), ("aguardar", "to wait"), ("esta noche", "tonight"),
                ("día siguiente", "next day"), ("sábado y domingo", "weekend"), ("adentro", "inside"),
                ("afuera", "outside"), ("balcón", "balcony"), ("fin de semana", "weekend"),
                # Encounter 6-10
                ("junto a la ventana", "by the window"), ("exterior", "outside"), ("rincón", "corner"),
                ("zona reservada", "reserved area"), ("mesa grande", "large table"), ("mesa pequeña", "small table"),
                ("acogedor", "cozy"), ("festejo", "celebration"), ("íntimo", "intimate"),
                ("celebración", "celebration"), ("cumpleaños", "birthday"), ("aniversario", "anniversary"),
                ("fiesta de cumpleaños", "birthday party"), ("fecha especial", "special date"), ("mesa para grupo", "group table"),
                # Encounter 11-15
                ("mesa para dos", "table for two"), ("reunión familiar", "family gathering"), ("modificar reserva", "to modify reservation"),
                ("reglas del local", "venue rules"), ("anticipación", "advance notice"), ("con antelación", "in advance"),
                ("cargo por cancelación", "cancellation fee"), ("carta del restaurante", "restaurant menu"), ("plato del día", "daily special"),
                ("de la estación", "seasonal"), ("horas de atención", "business hours"), ("en servicio", "open"),
                ("temprano", "early"), ("tarde", "late"), ("mediodía", "noon"),
                # Encounter 16-20
                ("alérgico", "allergic"), ("fuera de horario", "closed"), ("antes de tiempo", "early"),
                ("silla alta", "high chair"), ("niño", "child"), ("con retraso", "late"),
                ("hora del almuerzo", "lunchtime"), ("valet", "valet"), ("con alergia", "with allergy"),
                ("preferencia alimentaria", "dietary preference"), ("popular", "popular"), ("régimen alimenticio", "diet/regimen"),
                ("código de vestimenta", "dress code"), ("silla para bebé", "baby chair"), ("con acceso", "with access"),
                # Encounter 21-25
                ("lista de espera", "waiting list"), ("zona de estacionamiento", "parking area"), ("notificar", "to notify"),
                ("garantizar", "to guarantee"), ("asegurar", "to ensure"), ("compromiso", "commitment"),
                ("decoración", "decoration"), ("servicio de valet", "valet parking"), ("a poca distancia", "nearby"),
                ("sugerencia", "suggestion"), ("muy solicitado", "very popular"), ("predilecto", "favorite"),
                ("vista", "view"), ("vestimenta", "dress code"), ("fuente", "fountain"),
                # Encounter 26-30
                ("evento", "event"), ("banquete", "banquet"), ("catering", "catering"),
                ("de etiqueta", "formal dress"), ("relajado", "relaxed/casual"), ("por persona", "per person"),
                ("menú fijo", "fixed menu"), ("turno de espera", "waiting turn"), ("puesto en fila", "queued"),
                ("brindis", "toast"), ("champán", "champagne"), ("avisar", "to notify"),
                ("asegurar mesa", "to guarantee table"), ("velas", "candles"), ("sorpresa", "surprise"),
                # Encounter 31-35
                ("florista", "florist"), ("arreglo", "arrangement"), ("decorar", "to decorate"),
                ("fotógrafo", "photographer"), ("recuerdo", "memory/souvenir"), ("reservar con certeza", "to ensure reservation"),
                ("palabra", "commitment"), ("invitación", "invitation"), ("confirmar asistencia", "to RSVP"),
                ("adorno", "decoration"), ("salón", "hall/room"), ("atmósfera", "atmosphere"),
                ("melodía", "music/melody"), ("cocinero principal", "head chef"), ("bocina", "speaker"),
                # Encounter 36-40
                ("iluminación", "lighting"), ("vela", "candle"), ("romántico", "romantic"),
                ("mantel", "tablecloth"), ("vajilla", "dinnerware"), ("cristalería", "glassware"),
                ("servicio completo", "full service"), ("plato estrella", "signature dish"), ("buffet", "buffet"),
                ("coordinador", "coordinator"), ("gastronomía", "gastronomy"), ("planificar", "to plan"),
                ("panorama", "view"), ("patio", "patio/garden"), ("anticipo", "advance payment"),
                # Encounter 41-45
                ("cascada decorativa", "decorative fountain"), ("aforo", "capacity limit"), ("ocasión especial", "special event"),
                ("comentario", "review/comment"), ("cena de gala", "gala dinner"), ("servicio de banquete", "banquet service"),
                ("costo por persona", "cost per person"), ("en línea", "online"), ("sitio web", "website"),
                ("valor del evento", "event price"), ("menú cerrado", "set menu"), ("cupón", "coupon"),
                ("cata de vinos", "wine tasting"), ("inolvidable", "unforgettable"), ("combinación de platillos", "dish pairing"),
                # Encounter 46-50
                ("agradecimiento", "gratitude"), ("copa de champán", "glass of champagne"), ("espumoso", "sparkling wine"),
                ("tinto", "red wine"), ("tarta", "cake/tart"), ("velitas", "candles"),
                ("detalle sorpresa", "surprise detail"), ("reconocimiento", "recognition"), ("premio", "award"),
                ("recomendado", "recommended"), ("destacado", "outstanding"), ("excepcional", "exceptional"),
                ("arreglo floral", "flower arrangement"), ("hasta pronto", "see you soon"), ("centro de mesa", "centerpiece"),
            ],
        },
        {
            "title": "Asking for the Bill",
            "goal": "Ask for the bill, review the charges, and pay",
            "word_prefix": "rest_bill",
            "words": [
                # Encounter 1-5 (basic essentials)
                ("la cuenta por favor", "the check please"), ("cancelar la cuenta", "to pay the bill"), ("suma total", "total sum"),
                ("con tarjeta", "by card"), ("devuelta", "change"), ("gratificación", "tip/gratuity"),
                ("atención al cliente", "customer service"), ("ya incluido", "already included"), ("incluido", "included"),
                ("cargar a la cuenta", "to charge to the bill"), ("exacto", "correct"), ("correcto", "correct"),
                ("comprobante de pago", "payment receipt"), ("nota de venta", "sales receipt"), ("sacar copia", "to print"),
                # Encounter 6-10
                ("dividir", "to split"), ("partir la cuenta", "to split the bill"), ("cada uno", "each one"),
                ("por separado", "separately"), ("equivocación", "mistake"), ("confusión", "mistake"),
                ("lo que tomamos", "what we drank"), ("lo que comimos", "what we ate"), ("extra", "extra"),
                ("pedido extra", "extra order"), ("IVA", "VAT/sales tax"), ("tributación", "tax"),
                ("impuesto al consumo", "consumption tax"), ("precio especial", "special deal"), ("vale", "coupon"),
                # Encounter 11-15
                ("de débito", "debit"), ("de crédito", "credit"), ("lector de tarjetas", "card reader"),
                ("contactless", "contactless"), ("chip", "chip"), ("pago sin contacto", "contactless payment"),
                ("propina sugerida", "suggested tip"), ("voluntario", "voluntary"), ("obligatorio", "mandatory"),
                ("tarjeta con chip", "chip card"), ("gratificación sugerida", "suggested tip"), ("identificar", "to identify"),
                ("a voluntad", "voluntary"), ("saldar", "to pay off"), ("de cumplimiento", "mandatory"),
                # Encounter 16-20
                ("desglose", "breakdown"), ("detalle", "detail"), ("código de mesa", "table number"),
                ("ubicar", "to identify"), ("saldar la cuenta", "to settle the bill"), ("poner al día", "to pay off"),
                ("finiquitar", "to finalize"), ("sin alcohol", "non-alcoholic"), ("detalle de cargos", "charge details"),
                ("copa", "glass/drink"), ("ronda", "round"), ("pormenor", "detail"),
                ("cubierto", "cover charge"), ("rubro", "item/category"), ("suplemento", "supplement"),
                # Encounter 21-25
                ("postre del menú", "menu dessert"), ("copa alcohólica", "alcoholic drink"), ("QR", "QR code"),
                ("voucher", "voucher"), ("bebida sin alcohol", "non-alcoholic drink"), ("botella de agua", "bottle of water"),
                ("tanda", "round"), ("recompensa", "reward"), ("acumular", "to accumulate"),
                ("pedido adicional", "additional order"), ("cargo de cubierto", "cover charge"), ("cargo por servicio", "service charge"),
                ("cargo extra", "extra charge"), ("pago por transferencia", "payment by transfer"), ("app de pago", "payment app"),
                # Encounter 26-30
                ("sobrar", "to be left over"), ("código QR", "QR code"), ("sobrante", "leftover/surplus"),
                ("bono", "voucher"), ("cupón de regalo", "gift coupon"), ("hacer válido", "to redeem"),
                ("recibo digital", "digital receipt"), ("acumulación de puntos", "points accumulation"), ("sumar puntos", "to earn points"),
                ("moneda extranjera", "foreign currency"), ("mesa de grupo", "group table"), ("datos fiscales", "tax details"),
                ("cuenta individual", "individual bill"), ("empacar", "to pack"), ("contenedor", "container"),
                # Encounter 31-35
                ("dividir gastos", "to share expenses"), ("lo que quedó", "what's left over"), ("regresar", "to return"),
                ("doble cargo", "double charge"), ("excedente", "surplus/leftover"), ("punto de pago", "payment point"),
                ("responsable de caja", "cashier"), ("barra", "counter/bar"), ("recibo electrónico", "electronic receipt"),
                ("mandar", "to send"), ("datos tributarios", "tax data"), ("número fiscal", "tax number"),
                ("información tributaria", "tax info"), ("para llevar", "to go"), ("beneficio", "benefit"),
                # Encounter 36-40
                ("regalo", "gift"), ("invitar", "to treat/invite"), ("cortesía", "courtesy/complimentary"),
                ("envolver", "to wrap"), ("recipiente", "container"), ("ocasión", "occasion"),
                ("desacuerdo", "dispute"), ("esclarecer", "to clarify"), ("descorche", "corkage fee"),
                ("encargado", "manager"), ("cargo duplicado", "duplicate charge"), ("precio fijo", "fixed price"),
                ("todo incluido", "all-inclusive"), ("anular cargo", "to void charge"), ("devolución de dinero", "money refund"),
                # Encounter 41-45
                ("recibo de transacción", "transaction receipt"), ("permiso de cobro", "charge authorization"), ("sistema de reservas", "reservation system"),
                ("contabilidad", "accounting"), ("por internet", "online"), ("archivos", "files"),
                ("reserva previa", "prior reservation"), ("tarjeta de socio", "membership card"), ("consumidor", "consumer"),
                ("beneficio de socio", "member benefit"), ("ventaja exclusiva", "exclusive advantage"), ("obsequio", "gift"),
                ("de cortesía", "complimentary"), ("evento especial", "special event"), ("fecha señalada", "special occasion"),
                # Encounter 46-50
                ("copa de vino tinto", "glass of red wine"), ("botella de vino", "bottle of wine"), ("derecho de corcho", "corkage fee"),
                ("agradecido", "grateful"), ("probada", "tasting"), ("amable", "kind"),
                ("carta de precios", "price menu"), ("tarifa fija", "fixed rate"), ("paquete todo incluido", "all-inclusive package"),
                ("despedida", "farewell"), ("barra de alimentos", "food bar"), ("hasta luego", "see you later"),
                ("sin límite", "unlimited"), ("buen provecho", "enjoy your meal"), ("felicidades", "congratulations"),
            ],
        },
    ],
    "small_talk": [
        {
            "title": "Meeting a Neighbor",
            "goal": "Have a friendly conversation with your new neighbor",
            "word_prefix": "talk",
            "words": [
                # Encounter 1-5 (basic essentials)
                ("hola", "hello"), ("saludos", "greetings"), ("mucho gusto", "nice to meet you"),
                ("persona de al lado", "person next door"), ("vivir", "to live"), ("encantado", "delighted to meet you"),
                ("residir", "to reside"), ("hogar", "home"), ("parientes", "relatives"),
                ("ocupación", "occupation"), ("bonito", "nice/pretty"), ("tranquilo", "quiet/calm"),
                ("clima", "weather"), ("mudarse", "to move"), ("barrio", "neighborhood"),
                # Encounter 6-10
                ("esposa", "wife"), ("esposo", "husband"), ("hijo", "son/child"),
                ("sereno", "calm/peaceful"), ("recién llegado", "newcomer"), ("instalarse", "to settle in"),
                ("colonia", "neighborhood"), ("planta", "plant"), ("compañera", "wife/partner"),
                ("compañero", "husband/partner"), ("parque", "park"), ("animal doméstico", "pet"),
                ("cachorro", "puppy"), ("gatito", "kitten"), ("arbusto", "shrub"),
                # Encounter 11-15
                ("rosal", "rosebush"), ("local comercial", "shop"), ("anochecer", "evening"),
                ("deporte", "sport"), ("caminar", "to walk"), ("preparar comida", "to cook"),
                ("receta casera", "homemade recipe"), ("película", "movie"), ("libro", "book"),
                ("fiesta", "party"), ("actividad física", "exercise"), ("celebrar", "to celebrate"),
                ("pasear", "to walk/stroll"), ("favor", "favor"), ("trotar", "to jog"),
                # Encounter 16-20
                ("serie de TV", "TV show"), ("novela", "novel"), ("restaurante", "restaurant"),
                ("reunión social", "social gathering"), ("convidar", "to invite"), ("festejar", "to celebrate"),
                ("taxi", "taxi"), ("echar una mano", "to help"), ("estación", "station"),
                ("hacer falta", "to need"), ("peligroso", "dangerous"), ("mercado local", "local market"),
                ("fonda", "restaurant/eatery"), ("colegio", "school"), ("respetar", "to respect"),
                # Encounter 21-25
                ("basura", "trash"), ("reciclar", "to recycle"), ("templo", "church/temple"),
                ("clínica", "clinic"), ("taxi compartido", "shared taxi"), ("transporte", "transport"),
                ("parada", "stop/station"), ("sin peligro", "safe"), ("con riesgo", "dangerous"),
                ("electricidad", "electricity"), ("precaución", "caution"), ("sonido fuerte", "loud noise"),
                ("calma", "quiet/calm"), ("considerar", "to respect"), ("desechos", "garbage"),
                # Encounter 26-30
                ("reunión", "meeting/gathering"), ("reutilizar", "to recycle"), ("asociación", "association"),
                ("barrer", "to sweep/clean"), ("auto", "car"), ("juntos", "together"),
                ("renta", "rent"), ("propietario", "landlord"), ("llave de casa", "house key"),
                ("luz eléctrica", "electricity"), ("suministro de agua", "water supply"), ("gas doméstico", "domestic gas"),
                ("reglas", "rules"), ("convivencia", "coexistence"), ("conexión a internet", "internet connection"),
                # Encounter 31-35
                ("usar en conjunto", "to share"), ("junta vecinal", "neighborhood meeting"), ("felicitar", "to congratulate"),
                ("vacaciones", "vacation"), ("viajar", "to travel"), ("vecindario", "community"),
                ("grupo de vecinos", "neighborhood association"), ("en equipo", "together"), ("dueño", "landlord"),
                ("arrendatario", "tenant"), ("aprender", "to learn"), ("practicar", "to practice"),
                ("reparación", "maintenance"), ("generoso", "generous"), ("simpático", "nice/friendly"),
                # Encounter 36-40
                ("consejo", "advice"), ("informar", "to report"), ("normas del edificio", "building rules"),
                ("doctor", "doctor"), ("dentista", "dentist"), ("farmacia", "pharmacy"),
                ("vivir en armonía", "coexistence"), ("dar la enhorabuena", "to congratulate"), ("días de descanso", "vacation"),
                ("hacer un viaje", "to travel"), ("costa", "beach/coast"), ("nublado", "cloudy"),
                ("feriado", "holiday"), ("herencia cultural", "cultural tradition"), ("descanso", "rest"),
                # Encounter 41-45
                ("hábito", "custom/habit"), ("raíces", "cultural roots"), ("participar", "to participate"),
                ("nostalgia", "nostalgia"), ("extrañar", "to miss"), ("ejercitar", "to practice"),
                ("cordial", "kind/warm"), ("desprendido", "generous"), ("agradable de trato", "friendly"),
                ("nieto", "grandchild"), ("abuelo", "grandfather"), ("generación", "generation"),
                ("fotografía", "photography"), ("álbum", "album"), ("vivencia", "experience"),
                # Encounter 46-50
                ("confianza", "trust"), ("amistad", "friendship"), ("respeto", "respect"),
                ("médico", "doctor"), ("odontólogo", "dentist"), ("botica", "pharmacy"),
                ("bienvenida", "welcome"), ("bochorno", "heat wave"), ("feliz", "happy"),
                ("aguacero", "rainstorm"), ("bendición", "blessing"), ("día soleado", "sunny day"),
                ("cuídate", "take care"), ("cielo gris", "overcast"), ("buena suerte", "good luck"),
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
