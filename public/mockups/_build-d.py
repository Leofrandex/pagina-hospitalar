# Genera d.html (oscuro) y d-light.html (claro) desde _d-body.html.
# Las dos variantes comparten estructura y sólo cambian las superficies.
import io, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
body = open(os.path.join(HERE, "_d-body.html"), encoding="utf-8").read()

COMMON = r"""
/* ===== Dirección D — mezcla refinada =========================================
   · Sin vértices a 90°: todo con radio (tokens --r-*).
   · Sin bordes de 1px: superficie, aire y recorte.
   · Formas del manual como máscara recolorable.
   · Movimiento: curvas fuertes, <300ms, sólo transform/opacity.
   ============================================================================= */

body{background:var(--page);color:var(--tx)}
.sec-head{display:flex;justify-content:space-between;align-items:end;gap:32px;margin-bottom:44px;flex-wrap:wrap}

/* ---------- Textura de fondo: da vida sin ensuciar ---------- */
.bgfx{position:fixed;inset:0;z-index:0;pointer-events:none;
  background-image:
    radial-gradient(46rem 34rem at 82% -8%, var(--glow-a), transparent 70%),
    radial-gradient(38rem 30rem at 6% 42%, var(--glow-b), transparent 72%),
    radial-gradient(42rem 32rem at 92% 88%, var(--glow-c), transparent 70%),
    var(--dots);
  background-size:auto,auto,auto,22px 22px}
/* Las secciones se apilan sobre la textura; el header y la barra del Lab van más arriba. */
.hero,.marcas,.spec,.serv,.resenas,.cta,.foot{position:relative;z-index:1}

/* ---------- Header ---------- */
.nav{position:sticky;top:0;z-index:60;background:transparent;
  transition:background var(--dur-hover) var(--ease-hover)}
.nav.is-stuck{background:var(--nav-bg);backdrop-filter:blur(14px) saturate(1.2)}
.nav__in{max-width:var(--max);margin:0 auto;padding:20px var(--pad);display:flex;align-items:center;gap:40px;
  transition:padding 240ms var(--ease-out)}
.nav.is-stuck .nav__in{padding-block:13px}
.nav__logo{width:176px}
.nav__links{display:flex;gap:30px;margin-left:auto}
.nav__links a{position:relative;font-weight:600;font-size:13px;letter-spacing:.04em;color:var(--nav-link);
  padding-block:4px;transition:color var(--dur-hover) var(--ease-hover)}
.nav__links a::after{content:"";position:absolute;left:0;right:0;bottom:-4px;height:2px;border-radius:2px;
  background:var(--naranja);transform:scaleX(0);transform-origin:left;transition:transform 220ms var(--ease-out)}
@media (hover:hover) and (pointer:fine){.nav__links a:hover{color:var(--nav-link-on)}.nav__links a:hover::after{transform:scaleX(1)}}
.nav__links a.is-active{color:var(--nav-link-on)}
.nav__links a.is-active::after{transform:scaleX(1)}

/* ---------- Hero ---------- */
.hero{position:relative;background:var(--hero-bg);color:var(--hero-tx);overflow:hidden;
  margin-top:-84px;padding-top:84px;border-radius:0 0 var(--r-xl) var(--r-xl)}
.hero__fx{position:absolute;inset:0;z-index:0;pointer-events:none;background:var(--hero-fx)}
.hero__forma{position:absolute;z-index:1;right:-10%;top:-18%;width:min(62%,860px);aspect-ratio:1;
  --forma-color:var(--hero-forma);opacity:var(--hero-forma-op);will-change:transform}
.hero__silwrap{position:absolute;z-index:2;right:0;bottom:0;height:78%;overflow:hidden;
  border-radius:var(--r-xl) 0 0 0}
.hero__sil{height:100%;width:auto;
  -webkit-mask-image:linear-gradient(90deg,transparent,#000 56%),linear-gradient(180deg,transparent,#000 28%);
  mask-image:linear-gradient(90deg,transparent,#000 56%),linear-gradient(180deg,transparent,#000 28%);
  -webkit-mask-composite:source-in;mask-composite:intersect;
  opacity:var(--hero-sil-op);mix-blend-mode:var(--hero-sil-blend);pointer-events:none}
.hero__in{position:relative;z-index:3;max-width:var(--max);margin:0 auto;
  padding:clamp(64px,8vw,116px) var(--pad) clamp(56px,7vw,96px)}
.hero__eyebrow{color:var(--accent-eyebrow);margin-bottom:22px}
.hero h1{max-width:13ch;text-transform:lowercase;font-size:clamp(32px,4.9vw,62px);line-height:1;letter-spacing:-.035em}
.hero h1 em{font-style:normal;color:var(--hero-em)}
.hero .lead{margin-top:26px;max-width:42ch;color:var(--hero-tx-dim)}
.hero__cta{display:flex;flex-wrap:wrap;gap:14px;margin-top:38px}
.hero__meta{position:relative;z-index:3;max-width:var(--max);margin:0 auto;
  padding:0 var(--pad) clamp(56px,6vw,84px);display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:28px}
.hero__meta > div{max-width:280px}
.hero__meta .data{color:var(--hero-tx)}
.hero__meta span{display:block;margin-top:8px;font-size:13px;font-weight:600;letter-spacing:.04em;color:var(--hero-tx-dim)}
.hero__meta i{display:block;width:26px;height:3px;border-radius:2px;background:var(--naranja);margin-bottom:16px;
  transform:scaleX(0);transform-origin:left;transition:transform 420ms var(--ease-out)}
.hero__meta.is-in i{transform:scaleX(1)}
.btn--ghost{border:1.5px solid var(--ghost-line);color:var(--ghost-tx)}
.btn--ghost:hover{background:var(--ghost-tx);color:var(--hero-bg-solid)}

/* ---------- Marcas ---------- */
.marcas{background:var(--marcas-bg);padding:clamp(72px,7vw,104px) 0 clamp(64px,6vw,88px)}
.marcas__head{text-align:center;margin-bottom:clamp(40px,4vw,56px)}
.marcas__head h2{max-width:24ch;margin-inline:auto;font-size:clamp(26px,3.4vw,46px);line-height:1.02}
.marquee{display:flex;overflow:hidden;
  -webkit-mask-image:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent);
  mask-image:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent)}
.marquee__track{display:flex;flex:0 0 auto;align-items:center;gap:84px;padding-right:84px;
  animation:marquee 52s linear infinite}
.marquee:hover .marquee__track{animation-play-state:paused}
/* Cada logo enlaza al catalogo filtrado por esa marca (spec 7). El <a> es un
   item flex mas del track: display:flex para que no cambie ni el alto ni el
   gap respecto de cuando el <img> era hijo directo. */
.marquee a{display:flex;align-items:center;flex:0 0 auto}
.marquee a:focus-visible{outline:2px solid var(--naranja);outline-offset:6px;border-radius:4px}
.marquee a:focus-visible img{opacity:1;filter:none}
.marquee img{height:44px;width:auto;opacity:var(--logo-op);
  filter:var(--logo-filter);
  transition:opacity var(--dur-hover) var(--ease-hover),transform var(--dur-hover) var(--ease-out),filter var(--dur-hover) var(--ease-hover)}
@media (hover:hover) and (pointer:fine){.marquee img:hover{opacity:1;transform:scale(1.07);filter:none}}
@keyframes marquee{to{transform:translateX(-100%)}}
@media (prefers-reduced-motion:reduce){.marquee__track{animation:none}.marquee{overflow-x:auto}}

/* ---------- Especialidades ---------- */
.spec{background:var(--sec-1)}
/* 13 celdas + el banner ocupando el resto de la última fila = 4 filas exactas. */
.grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}
.cell{position:relative;background:var(--card);border-radius:var(--r-md);padding:28px 24px 24px;min-height:184px;
  display:flex;flex-direction:column;overflow:hidden;
  transition:background 200ms var(--ease-hover),transform 220ms var(--ease-out)}
.cell__face{display:flex;flex-direction:column;flex:1}
/* Los cuatro productos entran desde abajo; sólo transform, por debajo de 300ms. */
.cell__prods{position:absolute;inset:0;z-index:2;background:var(--violeta);color:#fff;
  padding:26px 24px;display:flex;flex-direction:column;justify-content:center;
  transform:translateY(101%);transition:transform 260ms var(--ease-out)}
.cell__prods strong{font-family:var(--display);font-weight:400;font-size:16px;letter-spacing:-.01em;
  margin-bottom:14px}
.cell__prods li{font-size:13px;line-height:1.65;color:rgba(255,255,255,.72);font-weight:600;letter-spacing:.02em}
.cell__bar{position:absolute;left:0;top:0;width:100%;height:3px;background:var(--naranja);
  transform:scaleX(0);transform-origin:left;transition:transform 260ms var(--ease-out)}
.cell__ico{width:26px;height:26px;stroke:var(--ico);stroke-width:1.5;fill:none;margin-bottom:auto;
  stroke-linecap:round;stroke-linejoin:round;
  transition:stroke 200ms var(--ease-hover),transform 260ms var(--ease-out)}
/* Nombres largos como "Gastroenterología" no entran en una línea: que corten
   con guion en sílaba y no a mitad de palabra. */
/* Escala calibrada para que los 13 nombres entren en una sola línea: el más
   ancho ("Gastroenterología") mide 216 de los 223px útiles de la tarjeta. */
.cell h3{margin-top:26px;white-space:nowrap;font-size:clamp(13px,1.02vw,16px)}
.cell p{margin-top:7px;font-size:13px;color:var(--tx-dim);font-weight:600;letter-spacing:.03em}
@media (hover:hover) and (pointer:fine){
  .cell:hover{background:var(--card-hover);transform:translateY(-3px)}
  .cell:hover .cell__bar{transform:scaleX(1)}
  .cell:hover .cell__ico{stroke:var(--naranja);transform:translateY(-2px)}
  .cell:hover .cell__prods{transform:translateY(0)}
}
/* Sin hover (táctil) los productos se muestran fijos abajo, no ocultos. */
@media not all and (hover:hover){
  .cell__prods{position:static;transform:none;background:none;color:inherit;padding:16px 0 0}
  .cell__prods strong{display:none}
  .cell__prods li{color:var(--tx-dim)}
  .cell__face p{display:none}
}
@media (max-width:1080px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}.specall{grid-column:span 1}}
@media (max-width:640px){.grid{grid-template-columns:1fr}.specall{grid-column:span 1}}
.specall{grid-column:span 3;display:flex;align-items:center;justify-content:space-between;gap:24px;
  background:var(--violeta);color:#fff;border-radius:var(--r-md);padding:26px 30px;
  transition:background 200ms var(--ease-hover)}
.specall strong{display:block;font-family:var(--display);font-weight:400;font-size:19px;letter-spacing:-.01em}
.specall small{display:block;margin-top:6px;font-size:13.5px;color:rgba(255,255,255,.68)}
.specall .arw{font-size:22px;transition:transform var(--dur-hover) var(--ease-out)}
@media (hover:hover) and (pointer:fine){.specall:hover{background:var(--violeta-2)}.specall:hover .arw{transform:translateX(5px)}}

/* ---------- Ciclo completo ---------- */
.serv{background:var(--sec-2);padding-top:clamp(72px,7vw,110px)}
.quad{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}
.tcard{position:relative;background:var(--card-2);border-radius:var(--r-md);padding:clamp(26px,2.4vw,34px);overflow:hidden;
  transition:background 220ms var(--ease-hover),transform 240ms var(--ease-out)}
.tcard__forma{position:absolute;right:-20%;bottom:-30%;width:70%;aspect-ratio:1;--forma-color:var(--accent);
  opacity:.12;transition:transform 520ms var(--ease-out),opacity 300ms var(--ease-hover)}
.tcard__n{font-family:var(--display);font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--tx-dim);position:relative}
.tcard h3{margin:16px 0 12px;position:relative;font-size:clamp(20px,1.7vw,24px);line-height:1.1}
.tcard .body-s{position:relative;color:var(--tx-dim)}
@media (hover:hover) and (pointer:fine){
  .tcard:hover{transform:translateY(-3px)}
  .tcard:hover .tcard__forma{transform:translate(-8%,-8%) scale(1.08);opacity:.2}
}

/* ---------- Reseñas ---------- */
/* ---------- Soporte técnico: cierra la sección de servicios ---------- */
.soporte{margin-top:14px;background:var(--violeta);color:#fff;border-radius:var(--r-md);
  padding:clamp(26px,2.4vw,34px);display:grid;grid-template-columns:1.1fr 1fr;gap:28px;align-items:center}
.soporte h3{max-width:18ch;line-height:1.12}
.soporte .body-s{color:rgba(255,255,255,.74)}
@media (max-width:820px){.soporte{grid-template-columns:1fr;gap:16px}}

/* ---------- Botón de mapa por sede ---------- */
.foot__maps{display:inline-flex;align-items:center;gap:8px;margin-top:14px;
  padding:9px 15px;border-radius:999px;background:rgba(255,255,255,.09);
  font-size:12px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:#fff;
  transition:background var(--dur-hover) var(--ease-hover),transform 200ms var(--ease-out)}
.foot__maps svg{width:14px;height:14px;stroke:currentColor;stroke-width:1.6;fill:none}
@media (hover:hover) and (pointer:fine){
  .foot__maps:hover{background:var(--naranja);transform:translateY(-2px)}
}

.resenas{position:relative;background:var(--sec-1);overflow:hidden}
.resenas__fx{position:absolute;inset:0;z-index:0;pointer-events:none;background:var(--resenas-fx)}
.resenas > .wrap{position:relative;z-index:1}
/* ---------- CTA ---------- */
/* ---------- Blog ---------- */
.blog{background:var(--sec-1)}
.posts{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}
.post{display:flex;flex-direction:column;background:var(--card);border-radius:var(--r-md);overflow:hidden;
  transition:background 200ms var(--ease-hover),transform 220ms var(--ease-out)}
.post__img{aspect-ratio:16/10;width:100%;object-fit:cover;background:var(--card-hover)}
.post__in{padding:24px;display:flex;flex-direction:column;flex:1}
.post__meta{font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--tx-dim);font-weight:700}
.post h3{margin:14px 0 10px;font-size:clamp(17px,1.3vw,20px);line-height:1.18;text-wrap:balance}
.post p{font-size:14px;line-height:1.6;color:var(--tx-dim)}
.post__go{margin-top:auto;padding-top:18px;font-size:12px;font-weight:700;letter-spacing:.06em;
  text-transform:uppercase;color:var(--naranja);display:flex;align-items:center;gap:8px}
.post__go .arw{transition:transform var(--dur-hover) var(--ease-out)}
@media (hover:hover) and (pointer:fine){
  .post:hover{background:var(--card-hover);transform:translateY(-3px)}
  .post:hover .post__go .arw{transform:translateX(5px)}
}
@media (max-width:900px){.posts{grid-template-columns:1fr}}

.cta{position:relative;overflow:hidden;background:var(--violeta-950);isolation:isolate;
  border-radius:var(--r-xl) var(--r-xl) 0 0;color:#fff}
.cta__img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.42;
  filter:saturate(.45) brightness(.62);mix-blend-mode:multiply}
.cta::after{content:"";position:absolute;inset:0;z-index:1;pointer-events:none;
  background:linear-gradient(90deg,var(--violeta-950) 18%,rgba(30,26,77,.55) 58%,rgba(30,26,77,.15))}
.cta__forma{position:absolute;left:0;bottom:0;z-index:2;width:min(38%,480px);aspect-ratio:1.5;
  --forma-color:var(--violeta-3);opacity:.4;
  -webkit-mask-image:url("/brand/formas/Hospitalar_forma4.png");mask-image:url("/brand/formas/Hospitalar_forma4.png");
  -webkit-mask-size:contain;mask-size:contain;-webkit-mask-repeat:no-repeat;mask-repeat:no-repeat;
  background-color:var(--violeta-3)}
.cta__in{position:relative;z-index:3;max-width:var(--max);margin:0 auto;padding:clamp(80px,9vw,128px) var(--pad);
  display:grid;grid-template-columns:minmax(0,1fr) auto;gap:40px;align-items:end}
.cta h2{max-width:17ch;text-transform:lowercase}

/* ---------- Footer ---------- */
.foot{background:var(--violeta-950);color:#fff}
.foot__in{max-width:var(--max);margin:0 auto;padding:clamp(56px,6vw,88px) var(--pad) 34px;
  display:grid;grid-template-columns:minmax(0,3fr) repeat(3,minmax(0,2fr));gap:40px}
.foot h4{font-size:11.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--naranja-3);margin-bottom:14px}
.foot li{font-size:14.5px;line-height:1.8;color:rgba(255,255,255,.6)}
.foot__logo{width:210px;margin-bottom:18px}
.foot__bar div{max-width:var(--max);margin:0 auto;padding:18px var(--pad);display:flex;gap:22px;
  font-size:13px;color:rgba(255,255,255,.38)}

/* ---------- Entradas ---------- */
.rv{opacity:0;transform:translateY(14px);transition:opacity var(--dur-enter) var(--ease-out),transform var(--dur-enter) var(--ease-out)}
.rv.is-in{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){
  .rv{opacity:1;transform:none;transition:opacity 200ms linear}
  .hero__forma{transform:none!important}
  .hero__meta i{transform:scaleX(1)}
}


@media (max-width:1180px){.quad{grid-template-columns:repeat(2,1fr)}
  .bento{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:1024px){.grid{grid-template-columns:repeat(2,1fr)}}
@media (max-width:900px){
  .nav__links{display:none}
  .hero__silwrap{display:none}
  .hero__meta{grid-template-columns:1fr 1fr}
  .bento{grid-template-columns:1fr;grid-auto-rows:auto}
  .rcard--xl,.rcard--wide{grid-column:span 1}
  .cta__in,.foot__in{grid-template-columns:1fr}
  .marquee img{height:34px}
}
"""

