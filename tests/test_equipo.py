# -*- coding: utf-8 -*-
from _catalogo_map import equipo_desde_producto, limpiar_html, raiz_de

# Índice de categorías recortado, con la misma forma que devuelve la Store API.
CATS = {
    100: {"id": 100, "name": "Diagnostico-por-Imagen", "parent": 0},
    101: {"id": 101, "name": "Ultrasonidos", "parent": 100},
    102: {"id": 102, "name": "Ecógrafos Diagnóstico por Imagen", "parent": 100},
    200: {"id": 200, "name": "Siemens", "parent": 0},
    300: {"id": 300, "name": "Destacado", "parent": 0},
    400: {"id": 400, "name": "Covid", "parent": 0},
    401: {"id": 401, "name": "Oxímetro de Pulso", "parent": 400},
    500: {"id": 500, "name": "Sonoscape", "parent": 0},
}


def producto(**kw):
    base = {
        "slug": "acuson-sequoia",
        "name": "ACUSON Sequoia",
        "permalink": "https://hospitalarve.com/producto/acuson-sequoia/",
        "short_description": "<p>Ecógrafo de <b>alta gama</b>.</p>",
        "description": "<p>Descripción larga.</p>",
        "categories": [{"id": 100}, {"id": 101}, {"id": 200}],
        "images": [{"src": "https://x/img.jpg", "thumbnail": "https://x/img-500x500.jpg"}],
    }
    base.update(kw)
    return base


def test_limpiar_html_quita_etiquetas_y_entidades():
    assert limpiar_html("<p>Hola <b>mundo</b></p>") == "Hola mundo"
    assert limpiar_html("Uno&nbsp;dos") == "Uno dos"
    assert limpiar_html("") == ""


def test_raiz_de_sube_hasta_el_padre_cero():
    assert raiz_de(101, CATS)["name"] == "Diagnostico-por-Imagen"
    assert raiz_de(100, CATS)["name"] == "Diagnostico-por-Imagen"
    assert raiz_de(999, CATS) is None


def test_equipo_separa_especialidad_de_marca():
    e = equipo_desde_producto(producto(), CATS)
    assert e["especialidades"] == ["Diagnóstico por Imagen"]
    assert e["marca"] == "Siemens"
    assert "Ultrasonidos" in e["tipos"]


def test_equipo_nunca_expone_precio_ni_stock():
    e = equipo_desde_producto(producto(), CATS)
    for prohibido in ("precio", "price", "sku", "stock"):
        assert prohibido not in e


def test_destacado_es_un_booleano_no_una_categoria():
    e = equipo_desde_producto(
        producto(categories=[{"id": 100}, {"id": 300}]), CATS)
    assert e["destacado"] is True
    assert "Destacado" not in e["especialidades"]
    assert "Destacado" not in e["tipos"]
    assert equipo_desde_producto(producto(), CATS)["destacado"] is False


def test_los_tipos_duplicados_se_colapsan_sin_repetirse():
    e = equipo_desde_producto(
        producto(categories=[{"id": 100}, {"id": 101}, {"id": 102}]), CATS)
    assert e["tipos"].count("Ecógrafos") == 1
    assert sorted(e["tipos"]) == ["Ecógrafos", "Ultrasonidos"]


def test_covid_se_reasigna_a_emergencia():
    e = equipo_desde_producto(
        producto(slug="oximetro-de-pulso-yonker", name="Oxímetro de Pulso Yonker",
                 categories=[{"id": 400}, {"id": 401}]), CATS)
    assert e["especialidades"] == ["Emergencia"]
    assert "Oxímetro de Pulso" in e["tipos"]


def test_los_huerfanos_conocidos_reciben_especialidad_a_mano():
    hockey = equipo_desde_producto(
        producto(slug="hockey-stick", name="Hockey Stick",
                 categories=[{"id": 500}]), CATS)
    assert hockey["especialidades"] == ["Diagnóstico por Imagen"]
    assert hockey["marca"] == "SonoScape"

    thermo = equipo_desde_producto(
        producto(slug="thermoglide-2", name="Thermoglide", categories=[]), CATS)
    assert thermo["especialidades"] == ["Ginecología"]


def test_sin_marca_identificable_queda_en_none():
    e = equipo_desde_producto(producto(categories=[{"id": 100}]), CATS)
    assert e["marca"] is None


def test_el_texto_de_busqueda_va_normalizado():
    e = equipo_desde_producto(producto(), CATS)
    # "ecografo" sin acento tiene que encontrar "Ecógrafo"
    assert "ecografo" in e["busqueda"]
    assert "siemens" in e["busqueda"]
    assert "<b>" not in e["busqueda"]


def test_resumen_sale_del_short_description_sin_html():
    e = equipo_desde_producto(producto(), CATS)
    assert e["resumen"] == "Ecógrafo de alta gama."


def test_el_slug_percent_encodeado_se_normaliza():
    """El navegador percent-decodifica la ruta antes de tocar el disco: dejar el
    '%XX' literal en el href y en el nombre del archivo daba 404 en diez fichas
    y diez imágenes."""
    e = equipo_desde_producto(
        producto(slug="ligasure-exact-dissector-nano%e2%80%91coated-lf2019"), CATS)
    assert e["slug"] == "ligasure-exact-dissector-nano-coated-lf2019"

    e2 = equipo_desde_producto(producto(slug="smartxide%c2%b2-trio"), CATS)
    assert e2["slug"] == "smartxide-trio"


def test_el_slug_normal_no_se_toca():
    assert equipo_desde_producto(producto(), CATS)["slug"] == "acuson-sequoia"


def test_el_nombre_llega_sin_entidades_html():
    """WooCommerce devuelve 'Dräger &#8211; Atlan&reg;'. Sin desescapar, esc() lo
    volvía a escapar y la página pintaba el '&#8211;' literal en el <title>, la
    tarjeta y el mensaje precargado de WhatsApp."""
    e = equipo_desde_producto(
        producto(name="Dr\u00e4ger &#8211; Atlan&reg; A300"), CATS)
    assert e["nombre"] == "Dr\u00e4ger \u2013 Atlan\u00ae A300"
    assert "&#8211;" not in e["busqueda"]


def test_slug_de_producto_siempre_devuelve_un_slug_limpio():
    from _catalogo_map import slug_de_producto
    import re
    for crudo in ("smartxide%c2%b2-wh", "Ya-Limpio", "con espacios", "%20%20"):
        s = slug_de_producto(crudo)
        assert s == "" or re.fullmatch(r"[a-z0-9-]+", s), crudo
