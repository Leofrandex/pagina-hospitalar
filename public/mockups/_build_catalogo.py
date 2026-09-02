# -*- coding: utf-8 -*-
"""Genera public/equipos.html y las fichas desde _catalogo.json.

No toca la red: todo sale del JSON congelado por _fetch_catalogo.py.
"""
import html as _html
import json
import os
import re
import urllib.parse

from _catalogo_map import CHIPS
from _rutas import ruta_larga

HERE = os.path.dirname(os.path.abspath(__file__))
PUBLIC = os.path.normpath(os.path.join(HERE, ".."))
WHATSAPP = "584241941573"


def _leer(nombre):
    with open(os.path.join(HERE, nombre), encoding="utf-8") as f:
        return f.read()


def cargar_catalogo():
    with open(os.path.join(HERE, "_catalogo.json"), encoding="utf-8") as f:
        return json.load(f)


def css_combinado():
    """El CSS que comparten el catálogo y las 215 fichas.

    Spec §7: va a un archivo externo (/equipos/_cat.css) en vez de inlinearse en
    cada una de las 216 páginas. Inlinearlo repetía ~10KB por ficha.
    """
    return _leer("_tema.css") + _leer("_catalogo.css")


CSS_EXTERNO = "/equipos/_cat.css"


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
<link rel="stylesheet" href="{CSS_EXTERNO}">
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
    img = ('<div class="eq__marco"><img class="eq__img" src="%s" alt="" loading="lazy"'
           ' width="238" height="179"></div>' % esc(e["imagen"])) if e["imagen"]         else '<div class="eq__marco"><div class="eq__img"></div></div>'
    dest = '<span class="eq__dest">Destacado</span>' if e.get("destacado") else ""
    # 37 equipos no tienen marca. El hueco se reserva igual para que el nombre
    # arranque a la misma altura en toda la fila; vacío, sin inventar texto.
    marca = ('<span class="eq__marca">%s</span>' % esc(e["marca"])) if e.get("marca")         else '<span class="eq__marca" aria-hidden="true"></span>'
    esp = '<span class="eq__esp">%s</span>' % esc(" · ".join(e["especialidades"])) \
        if e["especialidades"] else ""
    cmp_btn = ('<button class="eq__cmp" type="button" aria-pressed="false" '
               'aria-label="Comparar %s" data-cmp="%s" data-nombre="%s">+</button>'
               % (esc(e["nombre"]), esc(e["slug"]), esc(e["nombre"])))
    return (
        '<div class="eq " data-slug="%s">%s%s%s'
        '<div class="eq__in">%s<h3 class="eq__nombre">'
        '<a class="eq__link" href="/equipos/%s">%s</a></h3>%s</div></div>'
    ) % (esc(e["slug"]), cmp_btn, dest, img, marca,
         esc(e["slug"]), esc(e["nombre"]), esp)


def _faceta(clave, etiqueta, valores, abierta=False):
    filas = "".join(
        '<label data-valor="%s"><input type="checkbox" name="%s" value="%s">'
        '<span>%s</span><span class="n">%d</span></label>'
        % (esc(v["nombre"]), clave, esc(v["nombre"]), esc(v["nombre"]), v["total"])
        for v in valores)
    # role="group" + aria-labelledby y no <fieldset>: el fieldset trae su propio
    # box model y pelearía con el CSS de .faceta. La agrupación es lo que hace que
    # un lector de pantalla anuncie a qué eje pertenecen las casillas.
    #
    # El eje arranca plegado salvo Especialidad: con 72 tipos, abrir los tres de
    # golpe convierte el panel en un muro. La flecha y aria-expanded dicen que se
    # puede desplegar; el contenido plegado queda fuera del tabulador por el
    # visibility:hidden del CSS, no sólo con altura cero.
    return (
        '<div class="faceta" data-faceta="%s" data-abierta="%s" role="group" '
        'aria-labelledby="faceta-%s">'
        '<h3 class="faceta__cab"><button id="faceta-%s" type="button" '
        'aria-expanded="%s" aria-controls="faceta-%s-cuerpo">'
        '<svg class="faceta__flecha" viewBox="0 0 24 24" aria-hidden="true">'
        '<path d="m6 9 6 6 6-6"/></svg>%s'
        '<span class="faceta__n">%d</span></button></h3>'
        '<div class="faceta__cuerpo" id="faceta-%s-cuerpo">'
        '<div class="faceta__lista"><div>%s</div></div></div></div>'
    ) % (clave, "1" if abierta else "0", clave, clave,
         "true" if abierta else "false", clave, esc(etiqueta), len(valores),
         clave, filas)


