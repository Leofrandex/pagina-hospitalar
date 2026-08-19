# Design System: Hospitalar

**Fuente de verdad:** `Manual Corporativo, Scalto (1).pdf` (Manual de marca Hospitalar, Octubre 2022 — Grupo Nueve Once)
**Assets web:** `public/brand/` (logo, formas, fuentes, imágenes)
**Rama:** `redesign`
**Estado:** v1 — tokens cerrados desde el manual. Las decisiones de *dirección visual* (layout, densidad, movimiento) se validan en el Mockup Lab antes de tocar `src/`.

---

## 0. Reglas de oro

1. **El manual manda.** Ningún color, tipografía o forma fuera de lo definido aquí.
2. **Una sola forma complementaria por composición.** Nunca combinar forma 1 + forma 2 + etc. en el mismo bloque visual (manual p.22).
3. **Violeta es la voz, naranja es el gesto.** El naranja nunca es fondo dominante: es acento, CTA y foco. El verde es terciario (educación, soporte, "vida").
4. **Nada de gradientes, sombras ni bordes sobre el logo** (manual p.18).
5. **Fotografía fría, bien iluminada, sensación de calma y tecnología** (manual p.35). Nada de stock cálido/sonriente genérico.

---

## 1. Visual Theme & Atmosphere

**Atmósfera:** *clínica-tecnológica, serena y densa en autoridad*. Aire generoso, superficies planas, geometría recortada. La marca no grita: se apoya. La "h" del logo representa al paciente sentado/apoyado sobre Hospitalar — esa idea de **soporte** debe leerse en la estructura de la página: bloques que sostienen contenido, no cajas flotando.

**Adjetivos guía:** Apoyado · Preciso · Frío-luminoso · Institucional · Recortado (die-cut) · Sin ruido.

**Anti-patrones:** glassmorphism, degradados morado→rosa, blobs orgánicos, cards con sombra difusa genérica, íconos con relleno degradado, hero con overlay negro al 50%, "AI slop" de landing SaaS.

**Personalidad de marca (manual p.5, p.8):**
| Atributo | Cómo se traduce en UI |
|---|---|
| **Servicial** | Jerarquía clarísima, CTAs siempre visibles, rutas cortas a "Cotizar" y "Servicio técnico" |
| **Profesional** | Grilla estricta, tipografía disciplinada, cero decoración gratuita |
| **Innovativo** | Recortes en la silueta de la "h", movimiento preciso, datos y tecnología visibles |

**Propuesta de valor (manual p.6):** *"Somos referencia del extraordinario servicio al cliente, conectando la tecnología a un mejor vivir."*
**Slogan:** **UNIMOS TECNOLOGÍA Y VIDA** (siempre en Syncopate; junto al logo va todo en Syncopate Bold — manual p.33).
**Golden Circle (p.7):** *Why* — creamos la conexión entre la vida y la magia de la tecnología. *How* — excelencia + espíritu de colaboración. *What* — ayudamos a profesionales que ayudan a otros.

---

## 2. Color Palette & Roles

### 2.1 Colores principales (manual p.12, p.21)

| Nombre descriptivo | HEX | RGB | CMYK | Pantone | Rol funcional |
|---|---|---|---|---|---|
| **Violeta Hospitalar** (Índigo profundo saturado) | `#352E87` | 30-34-170 | 97-95-0-0 | 2736 C | Color madre. Fondos de sección, encabezados, texto de titulares sobre blanco, footer, barra de navegación. |
| **Naranja Vital** (Naranja bermellón cálido) | `#F26A36` | 250-70-22 | 0-73-87-0 | 172 C | Acento único. CTA primario, subrayados, el "taco" del isotipo, indicadores activos, hover de foco. |
| **Verde Cuidado** (Verde esmeralda clínico) | `#009639` | 0-150-57 | 84-12-100-0 | 355 C | Terciario. Educación continua, soporte técnico, estados de éxito/disponibilidad, líneas de acento en fichas. |

