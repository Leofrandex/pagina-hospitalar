/**
 * Sedes de Hospitalar Venezuela.
 *
 * `maps` alimenta el botón "Cómo llegar" del footer. Caracas y Barquisimeto usan
 * el enlace corto de su ficha en Google Maps; Maturín todavía usa una búsqueda
 * generada desde la dirección — reemplazar por su enlace corto cuando lo tengamos.
 */

export interface Sede {
  ciudad: string;
  direccion: string;
  telefono: string;
  maps: string;
}

export const sedes: Sede[] = [
  {
    ciudad: "Caracas",
    direccion:
      "Av. Francisco de Miranda, Centro Seguros La Paz. Piso 7, Local N°. O-71",
    telefono: "+58 212-2804934",
    maps: "https://share.google/Gubz2vY4BwwZcrTXH",
  },
  {
    ciudad: "Barquisimeto",
    direccion: "Av. Los Abogados, Barquisimeto 3001, Estado Lara",
    telefono: "+58 251-2524093",
    maps: "https://maps.app.goo.gl/FGTPHXG5rBZoE2tX6",
  },
  {
    ciudad: "Maturín",
    direccion:
      "Av. Andrés Eloy Blanco, Centro Profesional Cristina, piso 2, oficina C-05. Maturín, Edo. Monagas",
    telefono: "+58 424-1941573",
    maps: "https://www.google.com/maps/search/?api=1&query=Centro+Profesional+Cristina%2C+Av.+Andr%C3%A9s+Eloy+Blanco%2C+Matur%C3%ADn%2C+Monagas%2C+Venezuela",
  },
];
