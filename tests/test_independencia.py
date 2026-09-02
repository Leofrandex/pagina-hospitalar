# -*- coding: utf-8 -*-
"""El catálogo del sitio nuevo no puede depender de que hospitalarve.com siga en pie."""
import os
import re

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _leer(*partes):
    with open(os.path.join(RAIZ, *partes), encoding="utf-8") as f:
        return f.read()


def test_el_generador_no_toca_la_red():
    codigo = _leer("public", "mockups", "_build_catalogo.py")
    for prohibido in ("urllib.request", "requests", "http.client"):
        assert prohibido not in codigo


def test_ninguna_imagen_del_catalogo_apunta_al_wordpress_viejo():
    html = _leer("public", "equipos.html")
    assert "hospitalarve.com/wp-content" not in html


def test_las_fichas_tampoco_apuntan_al_wordpress_viejo():
    carpeta = os.path.join(RAIZ, "public", "equipos")
    for f in os.listdir(carpeta):
        if f.endswith(".html"):
            assert "hospitalarve.com/wp-content" not in _leer("public", "equipos", f), f


def test_todas_las_imagenes_referenciadas_existen():
    html = _leer("public", "equipos.html")
    for ruta in set(re.findall(r'src="(/equipos/img/[^"]+)"', html)):
        assert os.path.exists(os.path.join(RAIZ, "public", ruta.lstrip("/"))), ruta
