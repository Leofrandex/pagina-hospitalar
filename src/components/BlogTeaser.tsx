import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { getRecentPosts } from "@/lib/wp";
import { ScrollReveal } from "./ScrollReveal";
import PostCard from "./PostCard";

export default async function BlogTeaser() {
  const posts = await getRecentPosts(3);

  // Sin artículos disponibles no mostramos una sección vacía.
  if (posts.length === 0) return null;

  return (
    <section className="bg-white py-24" id="blog">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <ScrollReveal>
          <div className="mb-16 flex flex-col items-end justify-between gap-6 md:flex-row">
            <div className="max-w-2xl">
              <span className="mb-4 block font-syncopate text-[10px] font-bold uppercase tracking-[0.3em] text-accent">
                Learning Hub
              </span>
              <h2 className="mb-4 font-syncopate text-3xl font-bold text-primary md:text-5xl">
                Novedades y Noticias
              </h2>
              <div className="mb-6 h-1 w-24 rounded-full bg-accent" />
              <p className="text-lg font-light leading-relaxed text-gray-600">
                Historias, tendencias y conocimiento del sector salud en Venezuela. Lo que aprendemos
                trabajando junto a médicos, ingenieros y centros asistenciales de todo el país.
              </p>
            </div>

            <Link
              href="/blog"
              className="flex shrink-0 items-center gap-3 rounded-md border border-gray-200 bg-white px-8 py-4 font-syncopate text-[10px] font-bold uppercase tracking-widest text-primary shadow-sm transition-all duration-300 hover:bg-gray-50 hover:shadow-md"
            >
              Ver todos los artículos
              <ArrowRight className="h-4 w-4" />
            </Link>
          </div>
        </ScrollReveal>

        <div className="grid grid-cols-1 gap-8 md:grid-cols-2 lg:grid-cols-3">
          {posts.map((post, index) => (
            <ScrollReveal key={post.id} delay={index * 0.1} className="h-full" overflowHidden={false}>
              <PostCard post={post} />
            </ScrollReveal>
          ))}
        </div>
      </div>
    </section>
  );
}
