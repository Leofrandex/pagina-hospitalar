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
.marquee img{height:44px;width:auto;opacity:var(--logo-op);
  filter:var(--logo-filter);
  transition:opacity var(--dur-hover) var(--ease-hover),transform var(--dur-hover) var(--ease-out),filter var(--dur-hover) var(--ease-hover)}
@media (hover:hover) and (pointer:fine){.marquee img:hover{opacity:1;transform:scale(1.07);filter:none}}
@keyframes marquee{to{transform:translateX(-100%)}}
@media (prefers-reduced-motion:reduce){.marquee__track{animation:none}.marquee{overflow-x:auto}}

/* ---------- Especialidades ---------- */
.spec{background:var(--sec-1)}
.grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}
.cell{position:relative;background:var(--card);border-radius:var(--r-md);padding:28px 24px 24px;min-height:184px;
  display:flex;flex-direction:column;overflow:hidden;
  transition:background 200ms var(--ease-hover),transform 220ms var(--ease-out)}
.cell__bar{position:absolute;left:0;top:0;width:100%;height:3px;background:var(--naranja);
  transform:scaleX(0);transform-origin:left;transition:transform 260ms var(--ease-out)}
.cell__ico{width:26px;height:26px;stroke:var(--ico);stroke-width:1.5;fill:none;margin-bottom:auto;
  stroke-linecap:round;stroke-linejoin:round;
  transition:stroke 200ms var(--ease-hover),transform 260ms var(--ease-out)}
