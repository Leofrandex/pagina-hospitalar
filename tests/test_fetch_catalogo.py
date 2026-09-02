# -*- coding: utf-8 -*-

from _fetch_catalogo import _url_segura, nombre_local, url_500


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


def test_url_segura_codifica_tm_y_r_registrado():
    assert _url_segura("https://h.com/a/LigaSure\u2122-LF1837.png") == \
        "https://h.com/a/LigaSure%E2%84%A2-LF1837.png"
    assert _url_segura("https://h.com/a/Babylog\u00ae-VN600.png") == \
        "https://h.com/a/Babylog%C2%AE-VN600.png"


def test_url_segura_no_recodifica_lo_que_ya_viene_en_porcentaje():
    # Regresión: sin safe='%' esto se convertiría en %25c2%25b2 y dejaría de
    # resolver contra el servidor real.
    ya_codificada = "https://h.com/producto/smartxide%c2%b2-wh/"
    assert _url_segura(ya_codificada) == ya_codificada


def test_url_segura_deja_igual_una_url_ascii_comun():
    normal = "https://h.com/wp-content/uploads/2026/08/Equipo-500x500.jpeg"
    assert _url_segura(normal) == normal
