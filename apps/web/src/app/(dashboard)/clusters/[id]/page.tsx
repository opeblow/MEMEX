"use client";

import { useMemories } from "@/hooks";
import { useUIStore } from "@/lib/stores/ui-store";
import type { MemoryDetail } from "@memex/types";
import { Skeleton } from "@memex/ui";
import { motion } from "framer-motion";
import { ArrowLeft, Brain, FileText, Image, MessageSquare, Music, Video } from "lucide-react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";

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

export default function ClusterDetailPage() {
  const params = useParams();
  const id = params.id as string;
  const activeProjectId = useUIStore((s) => s.activeProjectId);
  const projectId = activeProjectId || "default";

  const { data: allMemories = [], isLoading } = useMemories(projectId, 200);
  const [filtered, setFiltered] = useState<MemoryDetail[]>([]);
  const [clusterLabel, setClusterLabel] = useState("");

  useEffect(() => {
    const decoded = decodeURIComponent(id);
    setClusterLabel(decoded);
    if (allMemories.length > 0) {
      const matches = allMemories.filter(
        (m) =>
          m.memory_type === decoded ||
          m.tags?.some((t) => t.toLowerCase() === decoded.toLowerCase()),
      );
      setFiltered(matches);
    }
  }, [id, allMemories]);

  if (isLoading) {
    return (
      <div className="max-w-3xl mx-auto p-6 space-y-4">
        <Skeleton className="h-5 w-24" />
        <Skeleton className="h-8 w-48" />
        {Array.from({ length: 5 }).map((_, i) => (
          // biome-ignore lint/suspicious/noArrayIndexKey: static skeleton list
          <Skeleton key={i} className="h-16 w-full rounded-xl" />
        ))}
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
        href="/clusters"
        className="inline-flex items-center gap-1.5 text-xs text-white/40 hover:text-white/60 transition-colors"
      >
        <ArrowLeft size={14} />
        Back to insights
      </Link>

      <div>
        <h1 className="text-lg font-semibold text-white/80 capitalize">{clusterLabel}</h1>
        <p className="text-xs text-white/30 mt-1">
          {filtered.length} related {filtered.length === 1 ? "memory" : "memories"}
        </p>
      </div>

      {filtered.length === 0 && (
        <div className="flex flex-col items-center gap-3 py-16 text-center">
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-white/5">
            <Brain size={20} className="text-white/30" />
          </div>
          <p className="text-sm text-white/50">No memories found</p>
          <p className="text-xs text-white/30 max-w-sm">
            No memories match &quot;{clusterLabel}&quot;.
          </p>
        </div>
      )}

      <div className="space-y-2">
        {filtered.map((memory) => (
          <Link
            key={memory.id}
            href={`/memories/${memory.id}`}
            className="flex items-center gap-3 px-4 py-3 rounded-xl bg-white/[0.02] border border-white/10 hover:bg-white/5 hover:border-white/20 transition-all group"
          >
            <div className="p-1.5 rounded-lg bg-white/5 shrink-0">
              {MEMORY_TYPE_ICONS[memory.memory_type] || (
                <FileText size={14} className="text-white/40" />
              )}
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm text-white/70 truncate group-hover:text-white/90 transition-colors">
                {memory.title || "Untitled"}
              </p>
              {memory.content_preview && (
                <p className="text-xs text-white/30 mt-0.5 line-clamp-1">
                  {memory.content_preview}
                </p>
              )}
            </div>
            <span
              className={`px-1.5 py-0.5 rounded text-[10px] border shrink-0 ${
                memory.importance >= 8
                  ? "bg-amber-500/15 text-amber-400 border-amber-500/20"
                  : memory.importance >= 5
                    ? "bg-cyan-500/10 text-cyan-400 border-cyan-500/15"
                    : "bg-white/5 text-white/40 border-white/10"
              }`}
            >
              {memory.importance.toFixed(1)}
            </span>
          </Link>
        ))}
      </div>
    </motion.div>
  );
}
