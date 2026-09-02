# -*- coding: utf-8 -*-
"""Utilidades de rutas de archivo especificas de Windows.

Responsabilidad unica: nada de red, nada de catalogo -- solo el manejo del
limite de longitud de ruta de Windows, que afecta tanto a `_fetch_catalogo.py`
(al bajar imagenes) como a `_build_catalogo.py` (al escribir y borrar las
fichas HTML).
"""
import os


def ruta_larga(ruta):
    r"""Antepone el prefijo \\?\ en Windows para rutas que superan MAX_PATH.

    Windows exige 260 caracteres o menos para una ruta a menos que se use este
    prefijo de "ruta extendida" (\\?\ + ruta absoluta), que le pide a la
    API de Win32 saltarse ese limite. Sin el, tanto bajar una imagen como
    escribir o borrar una ficha HTML puede fallar con `FileNotFoundError` en
    slugs largos (varios superan los 260 caracteres una vez armada la ruta
    completa). No afecta a Linux/Mac, donde no existe ese limite ni ese
    prefijo: ahi la funcion devuelve la ruta sin tocar.
    """
    if os.name == "nt":
        absoluta = os.path.abspath(ruta)
        if not absoluta.startswith("\\\\?\\"):
            return "\\\\?\\" + absoluta
    return ruta