### 2.2 Escala de tonos secundarios (manual p.21 — "restar 10/20/30 a cada valor CMYK")

Nivel 1 = color principal. Niveles 2–4 se usan para formas complementarias, fondos de bloque secundarios y capas de profundidad. **Valores muestreados del propio manual:**

| | Nivel 1 | Nivel 2 | Nivel 3 | Nivel 4 |
|---|---|---|---|---|
| **Violeta** | `#352E87` | `#473B90` | `#594E9C` | `#6C62A9` |
| **Naranja** | `#F26A36` | `#F08250` | `#F39969` | `#F6AF83` |
| **Verde** | `#009639` | `#3AAC54` | `#63B667` | `#84C17B` |

### 2.3 Neutros y extensiones de UI (no están en el manual — derivados, uso exclusivo digital)

| Token | HEX | Rol |
|---|---|---|
| `ink` | `#14113A` | Texto de máximo contraste sobre blanco (violeta desaturado y oscurecido; nunca negro puro). |
| `violeta-950` | `#1E1A4D` | Fondos ultra-oscuros, overlays de multiplicar, footer profundo. |
| `blanco` | `#FFFFFF` | Superficie base. |
| `hueso` | `#F6F5FA` | Fondo de sección alterna (violeta al ~3%). |
| `gris-100` | `#E8E7F0` | Bordes, divisores, líneas de grilla. |
| `gris-400` | `#8C89A6` | Texto secundario, labels, metadatos. |
| `gris-600` | `#565377` | Texto de cuerpo sobre hueso. |

**Escala de grises de marca (manual p.17):** solo para piezas que técnicamente no admiten color. En web no se usa como paleta, solo para el logo en versión monocromática.

### 2.4 Reglas de aplicación de color

- **Contraste mínimo AA:** cuerpo de texto ≥ 4.5:1, titulares ≥ 3:1. `#F26A36` sobre blanco **no** cumple para texto pequeño → el naranja se usa como **fondo de botón con texto blanco** (4.6:1) o en piezas ≥ 24px bold.
- **Sobre violeta:** texto blanco puro. Nunca naranja sobre violeta para texto de cuerpo.
- **Un solo naranja por pantalla visible.** Si hay dos CTAs naranjas compitiendo en el mismo viewport, uno baja a outline violeta.
- **Verde nunca como CTA primario.**

---

## 3. Typography Rules

### 3.1 Familias (manual p.30–34)

| Familia | Uso | Pesos disponibles | Archivo |
|---|---|---|---|
| **Syncopate** | Todos los títulos y frases destacadas. Slogan. | Regular, Bold | `public/brand/fonts/Syncopate-{Regular,Bold}.ttf` (también en Google Fonts) |
| **Myriad Pro / Myriad Variable Concept** | Textos secundarios y cuerpo. | Light, Regular, Semibold, Bold | `public/brand/fonts/MYRIADPRO-*.OTF` |

> **Nota de licencia:** Myriad Pro es Adobe y su *webfont embedding* requiere licencia de Adobe Fonts. Los OTF locales se usan en el Mockup Lab para fidelidad 1:1. Si no se resuelve licencia para producción, el sustituto aprobado es **Source Sans 3** (Adobe, open source, mismo linaje humanista, métricas muy cercanas). Decisión pendiente de confirmación con el cliente.

### 3.2 Carácter tipográfico

- **Syncopate** es extremadamente ancha y con tracking natural enorme. Por eso:
  - Nunca más de **6–8 palabras** en un titular.
  - Titulares en **minúsculas** para tono de marca (como el logo: `hospitalar`) o **MAYÚSCULAS** para etiquetas de sección cortas.
  - `letter-spacing` **negativo** en tamaños grandes (`-0.02em` a `-0.04em`) para que no se desarme; positivo (`+0.12em`) en eyebrow labels de 12px.
  - `line-height` apretado en display: `0.95`–`1.05`.
