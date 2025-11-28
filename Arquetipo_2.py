#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import unicodedata
import re

def normalizar_nombre(nombre):
    """
    Normaliza el nombre:
    - Pasa a mayúsculas
    - Quita acentos
    - Elimina caracteres que no sean letras A Z
    """
    if not isinstance(nombre, str):
        raise ValueError("El nombre debe ser una cadena de texto.")

    nfkd_form = unicodedata.normalize("NFKD", nombre)
    solo_ascii = "".join([c for c in nfkd_form if not unicodedata.combining(c)])
    solo_letras = re.sub(r"[^A-Za-z]", "", solo_ascii)
    return solo_letras.upper()


def letra_a_numero(letra):
    """
    Convierte una letra en su valor numerológico pitagórico.
    A 1, B 2, I 9, J 1, R 9, S 1, Z 8
    """
    mapa = {
        "A": 1, "J": 1, "S": 1,
        "B": 2, "K": 2, "T": 2,
        "C": 3, "L": 3, "U": 3,
        "D": 4, "M": 4, "V": 4,
        "E": 5, "N": 5, "W": 5,
        "F": 6, "O": 6, "X": 6,
        "G": 7, "P": 7, "Y": 7,
        "H": 8, "Q": 8, "Z": 8,
        "I": 9, "R": 9
    }
    return mapa.get(letra.upper(), 0)


def reducir_numero(numero):
    """
    Reduce un número sumando sus dígitos hasta obtener un dígito
    entre 1 y 9 o un número maestro 11, 22, 33.
    """
    if numero <= 0:
        raise ValueError("El número a reducir debe ser positivo.")

    while numero >= 10 and numero not in (11, 22, 33):
        suma = 0
        for digito in str(numero):
            suma += int(digito)
        numero = suma

    return numero


def reducir_simple(numero):
    """
    Reduce un número hasta un solo dígito entre 1 y 9,
    sin considerar números maestros.
    """
    if numero <= 0:
        raise ValueError("El número a reducir debe ser positivo.")

    while numero >= 10:
        suma = 0
        for digito in str(numero):
            suma += int(digito)
        numero = suma

    return numero


def analizar_fecha_numerologia(fecha_str):
    """
    Analiza la fecha de nacimiento y devuelve información detallada:
    día, mes, año, suma del año, total base y número de vida.
    Acepta formatos:
    DD/MM/AAAA
    AAAA-MM-DD
    """
    formatos_posibles = ["%d/%m/%Y", "%Y-%m-%d"]
    fecha_valida = None

    for fmt in formatos_posibles:
        try:
            fecha_valida = datetime.strptime(fecha_str.strip(), fmt)
            break
        except ValueError:
            continue

    if fecha_valida is None:
        raise ValueError("Formato de fecha no reconocido. Usa DD/MM/AAAA o AAAA-MM-DD.")

    dia = fecha_valida.day
    mes = fecha_valida.month
    ano = fecha_valida.year

    suma_ano = 0
    for caracter in str(ano):
        suma_ano += int(caracter)

    base_total = dia + mes + suma_ano
    numero_vida = reducir_numero(base_total)
    base_simple = reducir_simple(numero_vida)

    if numero_vida in (11, 22, 33):
        representacion_camino = f"{numero_vida}/{base_simple}"
    else:
        representacion_camino = str(numero_vida)

    return {
        "dia": dia,
        "mes": mes,
        "ano": ano,
        "suma_ano": suma_ano,
        "base_total": base_total,
        "numero_vida": numero_vida,
        "base_simple": base_simple,
        "representacion_camino": representacion_camino,
    }


def numero_desde_fecha(fecha_str):
    """
    Devuelve solo el número de vida a partir de la fecha.
    """
    info = analizar_fecha_numerologia(fecha_str)
    return info["numero_vida"]


def numero_desde_nombre(nombre):
    """
    Calcula el número del nombre desde el nombre completo.
    Devuelve un entero 1 9 o maestro 11, 22, 33.
    """
    nombre_normalizado = normalizar_nombre(nombre)
    if not nombre_normalizado:
        raise ValueError("El nombre no contiene letras válidas.")

    suma = 0
    for letra in nombre_normalizado:
        suma += letra_a_numero(letra)

    return reducir_numero(suma)


