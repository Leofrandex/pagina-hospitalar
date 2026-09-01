# -*- coding: utf-8 -*-
import json
import os

import pytest

from _build_catalogo import pagina_catalogo, tarjeta, wa_link

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOGO = os.path.join(RAIZ, "public", "mockups", "_catalogo.json")


@pytest.fixture(scope="module")
def catalogo():
    with open(CATALOGO, encoding="utf-8") as f:
        return json.load(f)


def test_el_catalogo_congelado_tiene_los_215_equipos(catalogo):
    assert len(catalogo["equipos"]) == 215
    assert len(catalogo["especialidades"]) == 18
    assert len(catalogo["marcas"]) == 25


def test_ningun_equipo_quedo_sin_especialidad(catalogo):
    huerfanos = [e["slug"] for e in catalogo["equipos"] if not e["especialidades"]]
    assert huerfanos == []


def test_wa_link_precarga_el_mensaje():
    url = wa_link("Hola, me interesa el ACUSON Sequoia")
    assert url.startswith("https://wa.me/584241941573?text=")
    assert "ACUSON%20Sequoia" in url


def test_la_tarjeta_escapa_el_html():
    html = tarjeta({"slug": "x", "nombre": 'Equipo "raro" & <b>', "marca": None,
                    "especialidades": [], "tipos": [], "resumen": "", "imagen": None,
                    "destacado": False})
    assert "<b>" not in html
    assert "&lt;b&gt;" in html


def test_la_pagina_trae_los_215_equipos_en_el_html(catalogo):
    html = pagina_catalogo(catalogo)
    assert html.count('class="eq ') == 215


def test_la_pagina_no_muestra_ruido_de_categorias(catalogo):
    html = pagina_catalogo(catalogo)
    for ruido in ("Sin categorizar", "Destacado</", "Radiología Computarizada"):
        assert ruido not in html


def test_la_pagina_no_tiene_nada_de_tienda(catalogo):
    """Se buscan marcadores inequívocos de e-commerce, no palabras sueltas: las
    descripciones vienen del sitio viejo y alguna podría decir 'comprar' en prosa."""
    html = pagina_catalogo(catalogo).lower()
    for prohibido in ("añadir al carrito", "add-to-cart", "add_to_cart",
                      "checkout", "woocommerce", "finalizar-compra", "mi-cuenta"):
        assert prohibido not in html, prohibido


def test_el_indice_embebido_no_lleva_precios(catalogo):
    for e in catalogo["equipos"]:
        for prohibido in ("precio", "prices", "price", "sku", "stock"):
            assert prohibido not in e, prohibido


def test_la_pagina_embebe_el_indice_y_el_buscador(catalogo):
    html = pagina_catalogo(catalogo)
    assert 'id="catalogo-datos"' in html
    assert "export function buscar" not in html   # inlineado sin `export`
    assert "function buscar" in html


def test_la_pagina_declara_las_tres_facetas(catalogo):
    html = pagina_catalogo(catalogo)
    for etiqueta in ("Especialidad", "Marca", "Tipo de equipo"):
        assert etiqueta in html
