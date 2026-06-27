"use client";

import { useState, useCallback, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Search, Command, Tag, ArrowRight } from "lucide-react";
import { useSearchMemories } from "@/hooks/use-memory";
import type { MemoryDetail } from "@memex/types";

const TYPE_COLORS: Record<string, string> = {
  text: "bg-amber-500/20 text-amber-400",
  code: "bg-cyan-500/20 text-cyan-400",
  conversation: "bg-purple-500/20 text-purple-400",
  meeting_note: "bg-emerald-500/20 text-emerald-400",
  research: "bg-pink-500/20 text-pink-400",
  decision: "bg-orange-500/20 text-orange-400",
  url: "bg-sky-500/20 text-sky-400",
  file: "bg-indigo-500/20 text-indigo-400",
  default: "bg-gray-500/20 text-gray-400",
};

interface CommandPaletteProps {
  isOpen: boolean;
  onClose: () => void;
  onSelectMemory: (memory: MemoryDetail) => void;
  projectId: string;
}

export function CommandPalette({ isOpen, onClose, onSelectMemory, projectId }: CommandPaletteProps) {
  const [query, setQuery] = useState("");
  const [selectedIndex, setSelectedIndex] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);
  const searchMutation = useSearchMemories();

  const results = searchMutation.data?.results || [];

  useEffect(() => {
    if (isOpen) {
      setQuery("");
      setSelectedIndex(0);
      setTimeout(() => inputRef.current?.focus(), 50);
    }
  }, [isOpen]);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (!isOpen) return;
      if (e.key === "Escape") {
        onClose();
        return;
      }
      if (e.key === "ArrowDown") {
        e.preventDefault();
        setSelectedIndex((prev) => Math.min(prev + 1, results.length - 1));
      }
      if (e.key === "ArrowUp") {
        e.preventDefault();
        setSelectedIndex((prev) => Math.max(prev - 1, 0));
      }
      if (e.key === "Enter" && results[selectedIndex]) {
        onSelectMemory(results[selectedIndex]);
        onClose();
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [isOpen, results, selectedIndex, onClose, onSelectMemory]);

  const handleSearch = useCallback(
    (value: string) => {
      setQuery(value);
      setSelectedIndex(0);
      if (value.length >= 2) {
        searchMutation.mutate({ query: value, projectId, limit: 10 });
      }
    },
    [projectId, searchMutation],
  );

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50"
            onClick={onClose}
          />
          <motion.div
            initial={{ opacity: 0, scale: 0.96, y: -20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.96, y: -20 }}
            transition={{ type: "spring", damping: 30, stiffness: 300 }}
            className="fixed top-[20%] left-1/2 -translate-x-1/2 w-full max-w-lg z-50"
          >
            <div className="bg-zinc-900/95 backdrop-blur-xl border border-white/10 rounded-2xl overflow-hidden shadow-2xl">
              <div className="flex items-center gap-3 px-5 py-4 border-b border-white/10">
                <Search size={18} className="text-white/40 shrink-0" />
                <input
                  ref={inputRef}
                  type="text"
                  value={query}
                  onChange={(e) => handleSearch(e.target.value)}
                  placeholder="Search memories..."
                  className="flex-1 bg-transparent text-white placeholder-white/30 outline-none text-sm"
                />
                <kbd className="hidden sm:inline-flex items-center gap-1 px-2 py-1 text-xs text-white/30 bg-white/5 rounded border border-white/10">
                  <Command size={12} />
                  K
                </kbd>
              </div>

              <div className="max-h-80 overflow-y-auto">
                {searchMutation.isPending && query.length >= 2 && (
                  <div className="px-5 py-8 text-center text-sm text-white/30">
                    Searching...
                  </div>
                )}

                {!searchMutation.isPending && query.length >= 2 && results.length === 0 && (
                  <div className="px-5 py-8 text-center text-sm text-white/30">
                    No memories found
                  </div>
                )}

                {results.map((memory, index) => (
                  <button
                    key={memory.id}
                    onClick={() => {
                      onSelectMemory(memory);
                      onClose();
                    }}
                    className={`w-full flex items-start gap-3 px-5 py-3 text-left transition-colors ${
                      index === selectedIndex
                        ? "bg-white/10"
                        : "hover:bg-white/5"
                    }`}
                  >
                    <span
                      className={`shrink-0 px-2 py-0.5 rounded text-xs font-medium ${
                        TYPE_COLORS[memory.memory_type] || TYPE_COLORS.default
                      }`}
                    >
                      {memory.memory_type}
                    </span>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm text-white truncate">
                        {memory.title || "Untitled"}
                      </p>
                      {memory.content_preview && (
                        <p className="text-xs text-white/40 truncate mt-0.5">
                          {memory.content_preview}
                        </p>
                      )}
                    </div>
                    {memory.tags && memory.tags.length > 0 && (
                      <div className="flex gap-1 shrink-0">
                        {memory.tags.slice(0, 2).map((tag) => (
                          <span
                            key={tag}
                            className="flex items-center gap-1 px-1.5 py-0.5 text-xs text-white/40 bg-white/5 rounded"
                          >
                            <Tag size={10} />
                            {tag}
                          </span>
                        ))}
                      </div>
                    )}
                    <ArrowRight
                      size={14}
                      className={`shrink-0 mt-1 ${
                        index === selectedIndex ? "text-amber-400" : "text-white/20"
                      }`}
                    />
                  </button>
                ))}
              </div>

              <div className="flex items-center gap-4 px-5 py-3 border-t border-white/10 text-xs text-white/30">
                <span>
                  <kbd className="px-1 py-0.5 bg-white/10 rounded">↑↓</kbd> Navigate
                </span>
                <span>
                  <kbd className="px-1 py-0.5 bg-white/10 rounded">↵</kbd> Open
                </span>
                <span>
                  <kbd className="px-1 py-0.5 bg-white/10 rounded">Esc</kbd> Close
                </span>
              </div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
