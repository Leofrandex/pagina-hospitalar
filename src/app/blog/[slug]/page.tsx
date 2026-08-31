import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { notFound } from "next/navigation";
import { ArrowLeft, ArrowRight, Calendar } from "lucide-react";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { formatDate, getPost } from "@/lib/wp";

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const post = await getPost(slug);

  if (!post) return { title: "Artículo no encontrado | Hospitalar Venezuela" };

  return {
    title: `${post.title} | Hospitalar Venezuela`,
    description: post.excerpt,
    openGraph: {
      title: post.title,
      description: post.excerpt,
      type: "article",
      publishedTime: post.date,
      images: post.image ? [post.image] : undefined,
    },
  };
}

export default async function ArticlePage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const post = await getPost(slug);

  if (!post) notFound();

  return (
    <main className="flex min-h-screen flex-col bg-background">
      <Header />

      <article className="flex-1">
        {/* Encabezado */}
        <div className="relative overflow-hidden bg-primary py-20 text-white">
          <div className="absolute -left-32 -top-32 h-96 w-96 rounded-full bg-accent/20 blur-[120px]" />
          <div className="relative mx-auto max-w-3xl px-4 sm:px-6 lg:px-8">
            <Link
              href="/blog"
              className="mb-10 inline-flex items-center gap-2 font-syncopate text-[10px] font-bold uppercase tracking-widest text-gray-300 transition-colors hover:text-accent"
            >
              <ArrowLeft className="h-4 w-4" />
              Volver al blog
            </Link>

            <span className="mb-5 block font-syncopate text-[10px] font-bold uppercase tracking-[0.3em] text-accent">
              {post.category}
            </span>

            <h1 className="mb-6 font-syncopate text-3xl font-bold leading-[1.2] md:text-5xl">
              {post.title}
            </h1>

            <span className="flex items-center gap-2 text-sm font-light text-gray-300">
              <Calendar className="h-4 w-4" />
              {formatDate(post.date)}
            </span>
          </div>
        </div>

        {/* Imagen destacada. Sin optimizar: ver la nota en PostCard. */}
        {post.image && (
          <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8">
            <div className="relative -mt-12 aspect-[16/9] w-full overflow-hidden rounded-2xl bg-gray-100 shadow-[0_30px_80px_rgba(53,46,135,0.15)]">
              <Image
                src={post.image}
                alt={post.imageAlt}
                fill
                sizes="(max-width: 1024px) 100vw, 1024px"
                className="object-cover"
                priority
                unoptimized
              />
            </div>
          </div>
        )}

        {/* Contenido */}
        <div className="mx-auto max-w-3xl px-4 py-16 sm:px-6 lg:px-8">
          <div className="wp-content" dangerouslySetInnerHTML={{ __html: post.content }} />
        </div>

        {/* Cierre */}
        <div className="mx-auto max-w-3xl px-4 pb-24 sm:px-6 lg:px-8">
          <div className="rounded-2xl border border-gray-100 bg-gray-50 p-10 text-center">
            <h2 className="mb-3 font-syncopate text-xl font-bold uppercase text-primary">
              ¿Hablamos de su proyecto?
            </h2>
            <p className="mx-auto mb-8 max-w-lg font-light leading-relaxed text-gray-600">
              Nuestros ingenieros y especialistas están listos para asesorarlo con tecnología médica
              de vanguardia.
            </p>
            <Link
              href="/#contacto"
              className="inline-flex items-center gap-3 rounded-lg bg-cta px-8 py-4 font-syncopate text-xs font-bold uppercase tracking-widest text-white shadow-xl shadow-cta/25 transition-all duration-300 hover:-translate-y-0.5 hover:bg-[#d95b2d]"
            >
              Solicitar asesoría
              <ArrowRight className="h-4 w-4" />
            </Link>
          </div>
        </div>
      </article>

      <Footer />
    </main>
  );
}