- **Myriad Light** para párrafos de introducción grandes (18–22px), **Regular** para cuerpo, **Semibold** para labels y datos, **Bold** solo para énfasis dentro de párrafo.

### 3.3 Escala tipográfica

| Token | Familia / peso | Tamaño (desktop → mobile) | LH | Tracking | Uso |
|---|---|---|---|---|---|
| `display-xl` | Syncopate Bold | 76 → 34 px | 0.95 | -0.035em | Titular de hero |
| `display-l` | Syncopate Bold | 56 → 28 px | 1.0 | -0.03em | Apertura de sección |
| `display-m` | Syncopate Bold | 36 → 24 px | 1.05 | -0.02em | Titular de bloque |
| `title-s` | Syncopate Regular | 22 → 19 px | 1.15 | -0.01em | Título de card |
| `eyebrow` | Syncopate Bold | 12 px | 1.2 | +0.14em, UPPERCASE | Etiqueta de sección |
| `lead` | Myriad Light | 21 → 18 px | 1.5 | 0 | Párrafo de entrada |
| `body` | Myriad Regular | 17 → 16 px | 1.6 | 0 | Cuerpo |
| `body-s` | Myriad Regular | 15 px | 1.55 | 0 | Texto de apoyo, pie de foto |
| `label` | Myriad Semibold | 13 px | 1.3 | +0.04em | Botones, chips, tabs |
| `data` | Syncopate Bold | 44 → 32 px | 1 | -0.02em | Cifras (40 años, +N equipos) |

---

## 3.4 Contenido real verificado (fuente: hospitalarve.com, leído el 18/08/2026)

Datos que corrigen lo que se había asumido en los primeros mockups:

- **La empresa opera desde 1982** → **43 años**, no 40.
- **Las 12 especialidades reales** son: Diagnóstico por Imagen · Ginecología y Obstetricia · Cardiología · Dermoestética · Cirugía · Gastroenterología · Anestesia · ORL · Emergencia · Esterilización · Neonatología · Urología.
- **Los cuatro servicios** son: Proyectos especiales · Actualización de equipos médicos · Hospitales llave en mano · Educación continua.
- **Contacto:** contigo@hospitalarve.com · +58 424 194 1573. Sedes: Caracas (Av. Francisco de Miranda, Centro Seguros La Paz, piso 7, local O-71), Barquisimeto (Av. Los Abogados), Maturín (Av. Andrés Eloy Blanco, Centro Profesional Cristina, piso 2, of. C05).
- **8 reseñas reales con nombre, cargo e institución** (Dra. Cristina Premerl, Dr. Víctor Ollarves, Samir Camacho, Dra. Gisela, Lic. Charlo Andrade, Ing. Carmen Barrios, Dra. Paola Bravo, Dra. Gusberly Zambrano). Se usan las ocho, completas, en la sección "Clientes".

> ⚠️ El sitio actual muestra un bloque *"Based on 4,500+ reviews · Trusted Score 4.8/5.0"* que **no se reproduce** en el rediseño: parece texto de plantilla y no hay fuente que lo respalde. Si el cliente puede acreditarlo (Google Business, encuestas propias), se incorpora; mientras tanto queda fuera.

---

## 4. Logo

**Versiones (manual p.11):** principal (`hospitalar`), con slogan, sintetizada (isotipo "h").
**Archivos web:**
- `public/brand/logo/hospitalar-cp.svg` — vectorial, color positivo (violeta + taco naranja). **Uso por defecto.**
- `public/brand/logo/hospitalar-neg.svg` — negativo (blanco), para fondos violeta/foto.
- `public/brand/logo/hospitalar-slogan-cp.svg` — con slogan, para footer y piezas de cierre.
- `public/brand/logo/isotipo-cp.png` — "h" sintetizada: favicon, avatar, loader, marca de agua.

