# Catálogo de equipos — diseño

**Fecha:** 2026-09-01
**Rama:** `redesign`
**Estado:** aprobado, pendiente de plan de implementación

---

## 1. Problema

El rediseño no tiene productos. El sitio actual (`hospitalarve.com`) sí: 215 equipos
desglosados por categoría. Falta traer ese inventario al sitio nuevo, con buscador, de
forma que un médico encuentre lo que necesita en segundos.

El desglose actual no se puede copiar tal cual. Tiene tres defectos de fondo:

1. **Mezcla dos taxonomías incomparables.** Las 49 categorías raíz ponen "Siemens" y
   "Cardiología" al mismo nivel, como si fueran la misma clase de cosa.
2. **Fragmenta los tipos de equipo.** "Ecógrafos" existe seis veces, con seis slugs
   distintos, uno por especialidad. No hay forma de ver todos los ecógrafos.
3. **Es una tienda que no vende.** Corre WooCommerce con carrito y checkout, pero
   **ningún producto tiene precio ni SKU** (verificado sobre los 215). El carrito es
   una función muerta que estorba.

## 2. Qué se construye

Una **vitrina de consulta**, no un e-commerce. El cliente ve el inventario, lee la
información del equipo y escribe por WhatsApp si le interesa. No hay carrito, ni
cuenta, ni checkout, ni precios.

## 3. Restricciones del proyecto

- **El rediseño es HTML estático, no React.** `/` está reescrito a `public/site.html`,
  que genera `public/mockups/_build-d.py` desde `_d-body.html` + `tokens.css`. La app
  de Next en `src/` es la versión anterior. El catálogo se construye en ese pipeline.
- **Los datos van congelados en el repo** (decisión del cliente). El WordPress viejo se
  usa como origen una sola vez, no como dependencia de runtime.
- **DESIGN.md manda** en color, tipografía y forma. La dirección visual se valida en el
  Mockup Lab (`/lab`) antes de promoverse.

## 4. Fuente de datos

WooCommerce expone su Store API **pública, sin autenticación**:

- `GET /wp-json/wc/store/v1/products` — 215 productos, 100% con imagen
- `GET /wp-json/wc/store/v1/products/categories` — 136 categorías

Campos útiles: `name`, `slug`, `permalink`, `short_description` (~950 caracteres),
`description`, `categories`, `images[]`. Campos inútiles: `prices` (todos en 0), `sku`
(todos vacíos), `brands` (taxonomía vacía), `add_to_cart`, `is_in_stock`.

## 5. Curaduría: tres ejes

Las 49 raíces se reparten con un **mapa explícito y versionado**, escrito a mano. No es
heurística: cada raíz se clasifica una vez y queda registrada.

### 5.1 Especialidad (18)

Diagnóstico por Imagen (62), Ginecología (43), Dermatología / Medicina Estética (41),
Otorrinolaringología (40), Cardiología (31), Cirugía (25), Anestesia (23),
Gastroenterología (19), Urología (17), Emergencia (14), Quirófano (9), Neurología (8),
Instrumental Médico (6), Esterilización (5), Cirugía Plástica (4), Mobiliario Médico (4),
Neonatología (3), Hospitalización (1).

El mapa además **corrige los nombres**: `Diagnostico-por-Imagen` → "Diagnóstico por
Imagen", `Dermatologia/Medicina-Estetica` → "Dermatología / Medicina Estética".

### 5.2 Marca (25)

Interacoustics (25), Siemens (22), Deka Laser (17), Sonoscape (15), Dräger (13),
Sony (13), Medtronic (9), Ebneuro (8), Hyun Laser (7), Mega Medical (7), Zoncare (7),
Inmode (6), Esaote (5), Canfield (4), Candela Medical (3), Hydrafacial (3),
Matachana (3), Barco (2), Olympus (2), UMF Medical (2), BMI (1), Cocoon Medical (1),
Echolight (1), Mobile ODT (1), Yonker (1).

36 productos no tienen marca identificable. No se les inventa una: el filtro de marca
simplemente no los incluye, y la ficha omite el dato.

### 5.3 Tipo de equipo (~74)

Las 87 subcategorías se normalizan colapsando los duplicados por especialidad. Siete
grupos se unifican:

| Tipo unificado | Absorbe |
|---|---|
| Ecógrafos | Ecógrafos ×3, Ecógrafos Emergencia, Ecógrafos Urología, Ecógrafos Para Anestesia |
| Monitores | Monitores, Monitores Anestesia, Monitores Cirugía, Monitores Hospitalización |
| Láser Quirúrgico | Láser Quirúrgico ×3 |
| Arcos en C | Arcos en C ×2 |
| Descartables | Descartables ×2 |
| Ginecoestética | Ginecoestética ×2 |
| Insumos | Insumos ×2 |

Este eje es el que más desbloquea: por primera vez se puede preguntar "todos los
ecógrafos" cruzando especialidades.

### 5.4 Ruido (6 raíces, no son filtros)

| Raíz | Qué se hace |
|---|---|
| `Destacado` (7) | Deja de ser categoría. Pasa a ser un campo booleano `destacado` en el equipo. |
| `Sin categorizar` (3) | Se reasignan a mano en el mapa. |
| `Covid` (1) | Se reasigna a Emergencia. |
| `Radiología Computarizada` (2), `Radiología Directa` (2) | Son tipos, no especialidades: pasan a tipo bajo Diagnóstico por Imagen. |
| `Estudios Óseos` (1) | Duplicada como raíz y como subcategoría. Se conserva sólo la subcategoría. |

Cualquier raíz futura sin mapear entra a un grupo "Otros" visible, para que se note que
falta curarla, sin romper el build.