def obtener_energia_basica(numero):
    """
    Devuelve una descripción breve de la energía básica de un número 1 9.
    Siempre lo reduce a un solo dígito.
    """
    reducido = reducir_simple(numero)
    descripciones = {
        1: "impulso, identidad, coraje para iniciar",
        2: "sensibilidad, cooperación y energía de vínculo",
        3: "creatividad, expresión y alegría",
        4: "estructura, orden y disciplina",
        5: "cambio, libertad y experiencias intensas",
        6: "amor, responsabilidad y cuidado",
        7: "búsqueda interior, análisis y espiritualidad",
        8: "poder personal, logro y materia",
        9: "compasión, cierre de ciclos y servicio",
    }
    return reducido, descripciones.get(reducido, "energía no definida")


def arquetipo_desde_numero(numero):
    """
    Devuelve un diccionario con el arquetipo asociado a un número,
    desde un enfoque kabalista tikkun o corrección del alma.
    """
    arquetipos = {
        1: {
            "nombre": "Canal de Voluntad y Autoafirmación",
            "descripcion": (
                "Energía asociada a la chispa inicial del deseo. Representa la capacidad de "
                "iniciar, liderar y abrir camino. En términos kabalistas, es un canal fuerte "
                "de voluntad que puede conectarse con un propósito elevado cuando se alinea con la Luz."
            ),
            "perfeccionar": (
                "Transformar el orgullo y la necesidad de tener siempre la razón en liderazgo al servicio de algo más grande que el ego."
            ),
        },
        2: {
            "nombre": "Canal de Unión y Receptividad",
            "descripcion": (
                "Energía vinculada a la sensibilidad y al mundo de las relaciones. Refleja la conciencia de separación "
                "y la búsqueda de unidad. Se conecta con la idea de aprender a recibir de manera equilibrada, sin perder la propia esencia."
            ),
            "perfeccionar": (
                "Aprender a poner límites sin culpa y a no perder tu voz interior por miedo a ser rechazado."
            ),
        },
        3: {
            "nombre": "Canal de Expresión y Alegría Creativa",
            "descripcion": (
                "Energía que se vincula con la expresión del alma a través de la palabra, el arte y la comunicación. "
                "En la Kábala se asocia con la capacidad de revelar Luz a través de la belleza y la vibración de la alegría."
            ),
            "perfeccionar": (
                "Convertir la dispersión y la necesidad de aprobación en responsabilidad creativa y expresión auténtica."
            ),
        },
        4: {
            "nombre": "Canal de Estructura y Disciplina Espiritual",
            "descripcion": (
                "Energía relacionada con la construcción de recipientes firmes. Es la tarea de crear vasijas internas "
                "estables para sostener la Luz: orden, disciplina y trabajo constante."
            ),
            "perfeccionar": (
                "Soltar la rigidez y el control excesivo para integrar confianza, flexibilidad y fe en el proceso."
            ),
        },
        5: {
            "nombre": "Canal de Cambio y Libertad del Alma",
            "descripcion": (
                "Energía asociada al movimiento, el viaje y la expansión. Representa al alma que busca romper "
                "viejas limitaciones y expandir su conciencia a través de experiencias intensas."
            ),
            "perfeccionar": (
                "Transformar la huida y el miedo al compromiso en libertad interior con responsabilidad."
            ),
        },
        6: {
            "nombre": "Canal de Responsabilidad y Amor en el Hogar",
            "descripcion": (
                "Energía ligada al cuidado, la armonía familiar y la belleza. Es un campo donde el alma aprende a manifestar "
                "amor consciente en lo cotidiano, sin olvidarse de sí misma."
            ),
            "perfeccionar": (
                "Sanar el perfeccionismo y la autoexigencia, aprendiendo a cuidar sin cargar con todo el peso del mundo."
            ),
        },
        7: {
            "nombre": "Canal de Sabiduría Interior y Búsqueda Espiritual",
            "descripcion": (
                "Energía conectada con la introspección, el estudio y el misterio. Es el alma que busca entender la causa "
                "detrás de cada efecto y no se conforma con lo superficial."
            ),
            "perfeccionar": (
                "Transformar el aislamiento, la desconfianza y el exceso de mente en confianza espiritual y apertura al vínculo."
            ),
        },
        8: {
            "nombre": "Canal de Poder, Abundancia y Rectificación del Deseo",
            "descripcion": (
                "Energía vinculada a la manifestación en el plano material: liderazgo, recursos y autoridad. "
                "Tiene que ver con corregir el deseo de recibir solo para uno mismo hacia el deseo de recibir para compartir."
            ),
            "perfeccionar": (
                "Usar el poder y la abundancia como canales de Luz, no solo como logros del ego."
            ),
        },
        9: {
            "nombre": "Canal de Compasión y Servicio Universal",
            "descripcion": (
                "Energía que vibra con el cierre de ciclos, el perdón y el servicio al colectivo. "
                "Invita a comprender que todas las almas están conectadas."
            ),
            "perfeccionar": (
                "Soltar el apego al sufrimiento y al rol de salvador, integrando un servicio equilibrado y amoroso."
            ),
        },
        11: {
            "nombre": "Canal Maestro de Intuición y Revelación",
            "descripcion": (
                "Número maestro asociado a una sensibilidad espiritual muy elevada. Es un canal para recibir inspiración, "
                "visiones y mensajes que aportan claridad a otros."
            ),
            "perfeccionar": (
                "Confiar en tu intuición sin dejarte paralizar por el miedo al juicio, integrando tu visión espiritual en la vida práctica diaria."
            ),
        },
        22: {
            "nombre": "Canal Maestro de Construcción del Mundo",
            "descripcion": (
                "Número maestro ligado a la capacidad de materializar grandes proyectos colectivos. Es la misión de convertir "
                "ideas elevadas en recipientes concretos en el mundo físico."
            ),
            "perfeccionar": (
                "Equilibrar la presión interna de lograr cosas grandes con el autocuidado, la paciencia y la humildad."
            ),
        },
        33: {
            "nombre": "Canal Maestro de Amor y Sanación",
            "descripcion": (
                "Número maestro conectado con el amor expansivo y la sanación profunda. Sostiene procesos emocionales o espirituales muy sensibles."
            ),
            "perfeccionar": (
                "Aprender a servir sin vaciarte, sosteniendo límites amorosos y respetando tu propia energía vital."
            ),
        },
    }

    info = arquetipos.get(numero)
    if info is None:
        return {
            "nombre": "Arquetipo no definido",
            "descripcion": "El número calculado no tiene un arquetipo configurado en este script.",
            "perfeccionar": "No hay información de tikkun configurada para este número."
        }
    return info


