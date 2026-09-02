# -*- coding: utf-8 -*-
import json
import os
import re
import urllib.parse

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


def test_el_ruido_no_aparece_como_faceta(catalogo):
    """El criterio del spec es que ninguna FACETA diga 'Destacado' o 'Sin categorizar'.

    Ojo: 'Destacado' sí puede (y debe) aparecer como distintivo en la tarjeta -- el
    diseño lo convirtió de categoría basura en atributo del equipo. Por eso el
    aserto se limita al panel de facetas y no a la página entera.
    """
    html = pagina_catalogo(catalogo)
    panel = re.search(r'<aside class="facetas">.*?</aside>', html, re.S)
    assert panel, "no se encontró el panel de facetas"
    for ruido in ("Sin categorizar", "Destacado", "Covid",
                  "Radiología Computarizada", "Radiología Directa"):
        assert ruido not in panel.group(0), ruido


def test_los_destacados_llevan_distintivo_en_la_tarjeta(catalogo):
    cuantos = sum(1 for e in catalogo["equipos"] if e["destacado"])
    assert cuantos == 7
    assert pagina_catalogo(catalogo).count('class="eq__dest"') == cuantos


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


def test_las_tarjetas_ocultas_se_pueden_ocultar_de_verdad(catalogo):
    """`display:flex` de autor le gana a `[hidden]{display:none}` del navegador,
    así que sin una regla propia el buscador no ocultaría nada."""
    html = pagina_catalogo(catalogo)
    assert ".eq[hidden]" in html and ".rejilla[hidden]" in html


def test_la_tarjeta_ancla_el_badge(catalogo):
    """`.eq__dest` es absolute: sin un ancestro posicionado los 7 badges se
    apilarían en el origen de la página."""
    html = pagina_catalogo(catalogo)
    bloque = re.search(r"\.eq\{[^}]*\}", html)
    assert bloque and "position:relative" in bloque.group(0)


from _build_catalogo import pagina_ficha


def _equipo(catalogo, slug):
    return next(e for e in catalogo["equipos"] if e["slug"] == slug)


def test_la_ficha_pone_el_nombre_del_equipo_en_el_whatsapp(catalogo):
    e = catalogo["equipos"][0]
    html = pagina_ficha(e, catalogo)
    assert "wa.me/584241941573?text=" in html
    assert urllib.parse.quote(e["nombre"])[:20] in html


def test_la_ficha_no_tiene_nada_de_tienda(catalogo):
    html = pagina_ficha(catalogo["equipos"][0], catalogo).lower()
    for prohibido in ("añadir al carrito", "add-to-cart", "checkout", "woocommerce"):
        assert prohibido not in html, prohibido


def test_la_ficha_enlaza_de_vuelta_al_catalogo_filtrado(catalogo):
    e = next(x for x in catalogo["equipos"] if x["especialidades"])
    html = pagina_ficha(e, catalogo)
    assert "/equipos?esp=" in html


def test_la_ficha_tiene_titulo_y_descripcion_propios(catalogo):
    e = catalogo["equipos"][0]
    html = pagina_ficha(e, catalogo)
    assert "<title>" in html and e["nombre"][:10] in html
    assert '<meta name="description"' in html


def test_se_generaron_las_215_fichas():
    carpeta = os.path.join(RAIZ, "public", "equipos")
    fichas = [f for f in os.listdir(carpeta) if f.endswith(".html")]
    assert len(fichas) == 215
