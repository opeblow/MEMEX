"use client";

import { Sidebar } from "@/components/layout/sidebar";
import { Menu } from "lucide-react";
import type { ReactNode } from "react";
import { useState } from "react";

export default function DashboardLayout({
  children,
}: {
  children: ReactNode;
}) {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="flex min-h-screen bg-black">
      <a
        href="#main-content"
        className="sr-only focus:not-sr-only focus:fixed focus:top-4 focus:left-4 focus:z-50 focus:px-4 focus:py-2 focus:bg-purple-500 focus:text-white focus:rounded-lg"
      >
        Skip to content
      </a>
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
      <div className="flex-1 flex flex-col min-w-0">
        <header className="flex items-center gap-3 px-4 py-3 border-b border-white/10 md:hidden bg-black/40 backdrop-blur-md">
          <button
            type="button"
            onClick={() => setSidebarOpen(true)}
            className="p-1 text-white/40 hover:text-white/80"
          >
            <Menu size={20} />
          </button>
          <span className="text-sm font-semibold text-amber-400">MEMEX</span>
        </header>
        <main id="main-content" className="flex-1 overflow-y-auto">
          {children}
        </main>
      </div>
    </div>
  );
}