.cell h3{margin-top:26px;overflow-wrap:break-word;hyphens:manual;font-size:clamp(17px,1.35vw,20px)}
.cell p{margin-top:7px;font-size:13px;color:var(--tx-dim);font-weight:600;letter-spacing:.03em}
@media (hover:hover) and (pointer:fine){
  .cell:hover{background:var(--card-hover);transform:translateY(-3px)}
  .cell:hover .cell__bar{transform:scaleX(1)}
  .cell:hover .cell__ico{stroke:var(--naranja);transform:translateY(-2px)}
}
.specall{display:flex;align-items:center;justify-content:space-between;gap:24px;margin-top:14px;
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
.resenas{position:relative;background:var(--sec-1);overflow:hidden}
.resenas__fx{position:absolute;inset:0;z-index:0;pointer-events:none;background:var(--resenas-fx)}
.resenas > .wrap{position:relative;z-index:1}
.rlist{columns:3;column-gap:14px}
.rcard{margin:0 0 14px;break-inside:avoid;position:relative;overflow:hidden;
  background:var(--card);border-radius:var(--r-md);padding:clamp(24px,2.2vw,32px);
  transition:background 220ms var(--ease-hover),transform 240ms var(--ease-out)}
.rcard__mark{position:absolute;right:-16%;top:-22%;width:52%;aspect-ratio:1;--forma-color:var(--naranja);opacity:.12;
  transition:transform 520ms var(--ease-out)}
.rcard blockquote{margin:0;position:relative;font-size:16px;line-height:1.6;color:var(--tx)}
.rcard--wide blockquote{font-weight:300;font-size:clamp(17px,1.45vw,20px);line-height:1.5}
.rcard figcaption{margin-top:20px;position:relative;display:flex;flex-direction:column;gap:3px}
.rcard figcaption strong{font-weight:600;font-size:14.5px;letter-spacing:.02em}
.rcard figcaption span{font-size:13px;color:var(--tx-dim)}
.rcard figcaption::before{content:"";display:block;width:22px;height:2px;border-radius:2px;background:var(--naranja);margin-bottom:12px}
@media (hover:hover) and (pointer:fine){
  .rcard:hover{background:var(--card-hover);transform:translateY(-3px)}
  .rcard:hover .rcard__mark{transform:translate(-6%,6%) rotate(-3deg)}
}

/* ---------- CTA ---------- */
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

@media (max-width:1180px){.quad{grid-template-columns:repeat(2,1fr)}.rlist{columns:2}}
@media (max-width:1024px){.grid{grid-template-columns:repeat(2,1fr)}}
@media (max-width:900px){
  .nav__links{display:none}
  .hero__silwrap{display:none}
  .hero__meta{grid-template-columns:1fr 1fr}
  .rlist{columns:1}
  .cta__in,.foot__in{grid-template-columns:1fr}
  .marquee img{height:34px}
}
"""

DARK = r"""
:root{
  --page:var(--violeta-950);
  --tx:#fff; --tx-dim:rgba(255,255,255,.62);
  --sec-1:transparent; --sec-2:rgba(255,255,255,.035);
  --card:rgba(255,255,255,.055); --card-hover:rgba(255,255,255,.095); --card-2:rgba(255,255,255,.05);
  --ico:#fff;
  --nav-bg:rgba(30,26,77,.82); --nav-link:rgba(255,255,255,.7); --nav-link-on:#fff;
  --accent-eyebrow:var(--naranja-3);
  --hero-bg:var(--violeta); --hero-bg-solid:var(--violeta); --hero-tx:#fff; --hero-tx-dim:rgba(255,255,255,.85);
  --hero-em:var(--naranja-3); --hero-forma:var(--violeta-4); --hero-forma-op:.5;
  --hero-sil-op:.78; --hero-sil-blend:luminosity;
  --hero-fx:radial-gradient(60rem 40rem at 12% 108%, rgba(108,98,169,.55), transparent 70%);
  --ghost-line:rgba(255,255,255,.6); --ghost-tx:#fff;
  --marcas-bg:transparent; --logo-op:.72; --logo-filter:none;
  --glow-a:rgba(89,78,156,.55); --glow-b:rgba(53,46,135,.6); --glow-c:rgba(242,106,54,.10);
  --dots:radial-gradient(rgba(255,255,255,.045) 1px, transparent 1px);
  --resenas-fx:radial-gradient(44rem 30rem at 50% 0%, rgba(89,78,156,.35), transparent 70%);
}
"""

LIGHT = r"""
:root{
  --page:#fff;
  --tx:var(--ink); --tx-dim:var(--gris-600);
  --sec-1:transparent; --sec-2:var(--hueso);
  --card:var(--hueso); --card-hover:#EEECF7; --card-2:#fff;
  --ico:var(--violeta);
  --nav-bg:rgba(255,255,255,.88); --nav-link:var(--gris-600); --nav-link-on:var(--violeta);
  --accent-eyebrow:var(--naranja);
  --hero-bg:var(--hueso); --hero-bg-solid:var(--hueso); --hero-tx:var(--ink); --hero-tx-dim:var(--gris-600);
  --hero-em:var(--naranja); --hero-forma:var(--violeta-4); --hero-forma-op:.3;
  --hero-sil-op:1; --hero-sil-blend:normal;
  --hero-fx:radial-gradient(58rem 38rem at 8% 104%, rgba(108,98,169,.20), transparent 72%);
  --ghost-line:var(--violeta); --ghost-tx:var(--violeta);
  --marcas-bg:transparent; --logo-op:.55; --logo-filter:grayscale(1);
  --glow-a:rgba(108,98,169,.16); --glow-b:rgba(53,46,135,.10); --glow-c:rgba(242,106,54,.10);
  --dots:radial-gradient(rgba(53,46,135,.055) 1px, transparent 1px);
  --resenas-fx:radial-gradient(44rem 30rem at 50% 0%, rgba(108,98,169,.16), transparent 70%);
}
/* En claro el botón fantasma del hero invierte a violeta */
.btn--ghost:hover{background:var(--violeta);color:#fff}
/* El logotipo del nav va en positivo */
.nav__logo{filter:none}
"""

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

def page(title, theme_css, logo, logos_dir, labbar_current, note):
    b = body.replace("{{LOGO}}", logo).replace("{{L}}", logos_dir)
    bar = """
<nav class="labbar">
  <span>MOCKUP LAB</span>
  <a href="/mockups/">Índice</a>
  <a href="/mockups/a.html">A</a>
  <a href="/mockups/b.html">B</a>
  <a href="/mockups/c.html">C</a>
  <a href="/mockups/d.html"%s>D · oscuro</a>
  <a href="/mockups/d-light.html"%s>D · claro</a>
  <span class="sp">%s</span>
</nav>""" % (' aria-current="page"' if labbar_current == "d" else "",
             ' aria-current="page"' if labbar_current == "dl" else "", note)
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<link rel="icon" href="/brand/logo/isotipo-cp.png">
<link rel="stylesheet" href="/mockups/tokens.css">
<style>{theme_css}{COMMON}</style>
</head>
<body>
<div class="bgfx" aria-hidden="true"></div>
{b}
{bar}
<script>{SCRIPT}</script>
</body>
</html>
"""

open(os.path.join(HERE, "d.html"), "w", encoding="utf-8").write(
    page("Hospitalar · Dirección D — oscuro", DARK, "/brand/logo/hospitalar-neg.svg", "/logos", "d",
         "D oscuro · reseñas reales · marcas grandes · esquinas redondeadas"))

open(os.path.join(HERE, "d-light.html"), "w", encoding="utf-8").write(
    page("Hospitalar · Dirección D — claro", LIGHT, "/brand/logo/hospitalar-cp.svg", "/brand/logos-dark", "dl",
         "D claro · mismas piezas sobre superficies claras"))

print("generados d.html y d-light.html")
