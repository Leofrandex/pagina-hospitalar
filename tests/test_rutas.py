# -*- coding: utf-8 -*-
import os

from _rutas import ruta_larga

PREFIJO_LARGO = "\\\\?\\"


def _ruta_larga_de_prueba():
    return "C:\\Users\\x\\" + ("a" * 250) + ".png"


def test_ruta_larga_antepone_el_prefijo_en_windows():
    ruta = _ruta_larga_de_prueba()
    resultado = ruta_larga(ruta)
    if os.name == "nt":
        assert resultado.startswith(PREFIJO_LARGO)
        assert resultado.endswith(os.path.abspath(ruta))
    else:
        # El prefijo \?\ es específico de Windows: en Linux/Mac no aplica y
        # ruta_larga debe devolver la ruta sin tocar.
        assert resultado == ruta


def test_ruta_larga_no_duplica_el_prefijo_si_ya_lo_trae():
    ruta = _ruta_larga_de_prueba()
    una_vez = ruta_larga(ruta)
    dos_veces = ruta_larga(una_vez)
    assert dos_veces == una_vez