TEMA = open(os.path.join(HERE, "_tema.css"), encoding="utf-8").read()

SCRIPT = r"""
const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

const io = new IntersectionObserver((es) => es.forEach(e => {
  if (!e.isIntersecting) return;
  e.target.classList.add('is-in');
  io.unobserve(e.target);
}), { threshold: .1, rootMargin: '0px 0px -5% 0px' });

document.querySelectorAll('.rv').forEach(el => {
  const sibs = [...(el.parentElement?.children || [])].filter(n => n.classList.contains('rv'));
  el.style.transitionDelay = Math.max(0, Math.min(sibs.indexOf(el), 5)) * 60 + 'ms';
  io.observe(el);
});

const nav = document.getElementById('nav');
addEventListener('scroll', () => nav.classList.toggle('is-stuck', scrollY > 12), { passive: true });

/* ---------- Tema: oscuro · claro · híbrido ---------- */
const root = document.documentElement;
const MODES = ['dark', 'light', 'hybrid'];
const LABEL = { dark: 'oscuro', light: 'claro', hybrid: 'híbrido' };
const sw = document.getElementById('tswitch');
const syncSwitch = () => {
  const m = root.dataset.theme;
  sw.dataset.mode = m;
  sw.setAttribute('aria-pressed', m === 'light' ? 'true' : 'false');
  sw.setAttribute('aria-label', 'Tema ' + LABEL[m] + '. Cambiar de tema');
  sw.title = 'Tema ' + LABEL[m];
};
syncSwitch();
sw.addEventListener('click', () => {
  root.dataset.theme = MODES[(MODES.indexOf(root.dataset.theme) + 1) % MODES.length];
  try { localStorage.setItem('hosp-theme', root.dataset.theme); } catch (e) {}
  syncSwitch();
});

/* ---------- Reseñas: revelar las restantes ---------- */
const bento = document.getElementById('bento');
const moreBtn = document.getElementById('rmore');
if (moreBtn) moreBtn.addEventListener('click', () => {
  bento.classList.add('is-open');
  moreBtn.setAttribute('aria-expanded', 'true');
  bento.querySelectorAll('.is-extra').forEach((el, i) => {
    el.style.opacity = 0; el.style.transform = 'translateY(10px)';
    el.style.transition = 'opacity 380ms var(--ease-out) ' + (i * 60) + 'ms, transform 380ms var(--ease-out) ' + (i * 60) + 'ms';
    requestAnimationFrame(() => { el.style.opacity = 1; el.style.transform = 'none'; });
  });
});

/* Parallax con resorte en la forma del hero: interpolado, no atado 1:1 al scroll */
if (!reduced) {
  const forma = document.getElementById('heroForma');
  let target = 0, current = 0, raf = null;
  const tick = () => {
    current += (target - current) * 0.08;
    forma.style.transform = `translate3d(0, ${current.toFixed(2)}px, 0)`;
    raf = Math.abs(target - current) > .1 ? requestAnimationFrame(tick) : null;
  };
  addEventListener('scroll', () => {
    target = Math.min(scrollY * 0.16, 90);
    if (!raf) raf = requestAnimationFrame(tick);
  }, { passive: true });
}
"""

