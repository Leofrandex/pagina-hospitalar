# Catálogo de equipos — plan de implementación

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Traer los 215 equipos del WooCommerce viejo al rediseño como una vitrina estática, curada en tres ejes, con buscador instantáneo y WhatsApp como único CTA.

**Architecture:** Un script manual baja la Store API y las imágenes una sola vez y escribe `_catalogo.json`, que se commitea y pasa a ser la fuente de verdad. Un segundo script genera `public/equipos.html` y 215 fichas estáticas desde ese JSON, reusando el shell HTML y los tokens del pipeline que ya genera `site.html`. La búsqueda es un módulo ES puro, testeado en Node y luego inlineado en la página.

**Tech Stack:** Python 3.14 (stdlib + Pillow), pytest 9, Node 24 (`node --test`), HTML/CSS estático, Next 16 sólo para los rewrites.

**Spec:** `docs/superpowers/specs/2026-09-01-catalogo-equipos-design.md`

## Global Constraints

- **El rediseño es HTML estático.** El catálogo se construye en `public/mockups/`, con el patrón de `_build-d.py`. **No** se tocan `src/` ni se crean componentes de React.
- **Sin red en el build.** `_fetch_catalogo.py` se corre a mano. `_build_catalogo.py` lee sólo `_catalogo.json` y debe funcionar con el WordPress viejo apagado.
- **Nunca mostrar precios, stock, SKU ni carrito.** Ningún producto tiene precio: `prices.price` es `"0"` en los 215.
- **CTA único:** `https://wa.me/584241941573` con el texto precargado. Es el número que ya usa `Footer.tsx:100`.
- **Módulos Python importables llevan guión bajo, no guión medio.** `_catalogo_map.py` se importa desde los tests; `_build-d.py` (con guión) sólo se ejecuta.
- **Los tokens de diseño mandan.** Colores, tipografía y radios salen de `/mockups/tokens.css` y de `DESIGN.md`. Violeta `#352E87`, naranja `#F26A36` sólo como acento y CTA, verde `#009639` terciario. Nunca naranja como fondo dominante ni como texto de cuerpo.
- **Todo texto de usuario va en español**, con acentos correctos.
- **Escapar siempre el HTML** de los datos con `html.escape(..., quote=True)`, como hace `_post_card`.

---

### Task 1: Mapa de curaduría

Las tablas que convierten las 49 raíces de WooCommerce en tres ejes. Funciones puras, sin red.

**Files:**
- Create: `public/mockups/_catalogo_map.py`
- Create: `tests/conftest.py`
- Create: `tests/test_catalogo_map.py`
- Create: `pytest.ini`

**Interfaces:**
- Consumes: nada.
- Produces:
  - `normalizar(texto: str) -> str` — minúsculas sin acentos, para comparar y buscar.
  - `slugificar(texto: str) -> str` — `"Diagnóstico por Imagen"` → `"diagnostico-por-imagen"`.
  - `ESPECIALIDADES: dict[str, str]` — nombre crudo de la raíz → nombre limpio.
  - `MARCAS: dict[str, str]` — nombre crudo → nombre limpio.
  - `RAICES_OCULTAS: set[str]`.
  - `TIPOS_UNIFICADOS: dict[str, str]` — nombre crudo de subcategoría → tipo unificado.
  - `clasificar_raiz(nombre: str) -> tuple[str, str]` — devuelve `("especialidad"|"marca"|"oculta"|"otros", nombre_limpio)`.
  - `tipo_unificado(nombre: str) -> str`.

- [ ] **Step 1: Crear la config de pytest y el conftest**

`pytest.ini`:

```ini
[pytest]
testpaths = tests
python_files = test_*.py
```

`tests/conftest.py`:

```python
"""Deja importar los módulos del pipeline de build, que viven en public/mockups."""
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "public", "mockups"))
```

- [ ] **Step 2: Escribir los tests que fallan**

`tests/test_catalogo_map.py`:

```python
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
```

- [ ] **Step 3: Correr los tests y verificar que fallan**

Run: `python -m pytest tests/test_catalogo_map.py -v`
Expected: FAIL con `ModuleNotFoundError: No module named '_catalogo_map'`

- [ ] **Step 4: Escribir el mapa**

`public/mockups/_catalogo_map.py`:

```python
# -*- coding: utf-8 -*-
"""Curaduría del catálogo: convierte las categorías de WooCommerce en tres ejes.

El sitio viejo aplana 49 categorías raíz en una sola lista, mezclando especialidades
médicas con marcas de fabricantes. Acá se separan a mano, una vez, y queda registrado.
Es deliberadamente una tabla explícita y no una heurística: cuando el equipo cree una
categoría nueva, tiene que pasar por acá.
"""
import re
import unicodedata

# Raíz cruda en WooCommerce -> nombre que mostramos.
ESPECIALIDADES = {
    "Diagnostico-por-Imagen": "Diagnóstico por Imagen",
    "Ginecologia": "Ginecología",
    "Dermatologia/Medicina-Estetica": "Dermatología / Medicina Estética",
    "Otorrinolaringologia": "Otorrinolaringología",
    "Cardiologia": "Cardiología",
    "Cirugía": "Cirugía",
    "Anestesia": "Anestesia",
    "Gastroenterologia": "Gastroenterología",
    "Urologia": "Urología",
    "Emergencia": "Emergencia",
    "Quirofano": "Quirófano",
    "Neurologia": "Neurología",
    "Instrumental Medico": "Instrumental Médico",
    "Esterilizacion": "Esterilización",
    "Cirugía Plástica": "Cirugía Plástica",
    "Mobiliario-Medico": "Mobiliario Médico",
    "Neonatología": "Neonatología",
    "Hospitalización": "Hospitalización",
}

MARCAS = {
    "Interacoustics": "Interacoustics",
    "Siemens": "Siemens",
    "Deka Laser": "Deka Laser",
    "Sonoscape": "SonoScape",
    "Dräger": "Dräger",
    "Sony": "Sony",
    "Medtronic": "Medtronic",
    "Ebneuro": "EB Neuro",
    "Hyun Laser": "Hyun Laser",
    "Mega Medical": "Mega Medical",
    "Zoncare": "Zoncare",
    "Inmode": "InMode",
    "Esaote": "Esaote",
    "Canfield": "Canfield",
    "Candela Medical": "Candela Medical",
    "Hydrafacial": "Hydrafacial",
    "Matachana": "Matachana",
    "Barco": "Barco",
    "Olympus": "Olympus",
    "UMF Medical": "UMF Medical",
    "BMI": "BMI",
    "Cocoon Medical": "Cocoon Medical",
    "Echolight": "Echolight",
    "Mobile ODT": "MobileODT",
    "Yonker": "Yonker",
}

# Raíces que no son ni especialidad ni marca. Ver §5.4 del spec.
#   Destacado          -> pasa a ser el booleano `destacado` del equipo
#   Sin categorizar    -> no tiene ningún producto publicado
#   Covid              -> su único producto se reasigna a Emergencia
#   Radiología Comp./Directa, Estudios Óseos -> son tipos, no especialidades
RAICES_OCULTAS = {
    "Destacado",
    "Sin categorizar",
    "Covid",
    "Radiología Computarizada",
    "Radiología Directa",
    "Estudios Óseos",
    "Densitometro Oseo",
}

# El sitio viejo repite el mismo tipo de equipo una vez por especialidad.
# Acá se colapsan para poder preguntar "todos los ecógrafos".
TIPOS_UNIFICADOS = {
    "Ecógrafos Emergencia": "Ecógrafos",
    "Ecógrafos Urología": "Ecógrafos",
    "Ecógrafos Para Anestesia": "Ecógrafos",
    "Ecógrafos Cardiología": "Ecógrafos",
    "Ecógrafos Diagnóstico por Imagen": "Ecógrafos",
    "Monitores Anestesia": "Monitores",
    "Monitores Cirugía": "Monitores",
    "Monitores Hospitalización": "Monitores",
    "Monitores Diagnóstico por Imagen": "Monitores",
    "Láser Quirúrgico Dermatología/Medicina-Estetica": "Láser Quirúrgico",
    "Láser Quirúrgico Cirugía": "Láser Quirúrgico",
    "Arcos en C Cirugía": "Arcos en C",
    "Descartables Ginecología": "Descartables",
    "Insumos Diagnóstico por Imagen": "Insumos",
    "Mobile ODT Diagnóstico por Imagen": "Colposcopia",
}


def normalizar(texto):
    """Minúsculas y sin acentos. Es lo que hace comparable 'ecografo' con 'Ecógrafos'.

    NFD y no NFKD a propósito: NFKD descompone los símbolos de compatibilidad y
    convertiría el '™' de 'MyLab™X75' en las letras 'TM'.
    """
    descompuesto = unicodedata.normalize("NFD", (texto or "").lower())
    return "".join(c for c in descompuesto if not unicodedata.combining(c))


def slugificar(texto):
    base = normalizar(texto)
    base = re.sub(r"[^a-z0-9]+", "-", base)
    return base.strip("-")


def clasificar_raiz(nombre):
    """Devuelve (eje, nombre_limpio). El eje 'otros' es la red de seguridad: una
    categoría nueva sin mapear se ve en la interfaz en vez de romper el build."""
    if nombre in ESPECIALIDADES:
        return ("especialidad", ESPECIALIDADES[nombre])
    if nombre in MARCAS:
        return ("marca", MARCAS[nombre])
    if nombre in RAICES_OCULTAS:
        return ("oculta", nombre)
    return ("otros", nombre)


def tipo_unificado(nombre):
    return TIPOS_UNIFICADOS.get(nombre, nombre)
```

- [ ] **Step 5: Correr los tests y verificar que pasan**

Run: `python -m pytest tests/test_catalogo_map.py -v`
Expected: PASS, 10 tests.

