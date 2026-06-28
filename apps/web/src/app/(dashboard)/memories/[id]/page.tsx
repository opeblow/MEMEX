"use client";

import { useArchiveMemory, useDeleteMemory, useMemory, useRestoreMemory } from "@/hooks";
import { Skeleton } from "@memex/ui";
import { AnimatePresence, motion } from "framer-motion";
import {
  Archive,
  ArrowLeft,
  Brain,
  FileText,
  Globe,
  Hash,
  Image,
  MessageSquare,
  Music,
  RefreshCw,
  Tag,
  Trash2,
  Video,
} from "lucide-react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { useCallback, useState } from "react";

const MEMORY_TYPE_ICONS: Record<string, React.ReactNode> = {
  text: <FileText size={16} />,
  file: <FileText size={16} />,
  code: <FileText size={16} />,
  image: <Image size={16} />,
  audio: <Music size={16} />,
  video: <Video size={16} />,
  url: <Globe size={16} />,
  conversation: <MessageSquare size={16} />,
  meeting_note: <FileText size={16} />,
  github_issue: <FileText size={16} />,
  support_ticket: <MessageSquare size={16} />,
  research: <Brain size={16} />,
  decision: <Brain size={16} />,
};

function DetailRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-center gap-3 py-2">
      <span className="text-xs text-white/40 w-24 shrink-0">{label}</span>
      <span className="text-xs text-white/70">{value}</span>
    </div>
  );
}