# Plantillas de tikkun detalladas por número de vida
PLANTILLAS_TIKKUN = {
    1: {
        "tema_central": [
            "Aprender a usar tu fuerza de inicio como canal de Luz y no como imposición del ego.",
            "Pasar de la soledad orgullosa a la autenticidad que permite recibir ayuda sin sentirse débil.",
        ],
        "patrones": [
            "Sentirte responsable de abrir camino y tomar decisiones incluso cuando preferirías descansar.",
            "Choques con figuras de autoridad donde aparece el impulso de competir o demostrar que tienes razón.",
            "Momentos donde te exiges ser fuerte y autosuficiente, evitando mostrar vulnerabilidad.",
        ],
        "rectificacion_frases": [
            "Rectificar el orgullo y la dureza, transformándolos en liderazgo valiente y compasivo.",
            "Rectificar la idea de que pedir ayuda es debilidad, entendiendo que compartir también es fuerza.",
        ],
        "claves": [
            "Practicar decisiones donde elijas liderar sin aplastar las voces de los demás.",
            "Aprender a delegar pequeñas tareas para que el alma se acostumbre a no cargar con todo.",
            "Reconocer tus necesidades emocionales y expresarlas con honestidad.",
        ],
        "preguntas": [
            "Dónde estoy intentando hacerlo todo solo por miedo a que otros no estén a la altura.",
            "Qué parte de mí se siente obligada a ser siempre fuerte.",
            "Qué cambiaría si permitiera que mi liderazgo viniera más del corazón y menos del orgullo.",
        ],
    },
    2: {
        "tema_central": [
            "Sanar la dependencia emocional y el miedo al rechazo para crear vínculos de igualdad.",
            "Pasar de la necesidad de aprobación a la cooperación desde la dignidad.",
        ],
        "patrones": [
            "Relaciones donde te adaptas demasiado para no generar conflicto.",
            "Miedo a decir lo que sientes por temor a perder al otro.",
            "Dificultad para tomar decisiones solo por no equivocarte o decepcionar.",
        ],
        "rectificacion_frases": [
            "Rectificar la tendencia a borrarte para sostener la paz, transformándola en acuerdos claros y honestos.",
            "Rectificar la creencia de que solo mereces amor si no incomodas a nadie.",
        ],
        "claves": [
            "Practicar conversaciones donde expreses lo que sientes sin suavizar en exceso tu verdad.",
            "Reconocer cuándo ayudas desde el amor y cuándo lo haces por miedo a ser abandonado.",
            "Elegir relaciones donde tu voz tenga el mismo peso que la de los demás.",
        ],
        "preguntas": [
            "En qué situaciones sigo callando por miedo a perder a alguien.",
            "Dónde siento que doy más de lo que recibo.",
            "Qué aspecto de mi verdad ya no quiero seguir escondiendo.",
        ],
    },
    3: {
        "tema_central": [
            "Transformar la necesidad de ser visto en expresión auténtica del alma.",
            "Canalizar la creatividad como servicio y no solo como entretenimiento.",
        ],
        "patrones": [
            "Subidas y bajadas de ánimo según cuánto reconocimiento sientes que recibes.",
            "Muchos comienzos creativos y pocas cosas terminadas.",
            "Uso del humor o la ligereza para evitar entrar en emociones profundas.",
        ],
        "rectificacion_frases": [
            "Rectificar la búsqueda de validación externa, reconociendo tu valor incluso cuando nadie aplaude.",
            "Rectificar la dispersión creativa, enfocando tus dones en proyectos que construyan algo real.",
        ],
        "claves": [
            "Elegir un par de proyectos clave y comprometerte a terminarlos.",
            "Usar la escritura, el arte o la voz para procesar emociones, no solo para distraer.",
            "Aceptar que no siempre serás entendido en el momento, pero tu mensaje puede sembrar a largo plazo.",
        ],
        "preguntas": [
            "Dónde estoy usando la risa o la distracción para no sentir lo que realmente me pasa.",
            "Qué proyecto creativo necesito honrar terminándolo.",
            "Cómo sería expresar mi verdad incluso si nadie la celebra al inicio.",
        ],
    },
    4: {
        "tema_central": [
            "Construir estructura interna y externa sin caer en la rigidez.",
            "Aprender a confiar en la Luz incluso cuando el plan no se cumple como esperabas.",
        ],
        "patrones": [
            "Necesidad de tener todo bajo control para sentirte seguro.",
            "Miedo a los cambios imprevistos o a lo que no se puede planear.",
            "Tendencia a cargar con más responsabilidades de las que te corresponden.",
        ],
        "rectificacion_frases": [
            "Rectificar la rigidez mental, transformándola en disciplina flexible.",
            "Rectificar la idea de que todo depende solo de tu esfuerzo, integrando la confianza en algo superior.",
        ],
        "claves": [
            "Dejar pequeños espacios de improvisación en tu día para entrenar la flexibilidad.",
            "Aprender a decir que no a responsabilidades que no te pertenecen.",
            "Ver la disciplina como un acto de amor propio y no como castigo.",
        ],
        "preguntas": [
            "Qué parte de mi vida siento que se derrumba si dejo de controlar tanto.",
            "Dónde estoy siendo demasiado duro conmigo mismo.",
            "Qué estructura puedo crear que me dé paz en lugar de presión.",
        ],
    },
    5: {
        "tema_central": [
            "Convertir el impulso de huir en capacidad de transformar.",
            "Aprender a vivir la libertad como elección consciente, no como reacción al miedo.",
        ],
        "patrones": [
            "Etapas de entusiasmo intenso seguidas de aburrimiento o ganas de escapar.",
            "Cambios frecuentes de rumbo cuando algo empieza a sentirse rutinario.",
            "Dificultad para sostener compromisos a largo plazo.",
        ],
        "rectificacion_frases": [
            "Rectificar la impulsividad, transformando el impulso en movimiento con propósito.",
            "Rectificar la idea de que compromiso significa cárcel, descubriendo acuerdos que respetan tu alma.",
        ],
        "claves": [
            "Elegir conscientemente qué batallas y qué caminos valen tu energía a largo plazo.",
            "Introducir cambios sanos dentro de tus compromisos en lugar de romperlo todo.",
            "Explorar nuevas experiencias que expandan tu conciencia, no solo tu adrenalina.",
        ],
        "preguntas": [
            "Dónde suelo irme cuando algo se vuelve incómodo en lugar de transformarlo.",
            "Qué compromisos me dan vida y cuáles siento como cadena.",
            "Cómo puedo honrar mi necesidad de cambio sin destruir lo que ya construí.",
        ],
    },
    6: {
        "tema_central": [
            "Aprender a cuidar sin cargarte de más.",
            "Equilibrar el amor hacia otros con el amor hacia ti mismo.",
        ],
        "patrones": [
            "Ponerte en el rol de quien sostiene a todos.",
            "Sentir culpa cuando haces algo solo para ti.",
            "Perfeccionismo en la familia, en el hogar o en el trabajo de cuidado.",
        ],
        "rectificacion_frases": [
            "Rectificar la autoexigencia, transformándola en responsabilidad amorosa.",
            "Rectificar la creencia de que solo mereces amor si lo das todo y nunca fallas.",
        ],
        "claves": [
            "Practicar el descanso como una forma de servicio a tu propia alma.",
            "Aceptar que el error también educa y humaniza las relaciones.",
            "Reconocer cuándo un cuidado es amor y cuándo se vuelve sacrificio tóxico.",
        ],
        "preguntas": [
            "En qué áreas me estoy descuidando mientras cuido a otros.",
            "Qué expectativas irreales tengo sobre mí en el rol de cuidador o figura de apoyo.",
            "Qué cambiaría si me permitiera ser suficiente tal como soy ahora.",
        ],
    },
    7: {
        "tema_central": [
            "Unir mente y corazón, conocimiento y experiencia.",
            "Aprender a confiar no solo en los datos, sino también en la intuición y en la vida.",
        ],
        "patrones": [
            "Necesidad de entenderlo todo antes de dar un paso.",
            "Periodos de aislamiento para proteger tu mundo interior.",
            "Desconfianza hacia lo emocional o hacia lo que no tiene una lógica clara.",
        ],
        "rectificacion_frases": [
            "Rectificar el exceso de análisis que paraliza la acción.",
            "Rectificar la desconfianza en la vida, abriéndote poco a poco al vínculo y a la vulnerabilidad.",
        ],
        "claves": [
            "Combinar estudio y práctica, no quedarte solo en la teoría.",
            "Elegir una o dos personas con las que puedas mostrar tu mundo interior sin máscaras.",
            "Tomar decisiones pequeñas guiadas por intuiciones suaves, no solo por cálculos mentales.",
        ],
        "preguntas": [
            "Dónde me escondo detrás de la mente para no sentir.",
            "Qué tipo de espiritualidad resuena conmigo más allá de dogmas.",
            "Qué miedo aparece cuando pienso en confiar más en otros.",
        ],
    },
    8: {
        "tema_central": [
            "Usar el poder y los recursos como canales de Luz.",
            "Aprender a liderar desde la ética y la conciencia, no solo desde el resultado.",
        ],
        "patrones": [
            "Atracción a escenarios de poder, dinero, liderazgo o conflicto.",
            "Sensación de cargar con grandes responsabilidades materiales.",
            "Tensiones con figuras de autoridad o con estructuras de control.",
        ],
        "rectificacion_frases": [
            "Rectificar el uso del poder para beneficio solo personal, transformándolo en poder compartido.",
            "Rectificar la dureza frente a la vulnerabilidad propia y ajena.",
        ],
        "claves": [
            "Definir qué significa para ti el éxito con conciencia.",
            "Elegir proyectos donde tu impacto beneficie a más personas, no solo a tu ego.",
            "Practicar la generosidad responsable con tu tiempo, dinero y energía.",
        ],
        "preguntas": [
            "Qué entiendo hoy por poder y qué me gustaría entender en el futuro.",
            "Dónde siento que el dinero o el reconocimiento gobiernan demasiado mis decisiones.",
            "Cómo puedo liderar de una forma que deje más Luz que miedo.",
        ],
    },
    9: {
        "tema_central": [
            "Cerrar ciclos con amor y desapego.",
            "Transformar el dolor del pasado en sabiduría y servicio.",
        ],
        "patrones": [
            "Tendencia a quedarte en historias que ya se terminaron.",
            "Fácil conexión con el sufrimiento ajeno y con causas colectivas.",
            "Dificultad para priorizarte cuando ves a otros pasándolo mal.",
        ],
        "rectificacion_frases": [
            "Rectificar el apego al rol de salvador, permitiendo que cada alma haga su camino.",
            "Rectificar la culpa por soltar personas o situaciones que ya cumplieron su ciclo.",
        ],
        "claves": [
            "Honrar los cierres como actos de amor, no como fracasos.",
            "Elegir pocas causas o personas a las que acompañar a profundidad.",
            "Usar tu sensibilidad para inspirar esperanza, no solo para cargar dolor.",
        ],
        "preguntas": [
            "Qué etapa de mi vida se siente cerrada, pero aún no me animo a soltar del todo.",
            "Dónde sigo cargando responsabilidades emocionales que no son mías.",
            "Qué me gustaría ofrecer al mundo desde mi experiencia de dolor y sanación.",
        ],
    },
    11: {
        "tema_central": [
            "Pasar del control al liderazgo consciente alineado con la Luz.",
            "Equilibrar una sensibilidad muy alta con una estructura interna sólida.",
            "Aprender a confiar en tu intuición como canal, sin miedo a lo que percibes.",
            "Transformar vínculos de dependencia en relaciones de cooperación y coautoría.",
        ],
        "patrones": [
            "Personas que se apoyan mucho en ti o que te buscan como consejero aunque tú no te sientas listo.",
            "Situaciones donde te toca tomar decisiones clave para otros o sostener procesos delicados.",
            "Relaciones en las que terminas dando más de lo que recibes, con dificultad para soltar.",
            "Momentos de contraste entre gran fuerza interior y estados de vulnerabilidad o agotamiento emocional.",
            "Encuentros repetidos con sistemas o figuras de autoridad rígidas, que te invitan a posicionarte sin destruirte ni someterte.",
        ],
        "rectificacion_frases": [
            "Rectificar el uso del poder personal, pasando del control y la dureza a la autoridad sana y compasiva.",
            "Rectificar la tendencia a perderte en el otro, creando vínculos con límites claros y reciprocidad.",
            "Rectificar el miedo a tu propia intuición, transformándolo en confianza en la guía interna y en la Luz.",
            "Rectificar la costumbre de cargar culpas ajenas, asumiendo solo la responsabilidad que realmente te corresponde.",
        ],
        "claves": [
            "Aprender a decir que no sin sentirte egoísta, entendiendo que el límite también es Luz.",
            "Cuidar tu sistema nervioso con descanso, silencio, escritura y espacios de conexión espiritual.",
            "Elegir relaciones y proyectos donde la cooperación sea real y no solo un discurso.",
            "Trabajar el perdón hacia ti mismo por decisiones pasadas, viendo cada etapa como parte del aprendizaje del alma.",
            "Convertir tu visión y sensibilidad en servicio concreto: proyectos, estudios, acompañamientos, contenido.",
            "Practicar actos pequeños de liderazgo consciente: hablar con honestidad, marcar dirección, sostener acuerdos claros.",
        ],
        "preguntas": [
            "En qué situaciones recientes sentí que estaba controlando por miedo y no liderando desde la confianza.",
            "Dónde sigo intentando salvar a personas o sistemas que no quieren cambiar.",
            "Qué parte de mi sensibilidad aún juzgo como debilidad.",
            "Qué tipo de líder del alma quiero ser en mi casa, trabajo y relaciones.",
            "Qué ciclo necesito cerrar para liberar energía y caminar más ligero.",
        ],
    },
    22: {
        "tema_central": [
            "Materializar visión espiritual en proyectos concretos.",
            "Usar tu capacidad organizativa para construir algo que trascienda lo personal.",
        ],
        "patrones": [
            "Atracción a metas grandes que a veces parecen imposibles.",
            "Sensación de presión interna por no estar haciendo lo suficiente.",
            "Dificultad para equilibrar la vida personal con proyectos de gran escala.",
        ],
        "rectificacion_frases": [
            "Rectificar la autoexigencia extrema, integrando paciencia y procesos.",
            "Rectificar la tendencia a descuidar tu mundo emocional por el logro externo.",
        ],
        "claves": [
            "Dividir tus grandes visiones en pasos pequeños y sostenibles.",
            "Recordar que el proyecto más importante también eres tú.",
            "Aliarte con personas que compartan tu visión en lugar de cargar tú solo con todo.",
        ],
        "preguntas": [
            "Qué visión de largo plazo me inspira de verdad.",
            "Qué parte de mí siente que nunca es suficiente.",
            "Cómo puedo construir algo grande cuidando también de mi cuerpo y mis emociones.",
        ],
    },
    33: {
        "tema_central": [
            "Encarnar un amor profundo que no olvida los propios límites.",
            "Sostener procesos de sanación sin sacrificar tu energía vital.",
        ],
        "patrones": [
            "Personas que descargan en ti sus dolores y confían en tu contención.",
            "Cansancio emocional por asumir demasiados procesos ajenos.",
            "Confusión entre ayudar y hacerse cargo de lo que no te corresponde.",
        ],
        "rectificacion_frases": [
            "Rectificar la identificación con el rol de salvador.",
            "Rectificar la culpa por poner límites cuando ya estás saturado.",
        ],
        "claves": [
            "Definir con claridad qué sí puedes ofrecer y qué no.",
            "Aprender a retirarte a tiempo antes de agotarte.",
            "Cuidar tu cuerpo, tu descanso y tu alegría como parte esencial de tu misión.",
        ],
        "preguntas": [
            "Dónde estoy intentando sanar algo que no me corresponde.",
            "Qué señales me da mi cuerpo cuando ya es demasiado.",
            "Qué tipo de amor quiero encarnar que incluya también amor por mí.",
        ],
    },
}


