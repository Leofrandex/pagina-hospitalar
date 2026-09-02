import { test } from 'node:test';
import assert from 'node:assert/strict';
import { buscar, contarFacetas, normalizar, paginar } from '../public/mockups/_buscador.mjs';

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

test('paginar recorta a 25 y calcula el total de páginas', () => {
  const slugs = Array.from({ length: 215 }, (_, i) => 's' + i);
  const r = paginar(slugs, 1, 25);
  assert.equal(r.paginas, 9);
  assert.equal(r.slugs.length, 25);
  assert.equal(r.slugs[0], 's0');
});

test('la última página trae el resto, no 25', () => {
  const slugs = Array.from({ length: 215 }, (_, i) => 's' + i);
  const r = paginar(slugs, 9, 25);
  assert.equal(r.slugs.length, 15);
  assert.equal(r.slugs[0], 's200');
});

test('una página fuera de rango se acota en vez de vaciar la pantalla', () => {
  const slugs = Array.from({ length: 30 }, (_, i) => 's' + i);
  assert.equal(paginar(slugs, 99, 25).pagina, 2);
  assert.equal(paginar(slugs, 0, 25).pagina, 1);
  assert.equal(paginar(slugs, -3, 25).pagina, 1);
});

test('sin resultados hay una sola página vacía', () => {
  const r = paginar([], 1, 25);
  assert.equal(r.paginas, 1);
  assert.deepEqual(r.slugs, []);
});