export default function MemoryDetailPage() {
  const params = useParams();
  const id = params.id as string;
  const { data: memory, isLoading, isError } = useMemory(id);
  const deleteMemory = useDeleteMemory();
  const archiveMemory = useArchiveMemory();
  const restoreMemory = useRestoreMemory();
  const [deleted, setDeleted] = useState(false);

  const handleDelete = useCallback(() => {
    deleteMemory.mutate({ memoryId: id, permanent: false });
    setDeleted(true);
  }, [deleteMemory, id]);

  const handleArchive = useCallback(() => {
    archiveMemory.mutate(id);
  }, [archiveMemory, id]);

  const handleRestore = useCallback(() => {
    restoreMemory.mutate(id);
  }, [restoreMemory, id]);

  if (isLoading) {
    return (
      <div className="max-w-3xl mx-auto p-6 space-y-6">
        <Skeleton className="h-5 w-24" />
        <Skeleton className="h-8 w-64" />
        <div className="space-y-4">
          <Skeleton className="h-4 w-full" />
          <Skeleton className="h-4 w-3/4" />
          <Skeleton className="h-4 w-1/2" />
        </div>
      </div>
    );
  }

  if (isError || !memory) {
    return (
      <div className="flex items-center justify-center h-64">
        <p className="text-sm text-white/30">Memory not found</p>
      </div>
    );
  }

  if (deleted) {
    return (
      <div className="flex flex-col items-center gap-4 py-24 text-center">
        <div className="flex h-12 w-12 items-center justify-center rounded-full bg-white/5">
          <Trash2 size={20} className="text-white/30" />
        </div>
        <p className="text-sm text-white/50">Memory deleted</p>
        <Link
          href="/memories"
          className="px-3 py-2 bg-white/5 border border-white/10 rounded-lg text-xs text-white/60 hover:text-white/80 transition-colors"
        >
          Back to memories
        </Link>
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 20 }}
      className="max-w-3xl mx-auto space-y-6 p-6"
    >
      <Link
        href="/memories"
        className="inline-flex items-center gap-1.5 text-xs text-white/40 hover:text-white/60 transition-colors"
      >
        <ArrowLeft size={14} />
        Back to memories
      </Link>

      <div className="flex items-start gap-4">
        <div className="p-3 rounded-xl bg-white/5 shrink-0">
          {MEMORY_TYPE_ICONS[memory.memory_type] || (
            <FileText size={20} className="text-white/40" />
          )}
        </div>
        <div className="flex-1 min-w-0">
          <h1 className="text-xl font-semibold text-white/90 break-words">
            {memory.title || "Untitled"}
          </h1>
          <div className="flex items-center gap-2 mt-2 flex-wrap">
            <span className="text-[10px] px-1.5 py-0.5 rounded bg-white/5 text-white/40 border border-white/10">
              {memory.memory_type}
            </span>
            <span
              className={`px-1.5 py-0.5 rounded text-[10px] border ${
                memory.importance >= 8
                  ? "bg-amber-500/15 text-amber-400 border-amber-500/20"
                  : memory.importance >= 5
                    ? "bg-cyan-500/10 text-cyan-400 border-cyan-500/15"
                    : "bg-white/5 text-white/50 border-white/10"
              }`}
            >
              {memory.importance.toFixed(1)} importance
            </span>
            <span
              className={`px-1.5 py-0.5 rounded text-[10px] ${
                memory.status === "archived"
                  ? "bg-yellow-500/10 text-yellow-400"
                  : memory.status === "failed"
                    ? "bg-red-500/10 text-red-400"
                    : memory.status === "processing"
                      ? "bg-purple-500/10 text-purple-400"
                      : "bg-emerald-500/10 text-emerald-400"
              }`}
            >
              {memory.status}
            </span>
          </div>
        </div>
      </div>

      <div className="bg-white/[0.02] border border-white/10 rounded-xl p-4 space-y-1">
        <DetailRow label="Type" value={memory.memory_type} />
        {memory.source && <DetailRow label="Source" value={memory.source} />}
        {memory.source_url && <DetailRow label="Source URL" value={memory.source_url} />}
        <DetailRow label="Created" value={new Date(memory.created_at).toLocaleString()} />
        <DetailRow label="Updated" value={new Date(memory.updated_at).toLocaleString()} />
        {memory.token_count != null && (
          <DetailRow label="Tokens" value={memory.token_count.toLocaleString()} />
        )}
        {memory.chunk_count != null && (
          <DetailRow label="Chunks" value={memory.chunk_count.toLocaleString()} />
        )}
      </div>

      {memory.tags && memory.tags.length > 0 && (
        <div>
          <div className="flex items-center gap-1.5 mb-2">
            <Tag size={12} className="text-white/30" />
            <span className="text-xs text-white/40">Tags</span>
          </div>
          <div className="flex gap-1.5 flex-wrap">
            {memory.tags.map((tag) => (
              <span
                key={tag}
                className="px-2 py-1 rounded-lg text-xs bg-white/5 text-white/50 border border-white/10"
              >
                {tag}
              </span>
            ))}
          </div>
        </div>
      )}

      {memory.content_preview && (
        <div>
          <div className="flex items-center gap-1.5 mb-2">
            <FileText size={12} className="text-white/30" />
            <span className="text-xs text-white/40">Content</span>
          </div>
          <div className="p-4 bg-white/[0.02] border border-white/10 rounded-xl">
            <p className="text-sm text-white/60 whitespace-pre-wrap leading-relaxed">
              {memory.content_preview}
            </p>
          </div>
        </div>
      )}

      <AnimatePresence>
        {memory.metadata && Object.keys(memory.metadata).length > 0 && (
          <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: "auto" }}>
            <div className="flex items-center gap-1.5 mb-2">
              <Hash size={12} className="text-white/30" />
              <span className="text-xs text-white/40">Metadata</span>
            </div>
            <div className="p-4 bg-white/[0.02] border border-white/10 rounded-xl">
              <pre className="text-xs text-white/40 whitespace-pre-wrap">
                {JSON.stringify(memory.metadata, null, 2)}
              </pre>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      <div className="flex items-center gap-2 pt-2 border-t border-white/5">
        {memory.status === "archived" ? (
          <button
            type="button"
            onClick={handleRestore}
            disabled={restoreMemory.isPending}
            className="flex items-center gap-1.5 px-3 py-2 bg-cyan-500/10 border border-cyan-500/20 rounded-lg text-xs text-cyan-400 hover:bg-cyan-500/20 disabled:opacity-50 transition-colors"
          >
            <RefreshCw size={14} />
            {restoreMemory.isPending ? "Restoring..." : "Restore"}
          </button>
        ) : (
          <button
            type="button"
            onClick={handleArchive}
            disabled={archiveMemory.isPending}
            className="flex items-center gap-1.5 px-3 py-2 bg-white/5 border border-white/10 rounded-lg text-xs text-white/50 hover:text-cyan-400 hover:border-cyan-500/20 disabled:opacity-50 transition-colors"
          >
            <Archive size={14} />
            {archiveMemory.isPending ? "Archiving..." : "Archive"}
          </button>
        )}
        <button
          type="button"
          onClick={handleDelete}
          disabled={deleteMemory.isPending}
          className="flex items-center gap-1.5 px-3 py-2 bg-white/5 border border-white/10 rounded-lg text-xs text-white/50 hover:text-red-400 hover:border-red-500/20 disabled:opacity-50 transition-colors"
        >
          <Trash2 size={14} />
          {deleteMemory.isPending ? "Deleting..." : "Delete"}
        </button>
      </div>
    </motion.div>
  );
}