**Reglas duras:**
- **Área de protección** = altura de la "O" del logotipo alrededor de todo el logo. Mínima permitida = la mitad (solo espacios muy reducidos). En web: `padding` equivalente reservado en header y footer; nada de texto o borde entrando en esa zona.
- **Tamaño mínimo:** versión principal y con slogan **≥ 115 px** de ancho; versión sintetizada **≥ 21 px**.
- Jamás encerrar el logo en un recuadro, ni inclinarlo, deformarlo, recolorearlo, contornearlo, sombrearlo, degradarlo, recrear su tipografía ni modificar la "h" (manual p.18).
- Sobre fotografía: si el fondo compromete la lectura, usar el **contenedor** de la "h" (§5.3), no un rectángulo semitransparente genérico.

---

## 5. Sistema gráfico

### 5.1 Formas complementarias (manual p.22–26)

Cuatro formas derivadas de la silueta de la "h". **Solo una por composición.**

| Forma | Espacio | Archivo | Reglas |
|---|---|---|---|
| **Forma 1** | Reducido / sintetizado | `public/brand/formas/Hospitalar_forma1.png` | Un color principal o un tono secundario. El **lateral recto siempre pegado al borde** del espacio (sangrado). Se puede voltear H/V, rotar 90°, duplicar, tocar o no el borde. **No** alargar ni recortar su extensión. **No** mezclar dos orientaciones en un mismo formato. |
| **Forma 2** | Horizontal alargado | `Hospitalar_forma2.png` | Voltear H/V manteniendo la posición indicada; rotar 90° para espacios altos. **No** rotar a ángulos distintos de 90°, no alargar/recortar, no reordenar. |
| **Forma 3** | Cuadrado | `Hospitalar_forma3.png` | Dos grupos de color (1 y 2): dos colores, o tonos secundarios de dos colores. Voltear H/V; **no rotar**. |
| **Forma 4** | Rectangular amplio | `Hospitalar_forma4.png` | Grupo 1 y 2 en primarios distintos, grupo 3 en tres tonos de un color. **Siempre a la izquierda** del espacio, solo se voltea verticalmente. No rotar, no posicionar a la derecha. Las puntas derechas se alargan todas juntas. |

En web las formas son **elementos de sangrado de sección** (bleed), no decoración interior, y se implementan como **máscara CSS**: el PNG aporta la silueta y el color sale de los tokens.

```css
.forma{ -webkit-mask-image:url("/brand/formas/Hospitalar_forma1.png"); mask-image:url(...);
        mask-size:contain; mask-repeat:no-repeat; background-color:var(--forma-color); }
```

Así una misma forma sirve en cualquier color principal o tono secundario sin generar un archivo por color, y sobre violeta puede ir en blanco o en tono nivel 4 como pide la p.28. Para el **Fondo 2** del manual se sustituye el `background-color` por la propia fotografía (`background-image` + `background-size:cover`): la foto queda literalmente dentro de la forma.

### 5.2 Fondos aprobados (manual p.28–29)

| Fondo | Receta exacta |
|---|---|
| **Fondo 1** | Imagen + capa del color principal al **60% de opacidad**. La forma va en el mismo color o un tono secundario. A la derecha de la figura la foto puede ir **sin** filtro de color. |
| **Fondo 2** | Imagen + color principal en modo **multiplicar**. Se **duplica la imagen dentro de una de las formas**; la otra forma va en un tono secundario. |
| **Fondo unicolor con formas** | Fondo blanco/claro; figuras en tonos 2, 3 y 4 de uno de los tres colores principales. |
| **Fondo violeta con formas** | Fondo violeta; formas en blanco + tonos del nivel 4, o en tres tonos de un color. Logo en positivo/blanco. |

Reglas de la p.28: sobre violeta, las formas van en blanco o tonos del nivel 4; los textos sobre violeta siempre en blanco; naranja o verde plenos solo detrás de **textos**, no de bloques enteros.

### 5.3 Contenedor (manual p.27)

Contenedor extraído del elemento característico de la "h". Se usa para garantizar lectura de logo o texto sobre fondos no unicolores.
- Siempre **sangrado** por el lateral derecho o izquierdo; la parte recta hacia el margen.
- Se puede voltear horizontalmente. **Nunca** alterar su forma.
- En web: es el patrón para etiquetas sobre foto, quotes de testimonial y badges de hero.

