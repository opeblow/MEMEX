import type { Metadata, Viewport } from "next";
import type { ReactNode } from "react";
import "./globals.css";
import { Providers } from "./providers";

export const metadata: Metadata = {
  title: {
    default: "MEMEX — The Operating System for Artificial Memory",
    template: "%s | MEMEX",
  },
  description:
    "The Operating System for Artificial Memory. Store, recall, improve, and visualize AI memory forever.",
  keywords: [
    "AI memory",
    "knowledge graph",
    "artificial memory",
    "Cognee",
    "semantic search",
    "AI agents",
  ],
  authors: [{ name: "MEMEX" }],
  creator: "MEMEX",
  openGraph: {
    type: "website",
    locale: "en_US",
    url: "https://memex.sh",
    siteName: "MEMEX",
    title: "MEMEX — The Operating System for Artificial Memory",
    description:
      "Store, recall, improve, and visualize AI memory forever.",
  },
  twitter: {
    card: "summary_large_image",
    title: "MEMEX — The Operating System for Artificial Memory",
    description:
      "Store, recall, improve, and visualize AI memory forever.",
  },
  robots: {
    index: true,
    follow: true,
  },
  icons: {
    icon: "/favicon.ico",
  },
};

export const viewport: Viewport = {
  themeColor: "#000000",
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({
  children,
}: {
  children: ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