## 6. Pipeline de datos

```
public/mockups/
  _catalogo-map.py     curaduría versionada: raíz -> especialidad|marca|oculta, renombres,
                       colapso de tipos, reasignaciones manuales
  _fetch-catalogo.py   se corre a mano. Lee la Store API, aplica el mapa, baja imágenes,
                       escribe _catalogo.json
  _catalogo.json       215 equipos ya curados. Commiteado. Fuente de verdad del sitio.
public/equipos/img/    imágenes vendorizadas
```

`_fetch-catalogo.py` es **deliberadamente manual**. No corre en el build. El catálogo del
sitio nuevo no depende de que el WordPress viejo siga en pie.

### 6.1 Imágenes

556 imágenes únicas, 67MB en original — demasiado para el repo. WordPress ya genera
variantes redimensionadas (66, 150, 200, 300, 500px), así que el script baja la de
**500px** para la imagen principal de cada equipo, que sirve tanto a la tarjeta del grid
como a la ficha.

Estimado: 8–12MB. Si excede, el script re-encoda a WebP.

Las imágenes de galería (2ª en adelante, 341 archivos) quedan **fuera del alcance de
esta entrega**: cada equipo muestra una sola imagen. Se puede ampliar después.

## 7. Rutas

| Ruta | Archivo | Qué es |
|---|---|---|
| `/equipos` | `public/equipos.html` | La vitrina: buscador, facetas, grid |
| `/equipos/<slug>` | `public/equipos/<slug>.html` | 215 fichas estáticas |

Ambas entran por `rewrites` en `next.config.ts`, siguiendo el patrón que ya usan `/` y
`/lab`. Las fichas comparten un CSS externo (`/equipos/_cat.css`) en vez de inlinearlo,
para que cada una pese ~8KB en vez de ~50KB.

El rewrite de `/equipos/:slug` va en **`afterFiles`**, no en `beforeFiles`: así el
sistema de archivos resuelve primero `/equipos/img/*` y `/equipos/_cat.css`, y sólo las
rutas que no son un archivo real caen en el rewrite a `<slug>.html`.

La home se conecta al catálogo:

- La sección `#spec` (Especialidades) pasa a mostrar **conteos reales** y enlaza a
  `/equipos?esp=<slug>`.
- La sección `#marcas` enlaza a `/equipos?marca=<slug>`.

Esto corrige un problema existente: `_d-body.html` y `src/components/Specialties.tsx`
listan equipos **inventados a mano** ("Doppler Fetal", "Desfibriladores", "Motores
Ortopédicos") que no existen en el inventario. Pasan a salir de `_catalogo.json`.

## 8. Búsqueda

Client-side pura. El índice viaja embebido en `/equipos`: 215 entradas con nombre,
marca, especialidad, tipo y los primeros 200 caracteres de la descripción. ~120KB en
crudo, ~35KB con gzip. Cero llamadas de red al filtrar.

Requisitos:

- **Insensible a acentos y mayúsculas.** "ecografo" encuentra "Ecógrafos".
- **Por tokens, con prefijo.** "sono x10" encuentra "X10 Sonoscape".
- **Facetas cruzables** entre los tres ejes, con conteos vivos. Una faceta que daría 0
  resultados se deshabilita en vez de desaparecer.
- **Estado en la URL:** `/equipos?q=ecografo&esp=cardiologia&marca=siemens`, para que un
  filtro se pueda compartir por WhatsApp. Navegable con atrás/adelante.
- **Sin resultados** ofrece la salida útil: escribir por WhatsApp describiendo lo que se
  busca.

## 9. Las tres ideas que lo diferencian

### 9.1 Buscar por necesidad, no por nomenclatura

Chips sobre el buscador con lenguaje clínico real — "Voy a montar un consultorio de
ginecología", "Necesito reemplazar un ecógrafo", "Equipamiento para quirófano" — que
aplican combinaciones predefinidas de filtros. El médico no siempre sabe cómo se llama
el equipo; sí sabe qué necesita. Los chips se definen en el mapa de curaduría.

### 9.2 Comparador

Se marcan 2 o 3 equipos y se ven lado a lado. El CTA manda **un solo** WhatsApp con los
tres. Es exactamente la conversación que hoy ocurre en mensajes sueltos.

### 9.3 CTA con contexto

Cada ficha abre `wa.me/584241941573` — el número que ya usa el footer — con el mensaje
precargado nombrando el equipo, para que del otro lado sepan de qué se habla sin
preguntar. Es el **único** CTA del catálogo.

## 10. Fuera de alcance

- Carrito, precios, stock, cuentas de usuario, checkout. No es una tienda.
- Galerías multi-imagen por equipo.
- Sincronización automática con WooCommerce.
- Migrar la app de `src/` al rediseño.
- Traducciones.

## 11. Criterios de éxito

1. Los 215 equipos son navegables y buscables desde `/equipos`.
2. Buscar "ecografo" devuelve resultados de todas las especialidades, no de una.
3. Ninguna faceta visible dice "Sin categorizar" ni "Destacado".
4. Las especialidades de la home muestran conteos reales y llevan al catálogo filtrado.
5. Cada ficha abre WhatsApp con el equipo nombrado en el mensaje.
6. El sitio construye y navega con el WordPress viejo apagado.
7. Ningún equipo muestra precio.

## 12. Plan de trabajo

Según DESIGN.md, la dirección visual se valida en el Mockup Lab antes de promoverse:
primero `/lab/equipos` con los 215 equipos reales adentro, se itera sobre algo vivo, y
recién entonces se promueve a `/equipos`.