### 5.4 Estilo fotográfico (manual p.35–39)

Cuatro estilos, todos **bien iluminados, tonos fríos, sensación de calma y tecnología**:
1. **Tecnológicas** — elementos digitales combinados con medicina (`img/tech-abstract.webp`, `img/lab-biotech.webp`).
2. **Silueteadas** — médicos recortados en su silueta, colocados sobre un fondo del sistema (`img/silueta-2.png`, `silueta-3.png`, `silueta-4.png`).
3. **Cercanas** — manos de pacientes y/o doctores (`img/manos.webp`, `img/manos-estetoscopio.webp`, `img/estetoscopio-mano.webp`, `img/enfermera-corazon.webp`).
4. **Con equipos médicos** — producto en contexto (`img/equipo-medico.webp`, `img/quirofano.webp`, `img/doctor-paciente.webp`).

Tratamiento web: `object-fit: cover`, sin viñeteado negro; el oscurecimiento se hace **siempre** con violeta (60% u overlay multiply), nunca con negro.

---

## 6. Component Stylings

### 6.1 Geometría y forma

**Decisión del cliente (18/08/2026): fuera los vértices a 90°.** El recorte sigue siendo el gesto de marca (lo aportan las formas y las máscaras), pero las superficies de UI van redondeadas.

| Token | Valor | Uso |
|---|---|---|
| `--r-xs` | 8px | Elementos menores, marcas de acento |
| `--r-sm` | 12px | **Botones** e inputs |
| `--r-md` | 18px | **Cards, tiles, tarjetas de reseña** |
| `--r-lg` | 26px | Media y contenedores de imagen |
| `--r-xl` | 34px | Redondeo de bloque completo (hero, CTA) |

- Los **chips** son píldora (`999px`); los botones **no** (píldora completa en botón queda fuera).
- El radio nunca se aplica a las formas complementarias: su silueta la define el manual.

### 6.2 Profundidad y elevación

**Sistema plano, sin bordes y sin sombras. Decisión del cliente (18/08/2026): nada de recuadros con línea de 1px.**
La separación se hace con **superficie** (blanco sobre `hueso`, `hueso` sobre blanco, violeta sobre violeta-950), **aire** y **recorte**. Un borde visible solo se admite si es un elemento de marca (barra de acento de 3px), nunca un contorno completo.
- `elev-0` — plano sobre `hueso`, **sin borde**. Estado por defecto de cards.
- `elev-1` — sombra apenas perceptible: `0 1px 2px rgba(20,17,58,.06)`. Solo dropdowns y elementos que se levantan al hover.
- `elev-2` — `0 12px 32px rgba(20,17,58,.12)`. Exclusivo de menús flotantes y modales.
- Prohibido: sombras coloreadas, glow, `box-shadow` difuso en cards estáticas.

### 6.3 Componentes

**Botón primario** — fondo `#F26A36`, texto blanco `label`, esquinas rectas, sin sombra. Hover: fondo `#D95A2A` (naranja -8% luz) + desplazamiento del ícono 2px a la derecha. Focus: outline `2px #352E87` con `offset 2px`. Disabled: `gris-100` con texto `gris-400`.

**Botón secundario** — outline `1.5px #352E87`, texto violeta, fondo transparente. Hover: fondo violeta, texto blanco.

**Botón sobre fondo violeta/foto** — outline blanco `1.5px`, texto blanco. Hover: fondo blanco, texto violeta.

**Botón terciario / link** — texto violeta `label` con subrayado naranja de `2px` que se extiende de 0 → 100% al hover.

**Cards / contenedores** — esquinas rectas, superficie `hueso` sobre blanco (o blanco sobre `hueso`), **sin borde ni sombra**, separadas por un gap de 14px que dibuja la retícula por sí solo. Acento de identidad: **barra de 3px** en el borde superior o izquierdo (naranja para comercial, verde para servicio/educación, violeta para institucional). Hover: el borde pasa a violeta y la barra crece a 5px.