- [ ] **Step 6: Commit**

```bash
git add pytest.ini tests/conftest.py tests/test_catalogo_map.py public/mockups/_catalogo_map.py
git commit -m "Separa las categorias de Woo en especialidad, marca y tipo"
```

---

### Task 2: Transformar producto de Woo en equipo curado

La función que toma un producto crudo de la Store API y devuelve el registro que consume el sitio. Pura: recibe el producto y el índice de categorías, no toca la red.

**Files:**
- Modify: `public/mockups/_catalogo_map.py` (agregar al final)
- Create: `tests/test_equipo.py`

**Interfaces:**
- Consumes: `clasificar_raiz`, `tipo_unificado`, `normalizar`, `slugificar` de Task 1.
- Produces:
  - `REASIGNACIONES: dict[str, dict]` — slug del producto → especialidad y tipo forzados.
  - `raiz_de(cat_id: int, cats_por_id: dict) -> dict | None`
  - `limpiar_html(fragmento: str) -> str` — quita etiquetas y normaliza espacios.
  - `equipo_desde_producto(producto: dict, cats_por_id: dict) -> dict` con las claves:
    `slug, nombre, url_original, resumen, descripcion, especialidades (list[str]),
    marca (str|None), tipos (list[str]), destacado (bool), imagen (str|None), busqueda (str)`

- [ ] **Step 1: Escribir los tests que fallan**

`tests/test_equipo.py`:

```python
# -*- coding: utf-8 -*-
import pytest

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
```

- [ ] **Step 2: Correr los tests y verificar que fallan**

Run: `python -m pytest tests/test_equipo.py -v`
Expected: FAIL con `ImportError: cannot import name 'equipo_desde_producto'`

- [ ] **Step 3: Implementar**

Agregar al final de `public/mockups/_catalogo_map.py`:

```python
import html as _html

# Cinco equipos no tienen ninguna especialidad en WooCommerce. En vez de dejarlos
# invisibles en el catálogo, se les asigna a mano según lo que son:
#   hockey-stick    transductor de ultrasonido
#   thermoglide-2   trata lesiones precancerosas de cuello uterino
#   valleylab-...   electrodos de electrocirugía
#   oxylog-3000-plus ventilador de transporte
#   oximetro-...    venía colgado de la categoría Covid
REASIGNACIONES = {
    "hockey-stick": {"especialidades": ["Diagnóstico por Imagen"], "tipos": ["Ultrasonidos"]},
    "thermoglide-2": {"especialidades": ["Ginecología"], "tipos": []},
    "valleylab-electrodos-con-cable-de-retorno-del-paciente": {
        "especialidades": ["Cirugía"], "tipos": ["Sellado de Vasos"]},
    "oxylog-3000-plus": {"especialidades": ["Emergencia"], "tipos": ["Respiradores Mecánicos"]},
    "oximetro-de-pulso-yonker": {"especialidades": ["Emergencia"], "tipos": []},
}

_ETIQUETAS = re.compile(r"<[^>]+>")
_ESPACIOS = re.compile(r"\s+")
# Cada etiqueta se reemplaza por un espacio para no pegar palabras de bloques
# distintos, pero eso deja "alta gama ." cuando el punto venía después de un </b>.
_ESPACIO_ANTES_DE_PUNTUACION = re.compile(r"\s+([.,;:!?%)\]»])")


def limpiar_html(fragmento):
    sin_etiquetas = _ETIQUETAS.sub(" ", fragmento or "")
    texto = _html.unescape(sin_etiquetas).replace("\xa0", " ")
    texto = _ESPACIOS.sub(" ", texto)
    return _ESPACIO_ANTES_DE_PUNTUACION.sub(r"\1", texto).strip()


def raiz_de(cat_id, cats_por_id):
    """Sube por el árbol de categorías hasta la que tiene parent 0."""
    cat = cats_por_id.get(cat_id)
    visitadas = set()
    while cat and cat["parent"] != 0:
        if cat["id"] in visitadas:  # ciclo defensivo
            return None
        visitadas.add(cat["id"])
        cat = cats_por_id.get(cat["parent"])
    return cat


def _sin_repetir(valores):
    vistos = []
    for v in valores:
        if v not in vistos:
            vistos.append(v)
    return vistos


def equipo_desde_producto(producto, cats_por_id):
    especialidades, tipos, marca, destacado = [], [], None, False

    for ref in producto.get("categories", []):
        cat = cats_por_id.get(ref["id"])
        if not cat:
            continue
        raiz = raiz_de(ref["id"], cats_por_id)
        if raiz is None:
            continue
        eje, limpio = clasificar_raiz(raiz["name"])

        if raiz["name"] == "Destacado":
            destacado = True

        es_la_raiz = cat["id"] == raiz["id"]
        if es_la_raiz:
            if eje == "especialidad":
                especialidades.append(limpio)
            elif eje == "marca":
                marca = marca or limpio
            # 'oculta' y 'otros' no aportan nada como raíz
        else:
            # Es una subcategoría: siempre es un tipo de equipo.
            tipos.append(tipo_unificado(cat["name"]))
            if eje == "especialidad":
                especialidades.append(limpio)
            elif eje == "marca":
                marca = marca or limpio

    forzado = REASIGNACIONES.get(producto["slug"])
    if forzado:
        especialidades = list(forzado["especialidades"])
        tipos = _sin_repetir(tipos + forzado["tipos"])

    especialidades = _sin_repetir(especialidades)
    tipos = _sin_repetir(tipos)

    resumen = limpiar_html(producto.get("short_description"))
    descripcion = limpiar_html(producto.get("description"))
    imagenes = producto.get("images") or []
    imagen = (imagenes[0].get("thumbnail") or imagenes[0].get("src")) if imagenes else None

    partes = [producto["name"], marca or "", " ".join(especialidades),
              " ".join(tipos), resumen[:200]]
    return {
        "slug": producto["slug"],
        "nombre": producto["name"],
        "url_original": producto.get("permalink", ""),
        "resumen": resumen,
        "descripcion": descripcion,
        "especialidades": especialidades,
        "marca": marca,
        "tipos": tipos,
        "destacado": destacado,
        "imagen": imagen,
        "busqueda": normalizar(" ".join(p for p in partes if p)),
    }
```

- [ ] **Step 4: Correr los tests y verificar que pasan**

Run: `python -m pytest tests/ -v`
Expected: PASS, 21 tests.

- [ ] **Step 5: Commit**

```bash
git add public/mockups/_catalogo_map.py tests/test_equipo.py
git commit -m "Convierte productos de Woo en equipos curados"
```

---

### Task 3: Bajar el catálogo y congelarlo

El script manual que toca la red una única vez. Sus helpers de URL son puros y se testean; la descarga se verifica corriéndola de verdad.

**Files:**
- Create: `public/mockups/_fetch_catalogo.py`
- Create: `tests/test_fetch_catalogo.py`
- Genera: `public/mockups/_catalogo.json`, `public/equipos/img/*.jpg`

**Interfaces:**
- Consumes: `equipo_desde_producto`, `slugificar` de Tasks 1-2.
- Produces:
  - `url_500(src: str) -> str` — la variante de 500px que ya generó WordPress.
  - `nombre_local(slug: str, url: str) -> str` — `"acuson-sequoia.jpg"`.
  - `traer(url: str) -> list` — paginado de la Store API.
  - Al correrlo: `_catalogo.json` con `{"equipos": [...], "especialidades": [...], "marcas": [...], "tipos": [...]}`.

- [ ] **Step 1: Escribir los tests que fallan**

`tests/test_fetch_catalogo.py`:

```python
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
```

- [ ] **Step 2: Correr los tests y verificar que fallan**

Run: `python -m pytest tests/test_fetch_catalogo.py -v`
Expected: FAIL con `ModuleNotFoundError: No module named '_fetch_catalogo'`

- [ ] **Step 3: Escribir el script**

`public/mockups/_fetch_catalogo.py`:

