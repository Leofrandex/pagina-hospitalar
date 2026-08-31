import Image from "next/image";
import Link from "next/link";
import { ArrowUpRight, Calendar } from "lucide-react";
import { formatDate, type Post } from "@/lib/wp";
import { BrandShape } from "./BrandShape";

export default function PostCard({ post }: { post: Post }) {
  return (
    <Link
      href={`/blog/${post.slug}`}
      className="group flex h-full flex-col overflow-hidden rounded-2xl border border-gray-100 bg-white transition-all duration-500 hover:-translate-y-2 hover:shadow-[0_30px_60px_rgba(53,46,135,0.12)]"
    >
      <div className="relative h-52 w-full overflow-hidden bg-gray-50">
        {/* El servidor de WordPress responde lento en frio y el optimizador de
            imagenes de Next agota su tiempo de espera contra el; la imagen ya
            viene redimensionada, asi que la servimos sin optimizar. */}
        {post.image ? (
          <Image
            src={post.image}
            alt={post.imageAlt}
            fill
            sizes="(max-width: 768px) 100vw, (max-width: 1280px) 50vw, 33vw"
            className="object-cover transition-transform duration-700 group-hover:scale-105"
            unoptimized
          />
        ) : (
          <div className="flex h-full w-full items-center justify-center bg-primary/5">
            <BrandShape className="h-24 w-24 text-primary/20" />
          </div>
        )}
        <span className="absolute left-4 top-4 rounded-full bg-white/95 px-4 py-1.5 font-syncopate text-[9px] font-bold uppercase tracking-widest text-primary shadow-sm">
          {post.category}
        </span>
      </div>

      <div className="flex flex-1 flex-col p-7">
        <span className="mb-4 flex items-center gap-2 text-[11px] font-light uppercase tracking-widest text-gray-400">
          <Calendar className="h-3.5 w-3.5" />
          {formatDate(post.date)}
        </span>

        <h3 className="mb-3 font-syncopate text-base font-bold leading-snug text-primary transition-colors duration-300 group-hover:text-accent">
          {post.title}
        </h3>

        <p className="mb-6 line-clamp-3 flex-1 text-sm font-light leading-relaxed text-gray-600">
          {post.excerpt}
        </p>

        <span className="mt-auto flex items-center gap-2 font-syncopate text-[10px] font-bold uppercase tracking-widest text-cta">
          Leer artículo
          <ArrowUpRight className="h-4 w-4 transition-transform duration-300 group-hover:translate-x-1 group-hover:-translate-y-1" />
        </span>
      </div>
    </Link>
  );
}
