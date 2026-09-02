# -*- coding: utf-8 -*-
"""Curaduría del catálogo: convierte las categorías de WooCommerce en tres ejes.

El sitio viejo aplana 49 categorías raíz en una sola lista, mezclando especialidades
médicas con marcas de fabricantes. Acá se separan a mano, una vez, y queda registrado.
Es deliberadamente una tabla explícita y no una heurística: cuando el equipo cree una
categoría nueva, tiene que pasar por acá.
"""
import re
import unicodedata
import urllib.parse

# Raíz cruda en WooCommerce -> nombre que mostramos.
ESPECIALIDADES = {
    "Diagnostico-por-Imagen": "Diagnóstico por Imagen",
    "Ginecologia": "Ginecología",
    "Dermatologia/Medicina-Estetica": "Dermatología / Medicina Estética",
    "Otorrinolaringologia": "Otorrinolaringología",
    "Cardiologia": "Cardiología",
    "Cirugía": "Cirugía",
    "Anestesia": "Anestesia",
    "Gastroenterologia": "Gastroenterología",
    "Urologia": "Urología",
    "Emergencia": "Emergencia",
    "Quirofano": "Quirófano",
    "Neurologia": "Neurología",
    "Instrumental Medico": "Instrumental Médico",
    "Esterilizacion": "Esterilización",
    "Cirugía Plástica": "Cirugía Plástica",
    "Mobiliario-Medico": "Mobiliario Médico",
    "Neonatología": "Neonatología",
    "Hospitalización": "Hospitalización",
}

MARCAS = {
    "Interacoustics": "Interacoustics",
    "Siemens": "Siemens",
    "Deka Laser": "Deka Laser",
    "Sonoscape": "SonoScape",
    "Dräger": "Dräger",
    "Sony": "Sony",
    "Medtronic": "Medtronic",
    "Ebneuro": "EB Neuro",
    "Hyun Laser": "Hyun Laser",
    "Mega Medical": "Mega Medical",
    "Zoncare": "Zoncare",
    "Inmode": "InMode",
    "Esaote": "Esaote",
    "Canfield": "Canfield",
    "Candela Medical": "Candela Medical",
    "Hydrafacial": "Hydrafacial",
    "Matachana": "Matachana",
    "Barco": "Barco",
    "Olympus": "Olympus",
    "UMF Medical": "UMF Medical",
    "BMI": "BMI",
    "Cocoon Medical": "Cocoon Medical",
    "Echolight": "Echolight",
    "Mobile ODT": "MobileODT",
    "Yonker": "Yonker",
}

# Raíces que no son ni especialidad ni marca. Ver §5.4 del spec.
#   Destacado          -> pasa a ser el booleano `destacado` del equipo
#   Sin categorizar    -> no tiene ningún producto publicado
#   Covid              -> su único producto se reasigna a Emergencia
#   Radiología Comp./Directa, Estudios Óseos -> son tipos, no especialidades
RAICES_OCULTAS = {
    "Destacado",
    "Sin categorizar",
    "Covid",
    "Radiología Computarizada",
    "Radiología Directa",
    "Estudios Óseos",
    "Densitometro Oseo",
}

# El sitio viejo repite el mismo tipo de equipo una vez por especialidad.
# Acá se colapsan para poder preguntar "todos los ecógrafos".
TIPOS_UNIFICADOS = {
    "Ecógrafos Emergencia": "Ecógrafos",
    "Ecógrafos Urología": "Ecógrafos",
    "Ecógrafos Para Anestesia": "Ecógrafos",
    "Ecógrafos Cardiología": "Ecógrafos",
    "Ecógrafos Diagnóstico por Imagen": "Ecógrafos",
    "Monitores Anestesia": "Monitores",
    "Monitores Cirugía": "Monitores",
    "Monitores Hospitalización": "Monitores",
    "Monitores Diagnóstico por Imagen": "Monitores",
    "Láser Quirúrgico Dermatología/Medicina-Estetica": "Láser Quirúrgico",
    "Láser Quirúrgico Cirugía": "Láser Quirúrgico",
    "Arcos en C Cirugía": "Arcos en C",
    "Descartables Ginecología": "Descartables",
    "Insumos Diagnóstico por Imagen": "Insumos",
    "Mobile ODT Diagnóstico por Imagen": "Colposcopia",
    # Singular y plural del mismo tipo, segun que especialidad lo nombro en Woo.
    "Ultrasonido": "Ultrasonidos",
}