import json
REVIEWS = json.load(open(os.path.join(HERE, "_reviews.json"), encoding="utf-8"))

# Los artículos se hornean al generar leyendo el WordPress actual. Si el origen
# no responde (suele ser lento), se usa la última copia guardada en _posts.json
# para no publicar una sección vacía.
import urllib.request, html as _html, datetime, re as _re2

POSTS_CACHE = os.path.join(HERE, "_posts.json")
WP = "https://hospitalarve.com/wp-json/wp/v2/posts?per_page=6&_embed=wp:featuredmedia,wp:term"

def _plain(t):
    t = _re2.sub(r"<[^>]*>", "", t or "")
    return _html.unescape(t).replace(" ", " ").strip()

def _fetch_posts():
    req = urllib.request.Request(WP, headers={"User-Agent": "hospitalar-build"})
    with urllib.request.urlopen(req, timeout=45) as r:
        raw = json.load(r)
    out = []
    for it in raw:
        title = _plain(it.get("title", {}).get("rendered", ""))
        if not title:
            continue
        media = (it.get("_embedded", {}).get("wp:featuredmedia") or [{}])[0]
        sizes = (media.get("media_details") or {}).get("sizes") or {}
        img = ""
        for k in ("medium_large", "fusion-800", "large", "medium"):
            if sizes.get(k, {}).get("source_url"):
                img = sizes[k]["source_url"]; break
        img = img or media.get("source_url", "")
        terms = [t for g in (it.get("_embedded", {}).get("wp:term") or []) for t in g]
        cat = next((t.get("name") for t in terms
                    if t.get("taxonomy") == "category" and t.get("name") not in (None, "Uncategorized")), "Artículo")
        out.append({"t": title, "u": "/blog/" + it.get("slug", ""), "img": img,
                    "cat": _plain(cat), "d": it.get("date", "")[:10],
                    "e": _plain(it.get("excerpt", {}).get("rendered", ""))})
        if len(out) == 3:
            break
    return out

