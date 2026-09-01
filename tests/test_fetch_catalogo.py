# -*- coding: utf-8 -*-
from _fetch_catalogo import nombre_local, url_500


def test_url_500_usa_la_variante_que_ya_genero_wordpress():
    assert url_500("https://h.com/wp-content/uploads/2026/08/Equipo.jpeg") == \
        "https://h.com/wp-content/uploads/2026/08/Equipo-500x500.jpeg"


def test_url_500_no_duplica_el_sufijo_si_ya_lo_trae():
    ya = "https://h.com/wp-content/uploads/2026/08/Equipo-500x500.jpeg"
    assert url_500(ya) == ya


def test_url_500_respeta_webp_y_png():
    assert url_500("https://h.com/a/Toro.webp") == "https://h.com/a/Toro-500x500.webp"
    assert url_500("https://h.com/a/3-8.png") == "https://h.com/a/3-8-500x500.png"


def test_nombre_local_usa_el_slug_del_equipo_no_el_del_archivo():
    assert nombre_local("acuson-sequoia", "https://h.com/a/Equipo-500x500.jpeg") == \
        "acuson-sequoia.jpeg"
    assert nombre_local("toro", "https://h.com/a/Toro.webp") == "toro.webp"