def normalizar(texto):
    """Minúsculas y sin acentos. Es lo que hace comparable 'ecografo' con 'Ecógrafos'.

    NFD y no NFKD a propósito: NFKD descompone los símbolos de compatibilidad y
    convertiría el '™' de 'MyLab™X75' en las letras 'TM'.
    """
    descompuesto = unicodedata.normalize("NFD", (texto or "").lower())
    return "".join(c for c in descompuesto if not unicodedata.combining(c))


def slugificar(texto):
    base = normalizar(texto)
    base = re.sub(r"[^a-z0-9]+", "-", base)
    return base.strip("-")


def slug_de_producto(slug):
    """Normaliza el slug que viene de WordPress a `^[a-z0-9-]+$`.

    Diez productos traen el slug ya percent-encodeado ('...nano%e2%80%91coated',
    'smartxide%c2%b2-trio'). Tomarlo tal cual dejaba el '%XX' literal en el nombre
    del archivo Y en el href/src, pero el navegador percent-decodifica la ruta
    antes de tocar el disco: pedía '...nano‑coated' y recibía un 404. Se
    decodifica primero y se vuelve a slugificar, para que la URL y el archivo
    coincidan siempre.
    """
    return slugificar(urllib.parse.unquote(slug or ""))


def clasificar_raiz(nombre):
    """Devuelve (eje, nombre_limpio). El eje 'otros' es la red de seguridad: una
    categoría nueva sin mapear se ve en la interfaz en vez de romper el build."""
    if nombre in ESPECIALIDADES:
        return ("especialidad", ESPECIALIDADES[nombre])
    if nombre in MARCAS:
        return ("marca", MARCAS[nombre])
    if nombre in RAICES_OCULTAS:
        return ("oculta", nombre)
    return ("otros", nombre)


def tipo_unificado(nombre):
    return TIPOS_UNIFICADOS.get(nombre, nombre)


import html as _html

# Cinco equipos no tienen ninguna especialidad en WooCommerce. En vez de dejarlos
# invisibles en el catálogo, se les asigna a mano según lo que son:
#   hockey-stick    transductor de ultrasonido
#   thermoglide-2   trata lesiones precancerosas de cuello uterino
#   valleylab-...   electrodos de electrocirugía
#   oxylog-3000-plus ventilador de transporte
#   oximetro-...    venía colgado de la categoría Covid
REASIGNACIONES = {
    "hockey-stick": {"especialidades": ["Diagnóstico por Imagen"], "tipos": ["Ultrasonidos"]},
    "thermoglide-2": {"especialidades": ["Ginecología"], "tipos": []},
    "valleylab-electrodos-con-cable-de-retorno-del-paciente": {
        "especialidades": ["Cirugía"], "tipos": ["Sellado de Vasos"]},
    "oxylog-3000-plus": {"especialidades": ["Emergencia"], "tipos": ["Respiradores Mecánicos"]},
    "oximetro-de-pulso-yonker": {"especialidades": ["Emergencia"], "tipos": []},
}

_ETIQUETAS = re.compile(r"<[^>]+>")
_ESPACIOS = re.compile(r"\s+")
# Cada etiqueta se reemplaza por un espacio para no pegar palabras de bloques
# distintos, pero eso deja "alta gama ." cuando el punto venía después de un </b>.
_ESPACIO_ANTES_DE_PUNTUACION = re.compile(r"\s+([.,;:!?%)\]»])")


def limpiar_html(fragmento):
    sin_etiquetas = _ETIQUETAS.sub(" ", fragmento or "")
    texto = _html.unescape(sin_etiquetas).replace("\xa0", " ")
    texto = _ESPACIOS.sub(" ", texto)
    return _ESPACIO_ANTES_DE_PUNTUACION.sub(r"\1", texto).strip()


