"""Central seed bank — single source of truth for all word and situation data.

All encounter words, high-frequency words, situations, and their links
are defined here. Grammar situations are in grammar_situations.py.
The seed script (scripts/seed_qa.py) reads from this module.

Structure: _SUB_SITUATIONS defines compact word data as (spanish, english, catalan) tuples.
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
                ("abordaje", "boarding process", "abordatge"), ("vuelo", "flight", "vol"), ("boleto", "ticket", "bitllet"),
                ("aterrizaje", "landing", "aterratge"), ("mostrador", "counter", "taulell"), ("agente", "agent", "agent"),
                ("asiento", "seat", "seient"), ("aéreo", "aerial", "aeri"), ("terminal", "terminal", "terminal"),
                ("maleta", "suitcase", "maleta"), ("embarque", "boarding", "embarcament"), ("salida", "departure", "sortida"),
                ("llegada", "arrival", "arribada"), ("destino", "destination", "destí"), ("fila", "line/queue", "fila"),
                # Encounter 6-10
                ("ventanilla", "window seat", "finestra"), ("vuelo directo", "direct flight", "vol directe"), ("reserva", "reservation", "reserva"),
                ("demora", "delay", "retard"), ("tráfico aéreo", "air traffic", "trànsit aeri"), ("zona", "zone", "zona"),
                ("documento", "document", "document"), ("identificación", "identification", "identificació"), ("nacionalidad", "nationality", "nacionalitat"),
                ("seguridad", "security", "seguretat"), ("azafata", "flight attendant", "azafata"), ("registro", "check-in", "registre"),
                ("directo", "direct", "directe"), ("escala", "layover", "escala"), ("conexión", "connection", "connexió"),
                # Encounter 11-15
                ("pase de abordar", "boarding pass", "passe d\'embarcament"), ("imprimir", "to print", "imprimir"), ("escanear", "to scan", "escanear"),
                ("disponible", "available", "disponible"), ("asignado", "assigned", "assignat"), ("seleccionar", "to select", "seleccionar"),
                ("equipaje de mano", "carry-on", "equipatge de mà"), ("hangar", "hangar", "hangar"), ("plataforma", "platform", "plataforma"),
                ("sobrepeso", "overweight", "sobrepès"), ("límite", "limit", "límit"), ("restricción", "restriction", "restricció"),
                ("facturar", "to check in luggage", "facturar"), ("despacho", "dispatch", "despatx"), ("tarifa", "fare", "tarifa"),
                # Encounter 16-20
                ("aerolínea", "airline", "aerolínia"), ("pasajero", "passenger", "passatger"), ("tripulación", "crew", "tripulació"),
                ("primera clase", "first class", "primera classe"), ("económica", "economy", "econòmica"), ("preferente", "preferred", "preferent"),
                ("ida", "one-way", "anada"), ("vuelta", "return", "tornada"), ("redondo", "round-trip", "rodó"),
                ("cinturón", "seatbelt", "cinturó"), ("abrocharse", "to fasten", "abrochar-se"), ("documentación", "documentation", "documentació"),
                ("cabina", "cabin", "cabina"), ("compartimento", "compartment", "compartiment"), ("superior", "overhead", "superior"),
                # Encounter 21-25
                ("aterrizar", "to land", "aterrar"), ("despegar", "to take off", "despegar"), ("pista", "runway", "pista"),
                ("auxiliar", "flight attendant", "auxiliar"), ("portaequipaje", "luggage rack", "portaequipatges"), ("asistencia", "assistance", "assistència"),
                ("sobrevolado", "overflown", "sobrevolat"), ("declarar", "to declare", "declarar"), ("inmigración", "immigration", "immigració"),
                ("transatlántico", "transatlantic", "transatlàntic"), ("llenar", "to fill out", "omplir"), ("firmar", "to sign", "signar"),
                ("recoger", "to pick up", "recollir"), ("reclamo", "claim", "reclam"), ("transcontinental", "transcontinental", "transcontinental"),
                # Encounter 26-30
                ("cancelación", "cancellation", "cancel·lació"), ("compensación", "compensation", "compensació"), ("reembolso", "refund", "reemborsament"),
                ("emergencia", "emergency", "emergència"), ("chaleco", "vest", "jaqueta"), ("oxígeno", "oxygen", "oxigen"),
                ("prohibido", "prohibited", "prohibit"), ("líquido", "liquid", "líquid"), ("gel", "gel", "gel"),
                ("inspección", "inspection", "inspecció"), ("detector", "detector", "detector"), ("rayos", "x-rays", "raigs"),
                ("electrónico", "electronic", "electrònic"), ("dispositivo", "device", "dispositiu"), ("apagar", "to turn off", "apagar"),
                # Encounter 31-35
                ("abordar", "to board", "embarcar"), ("llamada", "call/announcement", "crida"), ("final", "final", "final"),
                ("retraso", "delay", "retard"), ("itinerario", "itinerary", "itinerari"), ("cambiar", "to change", "canviar"),
                ("vacuna", "vaccine", "vacuna"), ("certificado", "certificate", "certificat"), ("salud", "health", "salut"),
                ("horario", "schedule", "horari"), ("puntual", "on time", "puntual"), ("bienvenida a bordo", "welcome aboard", "benvinguda a bord"),
                ("clase ejecutiva", "business class", "classe executiva"), ("reclinable", "reclining", "reclinable"), ("despegue", "takeoff", "despegue"),
                # Encounter 36-40
                ("frágil", "fragile", "fràgil"), ("especial", "special", "especial"), ("delicado", "delicate", "delicat"),
                ("transbordo", "transfer", "transbord"), ("mapa", "map", "mapa"), ("aduanal", "customs-related", "aduanal"),
                ("sala de espera", "waiting room", "sala d\'espera"), ("anuncio", "announcement", "anunci"), ("altavoz", "loudspeaker", "altaveu"),
                ("fumigación", "fumigation", "fumigació"), ("efectivo", "cash", "efectiu"), ("escáner corporal", "body scanner", "escàner corporal"),
                ("piloto", "pilot", "pilot"), ("copiloto", "co-pilot", "copilot"), ("banda transportadora", "conveyor belt", "banda transportadora"),
                # Encounter 41-45
                ("turbulencia", "turbulence", "turbulència"), ("altitud", "altitude", "altitud"), ("presión", "pressure", "pressió"),
                ("máscara", "mask", "màscara"), ("instrucciones", "instructions", "instruccions"), ("recogida", "pickup/collection", "recollida"),
                ("regulación", "regulation", "regulació"), ("norma", "rule", "norma"), ("vigente", "in effect", "vigent"),
                ("tránsito", "transit", "trànsit"), ("lounge", "lounge", "lounge"), ("acceso", "access", "accés"),
                ("equipaje perdido", "lost luggage", "equipatge perdut"), ("reporte", "report", "reporte"), ("oficina", "office", "oficina"),
                # Encounter 46-50
                ("sobrecargo", "surcharge", "sobrecàrrec"), ("cargo", "charge", "càrrec"), ("adicional", "additional", "addicional"),
                ("pasarela", "jet bridge", "passarel·la"), ("andén", "boarding platform", "andana"), ("entrada", "entry", "entrada"),
                ("zona franca", "duty-free zone", "zona franca"), ("altoparlante", "speaker/PA", "altaveu"), ("taquilla", "ticket counter", "taquilla"),
                ("válido", "valid", "vàlid"), ("vencimiento", "expiration", "venciment"), ("vigencia", "validity", "vigència"),
                ("buen viaje", "have a good trip", "bon viatge"), ("destino final", "final destination", "destí final"), ("llegada segura", "safe arrival", "arribada segura"),
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
                ("apertura", "opening", "obertura"), ("banco", "bank", "banc"), ("abrir", "to open", "obrir"),
                ("depósito inicial", "initial deposit", "dipòsit inicial"), ("depositar", "to deposit", "dipositar"), ("saldo", "balance", "saldo"),
                ("fondos", "funds", "fons"), ("boleta", "deposit slip", "boleta"), ("giro", "money order", "giro"),
                ("tarjeta", "card", "targeta"), ("débito", "debit", "dèbit"), ("crédito", "credit", "crèdit"),
                ("operación", "transaction", "operació"), ("corriente", "checking", "corrent"), ("fiador", "guarantor", "fiador"),
                # Encounter 6-10
                ("cajero", "teller", "caixer"), ("aval", "endorser/guarantor", "aval"), ("turno", "turn/number", "torn"),
                ("garante", "guarantor", "garant"), ("cuentahabiente", "account holder", "correntista"), ("datos", "data/details", "dades"),
                ("módulo", "service module", "mòdul"), ("dirección", "address", "adreça"), ("teléfono", "phone number", "telèfon"),
                ("requisito", "requirement", "requisit"), ("comprobante", "proof/receipt", "comprovant"), ("domicilio", "address/residence", "domicili"),
                ("clave", "PIN/password", "clau"), ("contraseña", "password", "contrasenya"), ("fila de espera", "waiting line", "fila d\'espera"),
                # Encounter 11-15
                ("papelería", "paperwork", "papereria"), ("cédula", "ID card", "cèdula"), ("acreditación", "accreditation", "acreditació"),
                ("huella digital", "fingerprint", "empremta digital"), ("tasa", "rate", "taxa"), ("porcentaje", "percentage", "percentatge"),
                ("plazo", "term/period", "termini"), ("fijo", "fixed", "fix"), ("variable", "variable", "variable"),
                ("comisión", "commission/fee", "comissió"), ("cobrar", "to charge", "cobrar"), ("mensual", "monthly", "mensual"),
                ("estado de cuenta", "account statement", "estat de compte"), ("biométrico", "biometric", "biomètric"), ("consultar", "to check", "consultar"),
                # Encounter 16-20
                ("transferencia", "transfer", "transferència"), ("enviar", "to send", "enviar"), ("código postal", "zip code", "codi postal"),
                ("beneficiario", "beneficiary", "beneficiari"), ("autorizar", "to authorize", "autoritzar"), ("RFC", "tax ID", "RFC"),
                ("retiro", "withdrawal", "retir"), ("retirar", "to withdraw", "retirar"), ("CURP", "national ID number", "CURP"),
                ("cheque", "check", "xec"), ("chequera", "checkbook", "xec"), ("endosar", "to endorse", "endossar"),
                ("banca en línea", "online banking", "banca en línia"), ("aplicación", "app", "aplicació"), ("mancomunado", "joint", "mancomunat"),
                # Encounter 21-25
                ("préstamo", "loan", "préstec"), ("solicitar", "to request", "sol·licitar"), ("aprobar", "to approve", "aprovar"),
                ("pago", "payment", "pagament"), ("cuota", "installment", "quota"), ("individual", "individual", "individual"),
                ("cancelar", "to cancel", "cancel·lar"), ("cerrar", "to close", "tancar"), ("motivo", "reason", "motiu"),
                ("extracto", "statement", "extracte"), ("historial", "history", "historial"), ("persona física", "individual person", "persona física"),
                ("número de cuenta", "account number", "número de compte"), ("titular", "account holder", "titular"), ("cotitular", "co-holder", "cotitular"),
                # Encounter 26-30
                ("dígito", "digit", "dígits"), ("cláusula", "clause", "clàusula"), ("NIP", "PIN number", "NIP"),
                ("cliente", "client", "client"), ("cifrado", "encrypted", "xifrat"), ("existente", "existing", "existent"),
                ("ventanilla de cajas", "teller window", "taquilla"), ("lobby", "lobby", "lobby"), ("extranjera", "foreign", "estrangera"),
                ("ejecutivo", "executive/officer", "executiu"), ("protección", "protection", "protecció"), ("cobertura", "coverage", "cobertura"),
                ("notificación", "notification", "notificació"), ("alerta", "alert", "alerta"), ("mensaje", "message", "missatge"),
                # Encounter 31-35
                ("sobregiro", "overdraft", "sobregir"), ("penalidad", "penalty", "penalització"), ("recargo", "surcharge", "recàrrec"),
                ("asesoramiento", "advisory", "assessorament"), ("orientación", "guidance", "orientació"), ("rendimiento", "yield/return", "rendiment"),
                ("fideicomiso", "trust", "fideïcomís"), ("patrimonio", "assets", "patrimoni"), ("herencia", "inheritance", "herència"),
                ("poder notarial", "power of attorney", "poder notarial"), ("apoderado", "authorized agent", "apoderat"), ("representante", "representative", "representant"),
                ("nómina", "payroll", "nòmina"), ("domiciliar", "to set up direct deposit", "domiciliar"), ("automático", "automatic", "automàtic"),
                # Encounter 36-40
                ("auditoría", "audit", "auditoria"), ("verificar", "to verify", "verificar"), ("cumplimiento", "compliance", "compliment"),
                ("expedición", "issuance", "expedició"), ("plástico", "card/plastic", "plàstic"), ("renovar", "to renew", "renovar"),
                ("sucursal principal", "main branch", "sucursal principal"), ("gerente", "manager", "gerent"), ("cita", "appointment", "cita"),
                ("bóveda", "vault", "bóveda"), ("caja fuerte", "safe deposit box", "caja forta"), ("estado financiero", "financial statement", "estat financer"),
                ("transacción", "transaction", "transacció"), ("retención", "withholding", "retenció"), ("declaración", "declaration", "declaració"),
                # Encounter 41-45
                ("cuenta conjunta", "joint account", "compte conjunt"), ("mancomunada", "joint/shared", "mancomunada"), ("separada", "separate", "separada"),
                ("tarjeta adicional", "additional card", "targeta addicional"), ("operación bancaria", "banking operation", "operació bancària"), ("aumentar", "to increase", "augmentar"),
                ("fraude", "fraud", "fraude"), ("bloquear", "to block", "bloquejar"), ("reportar", "to report", "reportar"),
                ("token", "token", "token"), ("autenticación", "authentication", "autenticació"), ("verificación", "verification", "verificació"),
                ("divisa", "foreign currency", "divisa"), ("póliza", "policy", "pòlissa"), ("cotización", "quote", "cotització"),
                # Encounter 46-50
                ("corresponsal", "correspondent bank", "corresponsal"), ("intermediario", "intermediary", "intermediari"), ("red", "network", "xarxa"),
                ("respaldo", "backing/support", "respaldo"), ("normativa", "policy", "normativa"), ("activo", "asset", "actiu"),
                ("cuentas por pagar", "accounts payable", "compte a pagar"), ("constancia", "proof/certificate", "constància"), ("rédito", "return/interest", "rèdit"),
                ("asesor", "advisor", "assessor"), ("consultoría", "consulting", "consultoria"), ("planificación", "planning", "planificació"),
                ("bienvenido", "welcome", "benvingut"), ("servicio al cliente", "customer service", "servei al client"), ("satisfacción", "satisfaction", "satisfacció"),
            ],
        },
        {
            "title": "Wire Transfer",
            "goal": "Complete a wire transfer by giving the teller the recipient details",
            "word_prefix": "bank_wire",
            "words": [
                # Encounter 1-5 (basic essentials)
                ("giro bancario", "bank draft", "giro bancari"), ("remesa", "remittance", "remesa"), ("canalizar", "to channel", "canalitzar"),
                ("depositante", "depositor", "dipositant"), ("receptor bancario", "bank receiver", "receptor bancari"), ("acreditado", "credited party", "acreditat"),
                ("monto", "amount", "import"), ("cifra", "figure/amount", "xifra"), ("receptor", "receiving", "receptor"),
                ("institución", "institution", "institució"), ("girado", "drawn on", "girador"), ("referencia", "reference", "referència"),
                ("titular de cuenta", "account holder", "titular de compte"), ("dígitos", "digits", "dígits"), ("clave de rastreo", "tracking code", "clau de rastreig"),
                # Encounter 6-10
                ("validar", "to validate", "validar"), ("costo", "cost", "cost"), ("información bancaria", "bank info", "informació bancària"),
                ("cotejar", "to compare/verify", "cotejar"), ("descontar", "to deduct", "descomptar"), ("doméstico", "domestic", "domèstic"),
                ("foráneo", "foreign", "estranger"), ("inmediato", "immediate", "immediat"), ("nación", "nation", "nació"),
                ("lapso", "timespan", "temps"), ("instantáneo", "instant", "instantani"), ("tardanza", "tardiness", "retard"),
                ("constancia de pago", "payment receipt", "constància de pagament"), ("justificante", "voucher", "justificant"), ("suficiente", "sufficient", "suficient"),
                # Encounter 11-15
                ("código SWIFT", "SWIFT code", "codi SWIFT"), ("copiar", "to copy", "copiar"), ("interbancario", "interbank", "interbancari"),
                ("bastante", "enough", "bastant"), ("dólar", "dollar", "dòlar"), ("clave bancaria", "bank code", "clau bancària"),
                ("tipo de cambio", "exchange rate", "tipus de canvi"), ("conversión", "conversion", "conversió"), ("equivalente", "equivalent", "equivalent"),
                ("llave interbancaria", "interbank key", "clau interbancària"), ("red bancaria", "bank network", "xarxa bancària"), ("divisa extranjera", "foreign currency", "divisa estrangera"),
                ("billete verde", "greenback", "bitllet verd"), ("máximo", "maximum", "màxim"), ("moneda local", "local currency", "moneda local"),
                # Encounter 16-20
                ("programar", "to schedule", "programar"), ("fecha", "date", "data"), ("recurrente", "recurring", "recurrent"),
                ("paridad cambiaria", "exchange parity", "paritat canviària"), ("modificar", "to modify", "modificar"), ("corregir", "to correct", "corregir"),
                ("tasa de cambio", "exchange rate", "taxa de canvi"), ("equiparable", "comparable", "equiparable"), ("solicitud de envío", "send request", "sol·licitud d\'enviament"),
                ("rellenar", "to fill in", "omplir"), ("rubricar", "to initial/sign", "rubricar"), ("tope", "cap", "topall"),
                ("origen", "origin", "origen"), ("emisor", "sender/issuer", "emissor"), ("ordenante", "originator", "ordenant"),
                # Encounter 21-25
                ("acreditar", "to credit", "acreditar"), ("debitar", "to debit", "debitar"), ("procesar", "to process", "processar"),
                ("cifra máxima", "maximum amount", "xifra màxima"), ("pendiente", "pending", "pendent"), ("completado", "completed", "completat"),
                ("rastrear", "to track", "rastrejar"), ("seguimiento", "tracking", "seguiment"), ("código", "code", "codi"),
                ("cotidiano", "daily/everyday", "quotidià"), ("plaza", "city/location", "plaça"), ("agendar", "to schedule", "agendar"),
                ("urgente", "urgent", "urgent"), ("prioritario", "priority", "prioritari"), ("express", "express", "exprés"),
                # Encounter 26-30
                ("anular", "to void", "anular"), ("editar", "to edit", "editar"), ("enmendar", "to amend", "enmendar"),
                ("aviso", "notice", "avís"), ("correo electrónico", "email", "correu electrònic"), ("texto", "text message", "text"),
                ("error", "error", "error"), ("rechazar", "to reject", "rechazar"), ("clave secreta", "secret code", "clau secreta"),
                ("procedencia", "origin/source", "procedència"), ("insuficiente", "insufficient", "insuficient"), ("cubrir", "to cover", "cubrir"),
                ("lote", "batch", "lot"), ("múltiple", "multiple", "múltiple"), ("masivo", "bulk", "massiu"),
                # Encounter 31-35
                ("solicitante", "applicant", "sol·licitant"), ("abonar", "to credit", "abonar"), ("ruta", "route", "ruta"),
                ("demora bancaria", "bank delay", "demora bancària"), ("hábil", "business (day)", "hàbil"), ("calendario", "calendar", "calendari"),
                ("reversar", "to reverse", "reversar"), ("devolución", "return/refund", "devolució"), ("original", "original", "original"),
                ("duplicado", "duplicate", "duplicat"), ("detectar", "to detect", "detectar"), ("prevenir", "to prevent", "prevenir"),
                ("IBAN", "IBAN", "IBAN"), ("cuenta CLABE", "CLABE account", "compte CLABE"), ("formato", "format", "format"),
                # Encounter 36-40
                ("beneficiario final", "ultimate beneficiary", "beneficiari final"), ("cargar", "to charge", "carregar"), ("concepto", "concept/description", "concepte"),
                ("tramitar", "to process", "tramitar"), ("en espera", "on hold", "en espera"), ("proveedor", "supplier", "proveïdor"),
                ("finalizado", "finalized", "finalitzat"), ("empleado", "employee", "empleat"), ("salario", "salary", "salari"),
                ("alquiler", "rent", "lloguer"), ("hipoteca", "mortgage", "hipoteca"), ("mensualidad", "monthly payment", "mensualitat"),
                ("localizar", "to locate", "localitzar"), ("monitorear", "to monitor", "monitorejar"), ("portafolio", "portfolio", "cartera"),
                # Encounter 41-45
                ("lavado de dinero", "money laundering", "blanqueig de diners"), ("prevención", "prevention", "prevenció"), ("referencia bancaria", "bank reference", "referència bancària"),
                ("tratado", "treaty", "tractat"), ("bilateral", "bilateral", "bilateral"), ("filial", "subsidiary", "filial"),
                ("domicilio bancario", "bank address", "domicili bancari"), ("apremiante", "pressing", "apremiant"), ("documentar", "to document", "documentar"),
                ("digital", "digital", "digital"), ("preferencial", "preferential", "preferencial"), ("veloz", "fast", "veloz"),
                ("blockchain", "blockchain", "blockchain"), ("cripto", "crypto", "cripto"), ("billetera digital", "digital wallet", "cartera digital"),
                # Encounter 46-50
                ("norma bancaria", "banking rule", "norma bancària"), ("fiduciario", "fiduciary", "fiduciari"), ("garantía", "guarantee", "garantia"),
                ("penalización", "penalty", "penalització"), ("reglamento", "rules", "reglament"), ("sanción", "sanction", "sanció"),
                ("disputa", "dispute", "disputa"), ("acatar", "to comply with", "acatar"), ("resolución", "resolution", "resolució"),
                ("exitoso", "successful", "exitós"), ("recibido", "received", "rebut"), ("deducción", "deduction", "deducció"),
                ("gracias", "thank you", "gràcies"), ("finalizar", "to finalize", "finalitzar"), ("completar", "to complete", "completar"),
            ],
        },
        {
            "title": "Currency Exchange",
            "goal": "Exchange your currency by negotiating with the teller",
            "word_prefix": "bank_exchange",
            "words": [
                # Encounter 1-5 (basic essentials)
                ("trocar", "to barter", "intercanviar"), ("capital", "capital/money", "capital"), ("dólar americano", "US dollar", "dòlar americà"),
                ("moneda mexicana", "Mexican currency", "moneda mexicana"), ("moneda europea", "European currency", "moneda europea"), ("euro", "euro", "euro"),
                ("cotización del día", "today's rate", "cotització del dia"), ("tarifa cambiaria", "exchange fee", "tarifa canviària"), ("jornada", "trading day", "jornada"),
                ("comprar", "to buy", "comprar"), ("vender", "to sell", "vendre"), ("adquirir", "to acquire", "adquirir"),
                ("enajenar", "to sell/dispose", "enajenar"), ("billete", "banknote", "bitllet"), ("centavo", "cent/coin", "centau"),
                # Encounter 6-10
                ("billetes", "banknotes/bills", "bitllets"), ("papel moneda", "paper money", "paper moneda"), ("gratis", "free", "gratuït"),
                ("casa de cambio", "exchange office", "casa de canvi"), ("centésimo", "hundredth/cent", "centèsim"), ("cargo por cambio", "exchange charge", "càrrec per canvi"),
                ("sin cargo", "no charge", "sense càrrec"), ("bureau de cambio", "exchange bureau", "bureau de canvi"), ("mostrar", "to show", "mostrar"),
                ("módulo cambiario", "exchange counter", "mòdul canviari"), ("operador", "operator", "operador"), ("guardar", "to keep", "guardar"),
                ("credencial", "credential", "credencial"), ("cuánto", "how much", "quant"), ("documento de viaje", "travel document", "document de viatge"),
                # Encounter 11-15
                ("exhibir", "to show/display", "exhibir"), ("peor", "worse", "pitjor"), ("comparar", "to compare", "comparar"),
                ("boleta de cambio", "exchange slip", "boleta de canvi"), ("paralelo", "parallel/unofficial", "paral·lel"), ("conservar", "to keep/preserve", "conservar"),
                ("subir", "to go up", "pujar"), ("bajar", "to go down", "baixar"), ("estable", "stable", "estable"),
                ("denominación", "denomination", "denominació"), ("suma", "sum", "suma"), ("cuántos", "how many", "quants"),
                ("cambio exacto", "exact change", "canvi exacte"), ("suelto", "loose change", "solt"), ("feria", "small change", "fira"),
                # Encounter 16-20
                ("cheque de viajero", "traveler's check", "xec de viatger"), ("monto total", "total amount", "munt total"), ("canjear", "to cash/redeem", "canviar"),
                ("inferior", "worse/lower", "inferior"), ("contrastar", "to contrast", "contrastat"), ("mínimo", "minimum", "mínim"),
                ("autorizado", "authorized", "autoritzat"), ("informal", "informal", "informal"), ("local", "local", "local"),
                ("negociar", "to negotiate", "negociar"), ("plaza cambiaria", "exchange market", "plaça canviària"), ("incrementar", "to increase", "incrementar"),
                ("libra", "pound", "llibre"), ("yen", "yen", "ien"), ("franco", "franc", "franc"),
                # Encounter 21-25
                ("fluctuar", "to fluctuate", "fluctuar"), ("variación", "variation", "variació"), ("diferencia", "difference", "diferència"),
                ("disminuir", "to decrease", "disminuir"), ("pérdida", "loss", "pèrdua"), ("margen", "margin", "marge"),
                ("constante", "constant", "constant"), ("billete grande", "large bill", "bitllet gran"), ("billete chico", "small bill", "bitllet petit"),
                ("banco central", "central bank", "banc central"), ("billete menudo", "small denomination", "bitllet menuda"), ("cambio justo", "fair change", "canvi just"),
                ("turista", "tourist", "turista"), ("viajero", "traveler", "viatger"), ("residente", "resident", "resident"),
                # Encounter 26-30
                ("transferir", "to transfer", "transferir"), ("moneda fraccionaria", "fractional currency", "moneda fraccionària"), ("vuelto", "change/remainder", "volta"),
                ("cheque viajero", "traveler's check", "xec viatger"), ("cobrar cheque", "to cash a check", "cobrar xec"), ("máxima cantidad", "maximum quantity", "màxima quantitat"),
                ("cantidad mínima", "minimum quantity", "quantitat mínima"), ("cajero automático", "ATM", "caixer automàtic"), ("moneda foránea", "foreign coin", "moneda estrangera"),
                ("de fuera", "from abroad", "de fora"), ("proteger", "to protect", "protegir"), ("cuidar", "to take care", "cuidar"),
                ("falsificado", "counterfeit", "falsificat"), ("de aquí", "from here", "d\'aquí"), ("auténtico", "authentic", "autèntic"),
                # Encounter 31-35
                ("pactar", "to agree", "pactar"), ("convenir", "to agree/suit", "convenir"), ("actualizar", "to update", "actualitzar"),
                ("libra esterlina", "pound sterling", "llibre esterlina"), ("yen japonés", "Japanese yen", "ien japonès"), ("cerrado", "closed", "tancat"),
                ("franco suizo", "Swiss franc", "franc suís"), ("oscilar", "to oscillate", "oscilar"), ("movimiento cambiario", "exchange movement", "moviment canviari"),
                ("brecha", "gap", "bretxa"), ("utilidad", "profit/utility", "utilitat"), ("metal", "metal", "metall"),
                ("inflación", "inflation", "inflació"), ("devaluación", "devaluation", "devaluació"), ("revaluación", "revaluation", "revaluació"),
                # Encounter 36-40
                ("spread", "spread", "spread"), ("diferencial", "differential", "diferencial"), ("quebranto", "loss/damage", "quebrant"),
                ("diferencia cambiaria", "exchange difference", "diferència canviària"), ("bitcoin", "bitcoin", "bitcoin"), ("papel oficial", "official document", "paper oficial"),
                ("copia original", "original copy", "còpia original"), ("banco emisor", "issuing bank", "banc emissor"), ("exento", "exempt", "exempt"),
                ("norma cambiaria", "exchange regulation", "norma canviària"), ("facultar", "to authorize", "facultar"), ("límite de efectivo", "cash limit", "límite d\'efectiu"),
                ("visitante", "visitor", "visitant"), ("habitante", "resident/inhabitant", "habitants"), ("traspasar", "to transfer", "traspassar"),
                # Encounter 41-45
                ("cuenta destino", "destination account", "compte de destí"), ("tarjeta bancaria", "bank card", "targeta bancària"), ("tarjeta de viaje", "travel card", "targeta de viatge"),
                ("sacar dinero", "to withdraw", "treure diners"), ("dispensador", "dispenser", "dispensador"), ("accesible", "accessible", "accessible"),
                ("reservar", "to reserve", "reservar"), ("separar", "to set aside", "separar"), ("apartar", "to put aside", "apartat"),
                ("resguardado", "safe/guarded", "resguardat"), ("postal", "postal", "postal"), ("telegráfico", "telegraphic", "telegràfic"),
                ("paridad", "parity", "paritat"), ("equilibrio", "equilibrium", "equilibri"), ("balanza", "balance", "balança"),
                # Encounter 46-50
                ("especulación", "speculation", "especulació"), ("blindar", "to protect", "blindar"), ("custodiar", "to guard", "custodiar"),
                ("billete falso", "counterfeit bill", "bitllet fals"), ("futuro", "futures", "futur"), ("derivado", "derivative", "derivat"),
                ("regulador", "regulator", "regulador"), ("supervisor", "supervisor", "supervisor"), ("legítimo", "legitimate", "legítim"),
                ("favorable", "favorable", "favorable"), ("conveniente", "convenient", "convenient"), ("ventajoso", "advantageous", "avantatjós"),
                ("operación exitosa", "successful transaction", "operació exitosa"), ("satisfecho", "satisfied", "satisfet"), ("completo", "complete", "complet"),
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
                ("talla", "size", "talla"), ("probador", "fitting room", "provador"), ("descuento", "discount", "descompte"),
                ("camisa", "shirt", "camisa"), ("pantalón", "pants", "pantaló"), ("zapatos", "shoes", "sabates"),
                ("prenda", "garment", "peça"), ("color", "color", "color"), ("vestidor", "dressing room", "vestidor"),
                ("rebaja", "markdown", "rebaixa"), ("playera", "t-shirt", "samarreta"), ("mediano", "medium", "mitjà"),
                ("buscar", "to look for", "buscar"), ("bermuda", "shorts", "bermuda"), ("sandalia", "sandal", "sandàlia"),
                # Encounter 6-10
                ("probarse", "to try on", "provar-se"), ("quedar", "to fit", "quedar"), ("tono", "tone/shade", "to"),
                ("ajustado", "tight", "ajustat"), ("flojo", "loose", "fluix"), ("cómodo", "comfortable", "còmode"),
                ("vestido", "dress", "vestit"), ("falda", "skirt", "falda"), ("blusa", "blouse", "blusa"),
                ("manga", "sleeve", "manga"), ("boutique", "boutique", "botiga"), ("holgado", "roomy", "holgat"),
                ("reducido", "small/reduced", "reduït"), ("tela", "fabric", "tela"), ("intermedio", "medium/intermediate", "intermedi"),
                # Encounter 11-15
                ("devolver", "to return", "devolver"), ("explorar", "to explore", "explorar"), ("requerir", "to require", "requerir"),
                ("medirse", "to try on (oneself)", "mesurar-se"), ("oferta", "offer/deal", "oferta"), ("temporada", "season", "temporada"),
                ("cremallera", "zipper", "cremallera"), ("botón", "button", "botó"), ("sentar", "to fit/suit", "seure"),
                ("ancho", "wide", "ample"), ("estrecho", "narrow", "estret"), ("entallado", "fitted", "entallat"),
                ("adecuado", "suitable", "adequat"), ("ceñido", "tight-fitting", "ceñit"), ("azul", "blue", "blau"),
                # Encounter 16-20
                ("agradable", "comfortable/pleasant", "agradable"), ("maxi", "maxi dress", "maxi"), ("gris", "gray", "gris"),
                ("estampado", "printed/patterned", "estampat"), ("liso", "plain", "llis"), ("rayas", "stripes", "ratlles"),
                ("elegante", "elegant", "elegant"), ("casual", "casual", "casual"), ("formal", "formal", "formal"),
                ("minifalda", "mini skirt", "minifaldilla"), ("corbata", "tie", "corbata"), ("pañuelo", "scarf/handkerchief", "mocador"),
                ("marca", "brand", "marca"), ("camiseta", "t-shirt/blouse", "samarreta"), ("resistente", "durable", "resistent"),
                # Encounter 21-25
                ("abrigo", "coat", "abric"), ("chaqueta", "jacket", "jaqueta"), ("suéter", "sweater", "suèter"),
                ("puño largo", "long sleeve", "puny llarg"), ("calcetín", "sock", "mitjó"), ("media", "stocking", "mitja"),
                ("tacón", "heel", "taló"), ("suela", "sole", "sola"), ("extenso", "long/extended", "extens"),
                ("joyería", "jewelry", "joieria"), ("anillo", "ring", "anell"), ("collar", "necklace", "collar"),
                ("gafas", "glasses", "ulleres"), ("sombrero", "hat", "barret"), ("gorra", "cap", "gorra"),
                # Encounter 26-30
                ("lavar", "to wash", "rentar"), ("planchar", "to iron", "planxar"), ("secar", "to dry", "secar"),
                ("coser", "to sew", "cosir"), ("arreglar", "to alter/fix", "arreglar"), ("sastre", "tailor", "sastre"),
                ("diseño", "design", "disseny"), ("breve", "short/brief", "breu"), ("colección", "collection", "col·lecció"),
                ("probador ocupado", "fitting room occupied", "provador ocupat"), ("fibra de algodón", "cotton fiber", "fibra de cotó"), ("tejido", "woven fabric", "teixit"),
                ("talla única", "one size", "talla única"), ("extra grande", "extra large", "extra gran"), ("extra pequeño", "extra small", "extra petit"),
                # Encounter 31-35
                ("componente", "component", "component"), ("reintegrar", "to return/refund", "reintegrar"), ("lino", "linen", "lli"),
                ("poliéster", "polyester", "polièster"), ("sintético", "synthetic", "sintètic"), ("elástico", "elastic/stretchy", "elàstic"),
                ("moda", "fashion", "moda"), ("tendencia", "trend", "tendència"), ("estilo", "style", "estil"),
                ("traje", "suit", "traje"), ("esmoquin", "tuxedo", "esmoquin"), ("intercambiar", "to exchange", "intercanviar"),
                ("impermeable", "waterproof", "impermeable"), ("térmico", "thermal", "tèrmic"), ("ligero", "lightweight", "lleuger"),
                # Encounter 36-40
                ("bordado", "embroidered", "bordat"), ("encaje", "lace", "encaix"), ("flecos", "fringe", "franges"),
                ("solapa", "lapel", "solapa"), ("puño", "cuff", "puny"), ("comprobante de compra", "proof of purchase", "comprovant de compra"),
                ("cierre", "fastener/closure", "tancament"), ("broche", "clasp", "brotxa"), ("hebilla", "buckle", "fivella"),
                ("planchado", "pressed", "planxat"), ("arrugado", "wrinkled", "arrugat"), ("manchado", "stained", "taumat"),
                ("guardarropa", "wardrobe", "guarda-roba"), ("percha", "hanger", "penja-robes"), ("liquidación", "clearance", "liquidació"),
                # Encounter 41-45
                ("confección", "tailoring", "confecció"), ("ganga", "bargain", "ganga"), ("cinta métrica", "measuring tape", "cinta mètrica"),
                ("patronaje", "pattern-making", "patronatge"), ("molde", "pattern/mold", "motlle"), ("cortar", "to cut", "tallar"),
                ("exhibición", "display", "exhibició"), ("época de rebajas", "sale season", "època de rebaixes"), ("maniquí", "mannequin", "maniquí"),
                ("exclusivo", "exclusive", "exclusiu"), ("limitado", "limited", "limitada"), ("edición", "edition", "edició"),
                ("ecológico", "eco-friendly", "ecològic"), ("sostenible", "sustainable", "sostenible"), ("reciclado", "recycled", "reciclat"),
                # Encounter 46-50
                ("alta costura", "haute couture", "alta costura"), ("cierre relámpago", "zipper", "tancament de cremallera"), ("diseñador", "designer", "dissenyador"),
                ("personalizado", "customized", "personalitzat"), ("ojal", "buttonhole", "ull"), ("hecho a mano", "handmade", "fet a mà"),
                ("compartimiento", "compartment", "compartiment"), ("angosto", "narrow/tight", "estret"), ("a la medida", "tailored", "a mida"),
                ("celeste", "sky blue", "celeste"), ("perfecto", "perfect", "perfecte"), ("ideal", "ideal", "ideal"),
                ("carmesí", "crimson", "carmesí"), ("compra", "purchase", "compra"), ("bolsa", "bag", "bossa"),
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
                ("plomero", "plumber", "lampista"), ("fontanero", "plumber", "fontaner"), ("desperfecto", "defect", "desperfecte"),
                ("componer", "to fix", "compondre"), ("tubo", "pipe", "tub"), ("fuga", "leak", "fuga"),
                ("conducto", "conduit", "conducte"), ("goteo", "drip", "goteig"), ("lavabo", "sink", "lavabo"),
                ("sanitario", "bathroom/toilet", "sanitari"), ("área de cocina", "kitchen area", "àrea de cuina"), ("fregadero", "kitchen sink", "fregadero"),
                ("de emergencia", "emergency", "d\'emergència"), ("precisar", "to need", "precisar"), ("ayuda", "help", "ajuda"),
                # Encounter 6-10
                ("socorro", "help/aid", "socors"), ("grifo de agua", "water tap", "griferia d\'aigua"), ("gotear", "to drip", "gotejar"),
                ("cañería", "plumbing/pipes", "canonada"), ("drenaje", "drain", "drenatge"), ("tapado", "clogged", "tapat"),
                ("reparar", "to repair", "reparar"), ("instalar", "to install", "instal·lar"), ("canilla", "tap/spigot", "canella"),
                ("escurrir", "to drip/drain", "escórrer"), ("pieza", "part/piece", "peça"), ("red de tuberías", "pipe network", "xarxa de canonades"),
                ("desagüe", "drain", "desguàs"), ("obstruido", "blocked", "obstruït"), ("cuándo", "when", "quan"),
                # Encounter 11-15
                ("inodoro", "toilet", "inodor"), ("regadera", "shower", "regadora"), ("tina", "bathtub", "tina"),
                ("calentador", "water heater", "calentador"), ("restaurar", "to restore", "restaurar"), ("montar", "to install/mount", "muntar"),
                ("roto", "broken", "trencat"), ("dañado", "damaged", "danyat"), ("reemplazar", "to replace", "substituir"),
                ("insumo", "supply", "insum"), ("utensilio", "utensil/tool", "utensili"), ("agenda de trabajo", "work schedule", "agenda de treball"),
                ("en qué momento", "at what time", "en quin moment"), ("duración", "duration", "durada"), ("excusado", "toilet", "excusat"),
                # Encounter 16-20
                ("mano de obra", "labor", "mà d\'obra"), ("ducha", "shower", "duxa"), ("bañera", "bathtub", "banyera"),
                ("boiler", "boiler", "boiler"), ("depósito de agua", "water tank", "dipòsit d\'aigua"), ("flujo", "flow", "flux"),
                ("averiado", "broken down", "avariat"), ("maltratado", "damaged", "maltractat"), ("junta", "joint/gasket", "junta"),
                ("válvula", "valve", "vàlvula"), ("recién comprado", "newly bought", "recent comprat"), ("pieza de recambio", "replacement part", "peça de recanvi"),
                ("de fábrica", "factory-made", "de fàbrica"), ("respaldo de producto", "product warranty", "respatllament de producte"), ("calcular", "to calculate", "calcular"),
                # Encounter 21-25
                ("permiso", "permit", "permiss"), ("licencia", "license", "llicència"), ("tiempo de vida", "lifespan", "temps de vida"),
                ("grado", "grade/quality", "grau"), ("trabajo manual", "manual labor", "treball manual"), ("recomendación", "recommendation", "recomanació"),
                ("desatascar", "to unclog", "desatascar"), ("destapador", "plunger", "destapador"), ("sonda", "drain snake", "sonda"),
                ("humedad", "humidity/moisture", "humitat"), ("moho", "mold", "moh"), ("filtración", "seepage", "filtració"),
                ("bomba", "pump", "bomba"), ("por hora", "per hour", "per hora"), ("eléctrico", "electric", "elèctric"),
                # Encounter 26-30
                ("nota de cobro", "bill", "nota de cobrament"), ("en billetes", "in cash", "en bitllets"), ("sistema de tuberías", "pipe system", "sistema de canonades"),
                ("adelanto", "advance payment", "adelantament"), ("enlace", "joint/link", "enllaç"), ("liquidar", "to settle/pay off", "liquidar"),
                ("sótano", "basement", "soterrani"), ("empaque", "gasket/seal", "empaquetatge"), ("llave de paso", "shutoff valve", "clau de pas"),
                ("excavación", "excavation", "excavació"), ("zanja", "trench", "fossat"), ("cavar", "to dig", "cavar"),
                ("control de agua", "water control", "control d\'aigua"), ("PVC", "PVC", "PVC"), ("galvanizado", "galvanized", "galvanitzat"),
                # Encounter 31-35
                ("sellador", "sealant", "segellador"), ("sellar", "to seal", "segellar"), ("altura", "height", "altura"),
                ("dimensión", "dimension", "dimensió"), ("soldar", "to weld/solder", "soldar"), ("estimar", "to estimate", "estimar"),
                ("autorización", "authorization", "autorització"), ("revisar", "to check/inspect", "revisar"), ("habilitación", "certification", "habilitació"),
                ("cisterna", "cistern", "cisterna"), ("aljibe", "water tank", "aljibe"), ("tinaco", "rooftop tank", "tinaco"),
                ("residuo", "residue", "residu"), ("obstrucción", "obstruction", "obstrucció"), ("limpiar", "to clean", "netejar"),
                # Encounter 36-40
                ("diploma", "diploma", "diploma"), ("trayectoria", "track record", "trajectòria"), ("daño", "damage", "dany"),
                ("antigüedad laboral", "work seniority", "antiguitat laboral"), ("referencia laboral", "job reference", "referència laboral"), ("reclamar", "to claim", "reclamar"),
                ("calefacción", "heating", "calefacció"), ("radiador", "radiator", "radiador"), ("termostato", "thermostat", "termostat"),
                ("gas", "gas", "gas"), ("destapar", "to unclog", "destapar"), ("sopapa", "plunger", "sopapa"),
                ("ventilación", "ventilation", "ventilació"), ("extractor", "extractor fan", "extractor"), ("ducto", "duct", "ducte"),
                # Encounter 41-45
                ("purificador", "purifier", "purificador"), ("filtro", "filter", "filtre"), ("suavizador", "water softener", "suavitzador"),
                ("riego", "irrigation", "reg"), ("cable de drenaje", "drain cable", "cable de drenatge"), ("aspersor", "sprinkler", "aspersor"),
                ("fosa séptica", "septic tank", "fossa sèptica"), ("drenaje pluvial", "storm drain", "drenatge pluvial"), ("alcantarilla", "sewer", "alcantarilla"),
                ("medidor", "meter", "mesurador"), ("consumo", "consumption", "consum"), ("lectura", "reading", "lectura"),
                ("remodelación", "remodeling", "remodelació"), ("ampliación", "expansion", "ampliació"), ("condensación", "condensation", "condensació"),
                # Encounter 46-50
                ("hongo", "fungus", "fong"), ("infiltración", "infiltration", "infiltració"), ("bomba de agua", "water pump", "bomba d\'aigua"),
                ("subcontratista", "subcontractor", "subcontractista"), ("equipo", "team/equipment", "equip"), ("impulsor", "impeller", "impulsor"),
                ("de corriente", "electric-powered", "de corrent"), ("convenio", "contract/agreement", "conveni"), ("terminar", "to finish", "terminar"),
                ("recomendar", "to recommend", "recomanar"), ("pacto", "agreement/pact", "pacte"), ("reseña", "review", "reseña"),
                ("buen trabajo", "good job", "bon treball"), ("pago inicial", "initial payment", "pagament inicial"), ("agradecer", "to thank", "agrair"),
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
                ("supermercado", "supermarket", "supermercat"), ("autoservicio", "self-service store", "autoservei"), ("lista", "list", "llista"),
                ("listado", "list/checklist", "llistat"), ("fruta fresca", "fresh fruit", "fruit fresc"), ("vegetal", "vegetable", "vegetal"),
                ("res", "beef", "res"), ("hogaza", "loaf of bread", "molla"), ("lácteo", "dairy", "làctic"),
                ("blanquillo", "egg", "blanquillo"), ("barato", "cheap", "barat"), ("caro", "expensive", "car"),
                ("costoso", "expensive", "costós"), ("carrito", "cart", "carret"), ("canasta", "basket", "cistella"),
                # Encounter 6-10
                ("funda", "bag", "fundes"), ("carro de compras", "shopping cart", "carro de compres"), ("sección", "section", "secció"),
                ("fresco", "fresh", "fresc"), ("congelado", "frozen", "congelat"), ("enlatado", "canned", "en conserva"),
                ("cesta", "basket", "cistella"), ("corredor", "aisle/corridor", "corredor"), ("anaquel", "shelf", "estanteria"),
                ("departamento", "department", "departament"), ("recién cortado", "freshly cut", "recent tallat"), ("pasta", "pasta", "pasta"),
                ("bajo cero", "frozen", "baix zero"), ("en conserva", "preserved", "en conserva"), ("pechuga", "chicken breast", "pit"),
                # Encounter 11-15
                ("caja", "checkout/cashier", "caja"), ("filete de pescado", "fish fillet", "filet de peix"), ("lomo", "pork loin", "llom"),
                ("grano", "grain", "gra"), ("fideos", "noodles", "fideus"), ("promoción", "promotion", "promoció"),
                ("kilo", "kilogram", "kilo"), ("gramo", "gram", "gram"), ("litro", "liter", "litre"),
                ("maduro", "ripe", "madur"), ("aceite de oliva", "olive oil", "oli d\'oliva"), ("podrido", "rotten", "podrit"),
                ("orgánico", "organic", "orgànic"), ("sal de mesa", "table salt", "sal de taula"), ("integral", "whole grain", "integral"),
                # Encounter 16-20
                ("panadería", "bakery", "panaderia"), ("carnicería", "butcher shop", "carnisseria"), ("pescadería", "fish counter", "peixateria"),
                ("endulzante", "sweetener", "endolcidor"), ("caja registradora", "cash register", "caixa registradora"), ("kilogramo", "kilogram", "quilogram"),
                ("bebida", "drink", "beguda"), ("jugo", "juice", "sucre"), ("medio kilo", "half kilo", "mitja quilo"),
                ("medio litro", "half liter", "mitja litre"), ("cereal", "cereal", "cereal"), ("chocolate", "chocolate", "xocolata"),
                ("condimento", "condiment", "condiment"), ("salsa", "sauce", "salsa"), ("en su punto", "ripe/ready", "en el seu punt"),
                # Encounter 21-25
                ("sin madurar", "unripe", "sense madurar"), ("ingrediente", "ingredient", "ingredient"), ("preparar", "to prepare", "preparar"),
                ("echado a perder", "spoiled", "estroncat"), ("genérico", "generic", "genèric"), ("importado", "imported", "importat"),
                ("bio", "organic/bio", "bio"), ("sin procesar", "unprocessed", "sense processar"), ("caducidad", "expiration", "caducitat"),
                ("refrigerador", "refrigerator section", "refrigerador"), ("congelador", "freezer section", "congelador"), ("ambiente", "room temperature", "ambient"),
                ("limpieza", "cleaning", "netedat"), ("de grano entero", "whole grain", "de gra sencer"), ("horno de pan", "bread oven", "forn de pa"),
                # Encounter 26-30
                ("local de carnes", "meat counter", "local de carn"), ("servilleta", "napkin", "tovalló"), ("aluminio", "aluminum foil", "alumini"),
                ("especia", "spice", "espècia"), ("mostrador de pescado", "fish counter", "taulell de peix"), ("canela", "cinnamon", "canel·la"),
                ("harina", "flour", "farina"), ("levadura", "yeast", " llevat"), ("producto lácteo", "dairy product", "producte làctic"),
                ("nuez", "nut", "nou"), ("almendra", "almond", "ametlla"), ("cacahuate", "peanut", "cacauet"),
                ("fiambre", "deli meat", "embotit"), ("queso fresco", "fresh cheese", "formatge fresc"), ("salchicha", "sausage", "salsitxa"),
                # Encounter 31-35
                ("yogur natural", "natural yogurt", "iogurt natural"), ("refresco", "soft drink", "refresc"), ("ajo", "garlic", "all"),
                ("jugo natural", "natural juice", "sucre natural"), ("zanahoria", "carrot", "pastanaga"), ("agua mineral", "mineral water", "aigua mineral"),
                ("bizcocho", "biscuit", "bescuit"), ("plátano", "banana", "plàtan"), ("golosina", "candy/sweet", "golosina"),
                ("aderezo", "dressing", "aderezo"), ("fresa", "strawberry", "mora"), ("uva", "grape", "raïm"),
                ("atún", "tuna", "tonyina"), ("sardina", "sardine", "sardina"), ("salsa picante", "hot sauce", "salsa picant"),
                # Encounter 36-40
                ("tortilla", "tortilla", "truita"), ("tostada", "toast/tostada", "tostada"), ("crema", "cream/sour cream", "crema"),
                ("aceto", "vinegar", "vinagre"), ("chile", "chili pepper", "xile"), ("cilantro", "cilantro", "cilantre"),
                ("fórmula", "recipe/formula", "fórmula"), ("cerveza", "beer", "cervesa"), ("vino", "wine", "vi"),
                ("pañal", "diaper", "bolquer"), ("elaborar", "to prepare", "elaborar"), ("sello comercial", "brand/trademark", "segell comercial"),
                ("mascota", "pet", "mascota"), ("alimento", "food/feed", "aliment"), ("lata", "can", "llauna"),
                # Encounter 41-45
                ("gourmet", "gourmet", "gourmet"), ("delicatessen", "delicatessen", "delicatessen"), ("especialidad", "specialty", "especialitat"),
                ("libre de gluten", "gluten-free", "lliure de gluten"), ("vegano", "vegan", "vegà"), ("sin lactosa", "lactose-free", "sense lactosa"),
                ("sin marca", "generic/unbranded", "sense marca"), ("báscula", "scale", "bàscula"), ("medir", "to measure", "mesurar"),
                ("empacador", "bagger", "envasador"), ("acomodar", "to arrange", "acomodar"), ("traído de fuera", "imported", "portat de fora"),
                ("envase", "container", "envas"), ("ticket", "receipt", "ticket"), ("rótulo", "label", "rètol"),
                # Encounter 46-50
                ("entrega", "delivery", "entrega"), ("fecha de vencimiento", "expiration date", "data de caducitat"), ("zona refrigerada", "refrigerated zone", "zona refrigerada"),
                ("estacionamiento", "parking lot", "aparcament"), ("zona de congelados", "frozen section", "zona de congelats"), ("temperatura ambiente", "room temp", "temperatura ambient"),
                ("artículo de limpieza", "cleaning product", "article de neteja"), ("limpiador", "cleaner", "netejador"), ("barra de jabón", "bar of soap", "barra de sabó"),
                ("fidelidad", "loyalty", "fidelitat"), ("puntos", "points", "punts"), ("membresía", "membership", "membresia"),
                ("hoja de papel", "paper sheet", "full de paper"), ("buen día", "good day", "bon dia"), ("pañuelo de mesa", "table napkin", "tovalló de taula"),
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
                ("internet", "internet", "internet"), ("wifi", "WiFi", "wifi"), ("red inalámbrica", "wireless network", "xarxa sense fils"),
                ("wifi doméstico", "home WiFi", "wifi domèstic"), ("clave de acceso", "access code", "clau d\'accés"), ("red local", "local network", "xarxa local"),
                ("router", "router", "router"), ("cable", "cable", "cable"), ("intensidad", "signal strength", "intensitat"),
                ("enrutador", "router", "enrutador"), ("cable de red", "network cable", "cable de xarxa"), ("tomacorriente", "outlet", "endoll"),
                ("plan", "plan", "pla"), ("pausado", "slow", "pausat"), ("rapidez", "speed", "rapidesa"),
                # Encounter 6-10
                ("paquete de datos", "data plan", "paquet de dades"), ("cuota mensual", "monthly fee", "quota mensual"), ("visita", "visit", "visita"),
                ("nombre de red", "network name", "nom de xarxa"), ("colocar", "to install", "col·locar"), ("configurar", "to configure", "configurar"),
                ("conectar", "to connect", "connectar"), ("desconectar", "to disconnect", "desconnectar"), ("reiniciar", "to restart", "reiniciar"),
                ("especialista", "specialist", "especialista"), ("cita de servicio", "service appointment", "cita de servei"), ("SSID", "SSID", "SSID"),
                ("funcionar", "to work/function", "funcionar"), ("renombrar", "to rename", "renombrar"), ("solución", "solution", "solució"),
                # Encounter 11-15
                ("banda ancha", "broadband", "banda ampla"), ("fibra óptica", "fiber optic", "fibra òptica"), ("megabits", "megabits", "megabits"),
                ("descargar", "to download", "descarregar"), ("ajustar", "to adjust", "ajustar"), ("enlazar", "to connect", "enllaçar"),
                ("cortar enlace", "to disconnect", "tallar enllaç"), ("rearrancar", "to restart", "rearrencar"), ("aparato", "device", "aparell"),
                ("portátil", "laptop", "portàtil"), ("teléfono móvil", "mobile phone", "telèfon mòbil"), ("operar", "to work/operate", "operar"),
                ("modem", "modem", "mòdem"), ("antena", "antenna", "antena"), ("inconveniente", "issue", "inconvenient"),
                # Encounter 16-20
                ("conexión de alta velocidad", "high-speed connection", "connexió d\'alta velocitat"), ("cable óptico", "fiber optic cable", "cable òptic"), ("alcance", "range", "abast"),
                ("corte", "outage", "cort"), ("interrupción", "interruption", "interrupció"), ("megabytes", "megabytes", "megabytes"),
                ("bajar archivos", "to download files", "baixar arxius"), ("permanencia", "commitment period", "permanència"), ("cargar archivos", "to upload files", "carregar arxius"),
                ("fecha de pago", "payment date", "data de pagament"), ("mejorar", "to improve", "millorar"), ("soporte al cliente", "customer support", "suport al client"),
                ("televisión", "television", "televisió"), ("comunicarse", "to communicate", "comunicar-se"), ("combo", "bundle", "combo"),
                # Encounter 21-25
                ("streaming", "streaming", "streaming"), ("videollamada", "video call", "videotrucada"), ("juego en línea", "online gaming", "joc en línia"),
                ("módem", "modem", "mòdem"), ("ilimitado", "unlimited", "il·limitat"), ("antena receptora", "receiving antenna", "antena receptora"),
                ("decodificador", "decoder", "decodificador"), ("firewall", "firewall", "firewall"), ("área de cobertura", "coverage area", "àrea de cobertura"),
                ("virus", "virus", "virus"), ("malware", "malware", "malware"), ("antivirus", "antivirus", "antivirus"),
                ("extensión", "extension/extender", "extensió"), ("repetidor", "repeater", "repetidor"), ("amplificar", "to amplify", "amplificar"),
                # Encounter 26-30
                ("dirección IP", "IP address", "adreça IP"), ("DNS", "DNS", "DNS"), ("puerto", "port", "port"),
                ("ethernet", "ethernet", "ethernet"), ("inalámbrico", "wireless", "inalàmbric"), ("bluetooth", "bluetooth", "bluetooth"),
                ("latencia", "latency", "latència"), ("ping", "ping", "ping"), ("estabilidad", "stability", "estabilitat"),
                ("asistencia técnica", "technical support", "assistència tècnica"), ("soporte", "support", "suport"), ("extensión de señal", "signal range", "extensió de senyal"),
                ("apagón", "outage", "apagada"), ("navegador", "browser", "navegador"), ("página web", "webpage", "pàgina web"),
                # Encounter 31-35
                ("usuario", "username", "usuari"), ("falla", "failure", "fallada"), ("registrar", "to register", "registrar"),
                ("restablecer", "to restore", "restablir"), ("acuerdo de servicio", "service agreement", "acord de servei"), ("periodo de permanencia", "commitment period", "període de permanència"),
                ("control parental", "parental controls", "control parental"), ("dar de baja", "to cancel", "donar de baixa"), ("renovar plan", "to upgrade plan", "renovar pla"),
                ("cámara", "camera", "càmera"), ("monitor", "monitor", "monitor"), ("vigilancia", "surveillance", "vigilància"),
                ("domótica", "home automation", "domòtica"), ("inteligente", "smart", "intel·ligent"), ("automatizar", "to automate", "automatitzar"),
                # Encounter 36-40
                ("optimizar", "to improve", "optimitzar"), ("almacenar", "to store", "emmagatzemar"), ("combo de servicios", "service bundle", "combo de serveis"),
                ("impresora", "printer", "impressora"), ("compartir", "to share", "compartir"), ("acceso remoto", "remote access", "accés remot"),
                ("VPN", "VPN", "VPN"), ("privacidad", "privacy", "privacitat"), ("encriptar", "to encrypt", "encriptar"),
                ("ancho de banda", "bandwidth", "ample de banda"), ("saturado", "saturated", "saturat"), ("TV por cable", "cable TV", "TV per cable"),
                ("línea fija", "landline", "línia fixa"), ("competencia", "competition", "competència"), ("paquete triple", "triple bundle", "paquet triple"),
                # Encounter 41-45
                ("instalación", "installation", "instal·lació"), ("cableado", "wiring", "cablejat"), ("infraestructura", "infrastructure", "infraestructura"),
                ("contratación", "hiring/contracting", "contractació"), ("video en vivo", "live streaming", "vídeo en viu"), ("llamada de video", "video call", "trucada de vídeo"),
                ("migración", "migration", "migració"), ("portabilidad", "portability", "portabilitat"), ("juego en red", "online gaming", "joc en xarxa"),
                ("tope de datos", "data cap", "topall de dades"), ("sin tope", "unlimited", "sense topall"), ("uso de datos", "data usage", "ús de dades"),
                ("queja", "complaint", "queixa"), ("protección de red", "network security", "protecció de xarxa"), ("cortafuegos", "firewall", "cortafocs"),
                # Encounter 46-50
                ("resguardar", "to protect", "resguardar"), ("consumo real", "actual usage", "consum real"), ("programa malicioso", "malicious software", "programa maliciós"),
                ("satelital", "satellite", "satel·lit"), ("rural", "rural", "rural"), ("urbano", "urban", "urbà"),
                ("mantenimiento", "maintenance", "manteniment"), ("actualización", "update", "actualització"), ("software dañino", "harmful software", "programari maliciós"),
                ("programa de protección", "protection software", "programa de protecció"), ("amplificador", "amplifier", "amplificador"), ("encuesta", "survey", "enquesta"),
                ("listo", "ready", "llest"), ("funcionando", "working", "funcionant"), ("repetidor de señal", "signal repeater", "repetidor de senyal"),
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
                ("lubricante", "lubricant", "lubricant"), ("reemplazo", "replacement", "substitució"), ("vehículo", "vehicle", "vehicle"),
                ("garage", "garage", "garatge"), ("técnico automotriz", "auto technician", "tècnic automotriu"), ("inspeccionar", "to inspect", "inspeccionar"),
                ("sonido", "sound", "so"), ("pastilla de freno", "brake pad", "pastilla de fre"), ("neumático", "tire", "pneumàtic"),
                ("timón", "steering wheel", "volant"), ("combustible", "fuel", "combustible"), ("abastecer", "to fill up", "abastir"),
                ("purificador de aire", "air filter", "purificador d\'aire"), ("electrodo", "spark plug/electrode", "electrode"), ("acumulador", "battery", "acumulador"),
                # Encounter 6-10
                ("foco delantero", "headlight", "focus davanter"), ("bujía", "spark plug", "bujia"), ("batería", "battery", "bateria"),
                ("farol", "lamp", "farol"), ("faro", "headlight", "far"), ("direccional", "turn signal", "direccional"),
                ("intermitente", "blinker", "intermitent"), ("kilómetro", "kilometer", "quilòmetre"), ("milla", "mile", "milla"),
                ("arrancar", "to start", "arrencar"), ("kilómetros", "kilometers", "quilòmetres"), ("encender", "to turn on", "encendre"),
                ("millas", "miles", "milles"), ("dar marcha", "to start", "donar marxa"), ("desactivar", "to turn off", "desactivar"),
                # Encounter 11-15
                ("prender", "to turn on", "encendre"), ("sustituir", "to replace", "substituir"), ("refacción", "spare part", "recanvi"),
                ("de agencia", "OEM/dealer", "d\'agència"), ("póliza de garantía", "warranty policy", "pòlissa de garantia"), ("meses de cobertura", "months of coverage", "mesos de cobertura"),
                ("aceite sintético", "synthetic oil", "oli sintètic"), ("aceite convencional", "conventional oil", "oli convencional"), ("meses", "months", "mesos"),
                ("grado de viscosidad", "viscosity grade", "grau de viscositat"), ("convencional", "conventional", "convencional"), ("viscosidad", "viscosity", "viscositat"),
                ("kilometraje", "mileage", "quilometratge"), ("recorrido", "mileage", "recorregut"), ("revisión periódica", "periodic maintenance", "revisió periòdica"),
                # Encounter 16-20
                ("transmisión", "transmission", "transmissió"), ("atención vehicular", "vehicle service", "atenció vehicular"), ("manual", "manual", "manual"),
                ("embrague", "clutch", "embragatge"), ("pedal", "pedal", "pedal"), ("palanca", "lever/shift", "palanca"),
                ("caja de velocidades", "gearbox", "caixa de canvis"), ("refrigerante", "coolant", "refrigerant"), ("temperatura", "temperature", "temperatura"),
                ("escape", "exhaust", "escape"), ("silenciador", "muffler", "silenciador"), ("transmisión automática", "automatic transmission", "transmissió automàtica"),
                ("suspensión", "suspension", "suspensió"), ("amortiguador", "shock absorber", "amortidor"), ("resorte", "spring", "molla"),
                # Encounter 21-25
                ("alineación", "alignment", "alineació"), ("balanceo", "balancing", "balanceig"), ("rotación", "rotation", "rotació"),
                ("correa", "belt", "correa"), ("transmisión manual", "manual transmission", "transmissió manual"), ("tensor", "tensioner", "tensió"),
                ("alternador", "alternator", "alternador"), ("generador", "generator", "generador"), ("disco de embrague", "clutch disc", "disc d\'embragatge"),
                ("fusible", "fuse", "fusible"), ("pedal de freno", "brake pedal", "pedal de fre"), ("cortocircuito", "short circuit", "curtcircuit"),
                ("aire acondicionado", "air conditioning", "aire condicionat"), ("compresor", "compressor", "compressor"), ("freón", "freon/refrigerant", "freó"),
                # Encounter 26-30
                ("palanca de cambios", "gear shift", "palanca de canvis"), ("enfriador", "cooler/radiator", "refredador"), ("escáner", "scanner", "escàner"),
                ("sensor", "sensor", "sensor"), ("líquido refrigerante", "coolant fluid", "líquid refrigerant"), ("grado de calor", "temperature level", "grau de calor"),
                ("oxidado", "rusted", "oxidat"), ("corroído", "corroded", "corroït"), ("desgastado", "worn", "desgastat"),
                ("apretar", "to tighten", "apretar"), ("aflojar", "to loosen", "afluixar"), ("torque", "torque", "torque"),
                ("tubo de escape", "exhaust pipe", "tub d\'escape"), ("mofle", "muffler", "mofle"), ("sistema de suspensión", "suspension system", "sistema de suspensió"),
                # Encounter 31-35
                ("aceite de motor", "engine oil", "oli de motor"), ("absorbedor de impactos", "shock absorber", "absorbedor d\'impactes"), ("dipstick", "dipstick", "dipstick"),
                ("espiral", "spring/coil", "espiral"), ("alineado de llantas", "tire alignment", "alineat de rodes"), ("equilibrar", "to balance", "equilibrar"),
                ("rotación de llantas", "tire rotation", "rotació de rodes"), ("banda", "belt", "banda"), ("inyector", "injector", "injector"),
                ("carburador", "carburetor", "carburador"), ("admisión", "intake", "admissió"), ("eslabón", "chain link", "eslabó"),
                ("cigüeñal", "crankshaft", "cigonyal"), ("pistón", "piston", "pistó"), ("cilindro", "cylinder", "cilindre"),
                # Encounter 36-40
                ("turbo", "turbo", "turbo"), ("sobrealimentador", "supercharger", "sobrealimentador"), ("potencia", "horsepower", "potència"),
                ("catalizador", "catalytic converter", "catalitzador"), ("emisión", "emission", "emissió"), ("contaminación", "pollution", "contaminació"),
                ("freno de disco", "disc brake", "freno de disc"), ("polea tensora", "tensioner pulley", "polea tensora"), ("rotor", "rotor", "rotor"),
                ("dirección hidráulica", "power steering", "direcció hidràulica"), ("fluido", "fluid", "fluid"), ("dínamo", "alternator/dynamo", "dínamo"),
                ("limpiaparabrisas", "windshield wiper", "netejaparabrisa"), ("generador eléctrico", "electric generator", "generador elèctric"), ("circuito eléctrico", "electrical circuit", "circuit elèctric"),
                # Encounter 41-45
                ("tapicería", "upholstery", "tapisseria"), ("vestidura", "seat cover", "vestidura"), ("fusible de seguridad", "safety fuse", "fusible de seguretat"),
                ("pintura", "paint", "pintura"), ("abollar", "to dent", "abollar"), ("rayar", "to scratch", "ratllar"),
                ("hojalatería", "body shop", "hojalateria"), ("carrocería", "body/chassis", "carrosseria"), ("arnés", "wiring harness", "arnès"),
                ("falla eléctrica", "electrical fault", "fallada elèctrica"), ("climatización", "climate control", "climatització"), ("deducible", "deductible", "deduïble"),
                ("compresor de aire", "air compressor", "compressor d\'aire"), ("remolcar", "to tow", "remolcar"), ("gas refrigerante", "refrigerant gas", "gas refrigerant"),
                # Encounter 46-50
                ("prueba de diagnóstico", "diagnostic test", "prova de diagnòstic"), ("placa", "license plate", "placa"), ("escáner automotriz", "automotive scanner", "escàner automotriu"),
                ("híbrido", "hybrid", "híbrid"), ("equipo de cómputo", "computer equipment", "equip de computació"), ("recarga", "recharge", "recàrrega"),
                ("tuning", "tuning", "tuning"), ("captador", "sensor", "captador"), ("personalizar", "to customize", "personalitzar"),
                ("indicador", "gauge", "indicador"), ("dato", "reading/data", "dada"), ("herrumbre", "rust", "ferrugem"),
                ("corrosión", "corrosion", "corrosió"), ("gastado", "worn out", "gastat"), ("soltar", "to loosen", "soltar"),
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
                ("permiso de conducir", "driver's license", "permís de conduir"), ("papeles", "papers", "papers"), ("documentos", "documents", "documents"),
                ("tarjeta de circulación", "vehicle registration", "targeta de circulació"), ("conducir", "to drive", "conduir"), ("pare", "stop", "pare"),
                ("letrero", "sign", "cartell"), ("luz de tráfico", "traffic light", "llum de trànsit"), ("matrícula", "license plate", "matrícula"),
                ("correa de seguridad", "safety belt", "cinturó de seguretat"), ("colocado", "wearing", "col·locat"), ("área", "area", "àrea"),
                ("zona escolar", "school zone", "zona escolar"), ("infracción", "violation", "infracció"), ("zona habitacional", "residential zone", "zona habitacional"),
                # Encounter 6-10
                ("facultad", "right", "facultat"), ("perdone", "excuse me", "perdoni"), ("comprender", "to understand", "comprendre"),
                ("aclarar", "to explain", "aclarir"), ("abrochado", "fastened", "abrotxat"), ("puesto", "on/wearing", "posat"),
                ("vía rápida", "highway", "via ràpida"), ("escolar", "school", "escolar"), ("residencial", "residential", "residencial"),
                ("autovía", "freeway", "autovia"), ("avenida", "avenue", "avinguda"), ("rumbo", "direction", "rumb"),
                ("disculpe", "excuse me", "disculpi"), ("vía", "way/route", "via"), ("sentido contrario", "wrong way", "sentit contrari"),
                # Encounter 11-15
                ("carretera", "highway", "carretera"), ("intersección", "intersection", "intersecció"), ("curva", "curve", "corba"),
                ("aparcar", "to park", "aparcar"), ("sentido", "direction/way", "sentit"), ("contrario", "opposite/wrong way", "contrari"),
                ("no permitido", "not allowed", "no permès"), ("bebida alcohólica", "alcoholic drink", "beguda alcohòlica"), ("exhalar", "to exhale/blow", "exhalar"),
                ("estacionar", "to park", "estacionar"), ("colisión", "collision", "col·lisió"), ("permitido", "allowed", "permès"),
                ("alcohol", "alcohol", "alcohol"), ("impacto", "impact", "impacte"), ("soplar", "to blow", "bufar"),
                # Encounter 16-20
                ("accidente", "accident", "accident"), ("servicio de emergencia", "emergency service", "servei d\'emergència"), ("situación de emergencia", "emergency situation", "situació d\'emergència"),
                ("ambulancia", "ambulance", "ambulància"), ("lesionado", "injured", "ferit"), ("herido", "injured", "ferit"),
                ("observador", "witness", "observador"), ("relato", "statement", "relat"), ("datos personales", "personal info", "dades personals"),
                ("falta de atención", "distraction", "falta d\'atenció"), ("distracción", "distraction", "distracció"), ("sancionado", "penalized", "sancionat"),
                ("cinturón de seguridad", "seatbelt", "cinturó de seguretat"), ("multado", "penalized", "multat"), ("menor", "minor", "menor"),
                # Encounter 21-25
                ("arnés de seguridad", "safety harness", "arnés de seguretat"), ("acompañante", "passenger", "acompanyant"), ("corralón", "impound lot", "corraló"),
                ("radar", "radar", "radar"), ("persona menor", "minor", "persona menor"), ("servicio de grúa", "tow truck", "servei de grua"),
                ("advertencia", "warning", "advertència"), ("primera vez", "first time", "primera vegada"), ("perdón", "pardon", "perdó"),
                ("carril", "lane", "carril"), ("rebasar", "to pass/overtake", "rebasar"), ("doble línea", "double line", "doble línia"),
                ("rotonda", "roundabout", "rotonda"), ("arrastrar", "to tow", "arrossegar"), ("ceder", "to yield", "cedir"),
                # Encounter 26-30
                ("peatón", "pedestrian", "peató"), ("cruzar", "to cross", "cruzar"), ("depósito vehicular", "impound lot", "dipòsit vehicular"),
                ("motocicleta", "motorcycle", "motocicleta"), ("detector de velocidad", "speed detector", "detector de velocitat"), ("ciclista", "cyclist", "ciclista"),
                ("retén", "checkpoint", "retén"), ("cámara de vigilancia", "surveillance camera", "càmera de vigilància"), ("prueba fotográfica", "photographic evidence", "prova fotogràfica"),
                ("licencia vencida", "expired license", "llicència vençuda"), ("amonestación", "warning", "amonestació"), ("primera ocasión", "first occasion", "primera ocasió"),
                ("extranjero", "foreigner", "estranger"), ("disculpa", "apology/pardon", "disculpa"), ("carril de circulación", "traffic lane", "carril de circulació"),
                # Encounter 31-35
                ("adelantar", "to overtake", "adelantar"), ("defensa", "defense", "defensa"), ("línea doble", "double line", "línia doble"),
                ("cargos", "charges", "càrrecs"), ("grave", "serious", "greu"), ("leve", "minor", "lleu"),
                ("comparecencia", "court appearance", "compareixença"), ("juzgado", "court", "jutjat"), ("redondel", "roundabout", "redondel"),
                ("imprudencia", "recklessness", "imprudència"), ("negligencia", "negligence", "negligència"), ("responsabilidad", "responsibility", "responsabilitat"),
                ("cruce circular", "traffic circle", "cruïlla circular"), ("impugnar", "to contest", "impugnar"), ("tribunal", "tribunal", "tribunal"),
                # Encounter 36-40
                ("arresto", "arrest", "arrest"), ("detención", "detention", "detenció"), ("esposas", "handcuffs", "manilles"),
                ("patrulla", "patrol car", "patrulla"), ("sirena", "siren", "sirena"), ("persecución", "pursuit", "persecució"),
                ("registro vehicular", "vehicle search", "registre vehicular"), ("dar paso", "to yield", "donar pas"), ("consentir", "to consent", "consentir"),
                ("transeúnte", "pedestrian", "transeünt"), ("uniforme", "uniform", "uniforme"), ("insignia", "badge", "insígnia"),
                ("atravesar", "to cross", "atravessar"), ("número de caso", "case number", "número de cas"), ("copia", "copy", "còpia"),
                # Encounter 41-45
                ("paso peatonal", "crosswalk", "pas per a vianants"), ("corrupción", "corruption", "corrupció"), ("denunciar", "to report/denounce", "denunciar"),
                ("derechos", "rights", "drets"), ("moto", "motorcycle", "moto"), ("inocente", "innocent", "innocent"),
                ("fianza", "bail", "fiança"), ("liberación", "release", "llibertat"), ("custodia", "custody", "custòdia"),
                ("bici", "bicycle", "bici"), ("consulado", "consulate", "consulat"), ("persona en bicicleta", "cyclist", "persona en bicicleta"),
                ("traducción", "translation", "traducció"), ("intérprete", "interpreter", "intèrpret"), ("idioma", "language", "idioma"),
                # Encounter 46-50
                ("protocolo", "protocol", "protocol"), ("procedimiento", "procedure", "procediment"), ("puesto de control", "checkpoint", "punt de control"),
                ("revisión vehicular", "vehicle inspection", "revisió vehicular"), ("asuntos internos", "internal affairs", "assumptes interns"), ("supervisión", "oversight", "supervisió"),
                ("antecedentes", "record/background", "antecedents"), ("examinar", "to check", "examinar"), ("limpio", "clean", "net"),
                ("cooperar", "to cooperate", "cooperar"), ("respetuoso", "respectful", "respectuós"), ("educado", "polite", "educat"),
                ("buenas noches", "good evening", "bona nit"), ("permiso vencido", "expired permit", "permissos caducat"), ("cuidado", "take care", "cuidado"),
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
                ("menú", "menu", "menú"), ("mesero", "waiter", "cambrer"), ("camarero", "waiter", "cambrer"),
                ("platillo", "dish", "plat"), ("trago", "drink", "beguda"), ("jarra de agua", "water pitcher", "gerra d\'aigua"),
                ("ordenar", "to order", "ordenar"), ("sugerir", "to suggest", "suggerir"), ("del día", "of the day", "del dia"),
                ("primer plato", "appetizer/starter", "primer plat"), ("plato fuerte", "main course", "plat fort"), ("plato principal", "main dish", "plat principal"),
                ("bistec", "steak", "bistec"), ("filete", "fish fillet", "filet"), ("guarnición de arroz", "rice side", "guarnició d\'arròs"),
                # Encounter 6-10
                ("verduras mixtas", "mixed salad", "verdures mixtes"), ("caldo", "broth", "caldo"), ("canasta de pan", "bread basket", "cistella de pa"),
                ("tortilla de harina", "flour tortilla", "tortilla de farina"), ("salero", "salt shaker", "sal"), ("pimentero", "pepper shaker", "pebre"),
                ("lima", "lime", "llima"), ("enchiloso", "spicy", "picant"), ("no picante", "mild", "no picant"),
                ("picante", "spicy", "picant"), ("suave", "mild", "suau"), ("gusto", "taste", "gust"),
                ("frío", "cold", "fred"), ("caliente", "hot", "calent"), ("tibio", "warm", "tèbi"),
                # Encounter 11-15
                ("cocinar", "to cook", "cocinar"), ("freír", "to fry", "fregir"), ("asar", "to grill", "assar"),
                ("hervir", "to boil", "bullir"), ("hornear", "to bake", "enfornar"), ("ardiente", "hot/burning", "ardent"),
                ("vegetariano", "vegetarian", "vegetarià"), ("alergia", "allergy", "al·lèrgia"), ("templado", "lukewarm", "templat"),
                ("guisar", "to cook", "guisar"), ("saltear", "to sauté", "saltejar"), ("asar a la parrilla", "to grill", "assar a la graella"),
                ("cocer", "to boil", "coure"), ("gratinar", "to bake/gratin", "gratinar"), ("alistar", "to prepare", "preparar"),
                # Encounter 16-20
                ("taco", "taco", "taco"), ("enchilada", "enchilada", "enchilada"), ("burrito", "burrito", "burrito"),
                ("guacamole", "guacamole", "guacamole"), ("frijoles", "beans", "fesols"), ("sin carne", "meatless", "sense carn"),
                ("intolerancia", "intolerance", "intolerància"), ("trinche", "fork", "trinxar"), ("cuchillo de mesa", "table knife", "ganivet de taula"),
                ("cucharita", "teaspoon", "cullera petita"), ("café", "coffee", "cafè"), ("té", "tea", "te"),
                ("porción", "portion", "porció"), ("loza", "plate/dish", "vaixella"), ("chico", "small", "nen"),
                # Encounter 21-25
                ("mariscos", "seafood", "marisc"), ("copa de agua", "water glass", "copa d\'aigua"), ("pulpo", "octopus", "polp"),
                ("taco al pastor", "pastor taco", "taco al pastor"), ("cordero", "lamb", "corder"), ("enchilada suiza", "Swiss enchilada", "enchilada suïssa"),
                ("vegetales", "vegetables", "verdures"), ("champiñón", "mushroom", "xampinyó"), ("burrito de frijol", "bean burrito", "burrito de fesol"),
                ("guacamole fresco", "fresh guacamole", "guacamole fresc"), ("frijoles refritos", "refried beans", "fesols fregits"), ("queso fundido", "melted cheese", "formatge fos"),
                ("cerveza de barril", "draft beer", "cervesa de barril"), ("jalapeño", "jalapeño", "jalapeño"), ("habanero", "habanero", "habanero"),
                # Encounter 26-30
                ("copa de vino", "glass of wine", "copa de vi"), ("agua de sabor", "flavored water", "aigua de sabor"), ("jugo de naranja", "orange juice", "suc de taronja"),
                ("café americano", "American coffee", "cafè americà"), ("té de manzanilla", "chamomile tea", "te de camamilla"), ("ración", "serving", "ració"),
                ("delicioso", "delicious", "deliciós"), ("rico", "tasty", "bo"), ("sabroso", "flavorful", "sabros"),
                ("tamaño grande", "large size", "tamaño gran"), ("casero", "homemade", "casolà"), ("tradicional", "traditional", "tradicional"),
                ("dieta", "diet", "dieta"), ("sin gluten", "gluten-free", "sense gluten"), ("tamaño chico", "small size", "tamaño petit"),
                # Encounter 31-35
                ("ceviche", "ceviche", "ceviche"), ("mole", "mole", "mole"), ("tamales", "tamales", "tamals"),
                ("mezcal", "mezcal", "mezcal"), ("tequila", "tequila", "tequila"), ("margarita", "margarita", "margarita"),
                ("antojito", "snack/appetizer", "antojo"), ("quesadilla", "quesadilla", "quesadilla"), ("frutos del mar", "seafood", "fruits del mar"),
                ("sazón", "seasoning", "sazonar"), ("langostino", "prawn", "gambes"), ("chef", "chef", "xef"),
                ("parrilla", "grill", "graella"), ("calamar", "squid", "calamar"), ("borrego", "lamb", "xai"),
                # Encounter 36-40
                ("maridaje", "pairing", "maridatge"), ("acompañamiento", "side dish", "acompanyament"), ("guarnición", "garnish", "guarnició"),
                ("degustación", "tasting", "degustació"), ("menú del día", "daily menu", "menú del dia"), ("corte de res", "beef cut", "cort de vedella"),
                ("reservación", "reservation", "reservació"), ("privado", "private", "privat"), ("terraza", "terrace", "terrassa"),
                ("propina", "tip", "propina"), ("verdura de temporada", "seasonal vegetables", "verdura de temporada"), ("excelente", "excellent", "excel·lent"),
                ("comensal", "diner", "comensal"), ("cebolla caramelizada", "caramelized onion", "ceba caramel·litzada"), ("familiar", "family-style", "familiar"),
                # Encounter 41-45
                ("diente de ajo", "garlic clove", "dient d\'all"), ("crudo", "raw", "cru"), ("al vapor", "steamed", "al vapor"),
                ("ahumado", "smoked", "fumada"), ("marinado", "marinated", "marinada"), ("empanizado", "breaded", "empanada"),
                ("fusión", "fusion", "fusió"), ("contemporáneo", "contemporary", "contemporani"), ("jitomate", "tomato", "tomàquet"),
                ("palta", "avocado", "alvocat"), ("chile serrano", "serrano chili", "xile serrano"), ("chile poblano", "poblano chili", "xile poblano"),
                ("flambear", "to flambé", "flambejar"), ("chile ancho", "ancho chili", "xile ancho"), ("reducción", "reduction", "reducció"),
                # Encounter 46-50
                ("sommelier", "sommelier", "sommelier"), ("catador", "taster", "catador"), ("selección", "selection", "selecció"),
                ("piloncillo", "raw sugar", "piloncillo"), ("sustentable", "sustainable", "sostenible"), ("néctar", "nectar/honey", "nectar"),
                ("nata", "cream", "nata"), ("manteca", "lard/butter", "mantega"), ("jugo de limón", "lemon juice", "jugo de llimona"),
                ("memorable", "memorable", "memorable"), ("felicitaciones", "congratulations", "felicitacions"), ("al chef", "to the chef", "al xef"),
                ("exquisito", "exquisite", "exquisit"), ("sazonado", "seasoned", "sazonat"), ("favorito", "favorite", "favorit"),
            ],
        },
        {
            "title": "Making a Reservation",
            "goal": "Make a restaurant reservation by speaking with the waiter",
            "word_prefix": "rest_reserve",
            "words": [
                # Encounter 1-5 (basic essentials)
                ("reserva de mesa", "table reservation", "reserva de taula"), ("lugar para sentarse", "seating", "lloc per seure"), ("comensales", "diners/guests", "comensals"),
                ("por la noche", "in the evening", "per la nit"), ("apellido", "last name", "cognom"), ("número de contacto", "contact number", "número de contacte"),
                ("ratificar", "to confirm", "ratificar"), ("aguardar", "to wait", "esperar"), ("esta noche", "tonight", "aquesta nit"),
                ("día siguiente", "next day", "dia següent"), ("sábado y domingo", "weekend", "dissabte i diumenge"), ("adentro", "inside", "dins"),
                ("afuera", "outside", "fora"), ("balcón", "balcony", "balcó"), ("fin de semana", "weekend", "cap de setmana"),
                # Encounter 6-10
                ("junto a la ventana", "by the window", "al costat de la finestra"), ("exterior", "outside", "exterior"), ("rincón", "corner", "racó"),
                ("zona reservada", "reserved area", "zona reservada"), ("mesa grande", "large table", "taula gran"), ("mesa pequeña", "small table", "taula petita"),
                ("acogedor", "cozy", "acollidor"), ("festejo", "celebration", "festeig"), ("íntimo", "intimate", "íntim"),
                ("celebración", "celebration", "celebració"), ("cumpleaños", "birthday", "aniversari"), ("aniversario", "anniversary", "aniversari"),
                ("fiesta de cumpleaños", "birthday party", "festa d\'aniversari"), ("fecha especial", "special date", "data especial"), ("mesa para grupo", "group table", "taula per grup"),
                # Encounter 11-15
                ("mesa para dos", "table for two", "taula per a dos"), ("reunión familiar", "family gathering", "reunió familiar"), ("modificar reserva", "to modify reservation", "modificar reserva"),
                ("reglas del local", "venue rules", "regles del local"), ("anticipación", "advance notice", "anticipació"), ("con antelación", "in advance", "amb antelació"),
                ("cargo por cancelación", "cancellation fee", "càrrec per cancel·lació"), ("carta del restaurante", "restaurant menu", "carta del restaurant"), ("plato del día", "daily special", "plat del dia"),
                ("de la estación", "seasonal", "de l\'estació"), ("horas de atención", "business hours", "hores d\'atenció"), ("en servicio", "open", "en servei"),
                ("temprano", "early", "d\'hora"), ("tarde", "late", "tarda"), ("mediodía", "noon", "migdia"),
                # Encounter 16-20
                ("alérgico", "allergic", "al·lèrgic"), ("fuera de horario", "closed", "fora d\'horari"), ("antes de tiempo", "early", "abans d\'hora"),
                ("silla alta", "high chair", "cadira alta"), ("niño", "child", "nen"), ("con retraso", "late", "amb retard"),
                ("hora del almuerzo", "lunchtime", "hora del dinar"), ("valet", "valet", "valet"), ("con alergia", "with allergy", "amb al·lèrgia"),
                ("preferencia alimentaria", "dietary preference", "preferència alimentària"), ("popular", "popular", "popular"), ("régimen alimenticio", "diet/regimen", "règim alimentari"),
                ("código de vestimenta", "dress code", "codi de vestimenta"), ("silla para bebé", "baby chair", "cadira per a nadons"), ("con acceso", "with access", "amb accés"),
                # Encounter 21-25
                ("lista de espera", "waiting list", "llista d\'espera"), ("zona de estacionamiento", "parking area", "zona d\'estacionament"), ("notificar", "to notify", "notificar"),
                ("garantizar", "to guarantee", "garantir"), ("asegurar", "to ensure", "assegurar"), ("compromiso", "commitment", "compromís"),
                ("decoración", "decoration", "decoració"), ("servicio de valet", "valet parking", "servei de valet"), ("a poca distancia", "nearby", "a poca distància"),
                ("sugerencia", "suggestion", "suggerència"), ("muy solicitado", "very popular", "molt sol·licitat"), ("predilecto", "favorite", "predilecte"),
                ("vista", "view", "vista"), ("vestimenta", "dress code", "vestimenta"), ("fuente", "fountain", "font"),
                # Encounter 26-30
                ("evento", "event", "esdeveniment"), ("banquete", "banquet", "banquet"), ("catering", "catering", "catering"),
                ("de etiqueta", "formal dress", "de etiqueta"), ("relajado", "relaxed/casual", "relaxat"), ("por persona", "per person", "per persona"),
                ("menú fijo", "fixed menu", "menú fix"), ("turno de espera", "waiting turn", "torn d\'espera"), ("puesto en fila", "queued", "posat en fila"),
                ("brindis", "toast", "brindis"), ("champán", "champagne", "xampany"), ("avisar", "to notify", "avisar"),
                ("asegurar mesa", "to guarantee table", "assegurar taula"), ("velas", "candles", "espelmes"), ("sorpresa", "surprise", "sorpresa"),
                # Encounter 31-35
                ("florista", "florist", "florista"), ("arreglo", "arrangement", "arreglo"), ("decorar", "to decorate", "decorar"),
                ("fotógrafo", "photographer", "fotògraf"), ("recuerdo", "memory/souvenir", "recordatori"), ("reservar con certeza", "to ensure reservation", "reservar amb certesa"),
                ("palabra", "commitment", "paraula"), ("invitación", "invitation", "invitació"), ("confirmar asistencia", "to RSVP", "confirmar assistència"),
                ("adorno", "decoration", "adorno"), ("salón", "hall/room", "saló"), ("atmósfera", "atmosphere", "atmòsfera"),
                ("melodía", "music/melody", "melodia"), ("cocinero principal", "head chef", "cuiner principal"), ("bocina", "speaker", "bocina"),
                # Encounter 36-40
                ("iluminación", "lighting", "il·luminació"), ("vela", "candle", "espelma"), ("romántico", "romantic", "romàntic"),
                ("mantel", "tablecloth", "mantell"), ("vajilla", "dinnerware", "vaixella"), ("cristalería", "glassware", "cristalleria"),
                ("servicio completo", "full service", "servei complet"), ("plato estrella", "signature dish", "plat estrella"), ("buffet", "buffet", "bufet"),
                ("coordinador", "coordinator", "coordinador"), ("gastronomía", "gastronomy", "gastronomia"), ("planificar", "to plan", "planificar"),
                ("panorama", "view", "panorama"), ("patio", "patio/garden", "patio"), ("anticipo", "advance payment", "anticipació"),
                # Encounter 41-45
                ("cascada decorativa", "decorative fountain", "cascada decorativa"), ("aforo", "capacity limit", "aforament"), ("ocasión especial", "special event", "ocasió especial"),
                ("comentario", "review/comment", "comentari"), ("cena de gala", "gala dinner", "cena de gala"), ("servicio de banquete", "banquet service", "servei de banquet"),
                ("costo por persona", "cost per person", "cost per persona"), ("en línea", "online", "en línia"), ("sitio web", "website", "lloc web"),
                ("valor del evento", "event price", "valor de l\'esdeveniment"), ("menú cerrado", "set menu", "menú tancat"), ("cupón", "coupon", "cupó"),
                ("cata de vinos", "wine tasting", "cata de vins"), ("inolvidable", "unforgettable", "inolvidable"), ("combinación de platillos", "dish pairing", "combinació de plats"),
                # Encounter 46-50
                ("agradecimiento", "gratitude", "agraïment"), ("copa de champán", "glass of champagne", "copa de xampany"), ("espumoso", "sparkling wine", "escumós"),
                ("tinto", "red wine", "tinto"), ("tarta", "cake/tart", "pastís"), ("velitas", "candles", "espelmetes"),
                ("detalle sorpresa", "surprise detail", "detall sorpresa"), ("reconocimiento", "recognition", "reconeixement"), ("premio", "award", "premi"),
                ("recomendado", "recommended", "recomanat"), ("destacado", "outstanding", "destacat"), ("excepcional", "exceptional", "excepcional"),
                ("arreglo floral", "flower arrangement", "arreglo floral"), ("hasta pronto", "see you soon", "fins aviat"), ("centro de mesa", "centerpiece", "centre de taula"),
            ],
        },
        {
            "title": "Asking for the Bill",
            "goal": "Ask for the bill, review the charges, and pay",
            "word_prefix": "rest_bill",
            "words": [
                # Encounter 1-5 (basic essentials)
                ("la cuenta por favor", "the check please", "la compte per favor"), ("cancelar la cuenta", "to pay the bill", "cancel·lar la compte"), ("suma total", "total sum", "suma total"),
                ("con tarjeta", "by card", "amb targeta"), ("devuelta", "change", "devolució"), ("gratificación", "tip/gratuity", "gratuïtat"),
                ("atención al cliente", "customer service", "atenció al client"), ("ya incluido", "already included", "ja inclòs"), ("incluido", "included", "inclòs"),
                ("cargar a la cuenta", "to charge to the bill", "carregar a la compte"), ("exacto", "correct", "exacte"), ("correcto", "correct", "correcte"),
                ("comprobante de pago", "payment receipt", "comprovant de pagament"), ("nota de venta", "sales receipt", "nota de venda"), ("sacar copia", "to print", "treure còpia"),
                # Encounter 6-10
                ("dividir", "to split", "dividir"), ("partir la cuenta", "to split the bill", "partir la compte"), ("cada uno", "each one", "cada un"),
                ("por separado", "separately", "per separat"), ("equivocación", "mistake", "equivocació"), ("confusión", "mistake", "confusió"),
                ("lo que tomamos", "what we drank", "el que vam prendre"), ("lo que comimos", "what we ate", "el que vam menjar"), ("extra", "extra", "extra"),
                ("pedido extra", "extra order", "comanda extra"), ("IVA", "VAT/sales tax", "IVA"), ("tributación", "tax", "tributació"),
                ("impuesto al consumo", "consumption tax", "impost al consum"), ("precio especial", "special deal", "preu especial"), ("vale", "coupon", "val"),
                # Encounter 11-15
                ("de débito", "debit", "de dèbit"), ("de crédito", "credit", "de crèdit"), ("lector de tarjetas", "card reader", "lector de targetes"),
                ("contactless", "contactless", "contactless"), ("chip", "chip", "xip"), ("pago sin contacto", "contactless payment", "pagament sense contacte"),
                ("propina sugerida", "suggested tip", "propina suggerida"), ("voluntario", "voluntary", "voluntari"), ("obligatorio", "mandatory", "obligatori"),
                ("tarjeta con chip", "chip card", "targeta amb xip"), ("gratificación sugerida", "suggested tip", "gratuïtat suggerida"), ("identificar", "to identify", "identificar"),
                ("a voluntad", "voluntary", "a voluntat"), ("saldar", "to pay off", "saldar"), ("de cumplimiento", "mandatory", "de compliment"),
                # Encounter 16-20
                ("desglose", "breakdown", "desglaç"), ("detalle", "detail", "detall"), ("código de mesa", "table number", "codi de taula"),
                ("ubicar", "to identify", "ubicar"), ("saldar la cuenta", "to settle the bill", "saldar la compte"), ("poner al día", "to pay off", "posar al dia"),
                ("finiquitar", "to finalize", "finiquitar"), ("sin alcohol", "non-alcoholic", "sense alcohol"), ("detalle de cargos", "charge details", "detall de càrrecs"),
                ("copa", "glass/drink", "copa"), ("ronda", "round", "ronda"), ("pormenor", "detail", "pormenor"),
                ("cubierto", "cover charge", "cobert"), ("rubro", "item/category", "rubric"), ("suplemento", "supplement", "suplement"),
                # Encounter 21-25
                ("postre del menú", "menu dessert", "postre del menú"), ("copa alcohólica", "alcoholic drink", "copa alcohòlica"), ("QR", "QR code", "QR"),
                ("voucher", "voucher", "voucher"), ("bebida sin alcohol", "non-alcoholic drink", "beguda sense alcohol"), ("botella de agua", "bottle of water", "ampolla d\'aigua"),
                ("tanda", "round", "tanda"), ("recompensa", "reward", "recompensa"), ("acumular", "to accumulate", "acumular"),
                ("pedido adicional", "additional order", "pedido addicional"), ("cargo de cubierto", "cover charge", "càrrec de cobert"), ("cargo por servicio", "service charge", "càrrec per servei"),
                ("cargo extra", "extra charge", "càrrec extra"), ("pago por transferencia", "payment by transfer", "pagament per transferència"), ("app de pago", "payment app", "app de pagament"),
                # Encounter 26-30
                ("sobrar", "to be left over", "sobrar"), ("código QR", "QR code", "codi QR"), ("sobrante", "leftover/surplus", "sobrant"),
                ("bono", "voucher", "bo"), ("cupón de regalo", "gift coupon", "cupó de regal"), ("hacer válido", "to redeem", "fer vàlid"),
                ("recibo digital", "digital receipt", "rebuda digital"), ("acumulación de puntos", "points accumulation", "acumulació de punts"), ("sumar puntos", "to earn points", "sumar punts"),
                ("moneda extranjera", "foreign currency", "moneda estrangera"), ("mesa de grupo", "group table", "taula de grup"), ("datos fiscales", "tax details", "dades fiscals"),
                ("cuenta individual", "individual bill", "compte individual"), ("empacar", "to pack", "empacar"), ("contenedor", "container", "contenidor"),
                # Encounter 31-35
                ("dividir gastos", "to share expenses", "dividir despeses"), ("lo que quedó", "what's left over", "el que va quedar"), ("regresar", "to return", "tornar"),
                ("doble cargo", "double charge", "doble càrrec"), ("excedente", "surplus/leftover", "excedent"), ("punto de pago", "payment point", "punt de pagament"),
                ("responsable de caja", "cashier", "responsable de caixa"), ("barra", "counter/bar", "barra"), ("recibo electrónico", "electronic receipt", "rebuda electrònica"),
                ("mandar", "to send", "mandar"), ("datos tributarios", "tax data", "dades tributàries"), ("número fiscal", "tax number", "número fiscal"),
                ("información tributaria", "tax info", "informació tributària"), ("para llevar", "to go", "per emportar"), ("beneficio", "benefit", "benefici"),
                # Encounter 36-40
                ("regalo", "gift", "regal"), ("invitar", "to treat/invite", "invitar"), ("cortesía", "courtesy/complimentary", "cortesia"),
                ("envolver", "to wrap", "envoltar"), ("recipiente", "container", "recipient"), ("ocasión", "occasion", "ocasió"),
                ("desacuerdo", "dispute", "desacord"), ("esclarecer", "to clarify", "esclarir"), ("descorche", "corkage fee", "descorxar"),
                ("encargado", "manager", "encarregat"), ("cargo duplicado", "duplicate charge", "càrrec duplicat"), ("precio fijo", "fixed price", "preu fix"),
                ("todo incluido", "all-inclusive", "tot inclòs"), ("anular cargo", "to void charge", "anul·lar càrrec"), ("devolución de dinero", "money refund", "devolució de diners"),
                # Encounter 41-45
                ("recibo de transacción", "transaction receipt", "rebuda de transacció"), ("permiso de cobro", "charge authorization", "permissió de cobrament"), ("sistema de reservas", "reservation system", "sistema de reserves"),
                ("contabilidad", "accounting", "contabilitat"), ("por internet", "online", "per internet"), ("archivos", "files", "arxius"),
                ("reserva previa", "prior reservation", "reserva prèvia"), ("tarjeta de socio", "membership card", "targeta de soci"), ("consumidor", "consumer", "consumidor"),
                ("beneficio de socio", "member benefit", "benefici de soci"), ("ventaja exclusiva", "exclusive advantage", "avantatge exclusiu"), ("obsequio", "gift", "obsequi"),
                ("de cortesía", "complimentary", "de cortesia"), ("evento especial", "special event", "esdeveniment especial"), ("fecha señalada", "special occasion", "data assenyalada"),
                # Encounter 46-50
                ("copa de vino tinto", "glass of red wine", "copa de vi negre"), ("botella de vino", "bottle of wine", "ampolla de vi"), ("derecho de corcho", "corkage fee", "dret de suro"),
                ("agradecido", "grateful", "agraït"), ("probada", "tasting", "provada"), ("amable", "kind", "amable"),
                ("carta de precios", "price menu", "carta de preus"), ("tarifa fija", "fixed rate", "tarifa fixa"), ("paquete todo incluido", "all-inclusive package", "paquet tot inclòs"),
                ("despedida", "farewell", "despedida"), ("barra de alimentos", "food bar", "barra d\'aliments"), ("hasta luego", "see you later", "fins després"),
                ("sin límite", "unlimited", "sense límit"), ("buen provecho", "enjoy your meal", "bon profit"), ("felicidades", "congratulations", "felicitats"),
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
                ("hola", "hello", "hola"), ("saludos", "greetings", "saluts"), ("mucho gusto", "nice to meet you", "molt de gust"),
                ("persona de al lado", "person next door", "persona del costat"), ("vivir", "to live", "viure"), ("encantado", "delighted to meet you", "encantat"),
                ("residir", "to reside", "residir"), ("hogar", "home", "llar"), ("parientes", "relatives", "parents"),
                ("ocupación", "occupation", "ocupació"), ("bonito", "nice/pretty", "bonic"), ("tranquilo", "quiet/calm", "tranquil"),
                ("clima", "weather", "clima"), ("mudarse", "to move", "canviar-se"), ("barrio", "neighborhood", "barri"),
                # Encounter 6-10
                ("esposa", "wife", "esposa"), ("esposo", "husband", "espos"), ("hijo", "son/child", "fill"),
                ("sereno", "calm/peaceful", "serè"), ("recién llegado", "newcomer", "recent arribat"), ("instalarse", "to settle in", "instal·lar-se"),
                ("colonia", "neighborhood", "colònia"), ("planta", "plant", "planta"), ("compañera", "wife/partner", "companya"),
                ("compañero", "husband/partner", "company"), ("parque", "park", "parc"), ("animal doméstico", "pet", "animal de companyia"),
                ("cachorro", "puppy", "cadell"), ("gatito", "kitten", "gatet"), ("arbusto", "shrub", "arbust"),
                # Encounter 11-15
                ("rosal", "rosebush", "rosal"), ("local comercial", "shop", "local comercial"), ("anochecer", "evening", "anoitejar"),
                ("deporte", "sport", "esport"), ("caminar", "to walk", "caminar"), ("preparar comida", "to cook", "preparar menjar"),
                ("receta casera", "homemade recipe", "recepta casolana"), ("película", "movie", "pel·lícula"), ("libro", "book", "llibre"),
                ("fiesta", "party", "festa"), ("actividad física", "exercise", "activitat física"), ("celebrar", "to celebrate", "celebrar"),
                ("pasear", "to walk/stroll", "passejar"), ("favor", "favor", "favor"), ("trotar", "to jog", "trotar"),
                # Encounter 16-20
                ("serie de TV", "TV show", "sèrie de TV"), ("novela", "novel", "novel·la"), ("restaurante", "restaurant", "restaurant"),
                ("reunión social", "social gathering", "reunió social"), ("convidar", "to invite", "convidar"), ("festejar", "to celebrate", "festejar"),
                ("taxi", "taxi", "taxi"), ("echar una mano", "to help", "donar un cop de mà"), ("estación", "station", "estació"),
                ("hacer falta", "to need", "fer falta"), ("peligroso", "dangerous", "perillós"), ("mercado local", "local market", "mercat local"),
                ("fonda", "restaurant/eatery", "fondes"), ("colegio", "school", "col·legi"), ("respetar", "to respect", "respectar"),
                # Encounter 21-25
                ("basura", "trash", "brossa"), ("reciclar", "to recycle", "reciclar"), ("templo", "church/temple", "temple"),
                ("clínica", "clinic", "clínica"), ("taxi compartido", "shared taxi", "taxi compartit"), ("transporte", "transport", "transport"),
                ("parada", "stop/station", "parada"), ("sin peligro", "safe", "sense perill"), ("con riesgo", "dangerous", "amb risc"),
                ("electricidad", "electricity", "electricitat"), ("precaución", "caution", "precaució"), ("sonido fuerte", "loud noise", "so fort"),
                ("calma", "quiet/calm", "calma"), ("considerar", "to respect", "considerar"), ("desechos", "garbage", "deseixos"),
                # Encounter 26-30
                ("reunión", "meeting/gathering", "reunió"), ("reutilizar", "to recycle", "reutilitzar"), ("asociación", "association", "associació"),
                ("barrer", "to sweep/clean", "escombrar"), ("auto", "car", "cotxe"), ("juntos", "together", "junts"),
                ("renta", "rent", "renda"), ("propietario", "landlord", "propietari"), ("llave de casa", "house key", "clau de casa"),
                ("luz eléctrica", "electricity", "llum elèctrica"), ("suministro de agua", "water supply", "subministrament d\'aigua"), ("gas doméstico", "domestic gas", "gas domèstic"),
                ("reglas", "rules", "regles"), ("convivencia", "coexistence", "convivència"), ("conexión a internet", "internet connection", "connexió a internet"),
                # Encounter 31-35
                ("usar en conjunto", "to share", "usar conjuntament"), ("junta vecinal", "neighborhood meeting", "junta veïnal"), ("felicitar", "to congratulate", "felicitar"),
                ("vacaciones", "vacation", "vacances"), ("viajar", "to travel", "viatjar"), ("vecindario", "community", "veïnat"),
                ("grupo de vecinos", "neighborhood association", "grup de veïns"), ("en equipo", "together", "en equip"), ("dueño", "landlord", "duenyo"),
                ("arrendatario", "tenant", "arrendatari"), ("aprender", "to learn", "aprendre"), ("practicar", "to practice", "practicar"),
                ("reparación", "maintenance", "reparació"), ("generoso", "generous", "generós"), ("simpático", "nice/friendly", "simpàtic"),
                # Encounter 36-40
                ("consejo", "advice", "consell"), ("informar", "to report", "informar"), ("normas del edificio", "building rules", "normes de l\'edifici"),
                ("doctor", "doctor", "metge"), ("dentista", "dentist", "dentista"), ("farmacia", "pharmacy", "farmàcia"),
                ("vivir en armonía", "coexistence", "viure en harmonia"), ("dar la enhorabuena", "to congratulate", "donar l\'enhorabona"), ("días de descanso", "vacation", "dies de descans"),
                ("hacer un viaje", "to travel", "fer un viatge"), ("costa", "beach/coast", "costa"), ("nublado", "cloudy", "nublat"),
                ("feriado", "holiday", "festiu"), ("herencia cultural", "cultural tradition", "herència cultural"), ("descanso", "rest", "descans"),
                # Encounter 41-45
                ("hábito", "custom/habit", "hàbit"), ("raíces", "cultural roots", "arrels"), ("participar", "to participate", "participar"),
                ("nostalgia", "nostalgia", "nostàlgia"), ("extrañar", "to miss", "enyorar"), ("ejercitar", "to practice", "exercitar"),
                ("cordial", "kind/warm", "cordial"), ("desprendido", "generous", "desprendit"), ("agradable de trato", "friendly", "agradable de tracte"),
                ("nieto", "grandchild", "nebot"), ("abuelo", "grandfather", "avi"), ("generación", "generation", "generació"),
                ("fotografía", "photography", "fotografia"), ("álbum", "album", "àlbum"), ("vivencia", "experience", "vivència"),
                # Encounter 46-50
                ("confianza", "trust", "confiança"), ("amistad", "friendship", "amistat"), ("respeto", "respect", "respecte"),
                ("médico", "doctor", "metge"), ("odontólogo", "dentist", "odontòleg"), ("botica", "pharmacy", "botiga"),
                ("bienvenida", "welcome", "benvinguda"), ("bochorno", "heat wave", "bochorno"), ("feliz", "happy", "feliç"),
                ("aguacero", "rainstorm", "xàfec"), ("bendición", "blessing", "benedicció"), ("día soleado", "sunny day", "dia assolellat"),
                ("cuídate", "take care", "cuida\'t"), ("cielo gris", "overcast", "cel gris"), ("buena suerte", "good luck", "bona sort"),
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
            for pos, (spanish, english, catalan) in enumerate([(w1[0], w1[1], w1[2]), (w2[0], w2[1], w2[2]), (w3[0], w3[1], w3[2])], 1):
                word_id = f"enc_{prefix}_{(enc_num - 1) * 3 + pos:03d}"
                category_words.append({
                    "id": word_id,
                    "spanish": spanish,
                    "english": english,
                    "catalan": catalan,
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
