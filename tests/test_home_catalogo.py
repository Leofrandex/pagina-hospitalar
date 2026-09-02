# -*- coding: utf-8 -*-
import json
import os

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
