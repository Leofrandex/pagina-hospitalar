import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    // Imágenes destacadas del blog, servidas desde el WordPress actual.
    remotePatterns: [
      {
        protocol: "https",
        hostname: "hospitalarve.com",
        pathname: "/wp-content/uploads/**",
      },
    ],
  },
  async rewrites() {
    return {
      // beforeFiles corre antes del sistema de archivos: es la única forma de que
      // "/" sirva el rediseño en vez de la página de src/app/page.tsx.
      beforeFiles: [
        { source: "/", destination: "/site.html" },
      ],
      afterFiles: [
        // Mockup Lab del rediseño: /lab y /lab/<pieza> sirven los HTML de public/mockups.
        // Se comparte por enlace; no se indexa (cada página lleva robots noindex).
        { source: "/lab", destination: "/mockups/index.html" },
        { source: "/lab/:slug", destination: "/mockups/:slug.html" },
      ],
      fallback: [],
    };
  },
  async headers() {
    return [
      {
        source: "/lab/:path*",
        headers: [{ key: "X-Robots-Tag", value: "noindex, nofollow" }],
      },
      {
        source: "/mockups/:path*",
        headers: [{ key: "X-Robots-Tag", value: "noindex, nofollow" }],
      },
    ];
  },
};

export default nextConfig;
