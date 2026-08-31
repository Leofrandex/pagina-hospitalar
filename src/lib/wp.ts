/**
 * Cliente del blog de WordPress de hospitalarve.com.
 *
 * El sitio actual publica los artículos en WordPress y expone su API REST
 * públicamente, así que la web nueva los consume en lectura: lo que el equipo
 * publique allá aparece acá sin tocar código.
 *
 * Next 16 no cachea `fetch` por defecto, así que la revalidación es explícita.
 */

const WP_API = "https://hospitalarve.com/wp-json/wp/v2";
const REVALIDATE_SECONDS = 3600; // 1 hora

export interface Post {
  id: number;
  slug: string;
  title: string;
  excerpt: string;
  date: string;
  category: string;
  image: string | null;
  imageAlt: string;
}

export interface FullPost extends Post {
  content: string;
  originalUrl: string;
}

interface WpRendered {
  rendered: string;
}

interface WpMediaSize {
  source_url?: string;
}

interface WpMedia {
  source_url?: string;
  alt_text?: string;
  media_details?: {
    sizes?: Record<string, WpMediaSize>;
  };
}

interface WpTerm {
  taxonomy?: string;
  name?: string;
}

interface WpPost {
  id: number;
  slug: string;
  link: string;
  date: string;
  title: WpRendered;
  excerpt: WpRendered;
  content?: WpRendered;
  _embedded?: {
    "wp:featuredmedia"?: WpMedia[];
    "wp:term"?: WpTerm[][];
  };
}

const HTML_ENTITIES: Record<string, string> = {
  amp: "&",
  lt: "<",
  gt: ">",
  quot: '"',
  apos: "'",
  nbsp: " ",
  hellip: "…",
  ndash: "–",
  mdash: "—",
  laquo: "«",
  raquo: "»",
  rsquo: "'",
  lsquo: "'",
  ldquo: "“",
  rdquo: "”",
};

/** WordPress devuelve HTML con entidades; en títulos y extractos queremos texto plano. */
function toPlainText(html: string): string {
  return html
    .replace(/<[^>]*>/g, "")
    .replace(/&#(\d+);/g, (_, code: string) => String.fromCharCode(Number(code)))
    .replace(/&#x([0-9a-f]+);/gi, (_, code: string) => String.fromCharCode(parseInt(code, 16)))
    .replace(/&([a-z]+);/gi, (match, name: string) => HTML_ENTITIES[name.toLowerCase()] ?? match)
    .replace(/\s+/g, " ")
    .trim();
}

function primaryCategory(post: WpPost): string {
  const terms = post._embedded?.["wp:term"]?.flat() ?? [];
  const category = terms.find(
    (term) => term?.taxonomy === "category" && term.name && term.name !== "Uncategorized"
  );
  return category?.name ? toPlainText(category.name) : "Artículo";
}

/**
 * Los originales de WordPress pesan varios MB y el optimizador de imágenes de
 * Next agota su tiempo de espera al descargarlos. WordPress ya guarda versiones
 * redimensionadas: tomamos la más chica que sirva y sólo caemos al original si
 * no hay ninguna.
 */
function pickImage(media: WpMedia | undefined, preferred: string[]): string | null {
  if (!media) return null;
  const sizes = media.media_details?.sizes ?? {};
  for (const name of preferred) {
    const url = sizes[name]?.source_url;
    if (url) return url;
  }
  return media.source_url ?? null;
}

// El servidor de WordPress responde lento en frío, así que a la tarjeta le
// pedimos el archivo más liviano que se vea bien y al artículo uno mayor.
const CARD_SIZES = ["medium_large", "fusion-800", "large", "medium"];
const HERO_SIZES = ["large", "fusion-1200", "medium_large"];

function normalize(post: WpPost): Post {
  const media = post._embedded?.["wp:featuredmedia"]?.[0];
  const title = toPlainText(post.title?.rendered ?? "");

  return {
    id: post.id,
    slug: post.slug,
    title,
    excerpt: toPlainText(post.excerpt?.rendered ?? ""),
    date: post.date,
    category: primaryCategory(post),
    image: pickImage(media, CARD_SIZES),
    imageAlt: media?.alt_text ? toPlainText(media.alt_text) : title,
  };
}

/** Los borradores publicados sin título ensucian el listado; los dejamos fuera. */
function isPublishable(post: Post): boolean {
  return post.title.length > 0;
}

async function wpFetch(path: string): Promise<Response | null> {
  try {
    const response = await fetch(`${WP_API}${path}`, {
      next: { revalidate: REVALIDATE_SECONDS },
    });
    if (!response.ok) return null;
    return response;
  } catch {
    // El blog es contenido complementario: si WordPress no responde, la página
    // se sigue renderizando sin la sección en lugar de romperse.
    return null;
  }
}

export interface PostsPage {
  posts: Post[];
  totalPages: number;
}

export async function getPosts(page = 1, perPage = 9): Promise<PostsPage> {
  const response = await wpFetch(
    `/posts?per_page=${perPage}&page=${page}&_embed=wp:featuredmedia,wp:term`
  );
  if (!response) return { posts: [], totalPages: 0 };

  const data = (await response.json()) as WpPost[];
  const totalPages = Number(response.headers.get("x-wp-totalpages") ?? "1");

  return {
    posts: data.map(normalize).filter(isPublishable),
    totalPages: Number.isFinite(totalPages) ? totalPages : 1,
  };
}

export async function getRecentPosts(limit = 3): Promise<Post[]> {
  // Pedimos de más para compensar los que se descartan por no tener título.
  const { posts } = await getPosts(1, limit + 3);
  return posts.slice(0, limit);
}

export async function getPost(slug: string): Promise<FullPost | null> {
  const response = await wpFetch(`/posts?slug=${encodeURIComponent(slug)}&_embed=wp:featuredmedia,wp:term`);
  if (!response) return null;

  const data = (await response.json()) as WpPost[];
  const post = data[0];
  if (!post) return null;

  const media = post._embedded?.["wp:featuredmedia"]?.[0];

  return {
    ...normalize(post),
    // En el artículo la imagen se muestra a mayor tamaño que en la tarjeta.
    image: pickImage(media, HERO_SIZES),
    content: post.content?.rendered ?? "",
    originalUrl: post.link,
  };
}

export function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString("es-VE", {
    day: "numeric",
    month: "long",
    year: "numeric",
  });
}
