"use client";

import { useSearchMemories } from "@/hooks/use-memory";
import type { Entity, MemoryDetail } from "@memex/types";
import { AnimatePresence, motion } from "framer-motion";
import { ArrowRight, Blocks, Bot, Command, Hash, Search, Tag, User } from "lucide-react";
import React, { useState, useCallback, useEffect, useRef, useMemo } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

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

type SearchMode = "memories" | "entities" | "commands";

interface CommandItem {
  id: string;
  label: string;
  description: string;
  icon: React.ReactNode;
  action: () => void;
}

interface CommandPaletteProps {
  isOpen: boolean;
  onClose: () => void;
  onSelectMemory: (memory: MemoryDetail) => void;
  projectId: string;
  onOpenChat?: () => void;
}

const ResultsList = React.memo(function ResultsList({
  results,
  selectedIndex,
  onSelect,
  onClose,
}: {
  results: MemoryDetail[];
  selectedIndex: number;
  onSelect: (memory: MemoryDetail) => void;
  onClose: () => void;
}) {
  return (
    <>
      {results.map((memory, index) => (
        <button
          key={memory.id}
          type="button"
          id={`cp-mem-${memory.id}`}
          aria-selected={index === selectedIndex}
          onClick={() => {
            onSelect(memory);
            onClose();
          }}
          className={`w-full flex items-start gap-3 px-5 py-3 text-left transition-colors ${
            index === selectedIndex ? "bg-white/10" : "hover:bg-white/5"
          }`}
        >
          <span
            className={`shrink-0 px-2 py-0.5 rounded text-xs font-medium ${TYPE_COLORS[memory.memory_type] || TYPE_COLORS.default}`}
          >
            {memory.memory_type}
          </span>
          <div className="flex-1 min-w-0">
            <p className="text-sm text-white truncate">{memory.title || "Untitled"}</p>
            {memory.content_preview && (
              <p className="text-xs text-white/40 truncate mt-0.5">{memory.content_preview}</p>
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
            className={`shrink-0 mt-1 ${index === selectedIndex ? "text-amber-400" : "text-white/20"}`}
          />
        </button>
      ))}
    </>
  );
});

export const CommandPalette = React.memo(function CommandPalette({
  isOpen,
  onClose,
  onSelectMemory,
  projectId,
  onOpenChat,
}: CommandPaletteProps) {
  const [query, setQuery] = useState("");
  const [selectedIndex, setSelectedIndex] = useState(0);
  const [mode, setMode] = useState<SearchMode>("memories");
  const [entities, setEntities] = useState<Entity[]>([]);
  const inputRef = useRef<HTMLInputElement>(null);
  const previousFocusRef = useRef<HTMLElement | null>(null);
  const searchMutation = useSearchMemories();

  const results = searchMutation.data?.results || [];

  const debouncedQuery = useRef<string>("");
  const debounceTimer = useRef<ReturnType<typeof setTimeout> | undefined>(undefined);

  useEffect(() => {
    debouncedQuery.current = query;
    if (debounceTimer.current) clearTimeout(debounceTimer.current);
    if (query.length >= 2) {
      debounceTimer.current = setTimeout(() => {
        searchMutation.mutate({ query: debouncedQuery.current, projectId, limit: 10 });
      }, 300);
    }
    return () => {
      if (debounceTimer.current) clearTimeout(debounceTimer.current);
    };
  }, [query, projectId, searchMutation]);

  const commands: CommandItem[] = useMemo(
    () => [
      {
        id: "chat",
        label: "Open AI Chat",
        description: "Ask questions about your memories",
        icon: <Bot size={14} />,
        action: () => {
          onOpenChat?.();
          onClose();
        },
      },
      {
        id: "reason",
        label: "Reason over memories",
        description: "Get insights with evidence and confidence",
        icon: <Blocks size={14} />,
        action: () => {
          onOpenChat?.();
          onClose();
        },
      },
      {
        id: "search_entities",
        label: "Search entities",
        description: "Find people, projects, technologies",
        icon: <User size={14} />,
        action: () => setMode("entities"),
      },
    ],
    [onOpenChat, onClose],
  );

  useEffect(() => {
    if (isOpen) {
      previousFocusRef.current = document.activeElement as HTMLElement;
      setQuery("");
      setSelectedIndex(0);
      setMode("memories");
      setTimeout(() => inputRef.current?.focus(), 50);
      return () => {
        if (previousFocusRef.current) {
          previousFocusRef.current?.focus();
          previousFocusRef.current = null;
        }
      };
    }
  }, [isOpen]);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (!isOpen) return;
      if (e.key === "Escape") {
        if (query === "") {
          onClose();
        } else {
          setQuery("");
        }
        return;
      }
      if (e.key === "ArrowDown") {
        e.preventDefault();
        const maxItems =
          mode === "memories"
            ? results.length
            : mode === "entities"
              ? entities.length
              : commands.length;
        setSelectedIndex((prev) => Math.min(prev + 1, maxItems - 1));
      }
      if (e.key === "ArrowUp") {
        e.preventDefault();
        setSelectedIndex((prev) => Math.max(prev - 1, 0));
      }
      if (e.key === "Enter") {
        if (mode === "memories" && results[selectedIndex]) {
          onSelectMemory(results[selectedIndex]);
          onClose();
        } else if (mode === "entities" && entities[selectedIndex]) {
          setQuery(entities[selectedIndex].name);
          setMode("memories");
        } else if (mode === "commands" && commands[selectedIndex]) {
          commands[selectedIndex].action();
        }
      }
      if (e.key === "Backspace" && query === "" && mode !== "memories") {
        setMode("memories");
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [isOpen, results, entities, commands, selectedIndex, onClose, onSelectMemory, query, mode]);

  const handleSearch = useCallback(
    async (value: string) => {
      setQuery(value);
      setSelectedIndex(0);
      if (value.length >= 2) {
        try {
          const res = await fetch(
            `${API_BASE}/api/v1/memex/entities/search?project_id=${projectId}&query=${encodeURIComponent(value)}&limit=5`,
          );
          if (res.ok) {
            const data = await res.json();
            setEntities(data.entities || []);
          }
        } catch {
          setEntities([]);
        }
      } else {
        setEntities([]);
      }
    },
    [projectId],
  );

  useEffect(() => {
    if (query === "" && mode === "memories") {
      setSelectedIndex(-1);
    }
  }, [query, mode]);

  const showCommands = query.length === 0 && mode === "memories";

  const activeDescendantId = (() => {
    if (selectedIndex < 0) return undefined;
    if (showCommands && commands[selectedIndex]) return `cp-cmd-${commands[selectedIndex].id}`;
    if (mode === "entities" && entities[selectedIndex])
      return `cp-ent-${entities[selectedIndex].id}`;
    if (mode === "memories" && results[selectedIndex]) return `cp-mem-${results[selectedIndex].id}`;
    return undefined;
  })();

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
          {/* biome-ignore lint/a11y/useSemanticElements: framer-motion dialog */}
          <motion.div
            role="dialog"
            aria-modal="true"
            aria-label="Search commands and memories"
            aria-keyshortcuts="Control+k"
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
                  placeholder={
                    mode === "entities"
                      ? "Search entities..."
                      : "Search memories, entities, or type a command..."
                  }
                  aria-label="Search"
                  aria-activedescendant={activeDescendantId}
                  className="flex-1 bg-transparent text-white placeholder-white/30 outline-none text-sm"
                />
                {mode !== "memories" && (
                  <span className="text-xs text-purple-400 bg-purple-500/10 px-2 py-0.5 rounded">
                    {mode}
                  </span>
                )}
                <kbd className="hidden sm:inline-flex items-center gap-1 px-2 py-1 text-xs text-white/30 bg-white/5 rounded border border-white/10">
                  <Command size={12} />K
                </kbd>
              </div>

              {/* biome-ignore lint/a11y/useSemanticElements: complex listbox with custom items */}
              <div className="max-h-80 overflow-y-auto" role="listbox" tabIndex={0}>
                {showCommands && (
                  <div className="px-3 py-2">
                    <p className="text-xs text-white/30 px-2 py-1 uppercase tracking-wider">
                      Commands
                    </p>
                    {commands.map((cmd, index) => (
                      <button
                        key={cmd.id}
                        type="button"
                        id={`cp-cmd-${cmd.id}`}
                        aria-selected={index === selectedIndex}
                        onClick={cmd.action}
                        className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-left transition-colors ${
                          index === selectedIndex ? "bg-white/10" : "hover:bg-white/5"
                        }`}
                      >
                        <span className="text-purple-400">{cmd.icon}</span>
                        <div className="flex-1">
                          <p className="text-sm text-white">{cmd.label}</p>
                          <p className="text-xs text-white/40">{cmd.description}</p>
                        </div>
                        <ArrowRight size={14} className="text-white/20" />
                      </button>
                    ))}
                  </div>
                )}

                {entities.length > 0 && mode === "entities" && (
                  <div className="px-3 py-2">
                    <p className="text-xs text-white/30 px-2 py-1 uppercase tracking-wider">
                      Entities
                    </p>
                    {entities.map((entity, index) => (
                      <button
                        key={entity.id}
                        type="button"
                        id={`cp-ent-${entity.id}`}
                        aria-selected={index === selectedIndex}
                        onClick={() => {
                          setQuery(entity.name);
                          setMode("memories");
                        }}
                        className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-left transition-colors ${
                          index === selectedIndex ? "bg-white/10" : "hover:bg-white/5"
                        }`}
                      >
                        <span className="text-cyan-400">
                          <Hash size={14} />
                        </span>
                        <div className="flex-1">
                          <p className="text-sm text-white">{entity.name}</p>
                          <p className="text-xs text-white/40">
                            {entity.entity_type}
                            {entity.description ? ` — ${entity.description}` : ""}
                          </p>
                        </div>
                        <span className="text-xs text-white/30 bg-white/5 px-1.5 py-0.5 rounded">
                          {entity.entity_type}
                        </span>
                      </button>
                    ))}
                  </div>
                )}

                {mode === "memories" && query.length >= 2 && (
                  <>
                    {searchMutation.isPending && (
                      <output
                        className="block px-5 py-8 text-center text-sm text-white/30"
                        aria-live="polite"
                      >
                        Searching...
                      </output>
                    )}
                    {!searchMutation.isPending && results.length === 0 && entities.length === 0 && (
                      <output
                        className="block px-5 py-8 text-center text-sm text-white/30"
                        aria-live="polite"
                      >
                        No results found
                      </output>
                    )}
                    <ResultsList
                      results={results}
                      selectedIndex={selectedIndex}
                      onSelect={onSelectMemory}
                      onClose={onClose}
                    />
                  </>
                )}

                {entities.length > 0 && mode === "memories" && query.length >= 2 && (
                  <div className="border-t border-white/5 px-3 py-2">
                    <p className="text-xs text-white/30 px-2 py-1 uppercase tracking-wider">
                      Entities
                    </p>
                    {entities.map((entity) => (
                      <button
                        key={entity.id}
                        type="button"
                        onClick={() => {
                          setQuery(entity.name);
                        }}
                        className="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-left hover:bg-white/5 transition-colors"
                      >
                        <Hash size={14} className="text-cyan-400" />
                        <span className="text-sm text-white">{entity.name}</span>
                        <span className="ml-auto text-xs text-white/30">{entity.entity_type}</span>
                      </button>
                    ))}
                  </div>
                )}
              </div>

              <div className="flex items-center gap-4 px-5 py-3 border-t border-white/10 text-xs text-white/30">
                <span className="sr-only">
                  Use arrow keys to navigate, Enter to select, Escape to close
                </span>
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
});
