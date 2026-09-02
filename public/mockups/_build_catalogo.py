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
PUBLIC = os.path.normpath(os.path.join(HERE, ".."))
WHATSAPP = "584241941573"


def _leer(nombre):
    with open(os.path.join(HERE, nombre), encoding="utf-8") as f:
        return f.read()


def _ruta_larga(ruta):
    """Algunos slugs superan los 260 caracteres que Windows exige sin este
    prefijo (MAX_PATH). No afecta a Linux/Mac, donde no se usa este prefijo.

    Mismo criterio que `_ruta_larga` de `_fetch_catalogo.py`."""
    if os.name == "nt":
        absoluta = os.path.abspath(ruta)
        if not absoluta.startswith("\\\\?\\"):
            return "\\\\?\\" + absoluta
    return ruta


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
<style>{_leer("_tema.css")}{_leer("_catalogo.css")}</style>
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
    # `json.dumps` no escapa "</", así que un nombre o descripción que contuviera
    # "</script" cerraría la etiqueta antes de tiempo y dejaría inyectar markup.
    # Hoy ningún equipo lo trae, pero el JSON se regenera desde WordPress.
    datos = json.dumps(_indice(catalogo), ensure_ascii=False,
                       separators=(",", ":")).replace("</", "<\\/")
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


def main():
    catalogo = cargar_catalogo()
    with open(os.path.join(PUBLIC, "equipos.html"), "w", encoding="utf-8") as f:
        f.write(pagina_catalogo(catalogo))

    carpeta = os.path.join(PUBLIC, "equipos")
    os.makedirs(carpeta, exist_ok=True)
    for viejo in os.listdir(carpeta):
        if viejo.endswith(".html"):
            os.remove(_ruta_larga(os.path.join(carpeta, viejo)))
    for e in catalogo["equipos"]:
        ruta = _ruta_larga(os.path.join(carpeta, "%s.html" % e["slug"]))
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(pagina_ficha(e, catalogo))

    print("generado public/equipos.html y %d fichas" % len(catalogo["equipos"]))


if __name__ == "__main__":
    main()
