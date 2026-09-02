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
    fichas = [f for f in os.listdir(carpeta) if f.endswith(".html")]
    # Sin esto, una carpeta vacía haría pasar el test sin verificar nada: es
    # justamente el modo en que un test que demuestra una ausencia miente.
    assert len(fichas) == 215, "se esperaban 215 fichas, hay %d" % len(fichas)
    for f in fichas:
        assert "hospitalarve.com/wp-content" not in _leer("public", "equipos", f), f


def test_todas_las_imagenes_referenciadas_existen():
    html = _leer("public", "equipos.html")
    rutas = set(re.findall(r'src="(/equipos/img/[^"]+)"', html))
    # Si el marcado cambiara y el regex dejara de matchear, el bucle no correría
    # y el test pasaría en verde sin haber comprobado una sola imagen.
    assert len(rutas) == 215, "se esperaban 215 imágenes referenciadas, hay %d" % len(rutas)
    for ruta in rutas:
        assert os.path.exists(os.path.join(RAIZ, "public", ruta.lstrip("/"))), ruta
