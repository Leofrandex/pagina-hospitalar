# -*- coding: utf-8 -*-
"""Curaduría del catálogo: convierte las categorías de WooCommerce en tres ejes.

El sitio viejo aplana 49 categorías raíz en una sola lista, mezclando especialidades
médicas con marcas de fabricantes. Acá se separan a mano, una vez, y queda registrado.
Es deliberadamente una tabla explícita y no una heurística: cuando el equipo cree una
categoría nueva, tiene que pasar por acá.
"""
import re
import unicodedata

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
