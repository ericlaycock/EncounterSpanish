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
    "core": "Core",
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
                ("pasaporte", "passport", "passaport"), ("reserva", "reservation", "reserva"), ("confirmación", "confirmation", "confirmació"),  # Encounter 1
                ("número de reserva", "reservation number", "número de reserva"), ("nombre", "first name", "nom"), ("apellido", "last name", "cognom"),  # Encounter 2
                ("documento", "document", "document"), ("identificación", "ID", "identificació"), ("visa", "visa", "visa"),  # Encounter 3
                ("permiso", "permit", "permís"), ("documentos de viaje", "travel documents", "documents de viatge"), ("fecha de vencimiento", "expiration date", "data de caducitat"),  # Encounter 4
                ("a nombre de", "under the name of", "a nom de"), ("¿tiene reserva?", "do you have a reservation?", "té reserva?"), ("¿me muestra el pasaporte?", "do you show me your passport?", "em pot mostrar el passaport?"),  # Encounter 5
                ("¿a qué nombre?", "under what name?", "a quin nom?"), ("vuelo", "flight", "vol"), ("número de vuelo", "flight number", "número de vol"),  # Encounter 6
                ("destino", "destination", "destí"), ("destino final", "final destination", "destí final"), ("origen", "origin", "origen"),  # Encounter 7
                ("conexión", "connection", "connexió"), ("vuelo de conexión", "connecting flight", "vol de connexió"), ("vuelo directo", "direct flight", "vol directe"),  # Encounter 8
                ("vuelo lleno", "full flight", "vol ple"), ("vuelo anterior", "previous flight", "vol anterior"), ("vuelo siguiente", "next flight", "vol següent"),  # Encounter 9
                ("¿va directo a…?", "does it go direct to…?", "va directe a…?"), ("¿hasta dónde va?", "how far does it go?", "fins a on va?"), ("¿sale hoy?", "does it leave today?", "surt avui?"),  # Encounter 10
                ("¿sale mañana?", "does it leave tomorrow?", "surt demà?"), ("salida", "departure", "sortida"), ("llegada", "arrival", "arribada"),  # Encounter 11
                ("embarque", "boarding", "embarcament"), ("hora de embarque", "boarding time", "hora d'embarcament"), ("hora de salida", "departure time", "hora de sortida"),  # Encounter 12
                ("puerta", "gate", "porta"), ("número de puerta", "gate number", "número de porta"), ("puerta de embarque", "boarding gate", "porta d’embarcament"),  # Encounter 13
                ("zona de embarque", "boarding area", "zona d'embarcament"), ("preembarque", "preboarding", "preembarqui"), ("prioridad", "priority", "prioritat"),  # Encounter 14
                ("a tiempo", "on time", "a temps"), ("retraso", "delay", "retard"), ("demora", "delay", "retard"),  # Encounter 15
                ("cambio de puerta", "gate change", "canvi de porta"), ("¿cuál es la puerta?", "what is the gate?", "quina és la porta?"), ("aparece en las pantallas", "it appears on the screens", "apareix a les pantalles"),  # Encounter 16
                ("aparece en la app", "it appears in the app", "apareix a l'app"), ("no está asignada", "it is not assigned", "no està assignada"), ("asiento", "seat", "seient"),  # Encounter 17
                ("número de asiento", "seat number", "número de seient"), ("fila", "row", "cua"), ("ventana", "window", "finestra"),  # Encounter 18
                ("pasillo", "aisle", "passadís"), ("asiento del medio", "middle seat", "seient del mig"), ("asiento de ventana", "window seat", "seient de finestra"),  # Encounter 19
                ("asiento de pasillo", "aisle seat", "seient del passadís"), ("salida de emergencia", "exit row", "sortida d'emergència"), ("juntos", "together", "junts"),  # Encounter 20
                ("separados", "separate", "separats"), ("¿prefiere ventana o pasillo?", "do you prefer a window or an aisle?", "prefereix finestra o passadís?"), ("¿hay asientos juntos?", "are there seats together?", "hi ha seients junts?"),  # Encounter 21
                ("¿hay otro asiento?", "is there another seat?", "hi ha un altre seient?"), ("cambio de asiento", "seat change", "canvi de seient"), ("asignado", "assigned", "assignat"),  # Encounter 22
                ("equipaje", "luggage", "equipatge"), ("maleta", "suitcase", "maleta"), ("equipaje de mano", "carry-on", "equipatge de mà"),  # Encounter 23
                ("equipaje facturado", "checked baggage", "equipatge facturat"), ("maleta de cabina", "cabin bag", "maleta de cabina"), ("artículo personal", "personal item", "article personal"),  # Encounter 24
                ("primera maleta", "first bag", "primera maleta"), ("segunda maleta", "second bag", "segona maleta"), ("etiqueta", "tag", "etiqueta"),  # Encounter 25
                ("recibo de equipaje", "baggage receipt", "justificant d'equipatge"), ("cinta", "carousel", "cinta transportadora"), ("recogida de equipaje", "baggage claim", "recollida d'equipatge"),  # Encounter 26
                ("¿va a facturar equipaje?", "are you checking baggage?", "portarà equipatge per facturar?"), ("¿lleva equipaje?", "are you carrying luggage?", "porta equipatge?"), ("balanza", "scale", "balança"),  # Encounter 27
                ("peso", "weight", "pes"), ("límite", "limit", "límit"), ("exceso", "excess", "excés"),  # Encounter 28
                ("sobrepeso", "overweight", "sobrepès"), ("medidas", "dimensions", "mides"), ("medidas permitidas", "allowed dimensions", "mides permeses"),  # Encounter 29
                ("está demasiado pesado", "it is too heavy", "és massa pesat"), ("está demasiado grande", "it is too big", "és massa gran"), ("póngalo en la balanza", "put it on the scale (Ud.)", "posi-ho a la bàscula"),  # Encounter 30
                ("¿cuál es el límite?", "what is the limit?", "quin és el límit?"), ("¿cuánto cuesta?", "how much does it cost?", "quant costa?"), ("facturo el equipaje", "I check the baggage", "facturo l'equipatge"),  # Encounter 31
                ("etiquetan el equipaje", "they tag the baggage", "etiqueten l'equipatge"), ("abre la maleta", "open the suitcase (Ud.)", "obri la maleta"), ("saca los objetos", "take the items out (Ud.)", "treu els objectes"),  # Encounter 32
                ("pasa algunas cosas a la mochila", "move some things to the backpack (Ud.)", "passi algunes coses a la motxilla"), ("lo lleva con usted", "carry it with you", "el porti amb vostè"), ("no puede ir en la maleta", "it cannot go in the suitcase", "no pot anar a la maleta"),  # Encounter 33
                ("¿puede facturarlo?", "can you check it?", "pot facturar-ho?"), ("¿puede llevarlo con usted?", "can you carry it with you?", "pot portar-ho amb vostè?"), ("líquidos", "liquids", "líquids"),  # Encounter 34
                ("batería portátil", "power bank", "bateria externa"), ("cargador", "charger", "carregador"), ("computadora", "laptop", "ordinador portàtil"),  # Encounter 35
                ("objetos de valor", "valuables", "objectes de valor"), ("medicinas", "medication", "medicaments"), ("¿lleva líquidos?", "are you carrying liquids?", "porta líquids?"),  # Encounter 36
                ("¿lleva baterías?", "are you carrying batteries?", "porta bateries?"), ("no está permitido", "it is not allowed", "no està permès"), ("está permitido", "it is allowed", "està permès"),  # Encounter 37
                ("control de seguridad", "security check", "control de seguretat"), ("revisión", "inspection", "revisió"), ("revisión adicional", "additional screening", "revisió addicional"),  # Encounter 38
                ("selección aleatoria", "random selection", "selecció aleatòria"), ("control", "checkpoint", "control"), ("seguridad", "security", "seguretat"),  # Encounter 39
                ("terminal", "terminal", "terminal"), ("aeropuerto", "airport", "aeroport"), ("aerolínea", "airline", "aerolínia"),  # Encounter 40
                ("mostrador", "counter", "taulell"), ("sistema", "system", "sistema"), ("no funciona", "it does not work", "no funciona"),  # Encounter 41
                ("exceso de equipaje", "excess baggage", "excés d'equipatge"), ("paga el exceso", "pay the excess fee (Ud.)", "pagi l’excés"), ("con tarjeta", "with a card", "amb targeta"),  # Encounter 42
                ("en efectivo", "in cash", "en efectiu"), ("sin costo", "with no charge", "sense cost"), ("tarifa", "fee", "tarifa"),  # Encounter 43
                ("total", "total", "total"), ("recibo", "receipt", "rebut"), ("pasajero", "passenger", "passatger"),  # Encounter 44
                ("familia", "family", "família"), ("niño", "child", "nen"), ("niña", "girl", "nena"),  # Encounter 45
                ("coche de bebé", "stroller", "cotxet"), ("hasta la puerta", "up to the gate", "fins a la porta"), ("tarjeta de embarque", "boarding pass", "targeta d'embarcament"),  # Encounter 46
                ("imprimen la tarjeta de embarque", "they print the boarding pass", "imprimeixen la targeta d'embarcament"), ("celular", "cellphone", "telèfon mòbil"), ("correo", "email", "correu"),  # Encounter 47
                ("confirmación por correo", "email confirmation", "confirmació per correu"), ("hay espacio", "there is space", "hi ha espai"), ("no hay espacio", "there is no space", "no hi ha espai"),  # Encounter 48
                ("conexión corta", "short connection", "connexió curta"), ("conexión larga", "long connection", "connexió llarga"), ("aduana", "customs", "duana"),  # Encounter 49
                ("migración", "immigration", "migració"), ("control migratorio", "immigration control", "control migratori"), ("formulario de aduana", "customs form", "formulari de duana"),  # Encounter 50
            ],
        },
    ],
    "banking": [
        {
            "title": "Banking",
            "goal": "Handle banking tasks including accounts, transfers, cards, and loans",
            "word_prefix": "bank",
            "words": [
                ("banco", "bank", "banc"), ("cajero", "teller", "caixer"), ("cliente", "customer", "client"),  # Encounter 1
                ("cuenta", "account", "compte"), ("cuenta bancaria", "bank account", "compte bancari"), ("saldo", "balance", "saldo"),  # Encounter 2
                ("saldo disponible", "available balance", "saldo disponible"), ("saldo actual", "current balance", "saldo actual"), ("tarjeta", "card", "targeta"),  # Encounter 3
                ("tarjeta de débito", "debit card", "targeta de dèbit"), ("tarjeta de crédito", "credit card", "targeta de crèdit"), ("tarjeta bloqueada", "blocked card", "targeta bloquejada"),  # Encounter 4
                ("tarjeta nueva", "new card", "targeta nova"), ("PIN", "PIN", "PIN"), ("clave", "PIN", "clau"),  # Encounter 5
                ("contraseña", "password", "contrasenya"), ("número de cuenta", "account number", "número de compte"), ("número incorrecto", "wrong number", "número incorrecte"),  # Encounter 6
                ("transferencia", "transfer", "transferència"), ("transferencia enviada", "sent transfer", "transferència enviada"), ("transferencia recibida", "received transfer", "transferència rebuda"),  # Encounter 7
                ("no llegó", "it did not arrive", "no va arribar"), ("llegó tarde", "it arrived late", "va arribar tard"), ("comprobante", "receipt", "justificant"),  # Encounter 8
                ("muestro el comprobante", "I show the receipt", "mostro el comprovant"), ("reviso la cuenta", "I check the account", "reviso el compte"), ("revisan los movimientos", "they check the transactions", "revisen els moviments"),  # Encounter 9
                ("movimientos", "transactions", "moviments"), ("cargo", "charge", "càrrec"), ("cargos extra", "extra charges", "càrrecs extra"),  # Encounter 10
                ("no lo reconozco", "I do not recognize it", "no el reconec"), ("cargo sospechoso", "suspicious charge", "càrrec sospitós"), ("intento sospechoso", "suspicious attempt", "intent sospitós"),  # Encounter 11
                ("bloqueo", "block", "bloqueig"), ("se bloqueó", "it got blocked", "es va bloquejar"), ("desbloquean la tarjeta", "they unblock the card", "desbloquegen la targeta"),  # Encounter 12
                ("activan la tarjeta", "they activate the card", "activen la targeta"), ("emiten la tarjeta", "they issue the card", "emeten la targeta"), ("funciona ahora", "it works now", "funciona ara"),  # Encounter 13
                ("no funciona", "it does not work", "no funciona"), ("rechazada", "declined", "rebutjada"), ("pago rechazado", "declined payment", "pagament rebutjat"),  # Encounter 14
                ("hago el pago", "I make the payment", "faig el pagament"), ("pago aprobado", "approved payment", "pagament aprovat"), ("pago pendiente", "pending payment", "pagament pendent"),  # Encounter 15
                ("monto", "amount", "import"), ("monto total", "total amount", "import total"), ("cantidad", "amount", "quantitat"),  # Encounter 16
                ("deposito dinero", "I deposit money", "diposito diners"), ("retiro", "withdrawal", "retirada"), ("retiro dinero", "I withdraw money", "retiro diners"),  # Encounter 17
                ("efectivo", "cash", "efectiu"), ("con tarjeta", "with a card", "amb targeta"), ("cajero automático", "ATM", "caixer automàtic"),  # Encounter 18
                ("retiro en el cajero", "I withdraw at the ATM", "retiro a l'caixer"), ("saldo insuficiente", "insufficient funds", "saldo insuficient"), ("no hay fondos", "there are no funds", "no hi ha fons"),  # Encounter 19
                ("hay fondos", "there are funds", "hi ha fons"), ("abro una cuenta", "I open an account", "obro un compte"), ("abro una cuenta nueva", "I open a new account", "obro un compte nou"),  # Encounter 20
                ("cierro la cuenta", "I close the account", "tanco el compte"), ("cambio de cuenta", "account change", "canvi de compte"), ("tipo de cuenta", "account type", "tipus de compte"),  # Encounter 21
                ("cuenta principal", "main account", "compte principal"), ("cuenta de ahorros", "savings account", "compte d’estalvi"), ("cuenta corriente", "checking account", "compte corrent"),  # Encounter 22
                ("comisión", "fee", "comissió"), ("cobran comisión", "they charge a fee", "cobren comissió"), ("sin comisión", "without a fee", "sense comissió"),  # Encounter 23
                ("comisión mensual", "monthly fee", "comissió mensual"), ("eliminan la comisión", "they remove the fee", "eliminar la comissió"), ("contrato", "contract", "contracte"),  # Encounter 24
                ("condiciones", "terms", "condicions"), ("saldo mínimo", "minimum balance", "saldo mínim"), ("requiere saldo mínimo", "it requires a minimum balance", "requereix saldo mínim"),  # Encounter 25
                ("requiere depósitos", "it requires deposits", "requereix dipòsits"), ("historial", "history", "historial"), ("historial crediticio", "credit history", "historial creditici"),  # Encounter 26
                ("crédito", "credit", "crèdit"), ("buen crédito", "good credit", "bon crèdit"), ("mal crédito", "bad credit", "mal crèdit"),  # Encounter 27
                ("préstamo", "loan", "préstec"), ("solicito un préstamo", "I apply for a loan", "sol·licito un préstec"), ("monto del préstamo", "loan amount", "import del préstec"),  # Encounter 28
                ("aprueban el préstamo", "they approve the loan", "aproven el préstec"), ("rechazan el préstamo", "they reject the loan", "rebutgen el préstec"), ("aprobación", "approval", "aprovació"),  # Encounter 29
                ("está en proceso", "it is in process", "està en procés"), ("solicitud", "application", "sol·licitud"), ("envío la solicitud", "I send the application", "envio la sol·licitud"),  # Encounter 30
                ("documentos", "documents", "documents"), ("falta un documento", "one document is missing", "falta un document"), ("envío los documentos", "I send the documents", "envio els documents"),  # Encounter 31
                ("comprobante de ingresos", "proof of income", "justificant d'ingressos"), ("revisan el sistema", "they check the system", "revisen el sistema"), ("el sistema falla", "the system fails", "el sistema falla"),  # Encounter 32
                ("el sistema está lento", "the system is slow", "el sistema està lent"), ("error del sistema", "system error", "error del sistema"), ("abren un caso", "they open a case", "obren un cas"),  # Encounter 33
                ("número de caso", "case number", "número de cas"), ("seguimiento del caso", "case follow-up", "seguiment del cas"), ("tarda unos días", "it takes a few days", "triga uns dies"),  # Encounter 34
                ("tiempo estimado", "estimated time", "temps estimat"), ("depende del sistema", "it depends on the system", "depèn del sistema"), ("espero la respuesta", "I wait for the response", "espero la resposta"),  # Encounter 35
                ("hoy no", "not today", "avui no"), ("mañana sí", "tomorrow yes", "demà sí"), ("llamo al banco", "I call the bank", "truco al banc"),  # Encounter 36
                ("atención al cliente", "customer service", "atenció al client"), ("hablo con un agente", "I speak with an agent", "parlo amb un agent"), ("verifican mi identidad", "they verify my identity", "verifiquen la meva identitat"),  # Encounter 37
                ("confirman mis datos", "they confirm my information", "confirmen les meves dades"), ("fecha de nacimiento", "birth date", "data de naixement"), ("dirección", "address", "adreça"),  # Encounter 38
                ("número de teléfono", "phone number", "número de telèfon"), ("correo electrónico", "email", "correu electrònic"), ("actualizan mis datos", "they update my information", "actualitzen les meves dades"),  # Encounter 39
                ("datos incorrectos", "incorrect information", "dades incorrectes"), ("cambio mis datos", "I change my information", "canvio les meves dades"), ("código de seguridad", "security code", "codi de seguretat"),  # Encounter 40
                ("envían el código", "they send the code", "envien el codi"), ("ingreso el código", "I enter the code", "introdueixo el codi"), ("código válido", "valid code", "codi vàlid"),  # Encounter 41
                ("código inválido", "invalid code", "codi invàlid"), ("acceso a la cuenta", "account access", "accés al compte"), ("no tengo acceso", "I do not have access", "no tinc accés"),  # Encounter 42
                ("recupero el acceso", "I recover access", "recupero l'accés"), ("restablecen la clave", "they reset the password", "restableixen la clau"), ("cambio la clave", "I change the PIN", "canvio el codi PIN"),  # Encounter 43
                ("bloquean el acceso", "they block the access", "bloquegen l'accés"), ("acceso activo", "active access", "accés actiu"), ("sigue igual", "it is still the same", "segueix igual"),  # Encounter 44
                ("mejora un poco", "it improves a little", "millora una mica"), ("no mejora", "it does not improve", "no millora"), ("¿qué pasó?", "what happened?", "què va passar?"),  # Encounter 45
                ("¿qué hago?", "what do I do?", "què faig?"), ("¿cuánto tarda?", "how long does it take?", "quant triga?"), ("¿cuánto cuesta?", "how much does it cost?", "quant costa?"),  # Encounter 46
                ("no entiendo", "I do not understand", "no entenc"), ("¿puede repetir?", "can you repeat that?", "pot repetir-ho?"), ("más despacio", "more slowly", "més a poc a poc"),  # Encounter 47
                ("sucursal", "branch", "sucursal"), ("ejecutivo", "bank advisor", "assessor bancari"), ("ventanilla", "teller window", "mostrador"),  # Encounter 48
                ("firma registrada", "signature on file", "signatura registrada"), ("la firma no coincide", "the signature does not match", "la signatura no coincideix"), ("transferencia internacional", "international transfer", "transferència internacional"),  # Encounter 49
                ("tipo de cambio", "exchange rate", "tipus de canvi"), ("comisión por transferencia", "transfer fee", "comissió per transferència"), ("fondos retenidos", "held funds", "fons retinguts"),  # Encounter 50
            ],
        },
    ],
    "clothing": [
        {
            "title": "Clothing Shopping",
            "goal": "Navigate a clothing store, find your size, make a purchase, and handle returns",
            "word_prefix": "cloth",
            "words": [
                ("vendedor", "salesperson", "venedor"), ("cliente", "customer", "client"), ("tienda", "store", "botiga"),  # Encounter 1
                ("ropa", "clothing", "roba"), ("camisa", "shirt", "camisa"), ("pantalón", "pants", "pantalons"),  # Encounter 2
                ("chaqueta", "jacket", "jaqueta"), ("vestido", "dress", "vestit"), ("falda", "skirt", "falda"),  # Encounter 3
                ("talla", "size", "mida"), ("¿qué talla usa?", "what size do you wear?", "quina talla fa servir?"), ("le queda bien", "it fits you well", "li queda bé"),  # Encounter 4
                ("le queda grande", "it is too big on you", "li queda gran"), ("le queda pequeño", "it is too small on you", "li queda petit"), ("no le queda", "it does not fit you", "no li queda"),  # Encounter 5
                ("otra talla", "another size", "una altra talla"), ("más grande", "bigger", "més gran"), ("más pequeño", "smaller", "més petit"),  # Encounter 6
                ("probador", "fitting room", "probador"), ("usa el probador", "use the fitting room", "fes servir el vestidor"), ("espere su turno", "wait your turn (Ud.)", "esperi el seu torn"),  # Encounter 7
                ("hay fila", "there is a line", "hi ha cua"), ("modelo", "style", "model"), ("mismo modelo", "same style", "mateix model"),  # Encounter 8
                ("modelo diferente", "different style", "model diferent"), ("color", "color", "color"), ("otro color", "another color", "un altre color"),  # Encounter 9
                ("no hay talla", "there is no size available", "no hi ha talla"), ("no hay stock", "there is no stock", "no hi ha estoc"), ("está agotado", "it is sold out", "està esgotat"),  # Encounter 10
                ("reviso el stock", "I check the stock", "reviso l'estoc"), ("reviso el sistema", "I check the system", "reviso el sistema"), ("hay en otra sucursal", "it is available at another branch", "hi ha en una altra sucursal"),  # Encounter 11
                ("otra sucursal", "another branch", "una altra sucursal"), ("lo pueden pedir", "they can order it", "ho poden demanar"), ("llega en unos días", "it arrives in a few days", "arriba en uns dies"),  # Encounter 12
                ("tarda unos días", "it takes a few days", "triga uns dies"), ("lo aparto", "I put it on hold", "el reservo"), ("apartado", "item on hold", "apartat"),  # Encounter 13
                ("precio", "price", "preu"), ("precio normal", "regular price", "preu normal"), ("precio de oferta", "sale price", "preu d'oferta"),  # Encounter 14
                ("descuento", "discount", "descompte"), ("el descuento aplica", "the discount applies", "el descompte s'aplica"), ("no aplica", "it does not apply", "no s'aplica"),  # Encounter 15
                ("promoción", "promotion", "promoció"), ("condición", "condition", "condició"), ("con membresía", "with membership", "amb membresia"),  # Encounter 16
                ("sin membresía", "without membership", "sense membresia"), ("registro", "sign-up", "registre"), ("no quiero registrarme", "I do not want to sign up", "no vull registrar-me"),  # Encounter 17
                ("el sistema marca otro precio", "the system shows another price", "el sistema marca un altre preu"), ("no coincide", "it does not match", "no coincideix"), ("reviso el precio", "I check the price", "reviso el preu"),  # Encounter 18
                ("corrigen el precio", "they correct the price", "corregixen el preu"), ("ajuste manual", "manual adjustment", "ajust manual"), ("etiqueta", "tag", "etiqueta"),  # Encounter 19
                ("mal etiquetado", "mislabeled", "mal etiquetat"), ("letrero", "sign", "rètol"), ("política de la tienda", "store policy", "política de la botiga"),  # Encounter 20
                ("no aceptamos devoluciones", "we do not accept returns", "no acceptem devolucions"), ("solo damos crédito de tienda", "we only give store credit", "només donem crèdit de botiga"), ("crédito de tienda", "store credit", "crèdit de botiga"),  # Encounter 21
                ("devolución", "refund", "devolució"), ("procesan la devolución", "they process the refund", "procesen la devolució"), ("cambio de producto", "exchange", "canvi de producte"),  # Encounter 22
                ("producto defectuoso", "defective item", "producte defectuós"), ("está roto", "it is broken", "està trencat"), ("costura rota", "torn seam", "costura trencada"),  # Encounter 23
                ("recibo", "receipt", "rebut"), ("tiene recibo", "do you have a receipt?", "té rebut?"), ("sin recibo", "without a receipt", "sense rebut"),  # Encounter 24
                ("dentro del plazo", "within the return window", "dins del termini"), ("fuera del plazo", "outside the return window", "fora del termini"), ("quiero hablar con la gerente", "I want to speak with the manager", "vull parlar amb la gerent"),  # Encounter 25
                ("gerente", "manager", "gerent"), ("excepción", "exception", "excepció"), ("aprueban la excepción", "they approve the exception", "aproven l'excepció"),  # Encounter 26
                ("caja", "checkout", "caixa"), ("total", "total", "total"), ("monto total", "total amount", "import total"),  # Encounter 27
                ("pago", "payment", "pagament"), ("inserta la tarjeta", "insert the card", "insereix la targeta"), ("acerca la tarjeta", "tap the card", "acosta la targeta"),  # Encounter 28
                ("pasa la tarjeta", "swipe the card", "passi la targeta"), ("no pasa", "it does not go through", "no passa"), ("inténtalo otra vez", "try again", "torna-ho a provar"),  # Encounter 29
                ("pago aprobado", "approved payment", "pagament aprovat"), ("pago rechazado", "declined payment", "pagament rebutjat"), ("otra tarjeta", "another card", "una altra targeta"),  # Encounter 30
                ("efectivo", "cash", "efectiu"), ("pago en efectivo", "cash payment", "pagament en efectiu"), ("firma aquí", "sign here (Ud.)", "signi aquí"),  # Encounter 31
                ("bolsa", "bag", "bossa"), ("¿quiere bolsa?", "do you want a bag?", "vol bossa?"), ("bolsa grande", "big bag", "bossa gran"),  # Encounter 32
                ("bolsa pequeña", "small bag", "bossa petita"), ("sin bolsa", "no bag", "sense bossa"), ("lo empacan", "they pack it", "el empaqueten"),  # Encounter 33
                ("fila larga", "long line", "cua llarga"), ("mucha gente", "many people", "molta gent"), ("espera larga", "long wait", "espera llarga"),  # Encounter 34
                ("tarda mucho", "it takes a long time", "triga molt"), ("servicio lento", "slow service", "servei lent"), ("está abierto", "it is open", "està obert"),  # Encounter 35
                ("está cerrado", "it is closed", "està tancat"), ("horario", "store hours", "horari"), ("identificación", "ID", "identificació"),  # Encounter 36
                ("muestra su identificación", "show your ID (Ud.)", "mostri la seva identificació"), ("alarma", "alarm", "alarma"), ("sensor", "security tag", "sensor"),  # Encounter 37
                ("quitan el sensor", "they remove the security tag", "treuen l'etiqueta de seguretat"), ("sensor activo", "active security tag", "sensor actiu"), ("la alarma suena", "the alarm goes off", "la alarma sona"),  # Encounter 38
                ("revisan la compra", "they check the purchase", "revisen la compra"), ("el código escanea", "the barcode scans", "el codi escaneja"), ("el código no escanea", "the barcode does not scan", "el codi no escaneja"),  # Encounter 39
                ("ingreso manual", "manual entry", "introducció manual"), ("código manual", "manual code", "codi manual"), ("problema del sistema", "system issue", "problema del sistema"),  # Encounter 40
                ("ya quedó", "it is fixed now", "ja està arreglat"), ("sigue igual", "it is still the same", "segueix igual"), ("talla correcta", "correct size", "mida correcta"),  # Encounter 41
                ("talla incorrecta", "wrong size", "mida incorrecta"), ("se lo traigo", "I bring it to you", "li ho porto"), ("no le queda bien", "it does not fit you well", "no li queda bé"),  # Encounter 42
                ("le queda mejor", "it fits you better", "li queda millor"), ("me lo llevo", "I am taking it", "me'l porto"), ("devolución parcial", "partial refund", "devolució parcial"),  # Encounter 43
                ("monto reembolsado", "refunded amount", "import reemborsat"), ("te lo cambio", "I exchange it for you", "te'l canvio"), ("te hago un descuento", "I give you a discount", "et faig un descompte"),  # Encounter 44
                ("caja abierta", "open register", "caixa oberta"), ("caja cerrada", "closed register", "caixa tancada"), ("precio final", "final price", "preu final"),  # Encounter 45
                ("cupón", "coupon", "cupó"), ("el cupón vence hoy", "the coupon expires today", "el cupó venç avui"), ("temporada", "season", "temporada"),  # Encounter 46
                ("colección nueva", "new collection", "col·lecció nova"), ("prenda", "garment", "prenda"), ("prenda dañada", "damaged garment", "prenda danyada"),  # Encounter 47
                ("defecto de fábrica", "manufacturing defect", "defecte de fàbrica"), ("marca", "brand", "marca"), ("misma marca", "same brand", "mateixa marca"),  # Encounter 48
                ("línea premium", "premium line", "línia premium"), ("material", "material", "material"), ("algodón", "cotton", "cotó"),  # Encounter 49
                ("tela", "fabric", "tela"), ("se encoge", "it shrinks", "es contrau"), ("destiñe", "it bleeds color", "destenyeix"),  # Encounter 50
            ],
        },
    ],
    "contractor": [
        {
            "title": "Hiring a Contractor",
            "goal": "Manage a construction project, discuss plans, costs, and quality with your contractor",
            "word_prefix": "contr",
            "words": [
                ("contratista", "contractor", "contractista"), ("trabajador", "worker", "treballador"), ("equipo", "crew", "equip"),  # Encounter 1
                ("proyecto", "project", "projecte"), ("obra", "construction work", "obra"), ("trabajo", "work", "feina"),  # Encounter 2
                ("plano", "plan", "plànol"), ("diseño", "design", "disseny"), ("presupuesto", "budget", "pressupost"),  # Encounter 3
                ("estimado", "estimate", "estimació"), ("costo", "cost", "cost"), ("precio", "price", "preu"),  # Encounter 4
                ("total", "total", "total"), ("pago", "payment", "pagament"), ("anticipo", "deposit", "avançament"),  # Encounter 5
                ("pago final", "final payment", "pagament final"), ("material", "material", "material"), ("materiales", "materials", "materials"),  # Encounter 6
                ("proveedor", "supplier", "proveïdor"), ("disponibilidad", "availability", "disponibilitat"), ("no está disponible", "it is not available", "no està disponible"),  # Encounter 7
                ("retraso", "delay", "retard"), ("atraso", "delay", "retard"), ("va atrasado", "it is running late", "va amb retard"),  # Encounter 8
                ("a tiempo", "on time", "a temps"), ("horario", "schedule", "horari"), ("cumplen el horario", "they keep the schedule", "compleixen l’horari"),  # Encounter 9
                ("tiempo estimado", "estimated time", "temps estimat"), ("terminan hoy", "they finish today", "acaben avui"), ("empiezan hoy", "they start today", "comencen avui"),  # Encounter 10
                ("siguen trabajando", "they keep working", "segueixen treballant"), ("trabajo detenido", "stopped work", "feina aturada"), ("revisan esto", "they check this", "revisen això"),  # Encounter 11
                ("inspección", "inspection", "inspecció"), ("ajuste", "adjustment", "ajust"), ("alternativa", "alternative", "alternativa"),  # Encounter 12
                ("calidad", "quality", "qualitat"), ("misma calidad", "same quality", "mateixa qualitat"), ("es diferente", "it is different", "és diferent"),  # Encounter 13
                ("mejor opción", "better option", "millor opció"), ("es más caro", "it is more expensive", "és més car"), ("es más barato", "it is cheaper", "és més barat"),  # Encounter 14
                ("costo adicional", "additional cost", "cost addicional"), ("no estaba incluido", "it was not included", "no estava inclòs"), ("fuera del presupuesto", "over budget", "fora del pressupost"),  # Encounter 15
                ("¿cuánto cuesta?", "how much does it cost?", "quant costa?"), ("¿cuánto tarda?", "how long does it take?", "quant triga?"), ("¿cuándo terminan?", "when do they finish?", "quan acaben?"),  # Encounter 16
                ("¿cuándo empiezan?", "when do they start?", "quan comencen?"), ("¿por qué hay retraso?", "why is there a delay?", "per què hi ha retard?"), ("¿qué pasó?", "what happened?", "què va passar?"),  # Encounter 17
                ("¿puede explicar?", "can you explain it?", "pot explicar-ho?"), ("no entiendo", "I do not understand", "no entenc"), ("necesito más detalle", "I need more detail", "necessito més detall"),  # Encounter 18
                ("quiero ver el plano", "I want to see the plan", "vull veure el plànol"), ("me envía el plano", "send me the plan (Ud.)", "em envia el plànol"), ("está en proceso", "it is in progress", "està en procés"),  # Encounter 19
                ("ya empezaron", "they already started", "ja han començat"), ("ya terminaron", "they already finished", "ja han acabat"), ("falta trabajo", "work is still missing", "encara falta feina"),  # Encounter 20
                ("está incompleto", "it is incomplete", "està incomplet"), ("está mal hecho", "it is poorly done", "està mal fet"), ("está bien hecho", "it is well done", "està ben fet"),  # Encounter 21
                ("corrigen esto", "they fix this", "corregixen això"), ("reparan esto", "they repair this", "reparen això"), ("rehacen esto", "they redo this", "refan això"),  # Encounter 22
                ("ajustan el nivel", "they level this", "ajusten el nivell"), ("superficie", "surface", "superfície"), ("pared", "wall", "paret"),  # Encounter 23
                ("piso", "floor", "pis"), ("techo", "ceiling", "sostre"), ("pintura", "paint", "pintura"),  # Encounter 24
                ("hay manchas", "there are stains", "hi ha taques"), ("acabado", "finish", "acabat"), ("está nivelado", "it is level", "està nivellat"),  # Encounter 25
                ("está desnivelado", "it is uneven", "està desnivellat"), ("hay una grieta", "there is a crack", "hi ha una esquerda"), ("humedad", "moisture", "humitat"),  # Encounter 26
                ("hay una fuga", "there is a leak", "hi ha una fuita"), ("tubería", "pipe", "canonada"), ("instalación", "installation", "instal·lació"),  # Encounter 27
                ("sistema eléctrico", "electrical system", "sistema elèctric"), ("cable", "wire", "cable"), ("enchufe", "outlet", "endoll"),  # Encounter 28
                ("interruptor", "switch", "interruptor"), ("agua", "water", "aigua"), ("llave de agua", "water valve", "clau d'aigua"),  # Encounter 29
                ("abren la pared", "they open the wall", "obren la paret"), ("cierran la pared", "they close the wall", "tanquen la paret"), ("hay daño", "there is damage", "hi ha dany"),  # Encounter 30
                ("evitan el daño", "they avoid the damage", "eviten el dany"), ("es urgente", "it is urgent", "és urgent"), ("puede empeorar", "it can get worse", "pot empitjorar"),  # Encounter 31
                ("apruebo el cambio", "I approve the change", "aprovo el canvi"), ("no autorizo ese cambio", "I do not authorize that change", "no autoritzo aquest canvi"), ("sin autorización", "without authorization", "sense autorització"),  # Encounter 32
                ("avisan antes", "they notify me beforehand", "avisen abans"), ("falta comunicación", "there is poor communication", "hi ha poca comunicació"), ("nadie vino", "nobody came", "ningú va venir"),  # Encounter 33
                ("no llegaron", "they did not arrive", "no van arribar"), ("vienen mañana", "they come tomorrow", "venen demà"), ("vienen hoy", "they come today", "venen avui"),  # Encounter 34
                ("en la mañana", "in the morning", "al matí"), ("en la tarde", "in the afternoon", "a la tarda"), ("llegan tarde", "they arrive late", "arriben tard"),  # Encounter 35
                ("cumplen el plazo", "they meet the deadline", "compleixen el termini"), ("plazo", "deadline", "termini"), ("entrega", "delivery", "entrega"),  # Encounter 36
                ("entrega final", "final delivery", "entrega final"), ("inspección final", "final inspection", "inspecció final"), ("garantía", "warranty", "garantia"),  # Encounter 37
                ("incluye garantía", "it includes a warranty", "inclou garantia"), ("sin garantía", "without a warranty", "sense garantia"), ("herramienta", "tool", "eina"),  # Encounter 38
                ("maquinaria", "machinery", "maquinària"), ("cortan el material", "they cut the material", "tallen el material"), ("instalan esto", "they install this", "instal·len això"),  # Encounter 39
                ("miden esto", "they measure this", "mesuren això"), ("nivelan esto", "they level this", "nivel·len això"), ("fijan esto", "they secure this", "fixen això"),  # Encounter 40
                ("desmontan esto", "they remove this", "desmunten això"), ("montan esto", "they assemble this", "munten això"), ("limpian el área", "they clean the area", "netegen l'àrea"),  # Encounter 41
                ("retiran los escombros", "they remove the debris", "retiren les runes"), ("escombros", "debris", "enderrocs"), ("limpieza final", "final cleanup", "neteja final"),  # Encounter 42
                ("área", "area", "àrea"), ("espacio", "space", "espai"), ("acceso", "access", "accés"),  # Encounter 43
                ("entrada", "entrance", "entrada"), ("salida", "exit", "sortida"), ("vecino", "neighbor", "veí"),  # Encounter 44
                ("ruido", "noise", "soroll"), ("polvo", "dust", "pols"), ("seguridad", "safety", "seguretat"),  # Encounter 45
                ("riesgo", "risk", "risc"), ("protección", "protection", "protecció"), ("equipo de seguridad", "safety gear", "equip de seguretat"),  # Encounter 46
                ("casco", "helmet", "casca"), ("guantes", "gloves", "guants"), ("gafas de seguridad", "safety glasses", "ulleres de seguretat"),  # Encounter 47
                ("azulejo", "tile", "rajola"), ("baldosa", "floor tile", "rajola"), ("madera", "wood", "fusta"),  # Encounter 48
                ("cemento", "cement", "ciment"), ("yeso", "plaster", "guix"), ("sellador", "sealant", "segellant"),  # Encounter 49
                ("impermeabilización", "waterproofing", "impermeabilització"), ("permiso", "permit", "permís"), ("inspector", "inspector", "inspector"),  # Encounter 50
            ],
        },
    ],
    "groceries": [
        {
            "title": "At the Supermarket",
            "goal": "Check out at the supermarket, handle pricing issues, and bag your groceries",
            "word_prefix": "groc",
            "words": [
                ("cajero", "cashier", "caixer"), ("cliente", "customer", "client"), ("caja", "checkout", "caixa"),  # Encounter 1
                ("fila", "line", "cua"), ("turno", "turn", "torn"), ("siguiente", "next", "següent"),  # Encounter 2
                ("productos", "products", "productes"), ("artículo", "item", "article"), ("código de barras", "barcode", "codi de barres"),  # Encounter 3
                ("escanean el producto", "they scan the item", "escanejen el producte"), ("pasan los productos", "they pass the items through", "passen els productes"), ("precio", "price", "preu"),  # Encounter 4
                ("precio correcto", "correct price", "preu correcte"), ("precio incorrecto", "wrong price", "preu incorrecte"), ("oferta", "sale", "oferta"),  # Encounter 5
                ("descuento", "discount", "descompte"), ("promoción", "promotion", "promoció"), ("el descuento aplica", "the discount applies", "el descompte s'aplica"),  # Encounter 6
                ("no aplica", "it does not apply", "no s'aplica"), ("sistema", "system", "sistema"), ("no aparece", "it does not show up", "no apareix"),  # Encounter 7
                ("revisan el precio", "they check the price", "revisen el preu"), ("verifican el precio", "they verify the price", "verifiquen el preu"), ("letrero", "sign", "rètol"),  # Encounter 8
                ("estante", "shelf", "estalvi"), ("pasillo", "aisle", "passadís"), ("supervisor", "supervisor", "supervisor"),  # Encounter 9
                ("llaman al supervisor", "they call the supervisor", "trucen al supervisor"), ("corrigen el precio", "they correct the price", "corregixen el preu"), ("total", "total", "total"),  # Encounter 10
                ("monto total", "total amount", "import total"), ("subtotal", "subtotal", "subtotal"), ("impuesto", "tax", "impost"),  # Encounter 11
                ("incluye impuesto", "it includes tax", "inclou impost"), ("no incluye impuesto", "it does not include tax", "no inclou impostos"), ("pago", "payment", "pagament"),  # Encounter 12
                ("pago aprobado", "approved payment", "pagament aprovat"), ("pago rechazado", "declined payment", "pagament rebutjat"), ("tarjeta", "card", "targeta"),  # Encounter 13
                ("tarjeta rechazada", "declined card", "targeta rebutjada"), ("inserta la tarjeta", "insert the card", "insereix la targeta"), ("pasa la tarjeta", "swipe the card", "passi la targeta"),  # Encounter 14
                ("acerca la tarjeta", "tap the card", "acosta la targeta"), ("ingresa el PIN", "enter the PIN", "introdueix el PIN"), ("firma aquí", "sign here (Ud.)", "signi aquí"),  # Encounter 15
                ("efectivo", "cash", "efectiu"), ("pago en efectivo", "cash payment", "pagament en efectiu"), ("dividir el pago", "split the payment", "dividir el pagament"),  # Encounter 16
                ("pago dividido", "split payment", "pagament fraccionat"), ("pago parcial", "partial payment", "pagament parcial"), ("pago completo", "full payment", "pagament complet"),  # Encounter 17
                ("cambio", "change", "canvi"), ("le dan cambio", "they give you change", "li donen canvi"), ("recibo", "receipt", "rebut"),  # Encounter 18
                ("imprimen el recibo", "they print the receipt", "imprimeixen el rebut"), ("bolsa", "bag", "bossa"), ("bolsa grande", "big bag", "bossa gran"),  # Encounter 19
                ("bolsa pequeña", "small bag", "bossa petita"), ("sin bolsa", "no bag", "sense bossa"), ("separan los productos", "they separate the items", "separen els productes"),  # Encounter 20
                ("producto frío", "cold item", "producte fred"), ("producto congelado", "frozen item", "producte congelat"), ("producto seco", "dry item", "producte sec"),  # Encounter 21
                ("huevos", "eggs", "ous"), ("frágil", "fragile", "fràgil"), ("pesado", "heavy", "pesat"),  # Encounter 22
                ("liviano", "light", "lleuger"), ("cantidad", "quantity", "quantitat"), ("una unidad", "one unit", "una unitat"),  # Encounter 23
                ("dos unidades", "two units", "dues unitats"), ("marcan la cantidad", "they enter the quantity", "marquen la quantitat"), ("corrigen la cantidad", "they correct the quantity", "corregixen la quantitat"),  # Encounter 24
                ("quitan el producto", "they remove the item", "treuen el producte"), ("agregan el producto", "they add the item", "afegeixen el producte"), ("no es mío", "it is not mine", "no és meu"),  # Encounter 25
                ("es incorrecto", "it is incorrect", "és incorrecte"), ("revisan el producto", "they check the item", "revisen el producte"), ("escaneo doble", "double scan", "escaneig doble"),  # Encounter 26
                ("error del sistema", "system error", "error del sistema"), ("ya quedó", "it is fixed now", "ja està arreglat"), ("sigue igual", "it is still the same", "segueix igual"),  # Encounter 27
                ("cliente siguiente", "next customer", "següent client"), ("fila larga", "long line", "cua llarga"), ("mucha gente", "many people", "molta gent"),  # Encounter 28
                ("tarda mucho", "it takes a long time", "triga molt"), ("servicio", "service", "servei"), ("horario", "store hours", "horari"),  # Encounter 29
                ("está abierto", "it is open", "està obert"), ("está cerrado", "it is closed", "està tancat"), ("identificación", "ID", "identificació"),  # Encounter 30
                ("muestra su identificación", "show your ID (Ud.)", "mostri la seva identificació"), ("requiere edad mínima", "it requires a minimum age", "requereix edat mínima"), ("verifican la edad", "they verify your age", "verifiquen l'edat"),  # Encounter 31
                ("producto restringido", "restricted item", "producte restringit"), ("aprobado", "approved", "aprobat"), ("denegado", "denied", "denegat"),  # Encounter 32
                ("alcohol", "alcohol", "alcohol"), ("tabaco", "tobacco", "tabac"), ("bebida", "drink", "beguda"),  # Encounter 33
                ("comida", "food", "menjar"), ("pan", "bread", "pa"), ("leche", "milk", "llet"),  # Encounter 34
                ("carne", "meat", "carn"), ("verduras", "vegetables", "verdures"), ("fruta", "fruit", "fruita"),  # Encounter 35
                ("caja rápida", "express checkout", "caixa ràpida"), ("pocos productos", "few items", "pocs productes"), ("muchos productos", "many items", "molts productes"),  # Encounter 36
                ("carrito", "cart", "carret"), ("canasta", "basket", "cistella"), ("empacan los productos", "they pack the items", "empacuen els productes"),  # Encounter 37
                ("cliente espera", "the customer waits", "el client espera"), ("número de caja", "register number", "número de caixa"), ("caja abierta", "open register", "caixa oberta"),  # Encounter 38
                ("caja cerrada", "closed register", "caixa tancada"), ("cambio exacto", "exact change", "canvi exacte"), ("sin cambio", "without change", "sense canvi"),  # Encounter 39
                ("pago exacto", "exact payment", "pagament exacte"), ("tarjeta válida", "valid card", "targeta vàlida"), ("tarjeta inválida", "invalid card", "targeta invàlida"),  # Encounter 40
                ("saldo insuficiente", "insufficient funds", "saldo insuficient"), ("hay fondos", "there are funds", "hi ha fons"), ("no hay fondos", "there are no funds", "no hi ha fons"),  # Encounter 41
                ("listo para pagar", "ready to pay", "llest per pagar"), ("ingresa el código", "enter the code", "introdueix el codi"), ("código manual", "manual code", "codi manual"),  # Encounter 42
                ("ingreso manual", "manual entry", "introducció manual"), ("producto sin código", "item without a barcode", "producte sense codi"), ("pesa el producto", "weigh the item", "pesa el producte"),  # Encounter 43
                ("balanza", "scale", "balança"), ("etiqueta de precio", "price label", "etiqueta de preu"), ("no coincide", "it does not match", "no coincideix"),  # Encounter 44
                ("revise la etiqueta", "check the label (Ud.)", "revisi l'etiqueta"), ("actualizan el precio", "they update the price", "actualitzen el preu"), ("precio actualizado", "updated price", "preu actualitzat"),  # Encounter 45
                ("inténtalo otra vez", "try again", "torna-ho a provar"), ("caja central", "main checkout", "caixa central"), ("lector", "scanner", "lector"),  # Encounter 46
                ("el lector da error", "the scanner gives an error", "el lector dona error"), ("promoción vencida", "expired promotion", "promoció vençuda"), ("vence hoy", "it expires today", "vence avui"),  # Encounter 47
                ("unidad equivocada", "wrong unit", "unitat equivocada"), ("precio por kilo", "price per kilo", "preu per quilo"), ("precio por unidad", "price per unit", "preu per unitat"),  # Encounter 48
                ("pesa menos", "it weighs less", "pesa menys"), ("pesa más", "it weighs more", "pesa més"), ("producto abierto", "opened item", "producte obert"),  # Encounter 49
                ("producto dañado", "damaged item", "producte danyat"), ("reemplazo", "replacement", "substitució"), ("devolución al método de pago", "refund to the payment method", "devolució al mètode de pagament"),  # Encounter 50
            ],
        },
    ],
    "mechanic": [
        {
            "title": "At the Mechanic",
            "goal": "Describe car problems, get a diagnosis, and handle repairs and payment",
            "word_prefix": "mech",
            "words": [
                ("carro", "car", "cotxe"), ("vehículo", "vehicle", "vehicle"), ("motor", "engine", "motor"),  # Encounter 1
                ("batería", "battery", "bateria"), ("frenos", "brakes", "frens"), ("aceite", "oil", "oli"),  # Encounter 2
                ("filtro", "filter", "filtre"), ("transmisión", "transmission", "transmissió"), ("suspensión", "suspension", "suspensió"),  # Encounter 3
                ("llanta", "tire", "pneumàtic"), ("rueda", "wheel", "roda"), ("radiador", "radiator", "radiador"),  # Encounter 4
                ("bujía", "spark plug", "bugia"), ("correa", "belt", "cinturó"), ("alternador", "alternator", "alternador"),  # Encounter 5
                ("falla", "issue", "fallada"), ("ruido", "noise", "soroll"), ("vibración", "vibration", "vibració"),  # Encounter 6
                ("fuga", "leak", "fuita"), ("no arranca", "it does not start", "no arrenca"), ("no enciende", "it does not turn on", "no s'encén"),  # Encounter 7
                ("se apaga", "it shuts off", "s'apaga"), ("huele raro", "it smells strange", "fa una olor estranya"), ("se sobrecalienta", "it overheats", "s'escalfa massa"),  # Encounter 8
                ("tiene poca potencia", "it has low power", "té poca potència"), ("consume aceite", "it burns oil", "consumeix oli"), ("pierde líquido", "it is leaking fluid", "perd líquid"),  # Encounter 9
                ("frenos débiles", "weak brakes", "frens dèbils"), ("pedal suave", "soft pedal", "pedal suau"), ("revisan el carro", "they check the car", "revisen el cotxe"),  # Encounter 10
                ("inspección", "inspection", "inspecció"), ("diagnóstico", "diagnosis", "diagnòstic"), ("reparan", "they repair it", "reparen"),  # Encounter 11
                ("lo arreglan", "they fix it", "el reparen"), ("cambian la pieza", "they replace the part", "canvien la peça"), ("ajustan", "they adjust it", "ajusten"),  # Encounter 12
                ("instalan", "they install it", "instal·len"), ("limpian", "they clean it", "netegen"), ("lo prueban", "they test it", "ho proven"),  # Encounter 13
                ("revisan el motor", "they check the engine", "revisen el motor"), ("cambio de aceite", "oil change", "canvi d'oli"), ("cambian el filtro", "they change the filter", "canvien el filtre"),  # Encounter 14
                ("revisan los frenos", "they check the brakes", "revisen els frens"), ("alinean las llantas", "they align the tires", "alineen els pneumàtics"), ("¿qué problema tiene?", "what problem does it have?", "quin problema té?"),  # Encounter 15
                ("¿qué pasa?", "what is happening?", "què passa?"), ("¿desde cuándo?", "since when?", "des de quan?"), ("¿cuándo empezó?", "when did it start?", "quan va començar?"),  # Encounter 16
                ("¿hace ruido?", "does it make noise?", "fa soroll?"), ("¿cuánto cuesta?", "how much does it cost?", "quant costa?"), ("¿cuánto tarda?", "how long does it take?", "quant triga?"),  # Encounter 17
                ("¿es grave?", "is it serious?", "és greu?"), ("¿puede empeorar?", "can it get worse?", "pot empitjorar?"), ("¿puede revisarlo?", "can you check it?", "pot revisar-ho?"),  # Encounter 18
                ("precio", "price", "preu"), ("costo", "cost", "cost"), ("total", "total", "total"),  # Encounter 19
                ("estimado", "estimate", "estimació"), ("mano de obra", "labor", "mà d'obra"), ("piezas", "parts", "peces"),  # Encounter 20
                ("adicional", "additional", "addicional"), ("incluye", "it includes", "inclou"), ("no incluye", "it does not include", "no inclou"),  # Encounter 21
                ("presupuesto", "quote", "pressupost"), ("pago", "payment", "pagament"), ("en efectivo", "in cash", "en efectiu"),  # Encounter 22
                ("con tarjeta", "with a card", "amb targeta"), ("factura", "invoice", "factura"), ("recibo", "receipt", "rebut"),  # Encounter 23
                ("desgastado", "worn out", "gastat"), ("dañado", "damaged", "danyat"), ("roto", "broken", "trencat"),  # Encounter 24
                ("sucio", "dirty", "brut"), ("flojo", "loose", "fluix"), ("apretado", "tight", "estrenyit"),  # Encounter 25
                ("en buen estado", "in good condition", "en bon estat"), ("en mal estado", "in bad condition", "en mal estat"), ("urgente", "urgent", "urgent"),  # Encounter 26
                ("peligroso", "dangerous", "perillós"), ("sistema de frenos", "brake system", "sistema de frens"), ("sistema eléctrico", "electrical system", "sistema elèctric"),  # Encounter 27
                ("presión", "pressure", "pressió"), ("nivel", "level", "nivell"), ("nivel de aceite", "oil level", "nivell d'oli"),  # Encounter 28
                ("nivel bajo", "low level", "nivell baix"), ("nivel alto", "high level", "nivell alt"), ("luz de motor", "check-engine light", "testimoni del motor"),  # Encounter 29
                ("código de error", "error code", "codi d'error"), ("dejo el carro", "I leave the car", "deixo el cotxe"), ("recojo el carro", "I pick up the car", "recullo el cotxe"),  # Encounter 30
                ("listo", "ready", "llest"), ("todavía no", "not yet", "encara no"), ("en proceso", "in progress", "en procés"),  # Encounter 31
                ("espero", "I wait", "espero"), ("más tarde", "later", "més tard"), ("hoy", "today", "avui"),  # Encounter 32
                ("mañana", "tomorrow", "demà"), ("tiempo estimado", "estimated time", "temps estimat"), ("muy caro", "too expensive", "massa car"),  # Encounter 33
                ("más barato", "cheaper", "més barat"), ("solo eso", "just that", "només això"), ("no lo necesito", "I do not need it", "no el necessito"),  # Encounter 34
                ("prefiero eso primero", "I prefer that first", "prefereixo això primer"), ("después vemos", "we look at the rest later", "després ho veiem"), ("no autorizo ese trabajo", "I do not authorize that work", "no autoritzo aquesta feina"),  # Encounter 35
                ("sin autorización", "without authorization", "sense autorització"), ("quiero más detalle", "I want more detail", "vull més detall"), ("líquido de frenos", "brake fluid", "líquid de frens"),  # Encounter 36
                ("aceite de motor", "engine oil", "oli de motor"), ("refrigerante", "coolant", "refrigerant"), ("líquido", "fluid", "líquid"),  # Encounter 37
                ("combustible", "fuel", "combustible"), ("gasolina", "gasoline", "benzina"), ("diésel", "diesel", "dièsel"),  # Encounter 38
                ("tanque", "tank", "dipòsit"), ("manguera", "hose", "mànega"), ("válvula", "valve", " vàlvula"),  # Encounter 39
                ("al frenar", "when I brake", "en frenar"), ("al arrancar", "when I start it", "en arrencar"), ("en movimiento", "while it is moving", "en moviment"),  # Encounter 40
                ("en frío", "when it is cold", "en fred"), ("en caliente", "when it is hot", "en calent"), ("a alta velocidad", "at high speed", "a alta velocitat"),  # Encounter 41
                ("a baja velocidad", "at low speed", "a baixa velocitat"), ("en curva", "in a turn", "en corba"), ("en subida", "uphill", "de pujada"),  # Encounter 42
                ("en bajada", "downhill", "de baixada"), ("mecánico", "mechanic", "mecànic"), ("taller", "shop", "taller"),  # Encounter 43
                ("herramienta", "tool", "eina"), ("elevador", "lift", "ascensor"), ("garantía", "warranty", "garantia"),  # Encounter 44
                ("servicio", "service", "servei"), ("revisión general", "general inspection", "revisió general"), ("mantenimiento", "maintenance", "manteniment"),  # Encounter 45
                ("historial", "service history", "historial"), ("diagnóstico completo", "full diagnosis", "diagnòstic complet"), ("no entiendo", "I do not understand", "no entenc"),  # Encounter 46
                ("¿puede repetir?", "can you repeat that?", "pot repetir-ho?"), ("más despacio", "more slowly", "més a poc a poc"), ("¿qué significa?", "what does that mean?", "què significa?"),  # Encounter 47
                ("pastillas de freno", "brake pads", "pastilles de fre"), ("disco de freno", "brake rotor", "disc de fre"), ("amortiguador", "shock absorber", "amortidor"),  # Encounter 48
                ("dirección", "steering", "adreça"), ("alineación", "alignment", "alineació"), ("balanceo", "wheel balancing", "balanceig"),  # Encounter 49
                ("embrague", "clutch", "embragatge"), ("escape", "exhaust", "escape"), ("filtro de aire", "air filter", "filtre d’aire"),  # Encounter 50
            ],
        },
    ],
    "police": [
        {
            "title": "Traffic Stop",
            "goal": "Handle a traffic stop calmly by providing documents and following instructions",
            "word_prefix": "pol",
            "words": [
                ("policía", "police officer", "policia"), ("agente", "officer", "agent"), ("patrulla", "patrol car", "patrulla"),  # Encounter 1
                ("control policial", "traffic stop", "control policial"), ("licencia de conducir", "driver's license", "carnet de conduir"), ("registro del vehículo", "vehicle registration", "matrícula del vehicle"),  # Encounter 2
                ("prueba de seguro", "proof of insurance", "justificant d’assegurança"), ("documentos", "documents", "documents"), ("identificación", "ID", "identificació"),  # Encounter 3
                ("¿licencia, por favor?", "your license, please?", "la llicència, si us plau?"), ("¿tiene el registro?", "do you have the registration?", "té el registre?"), ("¿tiene seguro?", "do you have insurance?", "té assegurança?"),  # Encounter 4
                ("¿puede mostrarlo?", "can you show it?", "pot mostrar-ho?"), ("aquí tiene", "here you are", "aquí té"), ("está en el vehículo", "it is in the vehicle", "és al vehicle"),  # Encounter 5
                ("está en la guantera", "it is in the glove compartment", "és a la guantera"), ("lo detuve", "I stopped you", "t'he aturat"), ("parada", "stop", "parada"),  # Encounter 6
                ("¿sabe por qué lo detuve?", "do you know why I stopped you?", "sap per què l'he aturat?"), ("exceso de velocidad", "speeding", "excés de velocitat"), ("velocidad", "speed", "velocitat"),  # Encounter 7
                ("límite de velocidad", "speed limit", "límit de velocitat"), ("zona", "zone", "zona"), ("en esta zona", "in this zone", "en aquesta zona"),  # Encounter 8
                ("iba a", "were going at (speed)", "anava a"), ("por encima de", "above", "per sobre de"), ("infracción", "violation", "infracció"),  # Encounter 9
                ("motivo", "reason", "motiu"), ("vehículo", "vehicle", "vehicle"), ("carro", "car", "cotxe"),  # Encounter 10
                ("luces", "lights", "llums"), ("luz trasera", "tail light", "llum posterior"), ("luz delantera", "headlight", "llum davantera"),  # Encounter 11
                ("no funciona", "it does not work", "no funciona"), ("placa", "plate", "placa"), ("parabrisas", "windshield", "parabrisa"),  # Encounter 12
                ("cinturón", "seatbelt", "cinturó"), ("sin cinturón", "without a seatbelt", "sense cinturó"), ("en regla", "in order", "en regla"),  # Encounter 13
                ("apague el motor", "turn off the engine (Ud.)", "apagueu el motor"), ("baje la ventana", "roll down the window (Ud.)", "baixi la finestra"), ("salga del vehículo", "get out of the vehicle (Ud.)", "surti del vehicle"),  # Encounter 14
                ("quédese en el vehículo", "stay in the vehicle (Ud.)", "resti al vehicle"), ("espere aquí", "wait here (Ud.)", "esperi aquí"), ("despacio", "slowly", "a poc a poc"),  # Encounter 15
                ("con calma", "calmly", "amb calma"), ("siga mis instrucciones", "follow my instructions (Ud.)", "segueixi les meves instruccions"), ("no se mueva", "do not move (Ud.)", "no es mogui"),  # Encounter 16
                ("frenó fuerte", "braked hard (past)", "va frenar fort"), ("cambió de carril", "changed lanes (past)", "va canviar de carril"), ("sin señalizar", "without signaling", "sense senyalitzar"),  # Encounter 17
                ("conducción peligrosa", "dangerous driving", "conducció perillosa"), ("carril", "lane", "carril"), ("carril restringido", "restricted lane", "carril restringit"),  # Encounter 18
                ("giro", "turn", "gir"), ("no señalizó", "did not signal (past)", "no va senyalitzar"), ("tráfico", "traffic", "trànsit"),  # Encounter 19
                ("intersección", "intersection", "creuament"), ("semáforo", "traffic light", "semàfor"), ("luz roja", "red light", "llum vermella"),  # Encounter 20
                ("luz verde", "green light", "llum verda"), ("¿de dónde viene?", "where are you coming from?", "d'on ve?"), ("¿a dónde va?", "where are you going?", "on va?"),  # Encounter 21
                ("¿cuánto tiempo lleva manejando?", "how long have you been driving?", "quant de temps fa que condueix?"), ("¿es su vehículo?", "is this your vehicle?", "és el seu vehicle?"), ("¿es un vehículo de alquiler?", "is it a rental vehicle?", "és un vehicle de lloguer?"),  # Encounter 22
                ("¿tiene el contrato?", "do you have the contract?", "té el contracte?"), ("¿ha consumido alcohol?", "have you consumed alcohol?", "ha consumit alcohol?"), ("¿ha tomado algo?", "have you had anything to drink?", "ha pres alguna cosa?"),  # Encounter 23
                ("¿entiende?", "do you understand?", "entén?"), ("¿puede explicar?", "can you explain it?", "pot explicar-ho?"), ("alcohol", "alcohol", "alcohol"),  # Encounter 24
                ("prueba", "test", "prova"), ("prueba de alcohol", "breath test", "prova d’alcohol"), ("sople aquí", "blow here (Ud.)", "bufi aquí"),  # Encounter 25
                ("resultado", "result", "resultat"), ("negativo", "negative", "negatiu"), ("positivo", "positive", "positiu"),  # Encounter 26
                ("bajo la influencia", "under the influence", "sota la influència"), ("sobrio", "sober", "savi"), ("verifican el sistema", "they check the system", "comproven el sistema"),  # Encounter 27
                ("registro activo", "active registration", "registre actiu"), ("seguro activo", "active insurance", "assegurança activa"), ("no aparece", "it does not show up", "no apareix"),  # Encounter 28
                ("pendiente", "pending", "pendent"), ("multa", "ticket", "multa"), ("advertencia", "warning", "advertència"),  # Encounter 29
                ("sanción", "penalty", "sanció"), ("emiten la multa", "they issue the ticket", "emeten la multa"), ("dan una advertencia", "they give a warning", "donen un avís"),  # Encounter 30
                ("paga la multa", "pay the ticket", "pagi la multa"), ("en línea", "online", "en línia"), ("plazo", "deadline", "termini"),  # Encounter 31
                ("monto", "amount", "import"), ("carretera", "road", "carretera"), ("calle", "street", "carrer"),  # Encounter 32
                ("zona urbana", "urban area", "zona urbana"), ("zona escolar", "school zone", "zona escolar"), ("autopista", "highway", "autopista"),  # Encounter 33
                ("señal", "sign", "senyal"), ("señalización", "road signage", "senyalització"), ("dirección", "direction", "adreça"),  # Encounter 34
                ("carril derecho", "right lane", "carril dret"), ("alquiler", "rental", "lloguer"), ("contrato", "contract", "contracte"),  # Encounter 35
                ("propietario", "owner", "propietari"), ("está a su nombre", "it is in your name", "és al seu nom"), ("no es mío", "it is not mine", "no és meu"),  # Encounter 36
                ("vehículo prestado", "borrowed vehicle", "vehicle prestat"), ("permiso del dueño", "owner's permission", "permís del propietari"), ("no lo encuentro", "I cannot find it", "no el trobo"),  # Encounter 37
                ("no lo tengo", "I do not have it", "no el tinc"), ("no carga", "it does not load", "no carrega"), ("sin señal", "without signal", "sense senyal"),  # Encounter 38
                ("en el celular", "on the cellphone", "al mòbil"), ("copia digital", "digital copy", "còpia digital"), ("sin documento", "without the document", "sense document"),  # Encounter 39
                ("vencido", "expired", "vençut"), ("por vencer", "about to expire", "a punt de vèncer"), ("no es válido", "it is not valid", "no és vàlid"),  # Encounter 40
                ("no entiendo", "I do not understand", "no entenc"), ("¿puede repetir?", "can you repeat that?", "pot repetir-ho?"), ("más despacio", "more slowly", "més a poc a poc"),  # Encounter 41
                ("¿qué significa?", "what does that mean?", "què significa?"), ("¿es una multa?", "is it a ticket?", "és una multa?"), ("¿es una advertencia?", "is it a warning?", "és un avís?"),  # Encounter 42
                ("¿puedo irme?", "can I leave?", "em puc anar?"), ("¿puedo seguir?", "can I continue?", "puc continuar?"), ("control", "checkpoint", "control"),  # Encounter 43
                ("oríllese", "pull over (Ud.)", "aturi's al voral"), ("orilla", "roadside", "vorera"), ("luces de emergencia", "hazard lights", "intermitents d'emergència"),  # Encounter 44
                ("documento físico", "physical document", "document físic"), ("permiso de conducir", "driver's license", "permís de conduir"), ("matrícula", "license plate", "matrícula"),  # Encounter 45
                ("agente de tránsito", "traffic officer", "agent de trànsit"), ("triángulo", "warning triangle", "triangle de senyalització"), ("chaleco reflectante", "reflective vest", "armilla reflectant"),  # Encounter 46
                ("accidente", "accident", "accident"), ("choque", "crash", "xoc"), ("reporte", "report", "informe"),  # Encounter 47
                ("reporte policial", "police report", "informe policial"), ("testigo", "witness", "testimoni"), ("declaración", "statement", "declaració"),  # Encounter 48
                ("firme aquí", "sign here (Ud.)", "signi aquí"), ("corte", "court", "jutjat"), ("fecha de corte", "court date", "data de judici"),  # Encounter 49
                ("comparecencia", "court appearance", "compareixença"), ("grúa", "tow truck", "grua"), ("remolque", "towing", "remolc"),  # Encounter 50
            ],
        },
    ],
    "restaurant": [
        {
            "title": "Eating Out",
            "goal": "Order food, interact with the server, and pay for your meal",
            "word_prefix": "rest",
            "words": [
                ("menú", "menu", "menú"), ("carta", "menu", "carta"), ("mesero", "waiter", "cambrer"),  # Encounter 1
                ("mesa", "table", "taula"), ("reserva", "reservation", "reserva"), ("¿tienen reserva?", "do you have a reservation?", "tenen reserva?"),  # Encounter 2
                ("mesa para dos", "table for two", "taula per a dos"), ("pido", "I order", "demano"), ("¿qué desea?", "what would you like?", "què desitja?"),  # Encounter 3
                ("¿qué van a pedir?", "what are you going to order?", "què demanareu?"), ("tomo la orden", "I take the order", "prenc la comanda"), ("aquí está el menú", "here is the menu", "aquí teniu el menú"),  # Encounter 4
                ("recomendación", "recommendation", "recomanació"), ("¿qué recomienda?", "what do you recommend?", "què recomana?"), ("plato", "dish", "plat"),  # Encounter 5
                ("entrada", "appetizer", "entrada"), ("plato principal", "main dish", "plat principal"), ("postre", "dessert", "postres"),  # Encounter 6
                ("acompañamiento", "side dish", "acompanyament"), ("guarnición", "side dish", "guarnició"), ("porción", "portion", "porció"),  # Encounter 7
                ("ingrediente", "ingredient", "ingredient"), ("salsa", "sauce", "salsa"), ("arroz", "rice", "arròs"),  # Encounter 8
                ("pollo", "chicken", "pollastre"), ("carne", "meat", "carn"), ("pescado", "fish", "peix"),  # Encounter 9
                ("verduras", "vegetables", "verdures"), ("ensalada", "salad", "amanida"), ("vegetariano", "vegetarian", "vegetarià"),  # Encounter 10
                ("vegano", "vegan", "vegà"), ("alergia", "allergy", "al·lèrgia"), ("alérgico", "allergic", "al·lèrgic"),  # Encounter 11
                ("frutos secos", "nuts", "fruits secs"), ("sin", "without", "sense"), ("con", "with", "amb"),  # Encounter 12
                ("¿tiene…?", "does it have…?", "té…?"), ("¿lleva…?", "does it come with…?", "porta…?"), ("sin picante", "not spicy", "sense picant"),  # Encounter 13
                ("picante", "spicy", "picant"), ("poco picante", "mildly spicy", "poc picant"), ("sin carne", "without meat", "sense carn"),  # Encounter 14
                ("sin gluten", "gluten-free", "sense gluten"), ("¿se puede cambiar?", "can it be changed?", "es pot canviar?"), ("bebida", "drink", "beguda"),  # Encounter 15
                ("agua", "water", "aigua"), ("con gas", "sparkling", "amb gas"), ("sin gas", "still", "sense gas"),  # Encounter 16
                ("refresco", "soda", "refresc"), ("jugo", "juice", "suc"), ("cerveza", "beer", "cervesa"),  # Encounter 17
                ("vino", "wine", "vi"), ("copa", "glass", "copa"), ("botella", "bottle", "ampolla"),  # Encounter 18
                ("¿algo de tomar?", "would you like something to drink?", "vols alguna cosa per beure?"), ("tiempo de espera", "wait time", "temps d'espera"), ("¿cuánto tiempo tarda?", "how long does it take?", "quant de temps triga?"),  # Encounter 19
                ("regreso enseguida", "I come right back", "torno de seguida"), ("aquí está", "here it is", "aquí està"), ("falta", "it is missing", "falta"),  # Encounter 20
                ("no llegó", "it did not arrive", "no va arribar"), ("pedimos la comida", "we order the food", "demanem el menjar"), ("trae", "bring (command)", "porta"),  # Encounter 21
                ("lleva", "it comes with", "porta"), ("sirve", "it serves", "serveix"), ("mesa lista", "ready table", "taula preparada"),  # Encounter 22
                ("síganme", "follow me (Uds.)", "segueixin-me"), ("error", "mistake", "error"), ("equivocado", "wrong", "equivocat"),  # Encounter 23
                ("no es esto", "this is not it", "no és això"), ("no pedimos eso", "we did not order that", "no vam demanar això"), ("falta esto", "this is missing", "falta això"),  # Encounter 24
                ("cambio", "change", "canvi"), ("cambian el plato", "they change the dish", "canvien el plat"), ("cocina", "kitchen", "cuina"),  # Encounter 25
                ("preparan otro plato", "they prepare another dish", "preparen un altre plat"), ("tardó mucho", "it took too long", "va trigar molt"), ("frío", "cold", "fred"),  # Encounter 26
                ("caliente", "hot", "calent"), ("recalentado", "reheated", "recalentat"), ("¿qué es esto?", "what is this?", "què és això?"),  # Encounter 27
                ("¿qué lleva?", "what does it have?", "què porta?"), ("¿cómo es?", "what is it like?", "com és?"), ("¿está listo?", "is it ready?", "està llest?"),  # Encounter 28
                ("¿falta mucho?", "is there much longer to wait?", "queda molt?"), ("¿puede explicar?", "can you explain it?", "pot explicar-ho?"), ("no entiendo", "I do not understand", "no entenc"),  # Encounter 29
                ("repítalo", "repeat it (Ud.)", "repeteixi-ho"), ("más despacio", "more slowly", "més a poc a poc"), ("aclárelo", "clarify it (Ud.)", "aclari-ho"),  # Encounter 30
                ("cuenta", "bill", "compte"), ("la cuenta", "the bill", "el compte"), ("total", "total", "total"),  # Encounter 31
                ("precio", "price", "preu"), ("incluye", "it includes", "inclou"), ("no incluye", "it does not include", "no inclou"),  # Encounter 32
                ("propina", "tip", "propina"), ("servicio", "service", "servei"), ("dividimos la cuenta", "we split the bill", "dividim el compte"),  # Encounter 33
                ("pago", "payment", "pagament"), ("con tarjeta", "with a card", "amb targeta"), ("en efectivo", "in cash", "en efectiu"),  # Encounter 34
                ("terminal", "card terminal", "terminal"), ("no funciona", "it does not work", "no funciona"), ("recibo", "receipt", "rebut"),  # Encounter 35
                ("mesa libre", "free table", "taula lliure"), ("ocupado", "occupied", "ocupat"), ("lleno", "full", "ple"),  # Encounter 36
                ("afuera", "outside", "a fora"), ("adentro", "inside", "a dins"), ("terraza", "patio", "terrassa"),  # Encounter 37
                ("aire acondicionado", "air conditioning", "aire condicionat"), ("ruido", "noise", "soroll"), ("tranquilo", "quiet", "tranquil"),  # Encounter 38
                ("ambiente", "atmosphere", "ambient"), ("para dos", "for two", "per a dos"), ("más", "more", "més"),  # Encounter 39
                ("menos", "less", "menys"), ("suficiente", "enough", "suficient"), ("extra", "extra", "extra"),  # Encounter 40
                ("otra", "another one", "una altra"), ("lo mismo", "the same", "el mateix"), ("para llevar", "to go", "per emportar"),  # Encounter 41
                ("pedido", "order", "comanda"), ("factura", "invoice", "factura"), ("reserva confirmada", "confirmed reservation", "reserva confirmada"),  # Encounter 42
                ("mesa asignada", "assigned table", "taula assignada"), ("lista de espera", "waitlist", "llista d'espera"), ("disponibilidad", "availability", "disponibilitat"),  # Encounter 43
                ("horario", "opening hours", "horari"), ("cubiertos", "utensils", "estris"), ("cuchara", "spoon", "cullera"),  # Encounter 44
                ("tenedor", "fork", "forquilla"), ("cuchillo", "knife", "ganivet"), ("servilleta", "napkin", "tovalló"),  # Encounter 45
                ("vaso", "glass", "got"), ("taza", "cup", "tassa"), ("hielo", "ice", "gel"),  # Encounter 46
                ("sin hielo", "without ice", "sense gel"), ("otra ronda", "another round", "una altra ronda"), ("traen la cuenta", "they bring the bill", "porten el compte"),  # Encounter 47
                ("cobro adicional", "extra charge", "càrrec addicional"), ("cargo por servicio", "service charge", "càrrec per servei"), ("plato hondo", "bowl", "bol"),  # Encounter 48
                ("plato llano", "dinner plate", "plat pla"), ("cubierto extra", "extra utensil", "estri extra"), ("para compartir", "to share", "per compartir"),  # Encounter 49
                ("recogen los platos", "they clear the plates", "recullen els plats"), ("mesa sucia", "dirty table", "taula bruta"), ("mesa limpia", "clean table", "taula neta"),  # Encounter 50
            ],
        },
    ],
    "small_talk": [
        {
            "title": "Meeting a Neighbor",
            "goal": "Have a friendly conversation with your neighbor about building life",
            "word_prefix": "talk",
            "words": [
                ("vecino", "neighbor", "veí"), ("vecina", "female neighbor", "veïna"), ("edificio", "building", "edifici"),  # Encounter 1
                ("departamento", "apartment", "pis"), ("casa", "house", "casa"), ("zona", "area", "zona"),  # Encounter 2
                ("barrio", "neighborhood", "barri"), ("ruido", "noise", "soroll"), ("música", "music", "música"),  # Encounter 3
                ("volumen", "volume", "volum"), ("baja el volumen", "lower the volume", "baixa el volum"), ("reunión", "gathering", "reunió"),  # Encounter 4
                ("fiesta", "party", "festa"), ("anoche", "last night", "ahir a la nit"), ("tarde", "late", "tard"),  # Encounter 5
                ("temprano", "early", "d'hora"), ("trabajo temprano", "I work early", "treballo d'hora"), ("no pude dormir", "I could not sleep", "no vaig poder dormir"),  # Encounter 6
                ("quería comentarte algo", "I wanted to mention something to you", "volia comentar-te una cosa"), ("solo quería avisarte", "I just wanted to let you know", "només volia avisar-te"), ("la próxima vez", "next time", "la propera vegada"),  # Encounter 7
                ("tenga cuidado", "be careful (Ud.)", "tingui cura"), ("estacionamiento", "parking", "aparcament"), ("lugar", "spot", "lloc"),  # Encounter 8
                ("espacio", "space", "espai"), ("mi lugar", "my spot", "el meu lloc"), ("asignado", "assigned", "assignat"),  # Encounter 9
                ("visitante", "visitor", "visitant"), ("mueve el carro", "move the car", "mou el cotxe"), ("lo muevo ahora mismo", "I move it right now", "el moc ara mateix"),  # Encounter 10
                ("ya pasó dos veces", "it has already happened twice", "ja ha passat dues vegades"), ("no sabía", "I did not know", "no sabia"), ("no fue intencional", "it was not intentional", "no va ser intencionat"),  # Encounter 11
                ("paquete", "package", "paquet"), ("entrega", "delivery", "entrega"), ("repartidor", "delivery person", "repartidor"),  # Encounter 12
                ("puerta", "door", "porta"), ("lo dejó aquí por error", "he left it here by mistake", "el va deixar aquí per error"), ("nombre", "name", "nom"),  # Encounter 13
                ("mi nombre", "my name", "el meu nom"), ("aquí está su paquete", "here is your package", "aquí té el seu paquet"), ("lo tengo", "I have it", "ho tinc"),  # Encounter 14
                ("se perdió", "it got lost", "es va perdre"), ("pasa seguido", "it happens often", "passa sovint"), ("hace tiempo", "a long time ago", "fa temps"),  # Encounter 15
                ("hace meses", "months ago", "fa mesos"), ("hace un año", "a year ago", "fa un any"), ("vivo aquí", "I live here", "visc aquí"),  # Encounter 16
                ("me mudé", "I moved", "em vaig mudar"), ("¿te gusta vivir aquí?", "do you like living here?", "t'agrada viure aquí?"), ("me gusta", "I like it", "m'agrada"),  # Encounter 17
                ("es tranquilo", "it is quiet", "és tranquil"), ("es ruidoso", "it is noisy", "és sorollós"), ("agua", "water", "aigua"),  # Encounter 18
                ("fuga", "leak", "fuita"), ("humedad", "dampness", "humitat"), ("pared", "wall", "paret"),  # Encounter 19
                ("tubería", "pipe", "canonada"), ("problema de agua", "water issue", "problema d’aigua"), ("administración", "building management", "administració"),  # Encounter 20
                ("ya llamé", "I already called", "ja he trucat"), ("no han venido", "they have not come", "no han vingut"), ("mejor así", "it is better this way", "millor així"),  # Encounter 21
                ("más urgente", "more urgent", "més urgent"), ("cierra la llave de agua", "shut off the water valve", "tanca la clau de l'aigua"), ("llave de agua", "water valve", "clau d'aigua"),  # Encounter 22
                ("puede empeorar", "it can get worse", "pot empitjorar"), ("avísame", "let me know", "avisa'm"), ("me dices", "tell me", "em dius"),  # Encounter 23
                ("entiendo", "I understand", "entenc"), ("tiene sentido", "it makes sense", "té sentit"), ("cerca", "nearby", "a prop"),  # Encounter 24
                ("lejos", "far", "lluny"), ("piso", "floor", "pis"), ("mismo piso", "same floor", "mateix pis"),  # Encounter 25
                ("arriba", "upstairs", "a dalt"), ("abajo", "downstairs", "a baix"), ("toca la puerta", "knock on the door", "toca la porta"),  # Encounter 26
                ("abre", "it opens", "obre"), ("cierra", "it closes", "tanca"), ("trabajo", "work", "feina"),  # Encounter 27
                ("horario", "schedule", "horari"), ("ocupado", "busy", "ocupat"), ("libre", "free", "lliure"),  # Encounter 28
                ("fin de semana", "weekend", "cap de setmana"), ("hoy", "today", "avui"), ("mañana", "tomorrow", "demà"),  # Encounter 29
                ("ayer", "yesterday", "ahir"), ("en un rato", "in a little while", "d'aquí a una estona"), ("prestas una herramienta", "lend a tool", "prestes una eina"),  # Encounter 30
                ("herramienta", "tool", "eina"), ("llave inglesa", "wrench", "clau anglesa"), ("taladro", "drill", "trepant"),  # Encounter 31
                ("escalera", "ladder", "escala"), ("basura", "trash", "escombraries"), ("saco la basura", "I take out the trash", "trec la brossa"),  # Encounter 32
                ("reciclaje", "recycling", "reciclatge"), ("ascensor", "elevator", "ascensor"), ("timbre", "doorbell", "timbre"),  # Encounter 33
                ("portón", "gate", "porta gran"), ("entrada principal", "main entrance", "entrada principal"), ("llave", "key", "clau"),  # Encounter 34
                ("copia de llave", "spare key", "còpia de clau"), ("administración del edificio", "building management", "administració de l’edifici"), ("portero", "doorman", "porter"),  # Encounter 35
                ("conserje", "caretaker", "conserge"), ("paquete equivocado", "wrong package", "paquet equivocat"), ("se confundieron de puerta", "they got the door wrong", "es van confondre de porta"),  # Encounter 36
                ("visita", "visitor", "visita"), ("visitas", "guests", "visites"), ("¿espera visitas?", "are you expecting guests?", "espera visites?"),  # Encounter 37
                ("mudanza", "move", "mudança"), ("camión de mudanza", "moving truck", "camió de mudances"), ("se mudan hoy", "they move today", "es muden avui"),  # Encounter 38
                ("mascota", "pet", "mascota"), ("perro", "dog", "gos"), ("gato", "cat", "gat"),  # Encounter 39
                ("correa", "leash", "cinturó"), ("ladra mucho", "it barks a lot", "lladra molt"), ("¿cómo se llama?", "what is it called?", "com es diu?"),  # Encounter 40
                ("jardín", "garden", "jardí"), ("plantas", "plants", "plantes"), ("riego", "watering", "reg"),  # Encounter 41
                ("riega las plantas", "water the plants", "rega les plantes"), ("balcón", "balcony", "balcó"), ("ventana", "window", "finestra"),  # Encounter 42
                ("corriente de aire", "draft", "corrent d’aire"), ("hace frío aquí", "it is cold here", "fa fred aquí"), ("hace calor aquí", "it is hot here", "fa calor aquí"),  # Encounter 43
                ("humedad en el techo", "moisture on the ceiling", "humitat al sostre"), ("corte de agua", "water outage", "tall d’aigua"), ("corte de luz", "power outage", "tall de llum"),  # Encounter 44
                ("luz", "electricity", "llum"), ("se fue la luz", "the power went out", "va faltar la llum"), ("vuelve pronto", "it comes back soon", "torna aviat"),  # Encounter 45
                ("vecino nuevo", "new neighbor", "veí nou"), ("recién llegado", "newly arrived", "recent arribat"), ("¿desde cuándo vive aquí?", "since when do you live here?", "des de quan viu aquí?"),  # Encounter 46
                ("alquiler", "rent", "lloguer"), ("subió el alquiler", "the rent went up", "va pujar el lloguer"), ("administración no responde", "management does not respond", "l’administració no respon"),  # Encounter 47
                ("queja", "complaint", "queixa"), ("pongo una queja", "I file a complaint", "poso una queixa"), ("ruido arriba", "upstairs noise", "soroll a dalt"),  # Encounter 48
                ("ruido abajo", "downstairs noise", "soroll a baix"), ("pasillo", "hallway", "passadís"), ("entrada trasera", "back entrance", "entrada posterior"),  # Encounter 49
                ("puerta principal", "front door", "porta principal"), ("buzón", "mailbox", "bústia"), ("correo", "mail", "correu"),  # Encounter 50
            ],
        },
    ],
    "internet": [
        {
            "title": "Setting Up WiFi",
            "goal": "Set up your internet service by speaking with the technician",
            "word_prefix": "inet",
            "words": [
                ("internet", "internet", "internet"), ("wifi", "WiFi", "wifi"), ("red inalámbrica", "wireless network", "xarxa sense fils"),  # Encounter 1
                ("wifi doméstico", "home WiFi", "wifi domèstic"), ("clave de acceso", "access code", "clau d'accés"), ("red local", "local network", "xarxa local"),  # Encounter 2
                ("router", "router", "router"), ("cable", "cable", "cable"), ("intensidad", "signal strength", "intensitat"),  # Encounter 3
                ("enrutador", "router", "enrutador"), ("cable de red", "network cable", "cable de xarxa"), ("tomacorriente", "outlet", "endoll"),  # Encounter 4
                ("plan", "plan", "pla"), ("pausado", "slow", "pausat"), ("rapidez", "speed", "rapidesa"),  # Encounter 5
                ("paquete de datos", "data plan", "paquet de dades"), ("cuota mensual", "monthly fee", "quota mensual"), ("visita", "visit", "visita"),  # Encounter 6
                ("nombre de red", "network name", "nom de xarxa"), ("colocar", "to install", "col·locar"), ("configurar", "to configure", "configurar"),  # Encounter 7
                ("conectar", "to connect", "connectar"), ("desconectar", "to disconnect", "desconnectar"), ("reiniciar", "to restart", "reiniciar"),  # Encounter 8
                ("especialista", "specialist", "especialista"), ("cita de servicio", "service appointment", "cita de servei"), ("SSID", "SSID", "SSID"),  # Encounter 9
                ("funcionar", "to work/function", "funcionar"), ("renombrar", "to rename", "renombrar"), ("solución", "solution", "solució"),  # Encounter 10
                ("banda ancha", "broadband", "banda ampla"), ("fibra óptica", "fiber optic", "fibra òptica"), ("megabits", "megabits", "megabits"),  # Encounter 11
                ("descargar", "to download", "descarregar"), ("ajustar", "to adjust", "ajustar"), ("enlazar", "to connect", "enllaçar"),  # Encounter 12
                ("cortar enlace", "to disconnect", "tallar enllaç"), ("rearrancar", "to restart", "rearrencar"), ("aparato", "device", "aparell"),  # Encounter 13
                ("portátil", "laptop", "portàtil"), ("teléfono móvil", "mobile phone", "telèfon mòbil"), ("operar", "to work/operate", "operar"),  # Encounter 14
                ("modem", "modem", "mòdem"), ("antena", "antenna", "antena"), ("inconveniente", "issue", "inconvenient"),  # Encounter 15
                ("conexión de alta velocidad", "high-speed connection", "connexió d'alta velocitat"), ("cable óptico", "fiber optic cable", "cable òptic"), ("alcance", "range", "abast"),  # Encounter 16
                ("corte", "outage", "cort"), ("interrupción", "interruption", "interrupció"), ("megabytes", "megabytes", "megabytes"),  # Encounter 17
                ("bajar archivos", "to download files", "baixar arxius"), ("permanencia", "commitment period", "permanència"), ("cargar archivos", "to upload files", "carregar arxius"),  # Encounter 18
                ("fecha de pago", "payment date", "data de pagament"), ("mejorar", "to improve", "millorar"), ("soporte al cliente", "customer support", "suport al client"),  # Encounter 19
                ("televisión", "television", "televisió"), ("comunicarse", "to communicate", "comunicar-se"), ("combo", "bundle", "combo"),  # Encounter 20
                ("streaming", "streaming", "streaming"), ("videollamada", "video call", "videotrucada"), ("juego en línea", "online gaming", "joc en línia"),  # Encounter 21
                ("módem", "modem", "mòdem"), ("ilimitado", "unlimited", "il·limitat"), ("antena receptora", "receiving antenna", "antena receptora"),  # Encounter 22
                ("decodificador", "decoder", "decodificador"), ("firewall", "firewall", "firewall"), ("área de cobertura", "coverage area", "àrea de cobertura"),  # Encounter 23
                ("virus", "virus", "virus"), ("malware", "malware", "malware"), ("antivirus", "antivirus", "antivirus"),  # Encounter 24
                ("extensión", "extension/extender", "extensió"), ("repetidor", "repeater", "repetidor"), ("amplificar", "to amplify", "amplificar"),  # Encounter 25
                ("dirección IP", "IP address", "adreça IP"), ("DNS", "DNS", "DNS"), ("puerto", "port", "port"),  # Encounter 26
                ("ethernet", "ethernet", "ethernet"), ("inalámbrico", "wireless", "inalàmbric"), ("bluetooth", "bluetooth", "bluetooth"),  # Encounter 27
                ("latencia", "latency", "latència"), ("ping", "ping", "ping"), ("estabilidad", "stability", "estabilitat"),  # Encounter 28
                ("asistencia técnica", "technical support", "assistència tècnica"), ("soporte", "support", "suport"), ("extensión de señal", "signal range", "extensió de senyal"),  # Encounter 29
                ("apagón", "outage", "apagada"), ("navegador", "browser", "navegador"), ("página web", "webpage", "pàgina web"),  # Encounter 30
                ("usuario", "username", "usuari"), ("falla", "failure", "fallada"), ("registrar", "to register", "registrar"),  # Encounter 31
                ("restablecer", "to restore", "restablir"), ("acuerdo de servicio", "service agreement", "acord de servei"), ("periodo de permanencia", "commitment period", "període de permanència"),  # Encounter 32
                ("control parental", "parental controls", "control parental"), ("dar de baja", "to cancel", "donar de baixa"), ("renovar plan", "to upgrade plan", "renovar pla"),  # Encounter 33
                ("cámara", "camera", "càmera"), ("monitor", "monitor", "monitor"), ("vigilancia", "surveillance", "vigilància"),  # Encounter 34
                ("domótica", "home automation", "domòtica"), ("inteligente", "smart", "intel·ligent"), ("automatizar", "to automate", "automatitzar"),  # Encounter 35
                ("optimizar", "to improve", "optimitzar"), ("almacenar", "to store", "emmagatzemar"), ("combo de servicios", "service bundle", "combo de serveis"),  # Encounter 36
                ("impresora", "printer", "impressora"), ("compartir", "to share", "compartir"), ("acceso remoto", "remote access", "accés remot"),  # Encounter 37
                ("VPN", "VPN", "VPN"), ("privacidad", "privacy", "privacitat"), ("encriptar", "to encrypt", "encriptar"),  # Encounter 38
                ("ancho de banda", "bandwidth", "ample de banda"), ("saturado", "saturated", "saturat"), ("TV por cable", "cable TV", "TV per cable"),  # Encounter 39
                ("línea fija", "landline", "línia fixa"), ("competencia", "competition", "competència"), ("paquete triple", "triple bundle", "paquet triple"),  # Encounter 40
                ("instalación", "installation", "instal·lació"), ("cableado", "wiring", "cablejat"), ("infraestructura", "infrastructure", "infraestructura"),  # Encounter 41
                ("contratación", "hiring/contracting", "contractació"), ("video en vivo", "live streaming", "vídeo en viu"), ("llamada de video", "video call", "trucada de vídeo"),  # Encounter 42
                ("migración", "migration", "migració"), ("portabilidad", "portability", "portabilitat"), ("juego en red", "online gaming", "joc en xarxa"),  # Encounter 43
                ("tope de datos", "data cap", "topall de dades"), ("sin tope", "unlimited", "sense topall"), ("uso de datos", "data usage", "ús de dades"),  # Encounter 44
                ("queja", "complaint", "queixa"), ("protección de red", "network security", "protecció de xarxa"), ("cortafuegos", "firewall", "cortafocs"),  # Encounter 45
                ("resguardar", "to protect", "resguardar"), ("consumo real", "actual usage", "consum real"), ("programa malicioso", "malicious software", "programa maliciós"),  # Encounter 46
                ("satelital", "satellite", "satel·lit"), ("rural", "rural", "rural"), ("urbano", "urban", "urbà"),  # Encounter 47
                ("mantenimiento", "maintenance", "manteniment"), ("actualización", "update", "actualització"), ("software dañino", "harmful software", "programari maliciós"),  # Encounter 48
                ("programa de protección", "protection software", "programa de protecció"), ("amplificador", "amplifier", "amplificador"), ("encuesta", "survey", "enquesta"),  # Encounter 49
                ("listo", "ready", "llest"), ("funcionando", "working", "funcionant"), ("repetidor de señal", "signal repeater", "repetidor de senyal"),  # Encounter 50
            ],
        },
    ],
    "core": [
        {
            "title": "Core",
            "goal": "Practice essential everyday Spanish phrases and expressions",
            "word_prefix": "core",
            "words": [
                ("quiero dormir", "I want to sleep", ""), ("quiero comer", "I want to eat", ""), ("quiero irme", "I want to leave", ""),  # Encounter 1
                ("necesito comer", "I need to eat", ""), ("necesito dormir", "I need to sleep", ""), ("necesito salir", "I need to leave", ""),  # Encounter 2
                ("puedo entrar", "I can enter", ""), ("puedo pasar", "I can come in", ""), ("puedo sentarme", "I can sit down", ""),  # Encounter 3
                ("no puedo encontrarlo", "I can't find it", ""), ("no puedo hacerlo", "I can't do it", ""), ("no puedo verlo", "I can't see it", ""),  # Encounter 4
                ("voy a salir", "I'm going to leave", ""), ("voy a entrar", "I'm going to enter", ""), ("voy a volver", "I'm going to return", ""),  # Encounter 5
                ("estoy buscando", "I am looking", ""), ("estoy esperando", "I am waiting", ""), ("estoy trabajando", "I am working", ""),  # Encounter 6
                ("tengo que trabajar", "I have to work", ""), ("tengo que salir", "I have to leave", ""), ("tengo que pagar", "I have to pay", ""),  # Encounter 7
                ("no tengo que pagar", "I don't have to pay", ""), ("no tengo que ir", "I don't have to go", ""), ("no tengo que hacerlo", "I don't have to do it", ""),  # Encounter 8
                ("debo llamar", "I should call", ""), ("debo ir", "I should go", ""), ("debo pagar", "I should pay", ""),  # Encounter 9
                ("trato de entender", "I try to understand", ""), ("trato de encontrarlo", "I try to find it", ""), ("trato de hacerlo", "I try to do it", ""),  # Encounter 10
                ("puedes ayudarme", "can you help me", ""), ("puedes llamarme", "can you call me", ""), ("puedes esperarme", "can you wait for me", ""),  # Encounter 11
                ("puedes darme agua", "can you give me water", ""), ("puedes darme eso", "can you give me that", ""), ("puedes darme tiempo", "can you give me time", ""),  # Encounter 12
                ("me puedes ayudar con esto", "can you help me with this", ""), ("me puedes ayudar con eso", "can you help me with that", ""), ("me puedes ayudar con el problema", "can you help me with the problem", ""),  # Encounter 13
                ("necesito que vengas", "I need you to come", ""), ("necesito que me ayudes", "I need you to help me", ""), ("necesito que esperes", "I need you to wait", ""),  # Encounter 14
                ("dime la verdad", "tell me the truth", ""), ("dime qué pasa", "tell me what's happening", ""), ("dime dónde está", "tell me where it is", ""),  # Encounter 15
                ("explícame cómo funciona", "explain how it works to me", ""), ("explícame qué pasó", "explain what happened to me", ""), ("explícame por qué", "explain why to me", ""),  # Encounter 16
                ("muéstrame dónde está", "show me where it is", ""), ("muéstrame cómo funciona", "show me how it works", ""), ("muéstrame el camino", "show me the way", ""),  # Encounter 17
                ("déjame ver", "let me see", ""), ("déjame hacerlo", "let me do it", ""), ("déjame entrar", "let me enter", ""),  # Encounter 18
                ("ayúdame a encontrarlo", "help me find it", ""), ("ayúdame a hacerlo", "help me do it", ""), ("ayúdame a entender", "help me understand", ""),  # Encounter 19
                ("no me digas eso", "don't tell me that", ""), ("no me digas nada", "don't tell me anything", ""), ("no me digas mentiras", "don't tell me lies", ""),  # Encounter 20
                ("estoy en el hotel", "I am at the hotel", ""), ("estoy en casa", "I am at home", ""), ("estoy en la calle", "I am on the street", ""),  # Encounter 21
                ("voy al baño", "I'm going to the bathroom", ""), ("voy al hotel", "I'm going to the hotel", ""), ("voy al trabajo", "I'm going to work", ""),  # Encounter 22
                ("vengo de la tienda", "I come from the store", ""), ("vengo del trabajo", "I come from work", ""), ("vengo de casa", "I come from home", ""),  # Encounter 23
                ("estoy cerca del centro", "I'm near downtown", ""), ("estoy cerca de aquí", "I'm near here", ""), ("estoy cerca del lugar", "I'm near the place", ""),  # Encounter 24
                ("estoy lejos de aquí", "I'm far from here", ""), ("estoy lejos del centro", "I'm far from downtown", ""), ("estoy lejos de casa", "I'm far from home", ""),  # Encounter 25
                ("voy hacia la salida", "I'm heading toward the exit", ""), ("voy hacia el centro", "I'm heading toward downtown", ""), ("voy hacia la puerta", "I'm heading toward the door", ""),  # Encounter 26
                ("paso por tu casa", "I pass by your house", ""), ("paso por aquí", "I pass by here", ""), ("paso por el centro", "I pass through downtown", ""),  # Encounter 27
                ("entro al edificio", "I enter the building", ""), ("entro a la casa", "I enter the house", ""), ("entro al lugar", "I enter the place", ""),  # Encounter 28
                ("salgo del trabajo", "I leave work", ""), ("salgo de casa", "I leave home", ""), ("salgo del edificio", "I leave the building", ""),  # Encounter 29
                ("me quedo en casa", "I stay at home", ""), ("me quedo aquí", "I stay here", ""), ("me quedo en el hotel", "I stay at the hotel", ""),  # Encounter 30
                ("ya comí", "I already ate", ""), ("ya llegué", "I already arrived", ""), ("ya terminé", "I already finished", ""),  # Encounter 31
                ("todavía estoy aquí", "I'm still here", ""), ("todavía estoy esperando", "I'm still waiting", ""), ("todavía estoy trabajando", "I'm still working", ""),  # Encounter 32
                ("aún no llega", "it hasn't arrived yet", ""), ("aún no empieza", "it hasn't started yet", ""), ("aún no termina", "it hasn't finished yet", ""),  # Encounter 33
                ("ahora mismo voy", "I'm going right now", ""), ("ahora mismo llego", "I'm arriving right now", ""), ("ahora mismo salgo", "I'm leaving right now", ""),  # Encounter 34
                ("después de comer", "after eating", ""), ("después de trabajar", "after working", ""), ("después de salir", "after leaving", ""),  # Encounter 35
                ("antes de salir", "before leaving", ""), ("antes de comer", "before eating", ""), ("antes de entrar", "before entering", ""),  # Encounter 36
                ("desde ayer", "since yesterday", ""), ("desde hoy", "since today", ""), ("desde la mañana", "since the morning", ""),  # Encounter 37
                ("por dos horas", "for two hours", ""), ("por un rato", "for a while", ""), ("por unos días", "for a few days", ""),  # Encounter 38
                ("en diez minutos", "in ten minutes", ""), ("en un momento", "in a moment", ""), ("en un rato", "in a bit", ""),  # Encounter 39
                ("cuando llegues", "when you arrive", ""), ("cuando salgas", "when you leave", ""), ("cuando puedas", "when you can", ""),  # Encounter 40
                ("tengo hambre", "I'm hungry", ""), ("tengo sueño", "I'm sleepy", ""), ("tengo frío", "I'm cold", ""),  # Encounter 41
                ("tengo calor", "I'm hot", ""), ("me siento cansado", "I feel tired", ""), ("me siento bien", "I feel good", ""),  # Encounter 42
                ("me siento mal", "I feel bad", ""), ("me gusta este lugar", "I like this place", ""), ("me gusta esto", "I like this", ""),  # Encounter 43
                ("me gusta eso", "I like that", ""), ("no me gusta eso", "I don't like that", ""), ("no me gusta esto", "I don't like this", ""),  # Encounter 44
                ("no me gusta aquí", "I don't like it here", ""), ("necesito dinero", "I need money", ""), ("necesito ayuda", "I need help", ""),  # Encounter 45
                ("necesito tiempo", "I need time", ""), ("busco un baño", "I'm looking for a bathroom", ""), ("busco ayuda", "I'm looking for help", ""),  # Encounter 46
                ("busco el lugar", "I'm looking for the place", ""), ("encuentro la salida", "I find the exit", ""), ("encuentro el lugar", "I find the place", ""),  # Encounter 47
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

        num_encounters = len(words) // 3
        for enc_num in range(1, num_encounters + 1):
            # Word indices: 3 words per encounter
            base = (enc_num - 1) * 3
            w1 = words[base]
            w2 = words[base + 1]
            w3 = words[base + 2]

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