```python
# -*- coding: utf-8 -*-
"""Baja el inventario del WooCommerce viejo y lo congela en _catalogo.json.

Se corre A MANO, nunca en el build:

    python public/mockups/_fetch_catalogo.py

El sitio nuevo no depende de que hospitalarve.com siga en pie: una vez que este
script escribió _catalogo.json y las imágenes, todo lo demás sale del repo.
"""
import json
import os
import re
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from _catalogo_map import equipo_desde_producto, slugificar  # noqa: E402

API = "https://hospitalarve.com/wp-json/wc/store/v1"
SALIDA_JSON = os.path.join(HERE, "_catalogo.json")
SALIDA_IMG = os.path.join(HERE, "..", "equipos", "img")
UA = {"User-Agent": "Mozilla/5.0 (compatible; HospitalarBuild/1.0)"}

_SUFIJO_500 = re.compile(r"-500x500(\.[a-z]+)$", re.I)


def url_500(src):
    """WordPress ya generó variantes redimensionadas; usamos la de 500px en vez
    de la original, que promedia 124KB."""
    if _SUFIJO_500.search(src):
        return src
    base, punto, ext = src.rpartition(".")
    if not punto:
        return src
    return "%s-500x500.%s" % (base, ext)


def nombre_local(slug, url):
    ext = url.rsplit(".", 1)[-1].split("?")[0].lower()
    return "%s.%s" % (slug, ext)


def traer(ruta):
    """Pagina la Store API hasta que devuelve una página vacía."""
    todo, pagina = [], 1
    while True:
        url = "%s/%s?per_page=100&page=%d" % (API, ruta, pagina)
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=60) as r:
            lote = json.load(r)
        if not lote:
            break
        todo.extend(lote)
        if len(lote) < 100:
            break
        pagina += 1
    return todo


def bajar_imagen(url, destino):
    if os.path.exists(destino):
        return True
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            datos = r.read()
    except Exception:
        return False
    if len(datos) < 512:  # respuesta de error disfrazada
        return False
    with open(destino, "wb") as f:
        f.write(datos)
    return True


def main():
    print("Bajando categorías…")
    cats = traer("products/categories")
    cats_por_id = {c["id"]: c for c in cats}
    print("  %d categorías" % len(cats))

    print("Bajando productos…")
    productos = traer("products")
    print("  %d productos" % len(productos))

    os.makedirs(SALIDA_IMG, exist_ok=True)
    equipos = []
    for p in productos:
        e = equipo_desde_producto(p, cats_por_id)
        if e["imagen"]:
            url = url_500(e["imagen"])
            archivo = nombre_local(e["slug"], url)
            destino = os.path.join(SALIDA_IMG, archivo)
            if bajar_imagen(url, destino) or bajar_imagen(e["imagen"], destino):
                e["imagen"] = "/equipos/img/%s" % archivo
            else:
                print("  sin imagen: %s" % e["slug"])
                e["imagen"] = None
        equipos.append(e)

    equipos.sort(key=lambda e: (not e["destacado"], e["nombre"].lower()))

    def eje(clave):
        vistos = {}
        for e in equipos:
            valores = e[clave] if isinstance(e[clave], list) else ([e[clave]] if e[clave] else [])
            for v in valores:
                vistos[v] = vistos.get(v, 0) + 1
        return [{"nombre": n, "slug": slugificar(n), "total": t}
                for n, t in sorted(vistos.items(), key=lambda kv: (-kv[1], kv[0]))]

    catalogo = {
        "equipos": equipos,
        "especialidades": eje("especialidades"),
        "marcas": eje("marca"),
        "tipos": eje("tipos"),
    }
    with open(SALIDA_JSON, "w", encoding="utf-8") as f:
        json.dump(catalogo, f, ensure_ascii=False, indent=1)

    sin_esp = [e["slug"] for e in equipos if not e["especialidades"]]
    print("Escrito %s" % SALIDA_JSON)
    print("  %d equipos, %d especialidades, %d marcas, %d tipos" % (
        len(equipos), len(catalogo["especialidades"]),
        len(catalogo["marcas"]), len(catalogo["tipos"])))
    if sin_esp:
        print("  OJO, sin especialidad: %s" % ", ".join(sin_esp))


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Correr los tests y verificar que pasan**

Run: `python -m pytest tests/test_fetch_catalogo.py -v`
Expected: PASS, 4 tests.

- [ ] **Step 5: Correr el script de verdad**

Run: `python public/mockups/_fetch_catalogo.py`

Expected: imprime 136 categorías, 215 productos, y termina con
`215 equipos, 18 especialidades, 25 marcas, ...`.
**No debe imprimir ninguna línea "OJO, sin especialidad"** — si la imprime, falta una
entrada en `REASIGNACIONES` (Task 2).

- [ ] **Step 6: Verificar el peso de las imágenes**

Run: `du -sh public/equipos/img && ls public/equipos/img | wc -l`
Expected: ~215 archivos. Si el total supera **15MB**, agregar este paso de re-encodeo
al final de `main()` antes de continuar:

```python
def recomprimir(carpeta, limite_mb=15):
    """Sólo si hace falta: pasa a WebP calidad 82, que suele bajar un 60%."""
    from PIL import Image
    total = sum(os.path.getsize(os.path.join(carpeta, f)) for f in os.listdir(carpeta))
    if total <= limite_mb * 1024 * 1024:
        return
    for f in os.listdir(carpeta):
        origen = os.path.join(carpeta, f)
        if f.lower().endswith(".webp"):
            continue
        img = Image.open(origen).convert("RGB")
        img.save(os.path.splitext(origen)[0] + ".webp", "WEBP", quality=82)
        os.remove(origen)
```

(Si se usa, hay que reflejar la extensión `.webp` en el campo `imagen` del JSON.)

- [ ] **Step 7: Commit**

```bash
git add public/mockups/_fetch_catalogo.py tests/test_fetch_catalogo.py
git add public/mockups/_catalogo.json public/equipos/img
git commit -m "Congela los 215 equipos y sus imagenes en el repo"
```

---

### Task 4: La lógica del buscador

Módulo ES puro, sin DOM, para poder testearlo en Node. Después se inlinea en la página.

**Files:**
- Create: `public/mockups/_buscador.mjs`
- Create: `tests/buscador.test.mjs`

**Interfaces:**
- Consumes: nada.
- Produces:
  - `normalizar(texto) -> string`
  - `buscar(equipos, filtros) -> string[]` — devuelve slugs. `filtros` es
    `{q, esp, marca, tipo}` donde `esp`/`marca`/`tipo` son arrays de nombres.
  - `contarFacetas(equipos, filtros) -> {especialidades: {}, marcas: {}, tipos: {}}` —
    conteos que resultarían al agregar cada valor, dejando fuera la faceta propia.

- [ ] **Step 1: Escribir los tests que fallan**

`tests/buscador.test.mjs`:

```javascript
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { buscar, contarFacetas, normalizar } from '../public/mockups/_buscador.mjs';

const EQUIPOS = [
  { slug: 'acuson', nombre: 'ACUSON Sequoia', marca: 'Siemens',
    especialidades: ['Diagnóstico por Imagen'], tipos: ['Ecógrafos'],
    busqueda: 'acuson sequoia siemens diagnostico por imagen ecografos' },
  { slug: 'mylab', nombre: 'MyLab X75', marca: 'Esaote',
    especialidades: ['Cardiología', 'Diagnóstico por Imagen'], tipos: ['Ecógrafos'],
    busqueda: 'mylab x75 esaote cardiologia diagnostico por imagen ecografos' },
  { slug: 'oxylog', nombre: 'Oxylog 3000 plus', marca: 'Dräger',
    especialidades: ['Emergencia'], tipos: ['Respiradores Mecánicos'],
    busqueda: 'oxylog 3000 plus drager emergencia respiradores mecanicos' },
];

const vacio = { q: '', esp: [], marca: [], tipo: [] };

test('normalizar ignora acentos y mayúsculas', () => {
  assert.equal(normalizar('Ecógrafos'), 'ecografos');
  assert.equal(normalizar('Dräger'), 'drager');
});

test('sin filtros devuelve todo', () => {
  assert.deepEqual(buscar(EQUIPOS, vacio), ['acuson', 'mylab', 'oxylog']);
});

test('buscar sin acentos encuentra con acentos', () => {
  assert.deepEqual(buscar(EQUIPOS, { ...vacio, q: 'ecografo' }), ['acuson', 'mylab']);
});

test('varios términos exigen que estén todos', () => {
  assert.deepEqual(buscar(EQUIPOS, { ...vacio, q: 'sequoia siemens' }), ['acuson']);
  assert.deepEqual(buscar(EQUIPOS, { ...vacio, q: 'sequoia drager' }), []);
});

test('los términos coinciden por prefijo', () => {
  assert.deepEqual(buscar(EQUIPOS, { ...vacio, q: 'sono' }), []);
  assert.deepEqual(buscar(EQUIPOS, { ...vacio, q: 'oxy' }), ['oxylog']);
});

test('el eje tipo cruza especialidades', () => {
  assert.deepEqual(buscar(EQUIPOS, { ...vacio, tipo: ['Ecógrafos'] }), ['acuson', 'mylab']);
});

test('dos valores de la misma faceta son un O lógico', () => {
  assert.deepEqual(
    buscar(EQUIPOS, { ...vacio, esp: ['Cardiología', 'Emergencia'] }),
    ['mylab', 'oxylog']);
});

test('facetas distintas son un Y lógico', () => {
  assert.deepEqual(
    buscar(EQUIPOS, { ...vacio, esp: ['Cardiología'], marca: ['Siemens'] }), []);
});

test('un equipo con dos especialidades aparece filtrando por cualquiera', () => {
  assert.deepEqual(buscar(EQUIPOS, { ...vacio, esp: ['Cardiología'] }), ['mylab']);
  assert.ok(buscar(EQUIPOS, { ...vacio, esp: ['Diagnóstico por Imagen'] }).includes('mylab'));
});

test('los conteos de faceta ignoran la propia faceta', () => {
  // Con Cardiología puesta, el panel de especialidades debe seguir ofreciendo
  // Emergencia; si se contara sobre el resultado ya filtrado, daría 0.
  const c = contarFacetas(EQUIPOS, { ...vacio, esp: ['Cardiología'] });
  assert.equal(c.especialidades['Emergencia'], 1);
  assert.equal(c.especialidades['Cardiología'], 1);
  // Las otras facetas sí se cuentan sobre el resultado filtrado.
  assert.equal(c.marcas['Esaote'], 1);
  assert.equal(c.marcas['Siemens'], undefined);
});

test('los conteos respetan el texto buscado', () => {
  const c = contarFacetas(EQUIPOS, { ...vacio, q: 'ecografo' });
  assert.equal(c.especialidades['Emergencia'], undefined);
  assert.equal(c.tipos['Ecógrafos'], 2);
});
```

- [ ] **Step 2: Correr los tests y verificar que fallan**

Run: `node --test "tests/*.test.mjs"`
Expected: FAIL, no encuentra `../public/mockups/_buscador.mjs`

- [ ] **Step 3: Implementar**

`public/mockups/_buscador.mjs`:

```javascript
// Lógica de búsqueda del catálogo. Sin DOM a propósito: así corre en node --test
// y _build_catalogo.py la inlinea en la página tal cual.

