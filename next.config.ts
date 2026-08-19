import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      // Mockup Lab del rediseño: /lab y /lab/<pieza> sirven los HTML de public/mockups.
      // Se comparte por enlace; no se indexa (cada página lleva robots noindex).
      { source: "/lab", destination: "/mockups/index.html" },
      { source: "/lab/:slug", destination: "/mockups/:slug.html" },
    ];
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
