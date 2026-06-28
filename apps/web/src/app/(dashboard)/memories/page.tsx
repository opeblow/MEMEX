"use client";

import { useMemories, useSearchMemories } from "@/hooks";
import { useUIStore } from "@/lib/stores/ui-store";
import type { MemoryDetail } from "@memex/types";
import { Skeleton } from "@memex/ui";
import { AnimatePresence, motion } from "framer-motion";
import {
  Archive,
  Brain,
  FileText,
  Image,
  MessageSquare,
  Music,
  Search,
  Trash2,
  Video,
} from "lucide-react";
import Link from "next/link";
import { useCallback, useRef, useState } from "react";

const MEMORY_TYPE_ICONS: Record<string, React.ReactNode> = {
  text: <FileText size={14} />,
  file: <FileText size={14} />,
  code: <FileText size={14} />,
  image: <Image size={14} />,
  audio: <Music size={14} />,
  video: <Video size={14} />,
  url: <FileText size={14} />,
  conversation: <MessageSquare size={14} />,
  meeting_note: <FileText size={14} />,
  github_issue: <FileText size={14} />,
  support_ticket: <MessageSquare size={14} />,
  research: <Brain size={14} />,
  decision: <Brain size={14} />,
};

const container = {
  animate: {
    transition: { staggerChildren: 0.06 },
  },
};

const item = {
  initial: { opacity: 0, y: 16 },
  animate: { opacity: 1, y: 0, transition: { duration: 0.4, ease: "easeOut" } },
};

function ImportanceBadge({ importance }: { importance: number }) {
  const color =
    importance >= 8
      ? "bg-amber-500/15 text-amber-400 border-amber-500/20"
      : importance >= 5
        ? "bg-cyan-500/10 text-cyan-400 border-cyan-500/15"
        : importance >= 3
          ? "bg-white/5 text-white/50 border-white/10"
          : "bg-white/5 text-white/30 border-white/10";

  return (
    <span className={`px-1.5 py-0.5 rounded text-[10px] border ${color}`}>
      {importance.toFixed(1)}
    </span>
  );
}

function MemoryCard({
  memory,
  onDelete,
  onArchive,
}: {
  memory: MemoryDetail;
  onDelete: (id: string) => void;
  onArchive: (id: string) => void;
}) {
  return (
    <motion.div
      layout
      variants={item}
      className="group bg-white/[0.02] border border-white/10 rounded-xl overflow-hidden hover:border-white/20 transition-all"
    >
      <Link href={`/memories/${memory.id}`} className="block p-4">
        <div className="flex items-start gap-3">
          <div className="p-2 rounded-lg bg-white/5 shrink-0">
            {MEMORY_TYPE_ICONS[memory.memory_type] || (
              <FileText size={14} className="text-white/40" />
            )}
          </div>
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2">
              <h3 className="text-sm font-medium text-white/80 truncate">
                {memory.title || "Untitled"}
              </h3>
              <ImportanceBadge importance={memory.importance} />
            </div>
            {memory.content_preview && (
              <p className="text-xs text-white/30 mt-1.5 line-clamp-2">{memory.content_preview}</p>
            )}
            <div className="flex items-center gap-2 mt-2">
              <span className="text-[10px] text-white/30 px-1.5 py-0.5 rounded bg-white/5">
                {memory.memory_type}
              </span>
              {memory.tags?.slice(0, 3).map((tag) => (
                <span
                  key={tag}
                  className="text-[10px] text-white/30 px-1.5 py-0.5 rounded bg-white/5"
                >
                  {tag}
                </span>
              ))}
              {memory.tags?.length > 3 && (
                <span className="text-[10px] text-white/20">+{memory.tags.length - 3}</span>
              )}
            </div>
            <p className="text-[10px] text-white/20 mt-2">
              {new Date(memory.created_at).toLocaleDateString(undefined, {
                year: "numeric",
                month: "short",
                day: "numeric",
              })}
            </p>
          </div>
        </div>
      </Link>
      <div className="flex border-t border-white/5 opacity-0 group-hover:opacity-100 transition-opacity">
        <button
          type="button"
          onClick={() => onArchive(memory.id)}
          className="flex-1 flex items-center justify-center gap-1.5 py-2 text-[10px] text-white/30 hover:text-cyan-400 hover:bg-white/[0.02] transition-colors"
        >
          <Archive size={12} />
          Archive
        </button>
        <button
          type="button"
          onClick={() => onDelete(memory.id)}
          className="flex-1 flex items-center justify-center gap-1.5 py-2 text-[10px] text-white/30 hover:text-red-400 hover:bg-white/[0.02] transition-colors"
        >
          <Trash2 size={12} />
          Delete
        </button>
      </div>
    </motion.div>
  );
}