// NFD y no NFKD, igual que en _catalogo_map.py: NFKD convertiría el '™' de
// 'MyLab™X75' en las letras 'TM' y los dos lados dejarían de coincidir.
export function normalizar(texto) {
  return (texto || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
}

function coincideTexto(equipo, terminos) {
  // Todos los términos tienen que aparecer, cada uno como prefijo de palabra.
  return terminos.every((t) =>
    equipo.busqueda === t ||
    equipo.busqueda.startsWith(t) ||
    equipo.busqueda.includes(' ' + t));
}

function valoresDe(equipo, faceta) {
  if (faceta === 'esp') return equipo.especialidades || [];
  if (faceta === 'tipo') return equipo.tipos || [];
  return equipo.marca ? [equipo.marca] : [];
}

// Dentro de una faceta los valores suman (O); entre facetas se restringen (Y).
function coincideFaceta(equipo, faceta, seleccion) {
  if (!seleccion || !seleccion.length) return true;
  const propios = valoresDe(equipo, faceta);
  return seleccion.some((v) => propios.includes(v));
}

function terminosDe(q) {
  return normalizar(q).split(/\s+/).filter(Boolean);
}

export function buscar(equipos, filtros, omitir) {
  const terminos = terminosDe(filtros.q);
  return equipos
    .filter((e) => coincideTexto(e, terminos))
    .filter((e) => omitir === 'esp' || coincideFaceta(e, 'esp', filtros.esp))
    .filter((e) => omitir === 'marca' || coincideFaceta(e, 'marca', filtros.marca))
    .filter((e) => omitir === 'tipo' || coincideFaceta(e, 'tipo', filtros.tipo))
    .map((e) => e.slug);
}

export function contarFacetas(equipos, filtros) {
  const porSlug = new Map(equipos.map((e) => [e.slug, e]));
  const contar = (faceta) => {
    // Se cuenta ignorando la selección de la propia faceta: si no, marcar un valor
    // dejaría el resto del panel en cero y no se podría ampliar la búsqueda.
    const slugs = buscar(equipos, filtros, faceta);
    const cuenta = {};
    for (const slug of slugs) {
      for (const v of valoresDe(porSlug.get(slug), faceta)) {
        cuenta[v] = (cuenta[v] || 0) + 1;
      }
    }
    return cuenta;
  };
  return {
    especialidades: contar('esp'),
    marcas: contar('marca'),
    tipos: contar('tipo'),
  };
}
```

- [ ] **Step 4: Correr los tests y verificar que pasan**

Run: `node --test "tests/*.test.mjs"`
Expected: PASS, 11 tests.

- [ ] **Step 5: Commit**

```bash
git add public/mockups/_buscador.mjs tests/buscador.test.mjs
git commit -m "Agrega la logica de busqueda y facetas del catalogo"
```

---

### Task 5: Generar la página del catálogo

Construye `public/equipos.html` desde `_catalogo.json`, reusando los tokens y el shell del pipeline existente. Los 215 equipos se renderizan en HTML (sirven sin JavaScript y para buscadores) y el JS sólo los muestra u oculta.

**Files:**
- Create: `public/mockups/_build_catalogo.py`
- Create: `public/mockups/_catalogo.css`
- Create: `tests/test_build_catalogo.py`
- Genera: `public/equipos.html`

**Interfaces:**
- Consumes: `_catalogo.json` (Task 3), `_buscador.mjs` (Task 4).
- Produces:
  - `tarjeta(equipo) -> str`
  - `panel_facetas(catalogo) -> str`
  - `pagina_catalogo(catalogo) -> str`
  - `wa_link(texto: str) -> str`
  - `SHELL(titulo, descripcion, cuerpo, extra_head="", scripts="") -> str`

- [ ] **Step 1: Escribir los tests que fallan**

`tests/test_build_catalogo.py`:

```python
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
```

- [ ] **Step 2: Correr los tests y verificar que fallan**

Run: `python -m pytest tests/test_build_catalogo.py -v`
Expected: FAIL con `ModuleNotFoundError: No module named '_build_catalogo'`

- [ ] **Step 3: Escribir el CSS**

`public/mockups/_catalogo.css` — usa los tokens ya definidos en `/mockups/tokens.css`:

```css
/* Catálogo de equipos. Hereda tokens de /mockups/tokens.css.
   Reglas del manual: violeta manda, naranja sólo como acento y CTA. */
.cat{max-width:var(--max);margin:0 auto;padding:0 var(--pad)}
.cat__head{padding:56px 0 28px}
.cat__titulo{margin:14px 0 0;text-transform:lowercase}
.cat__conteo{color:var(--tx-dim);margin-top:14px}

.buscador{position:relative;margin-top:28px}
.buscador input{width:100%;padding:18px 20px 18px 52px;border:0;border-radius:var(--r-m);
  background:var(--card);color:var(--tx);font:inherit;font-size:17px}
.buscador input:focus{outline:2px solid var(--naranja);outline-offset:2px}
.buscador svg{position:absolute;left:20px;top:50%;transform:translateY(-50%);
  width:20px;height:20px;stroke:var(--tx-dim);fill:none;stroke-width:2}

.chips{display:flex;gap:10px;flex-wrap:wrap;margin-top:16px}
.chip{border:0;border-radius:999px;padding:9px 16px;background:var(--card);
  color:var(--tx);font:inherit;font-size:14px;cursor:pointer;
  transition:background var(--dur-hover) var(--ease-hover)}
.chip:hover{background:var(--card-hover)}
.chip[aria-pressed="true"]{background:var(--violeta);color:#fff}

.cat__cuerpo{display:grid;grid-template-columns:250px 1fr;gap:44px;padding:36px 0 88px;
  align-items:start}
@media (max-width:900px){.cat__cuerpo{grid-template-columns:1fr}}

.facetas{position:sticky;top:96px;display:grid;gap:26px}
.faceta h3{font-size:12px;letter-spacing:.09em;text-transform:uppercase;
  color:var(--tx-dim);margin:0 0 12px}
.faceta label{display:flex;align-items:center;gap:9px;padding:5px 0;cursor:pointer;
  font-size:15px}
.faceta label[data-vacia="1"]{opacity:.35;cursor:not-allowed}
.faceta .n{margin-left:auto;color:var(--tx-dim);font-size:13px;font-variant-numeric:tabular-nums}

.rejilla{display:grid;grid-template-columns:repeat(auto-fill,minmax(232px,1fr));gap:22px}
.eq{display:flex;flex-direction:column;border-radius:var(--r-m);overflow:hidden;
  background:var(--card);color:inherit;text-decoration:none;
  transition:transform var(--dur-hover) var(--ease-hover),background var(--dur-hover)}
.eq:hover{transform:translateY(-3px);background:var(--card-hover)}
.eq__img{aspect-ratio:4/3;object-fit:contain;width:100%;background:#fff;padding:14px}
.eq__in{padding:16px 18px 20px;display:flex;flex-direction:column;gap:7px;flex:1}
.eq__marca{font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--tx-dim)}
.eq__nombre{font-size:16px;line-height:1.3;margin:0}
.eq__esp{margin-top:auto;padding-top:10px;font-size:13px;color:var(--tx-dim)}
.eq__dest{position:absolute;margin:12px;padding:4px 10px;border-radius:999px;
  background:var(--naranja);color:#fff;font-size:11px;font-weight:700;letter-spacing:.05em}

.cat__vacio{padding:64px 0;text-align:center;color:var(--tx-dim)}
.cat__vacio a{color:var(--naranja);font-weight:600}
```

- [ ] **Step 4: Escribir el generador**

`public/mockups/_build_catalogo.py`:

```python
# -*- coding: utf-8 -*-
"""Genera public/equipos.html y las fichas desde _catalogo.json.

No toca la red: todo sale del JSON congelado por _fetch_catalogo.py.
"""
import html as _html
import json
import os
import re
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
PUBLIC = os.path.join(HERE, "..")
WHATSAPP = "584241941573"


def _leer(nombre):
    with open(os.path.join(HERE, nombre), encoding="utf-8") as f:
        return f.read()


def cargar_catalogo():
    with open(os.path.join(HERE, "_catalogo.json"), encoding="utf-8") as f:
        return json.load(f)


def esc(texto):
    return _html.escape(texto or "", quote=True)


def wa_link(texto):
    return "https://wa.me/%s?text=%s" % (WHATSAPP, urllib.parse.quote(texto))


def SHELL(titulo, descripcion, cuerpo, extra_head="", scripts=""):
    """Mismo shell que build() en _build-d.py: tokens, tema claro y bgfx."""
    boot = ("(function(){var t='light';try{var v=localStorage.getItem('hosp-theme-page-light');"
            "if(v)t=v}catch(e){}document.documentElement.dataset.theme=t})();")
    return f"""<!doctype html>
<html lang="es" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{esc(descripcion)}">
<title>{esc(titulo)}</title>
<meta name="color-scheme" content="dark light">
<link rel="icon" href="/brand/logo/isotipo-cp.png">
<script>{boot}</script>
<link rel="stylesheet" href="/mockups/tokens.css">
<style>{_leer("_catalogo.css")}</style>
{extra_head}
</head>
<body>
<div class="bgfx" aria-hidden="true"></div>
{cuerpo}
{scripts}
</body>
</html>
"""


def tarjeta(e):
    img = ('<img class="eq__img" src="%s" alt="" loading="lazy" width="232" height="174">'
           % esc(e["imagen"])) if e["imagen"] else '<div class="eq__img"></div>'
    dest = '<span class="eq__dest">Destacado</span>' if e.get("destacado") else ""
    marca = '<span class="eq__marca">%s</span>' % esc(e["marca"]) if e.get("marca") else ""
    esp = '<span class="eq__esp">%s</span>' % esc(" · ".join(e["especialidades"])) \
        if e["especialidades"] else ""
    return (
        '<a class="eq " href="/equipos/%s" data-slug="%s">%s%s'
        '<div class="eq__in">%s<h3 class="eq__nombre">%s</h3>%s</div></a>'
    ) % (esc(e["slug"]), esc(e["slug"]), dest, img, marca, esc(e["nombre"]), esp)


def _faceta(clave, etiqueta, valores):
    filas = "".join(
        '<label data-valor="%s"><input type="checkbox" name="%s" value="%s">'
        '<span>%s</span><span class="n">%d</span></label>'
        % (esc(v["nombre"]), clave, esc(v["nombre"]), esc(v["nombre"]), v["total"])
        for v in valores)
    return ('<div class="faceta" data-faceta="%s"><h3>%s</h3>%s</div>'
            % (clave, esc(etiqueta), filas))


def panel_facetas(catalogo):
    return ('<aside class="facetas">%s%s%s</aside>' % (
        _faceta("esp", "Especialidad", catalogo["especialidades"]),
        _faceta("marca", "Marca", catalogo["marcas"]),
        _faceta("tipo", "Tipo de equipo", catalogo["tipos"]),
    ))


def _indice(catalogo):
    """Sólo lo que necesita el buscador: el resto ya está en el HTML."""
    return [{"slug": e["slug"], "busqueda": e["busqueda"], "marca": e["marca"],
             "especialidades": e["especialidades"], "tipos": e["tipos"]}
            for e in catalogo["equipos"]]


def _buscador_inline():
    """Inlinea _buscador.mjs quitándole los `export`, para que corra como script
    clásico dentro de la página sin pedir un fetch extra."""
    codigo = _leer("_buscador.mjs")
    return re.sub(r"^export\s+", "", codigo, flags=re.M)


def pagina_catalogo(catalogo):
    total = len(catalogo["equipos"])
    tarjetas = "".join(tarjeta(e) for e in catalogo["equipos"])
    datos = json.dumps(_indice(catalogo), ensure_ascii=False, separators=(",", ":"))
    cuerpo = f"""
<main class="cat">
  <header class="cat__head">
    <p class="eyebrow" style="color:var(--accent-eyebrow)">Catálogo</p>
    <h1 class="display-l cat__titulo">equipos que representamos</h1>
    <div class="buscador">
      <svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
      <label class="sr-only" for="q">Buscar equipos</label>
      <input id="q" type="search" autocomplete="off"
             placeholder="Buscá un equipo, una marca o una técnica…">
    </div>
    <div class="chips" id="chips"></div>
    <p class="cat__conteo"><strong id="conteo">{total}</strong> equipos ·
       {len(catalogo["especialidades"])} especialidades ·
       {len(catalogo["marcas"])} marcas</p>
  </header>
  <div class="cat__cuerpo">
    {panel_facetas(catalogo)}
    <div>
      <div class="rejilla" id="rejilla">{tarjetas}</div>
      <div class="cat__vacio" id="vacio" hidden>
        <p>No encontramos equipos con esa búsqueda.</p>
        <p><a href="{wa_link("Hola, estoy buscando un equipo que no encontré en el catálogo:")}"
              target="_blank" rel="noopener">Contanos qué necesitás por WhatsApp →</a></p>
      </div>
    </div>
  </div>
</main>"""
    scripts = (
        '<script type="application/json" id="catalogo-datos">%s</script>\n'
        '<script>%s\n%s</script>' % (datos, _buscador_inline(), _CONTROLADOR))
    return SHELL("Equipos médicos | Hospitalar Venezuela",
                 "Catálogo de equipos médicos que representamos en Venezuela: "
                 "diagnóstico por imagen, ginecología, cardiología, quirófano y más.",
                 cuerpo, scripts=scripts)


_CONTROLADOR = r"""
// Conecta el buscador puro con el DOM y con la URL.
(function () {
  var EQUIPOS = JSON.parse(document.getElementById('catalogo-datos').textContent);
  var input = document.getElementById('q');
  var rejilla = document.getElementById('rejilla');
  var vacio = document.getElementById('vacio');
  var conteo = document.getElementById('conteo');
  var tarjetas = {};
  Array.prototype.forEach.call(rejilla.children, function (el) {
    tarjetas[el.dataset.slug] = el;
  });

  function leerURL() {
    var p = new URLSearchParams(location.search);
    var lista = function (k) { return p.getAll(k).filter(Boolean); };
    return { q: p.get('q') || '', esp: lista('esp'), marca: lista('marca'), tipo: lista('tipo') };
  }

  function escribirURL(f) {
    var p = new URLSearchParams();
    if (f.q) p.set('q', f.q);
    ['esp', 'marca', 'tipo'].forEach(function (k) {
      f[k].forEach(function (v) { p.append(k, v); });
    });
    var qs = p.toString();
    history.replaceState(null, '', qs ? '?' + qs : location.pathname);
  }

  function leerCasillas() {
    var f = { q: input.value, esp: [], marca: [], tipo: [] };
    document.querySelectorAll('.faceta input:checked').forEach(function (c) {
      f[c.name].push(c.value);
    });
    return f;
  }

  function pintar(f) {
    var visibles = buscar(EQUIPOS, f);
    var set = new Set(visibles);
    Object.keys(tarjetas).forEach(function (slug) {
      tarjetas[slug].hidden = !set.has(slug);
    });
    conteo.textContent = visibles.length;
    vacio.hidden = visibles.length !== 0;
    rejilla.hidden = visibles.length === 0;

    var cuentas = contarFacetas(EQUIPOS, f);
    var mapa = { esp: cuentas.especialidades, marca: cuentas.marcas, tipo: cuentas.tipos };
    document.querySelectorAll('.faceta').forEach(function (panel) {
      var c = mapa[panel.dataset.faceta];
      panel.querySelectorAll('label').forEach(function (label) {
        var n = c[label.dataset.valor] || 0;
        label.querySelector('.n').textContent = n;
        var casilla = label.querySelector('input');
        label.dataset.vacia = (n === 0 && !casilla.checked) ? '1' : '0';
        casilla.disabled = n === 0 && !casilla.checked;
      });
    });
    escribirURL(f);
  }

  function aplicar(f) {
    input.value = f.q;
    document.querySelectorAll('.faceta input').forEach(function (c) {
      c.checked = f[c.name].indexOf(c.value) !== -1;
    });
    pintar(f);
  }

  var t;
  input.addEventListener('input', function () {
    clearTimeout(t);
    t = setTimeout(function () { pintar(leerCasillas()); }, 120);
  });
  document.querySelectorAll('.faceta input').forEach(function (c) {
    c.addEventListener('change', function () { pintar(leerCasillas()); });
  });
  window.addEventListener('popstate', function () { aplicar(leerURL()); });

  aplicar(leerURL());
})();
"""


def main():
    catalogo = cargar_catalogo()
    destino = os.path.join(PUBLIC, "equipos.html")
    with open(destino, "w", encoding="utf-8") as f:
        f.write(pagina_catalogo(catalogo))
    print("generado public/equipos.html con %d equipos" % len(catalogo["equipos"]))


if __name__ == "__main__":
    main()
```

- [ ] **Step 5: Agregar la clase `sr-only` si no existe**

Run: `grep -n "sr-only" public/mockups/tokens.css`
Si no aparece, agregar al final de `_catalogo.css`:

```css
.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;
  clip:rect(0 0 0 0);white-space:nowrap;border:0}
```

- [ ] **Step 6: Generar y correr los tests**

Run: `python public/mockups/_build_catalogo.py && python -m pytest tests/test_build_catalogo.py -v`
Expected: imprime `generado public/equipos.html con 215 equipos`, y PASS en 9 tests.

- [ ] **Step 7: Commit**

```bash
git add public/mockups/_build_catalogo.py public/mockups/_catalogo.css
git add tests/test_build_catalogo.py public/equipos.html
git commit -m "Genera la pagina del catalogo con buscador y facetas"
```

---

### Task 6: Las 215 fichas

Una página por equipo, con CSS compartido y el CTA de WhatsApp nombrando el equipo.

**Files:**
- Modify: `public/mockups/_build_catalogo.py`
- Modify: `tests/test_build_catalogo.py`
- Genera: `public/equipos/<slug>.html` ×215

**Interfaces:**
- Consumes: `SHELL`, `esc`, `wa_link`, `cargar_catalogo` de Task 5.
- Produces: `pagina_ficha(equipo, catalogo) -> str`; `main()` ahora escribe también las fichas.

- [ ] **Step 1: Escribir los tests que fallan**

Agregar a `tests/test_build_catalogo.py`:

```python
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
```

Y agregar `import urllib.parse` arriba del archivo de tests.

- [ ] **Step 2: Correr y verificar que fallan**

Run: `python -m pytest tests/test_build_catalogo.py -v`
Expected: FAIL con `ImportError: cannot import name 'pagina_ficha'`

- [ ] **Step 3: Implementar la ficha**

Agregar a `public/mockups/_catalogo.css`:

```css
.ficha{max-width:var(--max);margin:0 auto;padding:44px var(--pad) 88px}
.ficha__volver{color:var(--tx-dim);text-decoration:none;font-size:14px}
.ficha__volver:hover{color:var(--naranja)}
.ficha__cuerpo{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);
  gap:52px;margin-top:26px;align-items:start}
@media (max-width:860px){.ficha__cuerpo{grid-template-columns:1fr;gap:30px}}
.ficha__img{width:100%;border-radius:var(--r-m);background:#fff;padding:26px;
  object-fit:contain;aspect-ratio:4/3}
.ficha__marca{font-size:12px;letter-spacing:.09em;text-transform:uppercase;color:var(--tx-dim)}
.ficha__nombre{margin:10px 0 0;line-height:1.15}
.ficha__meta{display:flex;gap:8px;flex-wrap:wrap;margin:20px 0 0}
.ficha__meta a{background:var(--card);border-radius:999px;padding:7px 14px;font-size:13px;
  color:var(--tx);text-decoration:none}
.ficha__meta a:hover{background:var(--card-hover)}
.ficha__texto{margin-top:24px;line-height:1.65;color:var(--tx-dim)}
.ficha__cta{display:inline-flex;align-items:center;gap:10px;margin-top:30px;
  background:var(--naranja);color:#fff;text-decoration:none;font-weight:700;
  padding:16px 26px;border-radius:var(--r-s);
  transition:transform var(--dur-hover) var(--ease-hover)}
.ficha__cta:hover{transform:translateY(-2px)}
.ficha__nota{margin-top:12px;font-size:13px;color:var(--tx-dim)}
```

Agregar a `public/mockups/_build_catalogo.py`, antes de `main()`:

```python
def pagina_ficha(e, catalogo):
    mensaje = "Hola, me interesa el %s. ¿Me pueden dar más información?" % e["nombre"]
    img = ('<img class="ficha__img" src="%s" alt="%s" width="600" height="450">'
           % (esc(e["imagen"]), esc(e["nombre"]))) if e["imagen"] else \
          '<div class="ficha__img"></div>'
    marca = '<p class="ficha__marca">%s</p>' % esc(e["marca"]) if e.get("marca") else ""

    enlaces = []
    for nombre in e["especialidades"]:
        enlaces.append('<a href="/equipos?esp=%s">%s</a>'
                       % (urllib.parse.quote(nombre), esc(nombre)))
    for nombre in e["tipos"]:
        enlaces.append('<a href="/equipos?tipo=%s">%s</a>'
                       % (urllib.parse.quote(nombre), esc(nombre)))
    if e.get("marca"):
        enlaces.append('<a href="/equipos?marca=%s">%s</a>'
                       % (urllib.parse.quote(e["marca"]), esc(e["marca"])))
    meta = '<div class="ficha__meta">%s</div>' % "".join(enlaces) if enlaces else ""

    texto = e["descripcion"] or e["resumen"]
    cuerpo = f"""
<main class="ficha">
  <a class="ficha__volver" href="/equipos">← Volver al catálogo</a>
  <div class="ficha__cuerpo">
    <div>{img}</div>
    <div>
      {marca}
      <h1 class="display-m ficha__nombre">{esc(e["nombre"])}</h1>
      {meta}
      <div class="ficha__texto"><p>{esc(texto)}</p></div>
      <a class="ficha__cta" href="{wa_link(mensaje)}" target="_blank" rel="noopener">
        Consultar por WhatsApp →</a>
      <p class="ficha__nota">Te respondemos con disponibilidad, condiciones y respaldo técnico.</p>
    </div>
  </div>
</main>"""
    descripcion = (e["resumen"] or e["nombre"])[:155]
    return SHELL("%s | Hospitalar Venezuela" % e["nombre"], descripcion, cuerpo)
```

Y reemplazar `main()`:

```python
def main():
    catalogo = cargar_catalogo()
    with open(os.path.join(PUBLIC, "equipos.html"), "w", encoding="utf-8") as f:
        f.write(pagina_catalogo(catalogo))

    carpeta = os.path.join(PUBLIC, "equipos")
    os.makedirs(carpeta, exist_ok=True)
    for viejo in os.listdir(carpeta):
        if viejo.endswith(".html"):
            os.remove(os.path.join(carpeta, viejo))
    for e in catalogo["equipos"]:
        with open(os.path.join(carpeta, "%s.html" % e["slug"]), "w", encoding="utf-8") as f:
            f.write(pagina_ficha(e, catalogo))

    print("generado public/equipos.html y %d fichas" % len(catalogo["equipos"]))
```

- [ ] **Step 4: Generar y correr los tests**

Run: `python public/mockups/_build_catalogo.py && python -m pytest tests/ -v`
Expected: `generado public/equipos.html y 215 fichas`, y PASS en todos los tests.

- [ ] **Step 5: Commit**

```bash
git add public/mockups/_build_catalogo.py public/mockups/_catalogo.css
git add tests/test_build_catalogo.py public/equipos
git commit -m "Genera las 215 fichas con CTA de WhatsApp"
```

---

### Task 7: Servir /equipos desde Next

**Files:**
- Modify: `next.config.ts:20-32` (el bloque `rewrites`)

**Interfaces:**
- Consumes: los archivos generados en Tasks 5-6.
- Produces: las rutas `/equipos` y `/equipos/<slug>`.

- [ ] **Step 1: Agregar los rewrites**

En `next.config.ts`, dentro de `afterFiles`, después del bloque de `/lab`:

```ts
        // Catálogo de equipos: HTML estático generado por
        // public/mockups/_build_catalogo.py desde _catalogo.json.
        // Va en afterFiles a propósito: así /equipos/img/* y los assets reales
        // los resuelve el sistema de archivos, y sólo los slugs caen acá.
        { source: "/equipos", destination: "/equipos.html" },
        { source: "/equipos/:slug", destination: "/equipos/:slug.html" },
```

- [ ] **Step 2: Verificar que las tres rutas responden**

Run: `npm run dev` y en otra terminal:

```bash
curl -s -o /dev/null -w "%{http_code} %{content_type}\n" http://localhost:3000/equipos
curl -s -o /dev/null -w "%{http_code} %{content_type}\n" http://localhost:3000/equipos/acuson-sequoia
curl -s -o /dev/null -w "%{http_code} %{content_type}\n" http://localhost:3000/equipos/img/acuson-sequoia.jpeg
```

Expected: las tres devuelven `200`, las dos primeras `text/html`, la tercera `image/*`.
Si la de la imagen devuelve HTML, el rewrite quedó en `beforeFiles`: moverlo a `afterFiles`.

- [ ] **Step 3: Probar la búsqueda en el navegador**

Abrir `http://localhost:3000/equipos` y comprobar a mano:
1. Escribir `ecografo` → quedan equipos de varias especialidades (Cardiología, Ginecología, Diagnóstico por Imagen), y el conteo baja.
2. Tildar **Especialidad → Cardiología** → la URL pasa a `?q=ecografo&esp=Cardiolog%C3%ADa`.
3. Recargar esa URL → el buscador y la casilla siguen puestos.
4. Botón atrás → vuelve al estado anterior.
5. Buscar `zzzz` → aparece el bloque vacío con el enlace a WhatsApp.

- [ ] **Step 4: Commit**

```bash
git add next.config.ts
git commit -m "Sirve /equipos y las fichas como rutas del sitio"
```

---

### Gate de revisión visual — PARAR ACÁ

El spec (§12) pide que la dirección visual se valide antes de promoverse, siguiendo lo
que ya dice `DESIGN.md`. Hasta acá el catálogo existe y se navega, pero **la home
pública sigue intacta**: nadie que entre a `hospitalar` ve nada distinto todavía. Task 8
es la que cambia eso.

- [ ] **Mostrar `/equipos` y dos o tres fichas al cliente y esperar su visto bueno.**

Qué mirar, contra `DESIGN.md`:

1. **Color.** ¿El naranja aparece sólo como acento y CTA, nunca como fondo dominante?
   ¿Hay un solo naranja compitiendo por viewport?
2. **Densidad.** Con 215 tarjetas, ¿la rejilla respira o se siente un muro?
3. **Las tarjetas.** Las fotos vienen del sitio viejo, con fondos y encuadres dispares.
   ¿El `object-fit:contain` sobre blanco las unifica lo suficiente, o hace falta
   recortarlas a cuadrado en `_fetch_catalogo.py`?
4. **La ficha.** ¿El texto de WooCommerce se lee bien en una columna, o hay que
   partirlo en párrafos?
5. **El panel de facetas.** 74 tipos es mucho: ¿hace falta colapsarlo tras un
   "ver más" a partir del décimo?

Si algo hay que cambiar, se cambia **acá**, en `_catalogo.css` y en los generadores,
antes de seguir. Iterar sobre `/equipos` ya construido es más barato que rehacerlo
después de haberlo enganchado a la home.

---

### Task 8: Conectar la home con el catálogo

Las especialidades de la home dejan de listar equipos inventados y pasan a mostrar conteos reales enlazados al catálogo.

**Files:**
- Modify: `public/mockups/_d-body.html:84-135` (sección `#spec` completa)
- Modify: `public/mockups/_build-d.py:513-522`
- Create: `tests/test_home_catalogo.py`

**Interfaces:**
- Consumes: `_catalogo.json`.
- Produces: el placeholder `{{ESPECIALIDADES}}` en `_d-body.html`, resuelto por `_build-d.py`.

- [ ] **Step 1: Escribir los tests que fallan**

`tests/test_home_catalogo.py`:

```python
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
```

- [ ] **Step 2: Correr y verificar que fallan**

Run: `python -m pytest tests/test_home_catalogo.py -v`
Expected: FAIL — la home todavía dice "Doppler fetal".

- [ ] **Step 3: Reemplazar la sección `#spec` de `_d-body.html`**

Borrar todo el contenido de `<div class="grid">…</div>` dentro de
`<section class="spec section" id="spec" …>` (las 13 celdas `<a class="cell rv">`
escritas a mano) y dejar la sección así:

```html
<section class="spec section" id="spec" data-sec="light">
  <div class="wrap">
    <div class="rv sec-head">
      <div>
        <p class="eyebrow" style="color:var(--accent-eyebrow)">Especialidades</p>
        <h2 class="display-l" style="margin-top:16px;text-transform:lowercase">soluciones por área clínica</h2>
      </div>
      <p class="body-s" style="max-width:34ch">Equipos, consumibles y soporte biomédico especializado, con respaldo técnico local en cada línea.</p>
    </div>
    <div class="grid">{{ESPECIALIDADES}}</div>
    <p class="rv" style="margin-top:36px">
      <a class="ghost" href="/equipos">Ver el catálogo completo →</a>
    </p>
  </div>
</section>
```

En el `<nav>` de `_d-body.html` (línea ~7), cambiar el enlace de Especialidades para
que apunte al catálogo:

```html
<a href="/equipos">Equipos</a>
```

- [ ] **Step 4: Resolver el placeholder en `_build-d.py`**

Agregar antes de la definición de `build()` (después de `POSTS_HTML`):

```python
# Las especialidades salen del catálogo congelado: conteos y nombres reales,
# nunca listas escritas a mano.
CATALOGO = json.load(open(os.path.join(HERE, "_catalogo.json"), encoding="utf-8"))

_ICONOS = {
    "Diagnóstico por Imagen": '<circle cx="12" cy="12" r="9"/><path d="M12 3v18M3 12h18"/>',
    "Ginecología": '<circle cx="12" cy="8" r="4"/><path d="M6 21c0-4 3-6 6-6s6 2 6 6"/>',
    "Cardiología": '<path d="M12 20s-7-4.6-7-9.5A3.9 3.9 0 0 1 12 8a3.9 3.9 0 0 1 7 2.5C19 15.4 12 20 12 20z"/>',
}
_ICONO_POR_DEFECTO = '<rect x="4" y="4" width="16" height="16" rx="4"/><path d="M9 12h6"/>'


def _tipos_de(especialidad, cuantos=4):
    """Los tipos de equipo más frecuentes dentro de una especialidad.
    Reemplaza a las listas que antes estaban escritas a mano en _d-body.html."""
    import collections
    cuenta = collections.Counter()
    for e in CATALOGO["equipos"]:
        if especialidad in e["especialidades"]:
            cuenta.update(e["tipos"])
    return [nombre for nombre, _ in cuenta.most_common(cuantos)]


def _celda_especialidad(esp):
    import urllib.parse
    tipos = _tipos_de(esp["nombre"])
    lis = "".join("<li>%s</li>" % _html.escape(t) for t in tipos)
    ico = _ICONOS.get(esp["nombre"], _ICONO_POR_DEFECTO)
    return (
        '<a class="cell rv" href="/equipos?esp=%s">'
        '<span class="cell__bar"></span>'
        '<div class="cell__face"><svg class="cell__ico" viewBox="0 0 24 24">%s</svg>'
        '<h3 class="title-s">%s</h3><p>%d equipos</p></div>'
        '<div class="cell__prods"><strong>%s</strong><ul>%s</ul></div></a>'
    ) % (urllib.parse.quote(esp["nombre"]), ico, _html.escape(esp["nombre"]),
         esp["total"], _html.escape(esp["nombre"]), lis)


ESPECIALIDADES_HTML = "".join(
    _celda_especialidad(e) for e in CATALOGO["especialidades"][:12])
```

Y en `build()`, encadenar el reemplazo (línea 522):

```python
    b = (body.replace("{{POSTS}}", POSTS_HTML)
             .replace("{{ESPECIALIDADES}}", ESPECIALIDADES_HTML)
             .replace("{{LOGO}}", "")
             .replace('<img class="nav__logo" src="" alt="Hospitalar">', LOGO))
```

- [ ] **Step 5: Regenerar y correr los tests**

Run: `python public/mockups/_build-d.py && python -m pytest tests/ -v && node --test "tests/*.test.mjs"`
Expected: PASS en todo.

- [ ] **Step 6: Revisar la home en el navegador**

Abrir `http://localhost:3000/` y comprobar que la sección Especialidades muestra 12
celdas con conteos reales, que el hover sigue revelando la lista de tipos, y que
hacer clic lleva a `/equipos` con la faceta puesta.

- [ ] **Step 7: Commit**

```bash
git add public/mockups/_d-body.html public/mockups/_build-d.py
git add tests/test_home_catalogo.py public/site.html public/mockups/d*.html
git commit -m "Conecta las especialidades de la home con el catalogo real"
```

---

### Task 9: Chips de necesidad clínica

Atajos escritos en el lenguaje del médico, que aplican combinaciones de filtros.

**Files:**
- Modify: `public/mockups/_catalogo_map.py` (agregar `CHIPS`)
- Modify: `public/mockups/_build_catalogo.py` (renderizar los chips)
- Modify: `tests/test_build_catalogo.py`

**Interfaces:**
- Consumes: `pagina_catalogo` de Task 5.
- Produces: `CHIPS: list[dict]` con `{"texto": str, "filtros": {"esp": [...], "tipo": [...]}}`.

- [ ] **Step 1: Escribir los tests que fallan**

Agregar a `tests/test_build_catalogo.py`:

```python
from _catalogo_map import CHIPS


def test_los_chips_apuntan_a_facetas_que_existen(catalogo):
    validos = {
        "esp": {v["nombre"] for v in catalogo["especialidades"]},
        "tipo": {v["nombre"] for v in catalogo["tipos"]},
        "marca": {v["nombre"] for v in catalogo["marcas"]},
    }
    for chip in CHIPS:
        for eje, valores in chip["filtros"].items():
            for v in valores:
                assert v in validos[eje], "%s -> %s" % (chip["texto"], v)


def test_ningun_chip_deja_la_pantalla_vacia(catalogo):
    """Un atajo que no devuelve nada es peor que no tenerlo."""
    def coincide(equipo, filtros):
        # Dentro de una faceta los valores suman; entre facetas se restringen.
        # Mismo criterio que buscar() en _buscador.mjs.
        campos = {"esp": equipo["especialidades"],
                  "tipo": equipo["tipos"],
                  "marca": [equipo["marca"]] if equipo["marca"] else []}
        for eje, elegidos in filtros.items():
            if elegidos and not any(v in campos[eje] for v in elegidos):
                return False
        return True

    for chip in CHIPS:
        hay = [e for e in catalogo["equipos"] if coincide(e, chip["filtros"])]
        assert hay, chip["texto"]


def test_la_pagina_renderiza_los_chips(catalogo):
    html = pagina_catalogo(catalogo)
    for chip in CHIPS:
        assert chip["texto"] in html
```

- [ ] **Step 2: Correr y verificar que fallan**

Run: `python -m pytest tests/test_build_catalogo.py -v`
Expected: FAIL con `ImportError: cannot import name 'CHIPS'`

- [ ] **Step 3: Definir los chips**

Agregar al final de `public/mockups/_catalogo_map.py`:

```python
# Atajos en el idioma del médico, no en el del catálogo. El que busca no siempre
# sabe que lo que necesita se llama "arco en C"; sí sabe que va a operar.
# Los valores tienen que existir en _catalogo.json: hay un test que lo verifica.
CHIPS = [
    {"texto": "Voy a montar un consultorio de ginecología",
     "filtros": {"esp": ["Ginecología"]}},
    {"texto": "Necesito reemplazar un ecógrafo",
     "filtros": {"tipo": ["Ecógrafos"]}},
    {"texto": "Equipamiento para quirófano",
     "filtros": {"esp": ["Quirófano", "Cirugía"]}},
    {"texto": "Diagnóstico por imagen",
     "filtros": {"esp": ["Diagnóstico por Imagen"]}},
    {"texto": "Medicina estética",
     "filtros": {"esp": ["Dermatología / Medicina Estética"]}},
    {"texto": "Consumibles y descartables",
     "filtros": {"tipo": ["Descartables", "Insumos"]}},
]
```

- [ ] **Step 4: Renderizarlos**

En `public/mockups/_build_catalogo.py`, importar `CHIPS` arriba:

```python
from _catalogo_map import CHIPS
```

(agregando también `import sys; sys.path.insert(0, HERE)` si hiciera falta, igual que
en `_fetch_catalogo.py`).

Reemplazar `<div class="chips" id="chips"></div>` en `pagina_catalogo` por:

```python
    chips = "".join(
        '<button class="chip" type="button" aria-pressed="false" '
        'data-filtros=\'%s\'>%s</button>'
        % (json.dumps(c["filtros"], ensure_ascii=False), esc(c["texto"]))
        for c in CHIPS)
```

y en el f-string del cuerpo: `<div class="chips" id="chips">{chips}</div>`.

Agregar al final de `_CONTROLADOR`, antes de `aplicar(leerURL());`:

```javascript
  document.querySelectorAll('.chip').forEach(function (boton) {
    boton.addEventListener('click', function () {
      var puesto = boton.getAttribute('aria-pressed') === 'true';
      document.querySelectorAll('.chip').forEach(function (o) {
        o.setAttribute('aria-pressed', 'false');
      });
      document.querySelectorAll('.faceta input').forEach(function (c) {
        c.checked = false;
      });
      if (!puesto) {
        boton.setAttribute('aria-pressed', 'true');
        var f = JSON.parse(boton.dataset.filtros);
        Object.keys(f).forEach(function (eje) {
          f[eje].forEach(function (valor) {
            var c = document.querySelector(
              '.faceta input[name="' + eje + '"][value="' + CSS.escape(valor) + '"]');
            if (c) c.checked = true;
          });
        });
      }
      pintar(leerCasillas());
    });
  });
```

- [ ] **Step 5: Generar y correr los tests**

Run: `python public/mockups/_build_catalogo.py && python -m pytest tests/ -v`
Expected: PASS.

- [ ] **Step 6: Probar en el navegador**

Abrir `/equipos`, hacer clic en "Necesito reemplazar un ecógrafo" → se tilda el tipo
Ecógrafos y quedan los equipos de varias especialidades. Volver a hacer clic → se limpia.

- [ ] **Step 7: Commit**

```bash
git add public/mockups/_catalogo_map.py public/mockups/_build_catalogo.py
git add tests/test_build_catalogo.py public/equipos.html
git commit -m "Agrega atajos de busqueda por necesidad clinica"
```

---

### Task 10: Comparador de equipos

Seleccionar hasta 3 equipos y consultarlos por WhatsApp en un solo mensaje.

**Files:**
- Modify: `public/mockups/_build_catalogo.py`
- Modify: `public/mockups/_catalogo.css`
- Modify: `tests/test_build_catalogo.py`

**Interfaces:**
- Consumes: `pagina_catalogo` de Task 5, `wa_link` de Task 5.
- Produces: la barra `#comparador` en `/equipos`.

- [ ] **Step 1: Escribir los tests que fallan**

Agregar a `tests/test_build_catalogo.py`:

```python
def test_la_pagina_trae_el_comparador(catalogo):
    html = pagina_catalogo(catalogo)
    assert 'id="comparador"' in html
    assert "Comparar" in html


def test_cada_tarjeta_permite_seleccionarse(catalogo):
    html = pagina_catalogo(catalogo)
    assert html.count('class="eq__cmp"') == 215


def test_el_comparador_arranca_oculto(catalogo):
    html = pagina_catalogo(catalogo)
    assert re.search(r'id="comparador"[^>]*\shidden', html)
```

(agregar `import re` al inicio del archivo de tests).

- [ ] **Step 2: Correr y verificar que fallan**

Run: `python -m pytest tests/test_build_catalogo.py -v`
Expected: FAIL — no existe `id="comparador"`.

- [ ] **Step 3: Estilos**

Agregar a `public/mockups/_catalogo.css`:

```css
.eq{position:relative}
.eq__cmp{position:absolute;top:10px;right:10px;z-index:2;width:26px;height:26px;
  border-radius:8px;border:0;background:rgba(255,255,255,.9);cursor:pointer;
  display:grid;place-items:center;font-size:15px;line-height:1;color:var(--violeta)}
.eq__cmp[aria-pressed="true"]{background:var(--violeta);color:#fff}

.comparador{position:fixed;left:50%;bottom:22px;transform:translateX(-50%);z-index:70;
  display:flex;align-items:center;gap:16px;padding:13px 16px 13px 20px;
  border-radius:var(--r-m);background:var(--violeta);color:#fff;
  box-shadow:0 14px 40px rgba(20,17,58,.34);max-width:calc(100vw - 32px)}
.comparador__lista{display:flex;gap:8px;flex-wrap:wrap;font-size:14px}
.comparador__lista span{background:rgba(255,255,255,.14);border-radius:999px;padding:5px 12px}
.comparador__cta{background:var(--naranja);color:#fff;text-decoration:none;font-weight:700;
  padding:11px 20px;border-radius:var(--r-s);white-space:nowrap}
.comparador__limpiar{background:none;border:0;color:rgba(255,255,255,.7);cursor:pointer;
  font:inherit;font-size:13px}
```

- [ ] **Step 4: Marcado y comportamiento**

En `tarjeta()` de `_build_catalogo.py`, agregar el botón justo después de `dest`:

```python
    cmp_btn = ('<button class="eq__cmp" type="button" aria-pressed="false" '
               'title="Comparar" data-cmp="%s" data-nombre="%s">+</button>'
               % (esc(e["slug"]), esc(e["nombre"])))
```

y cambiar el return para incluirlo:

```python
    return (
        '<a class="eq " href="/equipos/%s" data-slug="%s">%s%s%s'
        '<div class="eq__in">%s<h3 class="eq__nombre">%s</h3>%s</div></a>'
    ) % (esc(e["slug"]), esc(e["slug"]), cmp_btn, dest, img, marca,
         esc(e["nombre"]), esp)

```

Agregar la barra al cuerpo de `pagina_catalogo`, justo antes de `</main>`:

```html
  <div class="comparador" id="comparador" hidden>
    <div class="comparador__lista" id="comparador-lista"></div>
    <a class="comparador__cta" id="comparador-cta" href="#" target="_blank" rel="noopener">Consultar los 3</a>
    <button class="comparador__limpiar" type="button" id="comparador-limpiar">Limpiar</button>
  </div>
```

Agregar al final de `_CONTROLADOR`, antes de `aplicar(leerURL());`:

```javascript
  var elegidos = [];
  var barra = document.getElementById('comparador');
  var lista = document.getElementById('comparador-lista');
  var cta = document.getElementById('comparador-cta');

  function pintarComparador() {
    barra.hidden = elegidos.length === 0;
    lista.innerHTML = '';
    elegidos.forEach(function (e) {
      var s = document.createElement('span');
      s.textContent = e.nombre;
      lista.appendChild(s);
    });
    cta.textContent = elegidos.length === 1
      ? 'Consultar este equipo'
      : 'Consultar los ' + elegidos.length;
    var texto = 'Hola, me interesan estos equipos:\n' +
      elegidos.map(function (e) { return '• ' + e.nombre; }).join('\n');
    cta.href = 'https://wa.me/584241941573?text=' + encodeURIComponent(texto);
  }

  document.querySelectorAll('.eq__cmp').forEach(function (boton) {
    boton.addEventListener('click', function (ev) {
      ev.preventDefault();      // el botón vive dentro del <a> de la tarjeta
      ev.stopPropagation();
      var slug = boton.dataset.cmp;
      var i = elegidos.findIndex(function (e) { return e.slug === slug; });
      if (i !== -1) {
        elegidos.splice(i, 1);
        boton.setAttribute('aria-pressed', 'false');
        boton.textContent = '+';
      } else {
        if (elegidos.length === 3) return;   // tres es el máximo legible
        elegidos.push({ slug: slug, nombre: boton.dataset.nombre });
        boton.setAttribute('aria-pressed', 'true');
        boton.textContent = '✓';
      }
      pintarComparador();
    });
  });

  document.getElementById('comparador-limpiar').addEventListener('click', function () {
    elegidos = [];
    document.querySelectorAll('.eq__cmp').forEach(function (b) {
      b.setAttribute('aria-pressed', 'false');
      b.textContent = '+';
    });
    pintarComparador();
  });
```

- [ ] **Step 5: Generar y correr todos los tests**

Run: `python public/mockups/_build_catalogo.py && python -m pytest tests/ -v && node --test "tests/*.test.mjs"`
Expected: PASS en todo.

- [ ] **Step 6: Probar en el navegador**

En `/equipos`: marcar 3 equipos con el botón `+` → aparece la barra abajo con los tres
nombres. El clic en `+` **no** debe navegar a la ficha. El cuarto clic no agrega nada.
El CTA abre WhatsApp con los tres nombres en una lista. "Limpiar" vacía todo.

- [ ] **Step 7: Commit**

```bash
git add public/mockups/_build_catalogo.py public/mockups/_catalogo.css
git add tests/test_build_catalogo.py public/equipos.html
git commit -m "Agrega el comparador de hasta tres equipos"
```

---

### Task 11: Verificación final

**Files:**
- Create: `tests/test_independencia.py`
- Modify: `package.json` (scripts)

- [ ] **Step 1: Escribir el test de independencia**

`tests/test_independencia.py`:

```python
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
```

- [ ] **Step 2: Correr y verificar**

Run: `python -m pytest tests/test_independencia.py -v`
Expected: PASS, 4 tests. Si falla el de las imágenes, faltan archivos: volver a correr
`python public/mockups/_fetch_catalogo.py`.

- [ ] **Step 3: Dejar los comandos a mano en package.json**

En `"scripts"`, agregar:

```json
    "catalogo:bajar": "python public/mockups/_fetch_catalogo.py",
    "catalogo:build": "python public/mockups/_build_catalogo.py && python public/mockups/_build-d.py",
    "test": "python -m pytest tests -q && node --test \"tests/*.test.mjs\""
```

- [ ] **Step 4: Correr la suite completa**

Run: `npm test`
Expected: PASS en los tests de Python y en los de Node.

- [ ] **Step 5: Verificar los criterios de éxito del spec, uno por uno**

Con `npm run dev` corriendo:

1. `/equipos` lista 215 equipos. ✓
2. Buscar `ecografo` devuelve equipos de Cardiología, Ginecología y Diagnóstico por Imagen. ✓
3. Ninguna faceta dice "Sin categorizar" ni "Destacado". ✓
4. La home muestra conteos reales y sus celdas llevan a `/equipos?esp=…`. ✓
5. Cada ficha abre WhatsApp con el equipo nombrado. ✓
6. Apagar la red y recargar `/equipos` y una ficha: se ven completas, con imágenes. ✓
7. Buscar `precio`, `$`, `carrito` en `public/equipos.html` no devuelve nada. ✓

- [ ] **Step 6: Commit**

```bash
git add tests/test_independencia.py package.json
git commit -m "Verifica que el catalogo no dependa del sitio viejo"
```

---

## Notas para quien ejecute

- **El orden importa.** Task 3 tiene que correrse de verdad (baja datos e imágenes)
  antes de que Tasks 5-11 tengan algo que leer. Los tests de Task 5 en adelante leen
  `_catalogo.json` del repo.
- **Si `_fetch_catalogo.py` imprime "OJO, sin especialidad"**, hay un equipo nuevo sin
  clasificar: agregarlo a `REASIGNACIONES` en `_catalogo_map.py` y volver a correr. No
  seguir con las tareas siguientes hasta que la lista esté vacía.
- **Los conteos son datos, no constantes.** Si el equipo cargó productos nuevos en Woo
  desde que se escribió este plan, los números de los tests (215, 18, 25) van a diferir.
  Ajustar los tests al conteo real y anotarlo en el commit; no forzar los datos.
- **El patrón de `node --test` va entre comillas y con glob**, no como directorio:
  `node --test "tests/*.test.mjs"`. En este entorno (Node 24 sobre Windows),
  `node --test tests/` intenta cargar `tests` como módulo y falla con `MODULE_NOT_FOUND`.
  Está verificado; no "arreglarlo" a la forma corta.
- **El código de Tasks 1, 2 y 4 ya está validado:** se extrajo del plan y se corrió
  fuera del repo. Pasan los 21 tests de Python y los 11 de Node. Si al implementarlo
  fallan, es por una diferencia de transcripción, no por el diseño.
- **Pendiente de confirmar con el cliente:** los textos de los chips en Task 9 son una
  primera propuesta. Deberían salir de lo que la gente realmente pregunta por WhatsApp.
  Cambiarlos es editar `CHIPS` y regenerar.
