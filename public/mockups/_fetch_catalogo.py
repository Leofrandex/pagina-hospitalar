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
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from _catalogo_map import (clasificar_raiz, equipo_desde_producto,  # noqa: E402
                           raiz_de, slugificar)
from _rutas import ruta_larga  # noqa: E402

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


def _url_segura(url):
    """Codifica los caracteres que WordPress dejó crudos en el nombre del archivo.

    13 de las 215 imágenes traen '®' o '™' sin codificar, y eso rompe la línea de
    petición HTTP. El '%' va en `safe` a propósito: sin él, una URL que ya trae
    '%c2%b2' se re-codificaría a '%25c2%25b2' y dejaría de resolver.
    """
    return urllib.parse.quote(url, safe=":/%")


def bajar_imagen(url, destino):
    destino = ruta_larga(destino)
    if os.path.exists(destino):
        return True
    url = _url_segura(url)
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


def raices_sin_mapear(productos, cats_por_id):
    """Nombres de raíz que el mapa de curaduría no conoce (§5.4 del spec).

    `clasificar_raiz` los devuelve como eje "otros" y `equipo_desde_producto` los
    descarta: sin esto, una categoría raíz nueva le borraría la marca o la
    especialidad a un producto en silencio. Quedan escritos en _catalogo.json y
    hay un test que exige que la lista esté vacía, así que el silencio pasa a ser
    un test en rojo.
    """
    sueltas = set()
    for p in productos:
        for ref in p.get("categories", []):
            if ref["id"] not in cats_por_id:
                continue
            raiz = raiz_de(ref["id"], cats_por_id)
            if raiz is None:
                continue
            if clasificar_raiz(raiz["name"])[0] == "otros":
                sueltas.add(raiz["name"])
    return sorted(sueltas)


def barrer_imagenes(equipos):
    """Borra las imágenes que ya no referencia ningún equipo.

    El nombre del archivo sale del slug: cuando un slug cambia (o un producto
    desaparece de WooCommerce), la imagen vieja se quedaría en el repo para
    siempre. `_build_catalogo.py` ya hace lo mismo con las fichas HTML.
    """
    carpeta = os.path.join(SALIDA_IMG)
    if not os.path.isdir(carpeta):
        return []
    en_uso = {os.path.basename(e["imagen"]) for e in equipos if e.get("imagen")}
    borradas = []
    for archivo in sorted(os.listdir(carpeta)):
        if archivo in en_uso:
            continue
        os.remove(ruta_larga(os.path.join(carpeta, archivo)))
        borradas.append(archivo)
    return borradas


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
        "sin_mapear": raices_sin_mapear(productos, cats_por_id),
        "especialidades": eje("especialidades"),
        "marcas": eje("marca"),
        "tipos": eje("tipos"),
    }
    with open(SALIDA_JSON, "w", encoding="utf-8") as f:
        json.dump(catalogo, f, ensure_ascii=False, indent=1)

    borradas = barrer_imagenes(equipos)
    for archivo in borradas:
        print("  imagen huérfana borrada: %s" % archivo)

    sin_esp = [e["slug"] for e in equipos if not e["especialidades"]]
    print("Escrito %s" % SALIDA_JSON)
    print("  %d equipos, %d especialidades, %d marcas, %d tipos" % (
        len(equipos), len(catalogo["especialidades"]),
        len(catalogo["marcas"]), len(catalogo["tipos"])))
    if sin_esp:
        print("  OJO, sin especialidad: %s" % ", ".join(sin_esp))
    if catalogo["sin_mapear"]:
        print("  OJO, raíces sin mapear en _catalogo_map.py: %s"
              % ", ".join(catalogo["sin_mapear"]))


if __name__ == "__main__":
    main()
