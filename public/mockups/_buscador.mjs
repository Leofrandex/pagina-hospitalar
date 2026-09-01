// Lógica de búsqueda del catálogo. Sin DOM a propósito: así corre en node --test
// y _build_catalogo.py la inlinea en la página tal cual.

// NFD y no NFKD, igual que en _catalogo_map.py: NFKD convertiría el '™' de
// 'MyLab™X75' en las letras 'TM' y los dos lados dejarían de coincidir.
export function normalizar(texto) {
  return (texto || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
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