def raiz_de(cat_id, cats_por_id):
    """Sube por el árbol de categorías hasta la que tiene parent 0."""
    cat = cats_por_id.get(cat_id)
    visitadas = set()
    while cat and cat["parent"] != 0:
        if cat["id"] in visitadas:  # ciclo defensivo
            return None
        visitadas.add(cat["id"])
        cat = cats_por_id.get(cat["parent"])
    return cat


def _sin_repetir(valores):
    vistos = []
    for v in valores:
        if v not in vistos:
            vistos.append(v)
    return vistos


def equipo_desde_producto(producto, cats_por_id):
    especialidades, tipos, marca, destacado = [], [], None, False

    for ref in producto.get("categories", []):
        cat = cats_por_id.get(ref["id"])
        if not cat:
            continue
        raiz = raiz_de(ref["id"], cats_por_id)
        if raiz is None:
            continue
        eje, limpio = clasificar_raiz(raiz["name"])

        if raiz["name"] == "Destacado":
            destacado = True

        es_la_raiz = cat["id"] == raiz["id"]
        if not es_la_raiz:
            # Es una subcategoría: siempre es un tipo de equipo.
            tipos.append(tipo_unificado(cat["name"]))
        if eje == "especialidad":
            especialidades.append(limpio)
        elif eje == "marca":
            marca = marca or limpio
        # 'oculta' y 'otros' no aportan ni especialidad ni marca

    slug = slug_de_producto(producto["slug"])
    # Las reasignaciones a mano se escribieron contra el slug crudo de WooCommerce;
    # ninguno de los cinco trae percent-encoding, así que ambas claves coinciden.
    forzado = REASIGNACIONES.get(producto["slug"]) or REASIGNACIONES.get(slug)
    if forzado:
        especialidades = list(forzado["especialidades"])
        tipos = _sin_repetir(tipos + forzado["tipos"])

    especialidades = _sin_repetir(especialidades)
    tipos = _sin_repetir(tipos)

    resumen = limpiar_html(producto.get("short_description"))
    descripcion = limpiar_html(producto.get("description"))
    imagenes = producto.get("images") or []
    imagen = (imagenes[0].get("thumbnail") or imagenes[0].get("src")) if imagenes else None

    # WooCommerce devuelve el nombre con entidades HTML crudas
    # ('Dräger &#8211; Atlan&reg;'). Sin desescaparlo, esc() lo vuelve a
    # escapar y la página pinta el '&#8211;' literal en el <title>, el <h1>, la
    # tarjeta y el mensaje precargado de WhatsApp.
    nombre = _html.unescape(producto["name"] or "")

    partes = [nombre, marca or "", " ".join(especialidades),
              " ".join(tipos), resumen[:200]]
    return {
        "slug": slug,
        "nombre": nombre,
        "url_original": producto.get("permalink", ""),
        "resumen": resumen,
        "descripcion": descripcion,
        "especialidades": especialidades,
        "marca": marca,
        "tipos": tipos,
        "destacado": destacado,
        "imagen": imagen,
        "busqueda": normalizar(" ".join(p for p in partes if p)),
    }


# Atajos en el idioma del médico, no en el del catálogo. El que busca no siempre
# sabe que lo que necesita se llama "arco en C"; sí sabe que va a operar.
# Los valores tienen que existir en _catalogo.json: hay un test que lo verifica.
CHIPS = [
    {"texto": "Voy a montar un consultorio de ginecología",
     "filtros": {"esp": ["Ginecología"]}},
    {"texto": "Necesito reemplazar un ecógrafo",
     "filtros": {"tipo": ["Ecógrafos"]}},
    {"texto": "Equipamiento para quirófano",
     "filtros": {"esp": ["Quirófano", "Cirugía"]}},
    {"texto": "Diagnóstico por imagen",
     "filtros": {"esp": ["Diagnóstico por Imagen"]}},
    {"texto": "Medicina estética",
     "filtros": {"esp": ["Dermatología / Medicina Estética"]}},
    {"texto": "Consumibles y descartables",
     "filtros": {"tipo": ["Descartables", "Insumos"]}},
]