**Cards de especialidad** — ícono lineal `1.5px` violeta, título `title-s`, sin descripción en grilla densa. Al hover, el ícono pasa a naranja.

**Inputs / formularios** — sin caja: **línea inferior** `1.5px gris-100` sobre fondo transparente, label flotante en `label`/`gris-400`, foco → línea `#352E87` + label violeta. Error → línea y mensaje en `#F26A36`. Los buscadores sí llevan caja rectangular con borde `1px` e ícono lupa violeta.

**Navegación** — barra blanca, logo a la izquierda con área de protección respetada, links en `label` violeta, item activo con subrayado naranja de 2px. CTA "COTIZAR" como botón primario. En scroll: la barra se compacta y gana borde inferior `1px gris-100` (sin sombra).

**Badges / chips** — rectángulo recto, `label` 12px, fondo tono nivel 4 del color correspondiente, texto en nivel 1.

**Marquee de marcas** — los logos de representadas que tenemos (`public/logos/`) son **knockouts blancos**: solo funcionan sobre fondo oscuro. Para secciones claras se usa la versión invertida generada en `public/brand/logos-dark/`. En ambos casos: escala de grises al ~50% de opacidad, a color y 100% al hover. Pendiente: pedir al cliente los logos originales a color/vector.

**Testimonial** — usa el **contenedor** de la "h" sangrado por un lateral, texto en `lead` blanco sobre violeta, atribución en `label`.

---

## 7. Layout Principles

- **Grilla:** 12 columnas, `gutter 24px`, contenedor máximo **1280px**, márgenes laterales `clamp(20px, 5vw, 80px)`. Bloques de sangrado (formas, fotos) rompen el contenedor hasta el borde del viewport.
- **Escala de espaciado (base 4):** 4 · 8 · 12 · 16 · 24 · 32 · 48 · 64 · 96 · 128 · 160.
- **Ritmo vertical de sección:** `96px` móvil → `160px` desktop. El aire es la mitad del diseño; los bloques densos (grilla de especialidades, marcas) se compensan con secciones muy abiertas.
- **Alineación:** todo a la izquierda. Texto centrado solo en cierres de página de una sola columna.
- **Medida de línea:** 60–75 caracteres para `body`; 45–55 para `lead`.
- **Asimetría intencional:** los bloques de contenido se apoyan sobre una forma sangrada de un lado — reflejo literal de la "h" (paciente apoyado). Nunca composiciones perfectamente simétricas y centradas.
- **Breakpoints:** 480 / 768 / 1024 / 1280 / 1536.

### 7.1 Textura de fondo

El fondo plano se sentía vacío. Se resuelve con una capa fija `.bgfx` detrás de todo el contenido, compuesta por tres piezas y nada más:

1. **Tres halos radiales** muy abiertos en violeta nivel 3/4 y un tercero de naranja al 10% — dan profundidad y temperatura sin leerse como degradado.
2. **Trama de puntos** de 1px cada 22px, al 4-5% de opacidad: da materia y refuerza la idea de instrumento de precisión.
3. **Formas del manual** como marca de agua dentro de cada bloque (tarjetas de servicio, reseñas destacadas), al 12-20%, con parallax de resorte en el hero.

Regla: la textura nunca compite con el texto. Si un halo cae detrás de un párrafo, se mueve el halo.

---

## 8. Movimiento

Motion como precisión clínica, no como espectáculo. (Skills de referencia: `emil-design-eng`, `animate`, `animation-vocabulary`.)

