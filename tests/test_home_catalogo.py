# -*- coding: utf-8 -*-
import json
import os
import re

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(RAIZ, "public", "site.html")
CATALOGO = os.path.join(RAIZ, "public", "mockups", "_catalogo.json")


@pytest.fixture(scope="module")
def site():
    with open(SITE, encoding="utf-8") as f:
        return f.read()


def test_la_home_ya_no_lista_equipos_inventados(site):
    for inventado in ("Doppler fetal", "Desfibriladores", "Holters",
                      "Motores ortopédicos", "Rayos X digital"):
        assert inventado not in site, inventado


def test_las_especialidades_enlazan_al_catalogo_filtrado(site):
    assert "/equipos?esp=" in site


def test_la_home_muestra_los_conteos_reales(site):
    with open(CATALOGO, encoding="utf-8") as f:
        catalogo = json.load(f)
    top = catalogo["especialidades"][0]
    assert "%d equipos" % top["total"] in site


def test_el_nav_lleva_al_catalogo(site):
    assert 'href="/equipos"' in site


def test_los_logos_de_marcas_enlazan_al_catalogo_filtrado(site):
    """Spec §7: la sección #marcas lleva al catálogo. El valor de ?marca= tiene
    que ser el nombre exacto de la faceta, porque el controlador de /equipos
    compara contra el value de las casillas."""
    import urllib.parse
    with open(CATALOGO, encoding="utf-8") as f:
        facetas = {m["nombre"] for m in json.load(f)["marcas"]}
    enlaces = re.findall(r'href="/equipos\?marca=([^"]+)"', site)
    assert len(enlaces) >= 14, "se esperaban al menos 14 logos enlazados, hay %d" % len(enlaces)
    for crudo in set(enlaces):
        assert urllib.parse.unquote(crudo) in facetas, crudo


def test_el_track_duplicado_del_marquee_no_es_alcanzable_por_teclado(site):
    """El segundo track existe sólo para la animación y va aria-hidden: un enlace
    enfocable adentro de un aria-hidden es una trampa para el teclado."""
    oculto = site.split('<div class="marquee__track" aria-hidden="true">')[1]
    oculto = oculto.split("</div>")[0]
    for enlace in re.findall(r"<a [^>]*>", oculto):
        assert 'tabindex="-1"' in enlace, enlace
