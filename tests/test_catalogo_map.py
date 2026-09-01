# -*- coding: utf-8 -*-
from _catalogo_map import (
    ESPECIALIDADES,
    MARCAS,
    clasificar_raiz,
    normalizar,
    slugificar,
    tipo_unificado,
)


def test_normalizar_quita_acentos_y_baja_a_minusculas():
    assert normalizar("Ecógrafos") == "ecografos"
    assert normalizar("Dräger") == "drager"
    assert normalizar("MyLab™X75") == "mylab™x75"


def test_slugificar():
    assert slugificar("Diagnóstico por Imagen") == "diagnostico-por-imagen"
    assert slugificar("Dermatología / Medicina Estética") == "dermatologia-medicina-estetica"
    assert slugificar("Cirugía Plástica") == "cirugia-plastica"


def test_hay_18_especialidades_y_25_marcas():
    assert len(ESPECIALIDADES) == 18
    assert len(MARCAS) == 25


def test_clasificar_raiz_corrige_los_nombres_feos():
    assert clasificar_raiz("Diagnostico-por-Imagen") == ("especialidad", "Diagnóstico por Imagen")
    assert clasificar_raiz("Dermatologia/Medicina-Estetica") == (
        "especialidad",
        "Dermatología / Medicina Estética",
    )
    assert clasificar_raiz("Mobiliario-Medico") == ("especialidad", "Mobiliario Médico")
    assert clasificar_raiz("Otorrinolaringologia") == ("especialidad", "Otorrinolaringología")


def test_clasificar_raiz_separa_marcas_de_especialidades():
    assert clasificar_raiz("Siemens") == ("marca", "Siemens")
    assert clasificar_raiz("Deka Laser") == ("marca", "Deka Laser")
    assert clasificar_raiz("Cardiologia")[0] == "especialidad"


def test_clasificar_raiz_oculta_el_ruido():
    for ruido in ("Destacado", "Sin categorizar", "Covid",
                  "Radiología Computarizada", "Radiología Directa", "Estudios Óseos"):
        assert clasificar_raiz(ruido)[0] == "oculta", ruido


def test_raiz_desconocida_cae_en_otros_sin_romper():
    assert clasificar_raiz("Categoría Nueva Sin Mapear") == ("otros", "Categoría Nueva Sin Mapear")


def test_tipo_unificado_colapsa_los_ecografos():
    for crudo in ("Ecógrafos", "Ecógrafos Emergencia", "Ecógrafos Urología",
                  "Ecógrafos Para Anestesia", "Ecógrafos Cardiología",
                  "Ecógrafos Diagnóstico por Imagen"):
        assert tipo_unificado(crudo) == "Ecógrafos", crudo


def test_tipo_unificado_colapsa_monitores_y_laser():
    for crudo in ("Monitores", "Monitores Anestesia", "Monitores Cirugía",
                  "Monitores Hospitalización"):
        assert tipo_unificado(crudo) == "Monitores", crudo
    assert tipo_unificado("Láser Quirúrgico") == "Láser Quirúrgico"


def test_tipo_unificado_deja_pasar_lo_que_no_esta_en_la_tabla():
    assert tipo_unificado("Mamógrafos") == "Mamógrafos"