def panel_facetas(catalogo):
    return ('<aside class="facetas">%s%s%s</aside>' % (
        _faceta("esp", "Especialidad", catalogo["especialidades"], abierta=True),
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
    # data-filtros es un atributo HTML delimitado con comillas simples: el JSON
    # (que trae comillas dobles) va sin tocar, pero esc() lo protege igual por si
    # algún texto o valor de filtro llegara a traer comillas simples o "&".
    chips = "".join(
        '<button class="chip" type="button" aria-pressed="false" '
        'data-filtros=\'%s\'>%s</button>'
        % (esc(json.dumps(c["filtros"], ensure_ascii=False)), esc(c["texto"]))
        for c in CHIPS)
    cuerpo = f"""
<main class="cat">
  <div class="cat__hero">
    <header class="cat__head">
      <h1 class="display-l cat__titulo">equipos que representamos</h1>
      <p class="cat__bajada">
        <strong id="conteo" aria-live="polite">{total}</strong> equipos de
        {len(catalogo["especialidades"])} especialidades y {len(catalogo["marcas"])} marcas.
        Buscá por nombre, por marca o por la técnica que necesitás resolver.
      </p>
      <div class="buscador">
        <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
        <label class="sr-only" for="q">Buscar equipos</label>
        <input id="q" type="search" autocomplete="off"
               placeholder="Buscá un equipo, una marca o una técnica…">
      </div>
      <div class="chips" id="chips">{chips}</div>
    </header>
  </div>
  <div class="cat__cuerpo">
    {panel_facetas(catalogo)}
    <div>
      <div class="rejilla" id="rejilla">{tarjetas}</div>
      <nav class="paginacion" id="paginacion" aria-label="Paginación del catálogo" hidden>
        <button type="button" id="pag-antes">← Anteriores</button>
        <span class="paginacion__estado" id="pag-estado" aria-live="polite"></span>
        <button type="button" id="pag-despues">Siguientes →</button>
      </nav>
      <div class="cat__vacio" id="vacio" hidden>
        <p>No encontramos equipos con esa búsqueda.</p>
        <p><a href="{wa_link("Hola, estoy buscando un equipo que no encontré en el catálogo:")}"
              target="_blank" rel="noopener">Contanos qué necesitás por WhatsApp →</a></p>
      </div>
    </div>
  </div>
  <div class="comparador" id="comparador" hidden
       role="region" aria-label="Equipos elegidos para comparar">
    <div class="comparador__lista" id="comparador-lista" aria-live="polite"></div>
    <a class="comparador__cta" id="comparador-cta" href="#" target="_blank" rel="noopener">Consultar los 3</a>
    <button class="comparador__limpiar" type="button" id="comparador-limpiar">Limpiar</button>
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

  var POR_PAGINA = 25;
  var pagina = 1;
  var barraPag = document.getElementById('paginacion');
  var estadoPag = document.getElementById('pag-estado');
  var antesPag = document.getElementById('pag-antes');
  var despuesPag = document.getElementById('pag-despues');

  function leerURL() {
    var p = new URLSearchParams(location.search);
    var lista = function (k) { return p.getAll(k).filter(Boolean); };
    return { q: p.get('q') || '', esp: lista('esp'), marca: lista('marca'), tipo: lista('tipo'),
      pagina: parseInt(p.get('pagina') || '1', 10) };
  }

  // 'replace' para la normalización inicial y para lo que ya vino del historial;
  // 'push' para cada cambio que hizo el usuario, que es lo que da atrás/adelante
  // (spec §8). Antes siempre reemplazaba, así que el listener de popstate de más
  // abajo no podía dispararse nunca desde la propia página.
  function escribirURL(f, modo) {
    var p = new URLSearchParams();
    if (f.q) p.set('q', f.q);
    ['esp', 'marca', 'tipo'].forEach(function (k) {
      f[k].forEach(function (v) { p.append(k, v); });
    });
    if (pagina > 1) p.set('pagina', pagina);
    var qs = p.toString();
    var url = qs ? '?' + qs : location.pathname;
    if (modo === 'push') {
      history.pushState(null, '', url);
    } else {
      history.replaceState(null, '', url);
    }
  }

  function leerCasillas() {
    var f = { q: input.value, esp: [], marca: [], tipo: [] };
    document.querySelectorAll('.faceta input:checked').forEach(function (c) {
      f[c.name].push(c.value);
    });
    return f;
  }

  function pintar(f, modo) {
    var visibles = buscar(EQUIPOS, f);
    var pag = paginar(visibles, pagina, POR_PAGINA);
    pagina = pag.pagina;
    var enPantalla = new Set(pag.slugs);
    // `--i` se fija ANTES de mostrar la tarjeta: la animación de entrada arranca
    // en el momento en que el elemento deja de estar `hidden`, y el retardo
    // escalonado tiene que estar puesto para entonces.
    var orden = 0;
    Object.keys(tarjetas).forEach(function (slug) {
      var el = tarjetas[slug];
      var visible = enPantalla.has(slug);
      if (visible) el.style.setProperty('--i', orden++);
      el.hidden = !visible;
    });

    conteo.textContent = visibles.length;
    vacio.hidden = visibles.length !== 0;
    rejilla.hidden = visibles.length === 0;
    barraPag.hidden = pag.paginas < 2;
    if (pag.paginas > 1) {
      var desde = (pag.pagina - 1) * POR_PAGINA + 1;
      var hasta = desde + pag.slugs.length - 1;
      estadoPag.textContent = desde + '–' + hasta + ' de ' + visibles.length;
      antesPag.disabled = pag.pagina === 1;
      despuesPag.disabled = pag.pagina === pag.paginas;
    }

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
    escribirURL(f, modo);
    sincronizarChips(f);
  }

  // Un chip se ve "puesto" solo mientras las casillas coinciden exactamente con
  // su combinación de filtros. Si el usuario destilda una a mano (o marca otra),
  // el chip deja de reclamar un estado que ya no es cierto.
  function sincronizarChips(f) {
    document.querySelectorAll('.chip').forEach(function (boton) {
      var filtros = JSON.parse(boton.dataset.filtros);
      var coincide = ['esp', 'marca', 'tipo'].every(function (eje) {
        var actual = f[eje] || [];
        var esperado = filtros[eje] || [];
        return actual.length === esperado.length &&
          esperado.every(function (v) { return actual.indexOf(v) !== -1; });
      });
      boton.setAttribute('aria-pressed', String(coincide));
    });
  }

  // Cambiar de filtro devuelve a la primera página: quedarse en la 7 después de
  // filtrar a 30 resultados desorienta.
  function pintarDesdeElPrincipio(f, modo) {
    pagina = 1;
    pintar(f, modo);
  }

  function irAPagina(n) {
    pagina = n;
    pintar(leerCasillas(), 'push');
    rejilla.scrollIntoView({ block: 'start', behavior: 'smooth' });
  }

  antesPag.addEventListener('click', function () { irAPagina(pagina - 1); });
  despuesPag.addEventListener('click', function () { irAPagina(pagina + 1); });

  // aplicar() pinta un estado que YA está en el historial (la carga inicial o un
  // atrás/adelante): normaliza la URL con replaceState y no agrega una entrada.
  function aplicar(f) {
    input.value = f.q;
    document.querySelectorAll('.faceta input').forEach(function (c) {
      c.checked = f[c.name].indexOf(c.value) !== -1;
    });
    pagina = f.pagina || 1;
    escribiendoTexto = false;
    clearTimeout(finRafaga);
    pintar(f, 'replace');
  }

  // Escribir crea UNA entrada de historial por ráfaga de tecleo, no una por
  // tecla: la primera pulsación después de una pausa empuja el estado anterior
  // al historial y el resto de la ráfaga reemplaza. Así "atrás" vuelve a la
  // búsqueda anterior y no letra por letra.
  var t, finRafaga, escribiendoTexto = false;
  input.addEventListener('input', function () {
    clearTimeout(t);
    t = setTimeout(function () {
      pintarDesdeElPrincipio(leerCasillas(), escribiendoTexto ? 'replace' : 'push');
      escribiendoTexto = true;
      clearTimeout(finRafaga);
      finRafaga = setTimeout(function () { escribiendoTexto = false; }, 1200);
    }, 120);
  });
  document.querySelectorAll('.faceta input').forEach(function (c) {
    c.addEventListener('change', function () {
      pintarDesdeElPrincipio(leerCasillas(), 'push');
    });
  });
  window.addEventListener('popstate', function () { aplicar(leerURL()); });

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
      // Un chip cambia el conjunto de filtros: como cualquier otro cambio de
      // filtro, vuelve a la página 1 (ver pintarDesdeElPrincipio más arriba).
      pintarDesdeElPrincipio(leerCasillas(), 'push');
    });
  });

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
    // Con tres elegidos, los botones no marcados quedan visualmente
    // deshabilitados (pero siguen enfocables, para que un lector de pantalla
    // pueda anunciar por qué no responden) hasta que baje de tres.
    var tope = elegidos.length === 3;
    document.querySelectorAll('.eq__cmp').forEach(function (b) {
      if (tope && b.getAttribute('aria-pressed') !== 'true') {
        b.setAttribute('aria-disabled', 'true');
      } else {
        b.removeAttribute('aria-disabled');
      }
    });
  }

  document.querySelectorAll('.eq__cmp').forEach(function (boton) {
    boton.addEventListener('click', function () {
      // El botón ya no vive dentro de un <a> (ver .eq__link): no hay
      // navegación ambiente que cancelar aquí.
      var slug = boton.dataset.cmp;
      var i = elegidos.findIndex(function (e) { return e.slug === slug; });
      if (i !== -1) {
        elegidos.splice(i, 1);
        boton.setAttribute('aria-pressed', 'false');
        boton.textContent = '+';
        boton.setAttribute('aria-label', 'Comparar ' + boton.dataset.nombre);
      } else {
        if (elegidos.length === 3) return;   // tres es el máximo legible
        elegidos.push({ slug: slug, nombre: boton.dataset.nombre });
        boton.setAttribute('aria-pressed', 'true');
        boton.textContent = '✓';
        boton.setAttribute('aria-label', 'Quitar ' + boton.dataset.nombre);
      }
      pintarComparador();
    });
  });

  document.getElementById('comparador-limpiar').addEventListener('click', function () {
    elegidos = [];
    document.querySelectorAll('.eq__cmp').forEach(function (b) {
      b.setAttribute('aria-pressed', 'false');
      b.textContent = '+';
      b.setAttribute('aria-label', 'Comparar ' + b.dataset.nombre);
    });
    pintarComparador();
  });

  document.querySelectorAll('.faceta__cab button').forEach(function (boton) {
    boton.addEventListener('click', function () {
      var panel = boton.closest('.faceta');
      var abierta = panel.dataset.abierta === '1';
      panel.dataset.abierta = abierta ? '0' : '1';
      boton.setAttribute('aria-expanded', abierta ? 'false' : 'true');
    });
  });

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
    with open(os.path.join(carpeta, "_cat.css"), "w", encoding="utf-8") as f:
        f.write(css_combinado())
    for viejo in os.listdir(carpeta):
        if viejo.endswith(".html"):
            os.remove(ruta_larga(os.path.join(carpeta, viejo)))
    for e in catalogo["equipos"]:
        ruta = ruta_larga(os.path.join(carpeta, "%s.html" % e["slug"]))
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(pagina_ficha(e, catalogo))

    print("generado public/equipos.html y %d fichas" % len(catalogo["equipos"]))


if __name__ == "__main__":
    main()