export default function MemoriesPage() {
  const activeProjectId = useUIStore((s) => s.activeProjectId);
  const projectId = activeProjectId || "default";
  const [searchQuery, setSearchQuery] = useState("");
  const searchTimeout = useRef<ReturnType<typeof setTimeout> | undefined>(undefined);
  const [searchResults, setSearchResults] = useState<MemoryDetail[] | null>(null);
  const searchMemories = useSearchMemories();

  const { data: memories = [], isLoading } = useMemories(projectId);

  const handleSearch = useCallback(
    (query: string) => {
      setSearchQuery(query);
      if (searchTimeout.current) clearTimeout(searchTimeout.current);
      if (!query.trim()) {
        setSearchResults(null);
        return;
      }
      searchTimeout.current = setTimeout(() => {
        searchMemories.mutate(
          { query: query.trim(), projectId },
          {
            onSuccess: (data) => setSearchResults(data.results ?? []),
            onError: () => setSearchResults([]),
          },
        );
      }, 300);
    },
    [projectId, searchMemories],
  );

  const displayMemories = searchResults ?? memories;

  const containerClasses =
    searchResults !== null || (memories && memories.length > 0)
      ? "grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3"
      : "";

  if (isLoading) {
    return (
      <motion.div
        variants={container}
        initial="initial"
        animate="animate"
        className="flex flex-col gap-6 p-6"
      >
        <div className="flex items-center justify-between">
          <motion.div variants={item}>
            <Skeleton className="h-8 w-36" />
          </motion.div>
          <motion.div variants={item}>
            <Skeleton className="h-9 w-28 rounded-lg" />
          </motion.div>
        </div>
        <motion.div variants={item} className="flex gap-3">
          <Skeleton className="h-9 w-64 rounded-lg" />
          <Skeleton className="h-9 w-24 rounded-lg" />
        </motion.div>
        <motion.div
          variants={item}
          className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3"
        >
          {Array.from({ length: 6 }).map((_, i) => (
            // biome-ignore lint/suspicious/noArrayIndexKey: static skeleton list
            <Skeleton key={i} className="h-40 rounded-xl" />
          ))}
        </motion.div>
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 20 }}
      className="max-w-5xl mx-auto space-y-6 p-6"
    >
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-lg font-semibold text-white/80">Memories</h1>
          <p className="text-xs text-white/30 mt-1">Browse and manage your memory collection</p>
        </div>
        <Link
          href="/ingest"
          className="px-3 py-2 bg-amber-500/10 border border-amber-500/20 rounded-lg text-xs text-amber-400 hover:bg-amber-500/20 transition-colors"
        >
          Import
        </Link>
      </div>

      <div className="relative">
        <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-white/20" />
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => handleSearch(e.target.value)}
          placeholder="Search memories..."
          className="w-full h-9 bg-white/5 border border-white/10 rounded-lg pl-9 pr-3 text-sm text-white/60 focus:outline-none focus:border-amber-500/50 placeholder-white/20"
        />
      </div>

      {searchResults !== null && searchResults.length === 0 && (
        <div className="flex flex-col items-center gap-3 py-16 text-center">
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-white/5">
            <Search size={20} className="text-white/30" />
          </div>
          <p className="text-sm text-white/50">No results for &quot;{searchQuery}&quot;</p>
          <p className="text-xs text-white/30">Try a different search term</p>
        </div>
      )}

      {searchResults === null && memories.length === 0 && (
        <div className="flex flex-col items-center gap-3 py-16 text-center">
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-white/5">
            <Brain size={20} className="text-white/30" />
          </div>
          <p className="text-sm text-white/50">No memories yet</p>
          <p className="text-xs text-white/30 max-w-sm">
            Import data or use the recall feature to start building your memory collection.
          </p>
          <Link
            href="/ingest"
            className="mt-2 px-3 py-2 bg-amber-500/10 border border-amber-500/20 rounded-lg text-xs text-amber-400 hover:bg-amber-500/20 transition-colors"
          >
            Import your first data
          </Link>
        </div>
      )}

      <AnimatePresence>
        {displayMemories.length > 0 && (
          <motion.div
            variants={container}
            initial="initial"
            animate="animate"
            className={containerClasses}
          >
            {displayMemories.map((memory) => (
              <MemoryCard
                key={memory.id}
                memory={memory}
                onDelete={() => {}}
                onArchive={() => {}}
              />
            ))}
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}