MESES_NOMBRE = {
    1: "enero",
    2: "febrero",
    3: "marzo",
    4: "abril",
    5: "mayo",
    6: "junio",
    7: "julio",
    8: "agosto",
    9: "septiembre",
    10: "octubre",
    11: "noviembre",
    12: "diciembre",
}


def calcular_arquetipo(nombre, fecha_nacimiento):
    """
    Calcula información numerológica kabalista básica:
    número de vida, número del nombre y arquetipos asociados.
    """
    info_fecha = analizar_fecha_numerologia(fecha_nacimiento)
    num_vida = info_fecha["numero_vida"]
    num_nombre = numero_desde_nombre(nombre)

    arquetipo_vida = arquetipo_desde_numero(num_vida)
    arquetipo_nombre = arquetipo_desde_numero(num_nombre)

    resultado = {
        "nombre_input": nombre,
        "fecha_input": fecha_nacimiento,
        "info_fecha": info_fecha,
        "numero_vida": num_vida,
        "arquetipo_vida": arquetipo_vida,
        "numero_nombre": num_nombre,
        "arquetipo_nombre": arquetipo_nombre,
    }

    return resultado


def generar_informe_kabalista(nombre, fecha_nacimiento):
    """
    Genera un informe extenso de tikkun y arquetipo
    similar al ejemplo de lectura larga.
    """
    datos = calcular_arquetipo(nombre, fecha_nacimiento)
    info_fecha = datos["info_fecha"]

    dia = info_fecha["dia"]
    mes = info_fecha["mes"]
    ano = info_fecha["ano"]
    suma_ano = info_fecha["suma_ano"]
    base_total = info_fecha["base_total"]
    numero_vida = info_fecha["numero_vida"]
    representacion_camino = info_fecha["representacion_camino"]

    numero_nombre = datos["numero_nombre"]
    arq_vida = datos["arquetipo_vida"]
    arq_nombre = datos["arquetipo_nombre"]

    energia_dia_num, energia_dia_desc = obtener_energia_basica(dia)
    energia_mes_num, energia_mes_desc = obtener_energia_basica(mes)
    energia_ano_num, energia_ano_desc = obtener_energia_basica(suma_ano)

    plantilla = PLANTILLAS_TIKKUN.get(numero_vida)
    if plantilla is None:
        plantilla = PLANTILLAS_TIKKUN.get(info_fecha["base_simple"])

    if plantilla is None:
        plantilla = {
            "tema_central": [arq_vida["perfeccionar"]],
            "patrones": [],
            "rectificacion_frases": [arq_vida["perfeccionar"]],
            "claves": [],
            "preguntas": [],
        }

    nombre_mes = MESES_NOMBRE.get(mes, f"mes {mes}")

    lineas = []

    lineas.append(f"Voy directo al grano usando tu fecha: {dia} de {nombre_mes} de {ano}.")
    lineas.append("")
    lineas.append(
        "Desde la mirada numerológica kabalista, como mapa simbólico y no como sentencia rígida, "
        f"tu fecha habla de un camino {representacion_camino}."
    )
    lineas.append(
        "Ese camino se apoya especialmente en la energía de tu día y tu mes de nacimiento, "
        "que colorean la forma en que vives tu tikkun."
    )
    lineas.append("")

    lineas.append("Suma básica de la fecha:")
    lineas.append(f"• Día del nacimiento: {dia}")
    lineas.append(f"• Mes del nacimiento: {mes}")
    lineas.append(f"• Año de nacimiento: {ano} → suma de sus dígitos {suma_ano}")
    lineas.append(
        f"Total: {dia} (día) + {mes} (mes) + {suma_ano} (suma del año) = {base_total} → camino {representacion_camino}"
    )
    lineas.append("")

    lineas.append("Energías que sostienen tu camino de alma:")
    lineas.append(
        f"• Día {dia}: resuena en una energía {energia_dia_num} asociada a {energia_dia_desc}."
    )
    lineas.append(
        f"• Mes {mes}: resuena en una energía {energia_mes_num} asociada a {energia_mes_desc}."
    )
    lineas.append(
        f"• Año {ano} con suma {suma_ano}: energía {energia_ano_num} asociada a {energia_ano_desc}."
    )
    lineas.append("")

    lineas.append("Arquetipo central según tu número de vida:")
    lineas.append(f"• Arquetipo kabalista de vida: {arq_vida['nombre']}")
    lineas.append(f"• Descripción general: {arq_vida['descripcion']}")
    lineas.append("")

    lineas.append("Tema central de tu tikkun, lo que vienes a rectificar en esta encarnación:")
    for frase in plantilla["tema_central"]:
        lineas.append(f"• {frase}")
    lineas.append("")

    if plantilla["patrones"]:
        lineas.append("Patrones que tienden a repetirse para este arquetipo, donde suele activarse el trabajo del alma:")
        for frase in plantilla["patrones"]:
            lineas.append(f"• {frase}")
        lineas.append("")

    lineas.append("Lo que vienes a rectificar, en frases directas:")
    for frase in plantilla["rectificacion_frases"]:
        lineas.append(f"• {frase}")
    lineas.append(f"• En resumen, tu tikkun de fondo es: {arq_vida['perfeccionar']}")
    lineas.append("")

    if plantilla["claves"]:
        lineas.append("Claves de sanación y evolución para tu arquetipo:")
        for frase in plantilla["claves"]:
            lineas.append(f"• {frase}")
        lineas.append("")

    if plantilla["preguntas"]:
        lineas.append("Preguntas para trabajar este proceso en escritura, reflexión o meditación:")
        for frase in plantilla["preguntas"]:
            lineas.append(f"• {frase}")
        lineas.append("")

    lineas.append("Aportación de tu nombre, es decir, cómo se expresa tu alma en el mundo:")
    lineas.append(
        f"• Tu nombre, al vibrar en el número {numero_nombre}, se asocia al arquetipo {arq_nombre['nombre']}."
    )
    lineas.append(f"• Descripción: {arq_nombre['descripcion']}")
    lineas.append(
        f"• Tikkun asociado a tu forma de expresarte y relacionarte: {arq_nombre['perfeccionar']}"
    )
    lineas.append("")
    lineas.append(
        "En otras palabras, la fecha muestra el plan de fondo del alma y el nombre muestra "
        "el estilo con el que encarnas ese plan en la realidad diaria."
    )

    return "\n".join(lineas)


def mostrar_resultado(nombre, fecha_nacimiento):
    """
    Calcula y muestra por pantalla el informe kabalista completo.
    """
    informe = generar_informe_kabalista(nombre, fecha_nacimiento)
    print("======================================================")
    print("          Informe de Arquetipo y Tikkun (Kábala)      ")
    print("======================================================")
    print(informe)
    print("======================================================")


def modo_interactivo():
    """
    Ejecuta el programa en modo interactivo por consola.
    """
    print("Cálculo de arquetipo numerológico kabalista")
    print("-------------------------------------------")
    nombre = input("Ingresa tu nombre completo: ")
    fecha_nacimiento = input("Ingresa tu fecha de nacimiento (DD/MM/AAAA o AAAA-MM-DD): ")

    try:
        mostrar_resultado(nombre, fecha_nacimiento)
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    modo_interactivo()