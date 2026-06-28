import type { NextConfig } from "next";

const withBundleAnalyzer = require("@next/bundle-analyzer")({
  enabled: process.env.ANALYZE === "true",
});

const nextConfig: NextConfig = withBundleAnalyzer({
  reactStrictMode: true,
  poweredByHeader: false,
  compress: true,

  transpilePackages: [
    "@memex/ui",
    "@memex/types",
    "@memex/hooks",
    "@memex/animations",
    "@memex/config",
    "three",
  ],

  experimental: {
    optimizePackageImports: ["lucide-react", "framer-motion", "@tanstack/react-query", "@memex/ui"],
  },

  images: {
    formats: ["image/avif", "image/webp"],
    deviceSizes: [640, 750, 1080, 1200, 1920],
  },

  headers: async () => [
    {
      source: "/(.*)",
      headers: [
        { key: "X-Frame-Options", value: "DENY" },
        { key: "X-Content-Type-Options", value: "nosniff" },
        { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
        { key: "X-XSS-Protection", value: "1; mode=block" },
      ],
    },
    {
      source: "/fonts/(.*)",
      headers: [{ key: "Cache-Control", value: "public, max-age=31536000, immutable" }],
    },
  ],
});

export default nextConfig;