try:
    POSTS = _fetch_posts()
    json.dump(POSTS, open(POSTS_CACHE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("artículos leídos de WordPress:", len(POSTS))
except Exception as e:
    POSTS = json.load(open(POSTS_CACHE, encoding="utf-8")) if os.path.exists(POSTS_CACHE) else []
    print("WordPress no respondió (%s); uso la caché: %d artículos" % (type(e).__name__, len(POSTS)))

_MESES = ["enero","febrero","marzo","abril","mayo","junio","julio",
          "agosto","septiembre","octubre","noviembre","diciembre"]

def _fecha(iso):
    try:
        d = datetime.date.fromisoformat(iso)
        return "%d de %s de %d" % (d.day, _MESES[d.month - 1], d.year)
    except Exception:
        return ""

def _post_card(p):
    img = ('<img class="post__img" src="%s" alt="" loading="lazy">' % _html.escape(p["img"], quote=True)) if p["img"] else '<div class="post__img"></div>'
    return ('<a class="post rv" href="%s">%s<div class="post__in">'
            '<span class="post__meta">%s · %s</span><h3>%s</h3><p>%s</p>'
            '<span class="post__go">Leer artículo <span class="arw">→</span></span>'
            '</div></a>') % (_html.escape(p["u"], quote=True), img,
                             _html.escape(p["cat"]), _fecha(p["d"]),
                             _html.escape(p["t"]), _html.escape(p["e"][:130]))

POSTS_HTML = "".join(_post_card(p) for p in POSTS)

LOGO = """<span class="logoswap nav__logo">
      <img class="is-pos" src="/brand/logo/hospitalar-cp.svg" alt="Hospitalar">
      <img class="is-neg" src="/brand/logo/hospitalar-neg.svg" alt="">
    </span>"""

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


def build(theme, note, current, site=False):
    """site=True genera la versión pública: sin barra del Lab y sin noindex."""
    b = (body.replace("{{POSTS}}", POSTS_HTML)
             .replace("{{ESPECIALIDADES}}", ESPECIALIDADES_HTML)
             .replace("{{LOGO}}", "")
             .replace('<img class="nav__logo" src="" alt="Hospitalar">', LOGO))
    import re as _re
    b = _re.sub(r'<img src="\{\{L\}\}/([^"]+)"([^>]*)>',
                lambda m: '<img class="is-white" src="/logos/%s"%s><img class="is-dark" src="/brand/logos-dark/%s"%s>'
                          % (m.group(1), m.group(2), m.group(1), m.group(2)), b)
    def mark(f, name):
        return ' aria-current="page"' if f == current else ''
    bar = "" if site else """
<nav class="labbar">
  <span>HOSPITALAR · REDISEÑO</span>
  <a href="/lab">Inicio</a>
  <a href="/lab/d"%s>Híbrido</a>
  <a href="/lab/d-dark"%s>Oscuro</a>
  <a href="/lab/d-light"%s>Claro</a>
  <span class="sp">%s</span>
</nav>""" % (mark("hybrid", current), mark("dark", current), mark("light", current), note)
    head_robots = ("" if site else
        '<meta name="robots" content="noindex, nofollow">')
    head_title = ("Hospitalar Venezuela | Unimos tecnología y vida" if site
                  else "Hospitalar · Dirección D — %s" % LABELS[theme])
    head_desc = ('<meta name="description" content="Equipamiento médico de clase mundial, '
                 'servicio técnico local y soluciones integrales para centros de salud en Venezuela. '
                 'Representamos a las marcas líderes desde 1982.">') if site else ""
    boot = """(function(){var t='%s';try{var v=localStorage.getItem('hosp-theme-page-%s');if(v)t=v}catch(e){}
document.documentElement.dataset.theme=t})();""" % (theme, theme)
    return f"""<!doctype html>
<html lang="es" data-theme="{theme}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
{head_robots}{head_desc}
<title>{head_title}</title>
<meta name="color-scheme" content="dark light">
<link rel="icon" href="/brand/logo/isotipo-cp.png">
<script>{boot}</script>
<link rel="stylesheet" href="/mockups/tokens.css">
<style>{TEMA}{COMMON}</style>
</head>
<body>
<div class="bgfx" aria-hidden="true"></div>
{b}
{bar}
<script>{SCRIPT}</script>
</body>
</html>
"""

LABELS = {"hybrid": "híbrido", "dark": "oscuro", "light": "claro"}

open(os.path.join(HERE, "d.html"), "w", encoding="utf-8").write(
    build("hybrid", "D híbrido · secciones claras y oscuras alternadas · reseñas en bento", "hybrid"))
open(os.path.join(HERE, "d-dark.html"), "w", encoding="utf-8").write(
    build("dark", "D oscuro · variante pura", "dark"))
open(os.path.join(HERE, "d-light.html"), "w", encoding="utf-8").write(
    build("light", "D claro · variante pura", "light"))

# Versión pública: el modo claro, servido en / (ver rewrite en next.config.ts).
open(os.path.join(HERE, "..", "site.html"), "w", encoding="utf-8").write(
    build("light", "", "light", site=True))
print("generados d.html (híbrido), d-dark.html, d-light.html y public/site.html")