- **Duraciones:** micro-interacción 120–180ms; entrada de elemento 320–420ms; transición de sección 480ms máximo.
- **Easing:** `cubic-bezier(0.23, 1, 0.32, 1)` (ease-out fuerte) para entradas y hovers con desplazamiento; `cubic-bezier(0.4, 0, 0.2, 1)` para cambios de color; `cubic-bezier(0.77, 0, 0.175, 1)` para movimiento en pantalla. Nunca `ease-in` en UI: retrasa justo el instante que el usuario está mirando.
- **Sólo `transform` y `opacity`.** Nunca animar `width`, `height`, `padding` ni `margin`: un subrayado se anima con `scaleX` y origen a la izquierda, una barra de acento con `scaleX`/`scaleY`, un desplazamiento de fila con `translateX` sobre los hijos.
- **Feedback de pulsación:** todo elemento presionable baja a `scale(.97)` en `:active` con 140ms.
- **Nada entra desde `scale(0)`.** Si hay escala de entrada, arranca en `.95` con `opacity 0`.
- **Hovers detrás de `@media (hover:hover) and (pointer:fine)`** para que el táctil no dispare estados falsos.
- **Transiciones, no keyframes**, en todo lo que se pueda interrumpir (el marquee es la excepción legítima: movimiento constante y lineal).
- **Entrada por scroll:** desplazamiento de `16px` + `opacity 0→1`, escalonado `60ms` por hijo. Nunca escala ni rotación al entrar.
- **Formas complementarias:** parallax vertical máximo `40px` a lo largo de toda la sección.
- **Prohibido:** rebotes, spring exagerado, contadores animados chillones, texto letra por letra, autoplay de carruseles > 6s sin control.
- **`prefers-reduced-motion`:** todas las animaciones de scroll y parallax se desactivan; solo quedan cambios de color de 120ms.

---

## 9. Tokens (implementación Tailwind v4 — `@theme` en `globals.css`)

```css
@theme {
  /* Marca */
  --color-violeta:      #352E87;  --color-violeta-2:  #473B90;
  --color-violeta-3:    #594E9C;  --color-violeta-4:  #6C62A9;
  --color-violeta-950:  #1E1A4D;
  --color-naranja:      #F26A36;  --color-naranja-2:  #F08250;
  --color-naranja-3:    #F39969;  --color-naranja-4:  #F6AF83;
  --color-naranja-dark: #D95A2A;
  --color-verde:        #009639;  --color-verde-2:    #3AAC54;
  --color-verde-3:      #63B667;  --color-verde-4:    #84C17B;

  /* Neutros */
  --color-ink:      #14113A;  --color-hueso:    #F6F5FA;
  --color-gris-100: #E8E7F0;  --color-gris-400: #8C89A6;
  --color-gris-600: #565377;

  /* Tipografía */
  --font-display: "Syncopate", "Arial Black", sans-serif;
  --font-body:    "Myriad Pro", "Source Sans 3", system-ui, sans-serif;

  /* Radio y elevación */
  --radius-none: 0;   --radius-xs: 4px;
  --shadow-elev-1: 0 1px 2px rgba(20,17,58,.06);
  --shadow-elev-2: 0 12px 32px rgba(20,17,58,.12);

  /* Movimiento */
  --ease-brand: cubic-bezier(0.16, 1, 0.3, 1);
  --ease-hover: cubic-bezier(0.4, 0, 0.2, 1);
}
```

---

## 10. Inventario de assets

```
public/brand/
├── logo/     hospitalar-cp.svg · hospitalar-neg.svg · hospitalar-slogan-cp.svg
│             hospitalar-cp.png · hospitalar-neg.png · isotipo-cp.png
├── formas/   Hospitalar_forma1.png … forma4.png   (RGBA, ≤1600px)
├── fonts/    Syncopate-Regular.ttf · Syncopate-Bold.ttf
│             MyriadPro-Light.otf · MYRIADPRO-REGULAR.OTF · MYRIADPRO-SEMIBOLD.OTF · MYRIADPRO-BOLD.OTF
└── img/      tech-abstract · lab-biotech · quirofano · equipo-medico · doctor-paciente
             manos · manos-estetoscopio · estetoscopio-mano · enfermera-corazon · imagen  (.webp)
             silueta-2 · silueta-3 · silueta-4  (.png con alfa)
├── logos-dark/  versiones invertidas (oscuras) de public/logos/* para fondos claros
```
Originales sin tocar en `diseno/` (fuera del build). Fuente PDF de la marca en la raíz.

