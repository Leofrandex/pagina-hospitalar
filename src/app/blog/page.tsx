import type { Metadata } from "next";
import Link from "next/link";
import { ArrowLeft, ArrowRight } from "lucide-react";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import PostCard from "@/components/PostCard";
import { ScrollReveal } from "@/components/ScrollReveal";
import { getPosts } from "@/lib/wp";

export const metadata: Metadata = {
  title: "Novedades y Noticias | Hospitalar Venezuela",
  description:
    "Artículos, tendencias y conocimiento del sector salud en Venezuela: tecnología médica, ingeniería clínica e historias de nuestros clientes.",
};

export default async function BlogPage({
  searchParams,
}: {
  searchParams: Promise<{ page?: string }>;
}) {
  const { page } = await searchParams;
  const currentPage = Math.max(1, Number(page) || 1);
  const { posts, totalPages } = await getPosts(currentPage, 9);

  return (
    <main className="flex min-h-screen flex-col bg-background">
      <Header />

      {/* Encabezado */}
      <section className="relative overflow-hidden bg-primary py-24 text-white">
        <div className="absolute -left-32 -top-32 h-96 w-96 rounded-full bg-accent/20 blur-[120px]" />
        <div
          className="absolute inset-0 opacity-[0.06]"
          style={{
            backgroundImage: "radial-gradient(circle, #ffffff 1px, transparent 1px)",
            backgroundSize: "32px 32px",
          }}
        />
        <div className="relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <span className="mb-6 block font-syncopate text-[10px] font-bold uppercase tracking-[0.3em] text-accent">
            Learning Hub
          </span>
          <h1 className="mb-6 max-w-3xl font-syncopate text-4xl font-bold leading-[1.15] md:text-6xl">
            Novedades y Noticias
          </h1>
          <p className="max-w-2xl text-lg font-light leading-relaxed text-gray-300">
            Historias, tendencias y conocimiento del sector salud en Venezuela. Lo que aprendemos
            trabajando junto a médicos, ingenieros y centros asistenciales de todo el país.
          </p>
        </div>
      </section>

      {/* Listado */}
      <section className="flex-1 bg-gray-50 py-20">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          {posts.length === 0 ? (
            <div className="rounded-2xl border border-gray-100 bg-white py-24 text-center">
              <p className="font-light text-gray-500">
                No pudimos cargar los artículos en este momento. Intente de nuevo en unos minutos.
              </p>
            </div>
          ) : (
            <div className="grid grid-cols-1 gap-8 md:grid-cols-2 lg:grid-cols-3">
              {posts.map((post, index) => (
                <ScrollReveal
                  key={post.id}
                  delay={(index % 3) * 0.1}
                  className="h-full"
                  overflowHidden={false}
                >
                  <PostCard post={post} />
                </ScrollReveal>
              ))}
            </div>
          )}

          {totalPages > 1 && (
            <nav
              aria-label="Paginación de artículos"
              className="mt-16 flex items-center justify-center gap-4"
            >
              {currentPage > 1 ? (
                <Link
                  href={currentPage === 2 ? "/blog" : `/blog?page=${currentPage - 1}`}
                  className="flex items-center gap-2 rounded-md border border-gray-200 bg-white px-6 py-3 font-syncopate text-[10px] font-bold uppercase tracking-widest text-primary transition-colors hover:bg-white hover:shadow-md"
                >
                  <ArrowLeft className="h-4 w-4" />
                  Anterior
                </Link>
              ) : (
                <span className="w-[124px]" aria-hidden />
              )}

              <span className="font-syncopate text-[10px] font-bold uppercase tracking-widest text-gray-400">
                Página {currentPage} de {totalPages}
              </span>

              {currentPage < totalPages ? (
                <Link
                  href={`/blog?page=${currentPage + 1}`}
                  className="flex items-center gap-2 rounded-md border border-gray-200 bg-white px-6 py-3 font-syncopate text-[10px] font-bold uppercase tracking-widest text-primary transition-colors hover:bg-white hover:shadow-md"
                >
                  Siguiente
                  <ArrowRight className="h-4 w-4" />
                </Link>
              ) : (
                <span className="w-[124px]" aria-hidden />
              )}
            </nav>
          )}
        </div>
      </section>

      <Footer />
    </main>
  );
}