---

## 11. Dirección elegida — D · "Mezcla refinada"

Decisión del cliente el **18 de agosto de 2026**, sobre los mockups A/B/C:

| Bloque | Origen | Nota |
|---|---|---|
| Header | **C** | Oscuro, sticky, `backdrop-filter`, se compacta al hacer scroll |
| Hero | **A** | Violeta pleno, forma 1 sangrada arriba a la derecha, foto silueteada, fila de datos |
| Marcas | **carrusel automático** | Como el sitio actual: marquee infinito, pausa al hover, franja violeta-950 con los logos blancos originales |
| Especialidades | **B** | Grilla de tiles, ahora sin bordes; la última celda es el llamado al catálogo |
| Resto (ciclo, testimonial, CTA, footer) | **C** | Mundo oscuro violeta-950 |

Reglas nuevas que trae esta dirección y que rigen de aquí en adelante:
1. **Cero bordes de 1px** (ver §6.2).
2. **Los recursos visuales se usan de verdad**: formas como máscara recolorable, contenedor de la "h" en etiquetas y testimonial, Fondo 2 del manual en el testimonial.
3. **Sistema de movimiento explícito** (§8), con las curvas y reglas de Emil Kowalski.

Mockup: `public/mockups/d.html`.

---

## 12. Mockup Lab

Servidor dedicado, independiente del `next dev`, para revisar direcciones visuales **antes** de tocar `src/`.

```bash
python -m http.server 4321 --directory public     # o: npm run lab
```

| URL | Contenido |
|---|---|
| `http://127.0.0.1:4321/mockups/` | Índice: las 3 direcciones + swatches de color, escala tipográfica y las 4 formas |
| `…/mockups/a.html` | **A · Apoyo** — editorial institucional, fondo violeta con formas, foto silueteada |
| `…/mockups/b.html` | **B · Contenedor** — grilla suiza clara, Fondo 1 (foto + violeta 60%), buscador protagonista |
| `…/mockups/c.html` | **C · Sistema** — violeta profundo técnico, forma 4, índice de datos |
| `…/mockups/d.html` | **D · oscuro** — la dirección elegida (§11) |
| `…/mockups/d-light.html` | **D · claro** — mismas piezas sobre superficies claras |

Las dos variantes de D se generan desde `public/mockups/_d-body.html` + `public/mockups/_build-d.py` (`python public/mockups/_build-d.py`): comparten estructura y sólo cambian los tokens de superficie, así no se desincronizan mientras se decide cuál queda.

Los tres comparten `public/mockups/tokens.css`, que es la implementación literal de los tokens de §9. Cuando se elija dirección, ese archivo se traduce al `@theme` de Tailwind y los mockups quedan como referencia congelada.

---

## 13. Decisiones abiertas (se resuelven en el Mockup Lab, no en este documento)

1. ~~Dirección visual~~ — **resuelta**: dirección D (§11).
2. ~~Patrón de recorte de botón (`h-notch`)~~ — **descartado**: el cliente pidió esquinas redondeadas (§6.1).
2b. **Variante de superficie**: oscura (`d.html`) vs. clara (`d-light.html`) — pendiente de elegir.
3. ~~Vectorización de las formas~~ — **resuelta** con máscara CSS (§5.1); vectorizar a SVG queda como mejora opcional de nitidez.
4. **Licencia de Myriad Pro para web** vs. sustitución por Source Sans 3.
5. **Densidad de la grilla de especialidades** (12 ítems: 4×3 vs. 6×2 vs. lista indexada).
6. **Logos de representadas** — solo tenemos knockouts blancos; pedir originales.
7. **Modo oscuro** — el manual no lo contempla. Propuesta: no hacerlo; usar el fondo violeta del sistema como "modo oscuro" de marca.
