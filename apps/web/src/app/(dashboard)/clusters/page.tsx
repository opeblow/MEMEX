"use client";

import { useMemories, useTimelineSummary } from "@/hooks";
import { useUIStore } from "@/lib/stores/ui-store";
import { Skeleton } from "@memex/ui";
import { motion } from "framer-motion";
import { Brain, Calendar, FileText } from "lucide-react";
import { useEffect, useState } from "react";

const MEMORY_TYPE_LABELS: Record<string, string> = {
  text: "Text",
  file: "File",
  code: "Code",
  image: "Image",
  audio: "Audio",
  video: "Video",
  url: "URL",
  conversation: "Conversation",
  meeting_note: "Meeting Note",
  github_issue: "GitHub Issue",
  support_ticket: "Support Ticket",
  research: "Research",
  decision: "Decision",
};

const MEMORY_TYPE_COLORS: Record<string, string> = {
  text: "bg-blue-500/10 text-blue-400",
  file: "bg-white/5 text-white/50",
  code: "bg-green-500/10 text-green-400",
  image: "bg-pink-500/10 text-pink-400",
  audio: "bg-purple-500/10 text-purple-400",
  video: "bg-red-500/10 text-red-400",
  url: "bg-cyan-500/10 text-cyan-400",
  conversation: "bg-yellow-500/10 text-yellow-400",
  meeting_note: "bg-orange-500/10 text-orange-400",
  github_issue: "bg-gray-500/10 text-gray-400",
  support_ticket: "bg-indigo-500/10 text-indigo-400",
  research: "bg-emerald-500/10 text-emerald-400",
  decision: "bg-amber-500/10 text-amber-400",
};

const container = {
  animate: {
    transition: { staggerChildren: 0.08 },
  },
};

const item = {
  initial: { opacity: 0, y: 16 },
  animate: { opacity: 1, y: 0, transition: { duration: 0.4, ease: "easeOut" } },
};

export default function ClustersPage() {
  const activeProjectId = useUIStore((s) => s.activeProjectId);
  const projectId = activeProjectId || "default";
  const [typeCounts, setTypeCounts] = useState<Record<string, number>>({});

  const { data: memories = [], isLoading: memoriesLoading } = useMemories(projectId, 200);
  const { data: timelineSummary, isLoading: summaryLoading } = useTimelineSummary(projectId);

  useEffect(() => {
    if (memories.length > 0) {
      const counts: Record<string, number> = {};
      for (const m of memories) {
        counts[m.memory_type] = (counts[m.memory_type] || 0) + 1;
      }
      setTypeCounts(counts);
    }
  }, [memories]);

  const isLoading = memoriesLoading || summaryLoading;

  const totalMemories = memories.length;
  const totalTypes = Object.keys(typeCounts).length;
  const sortedTypes = Object.entries(typeCounts).sort(([, a], [, b]) => b - a);
  const maxCount = Math.max(...Object.values(typeCounts), 1);

  const timelineEvents = (timelineSummary as { total_events?: number })?.total_events;

  if (isLoading) {
    return (
      <motion.div
        variants={container}
        initial="initial"
        animate="animate"
        className="flex flex-col gap-6 p-6 max-w-3xl mx-auto"
      >
        <motion.div variants={item}>
          <Skeleton className="h-8 w-44" />
        </motion.div>
        <motion.div variants={item}>
          <Skeleton className="h-4 w-64" />
        </motion.div>
        <motion.div variants={item} className="grid grid-cols-3 gap-4">
          <Skeleton className="h-28 rounded-xl" />
          <Skeleton className="h-28 rounded-xl" />
          <Skeleton className="h-28 rounded-xl" />
        </motion.div>
        <motion.div variants={item}>
          <Skeleton className="h-48 rounded-xl" />
        </motion.div>
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 20 }}
      className="max-w-3xl mx-auto space-y-6 p-6"
    >
      <div>
        <h1 className="text-lg font-semibold text-white/80">Insights</h1>
        <p className="text-xs text-white/30 mt-1">Memory statistics and distribution overview</p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="p-4 bg-white/[0.02] border border-white/10 rounded-xl">
          <div className="flex items-center gap-2 mb-2">
            <Brain size={14} className="text-amber-400" />
            <span className="text-xs text-white/40">Total Memories</span>
          </div>
          <p className="text-2xl font-bold text-white">{totalMemories}</p>
        </div>

        <div className="p-4 bg-white/[0.02] border border-white/10 rounded-xl">
          <div className="flex items-center gap-2 mb-2">
            <FileText size={14} className="text-cyan-400" />
            <span className="text-xs text-white/40">Memory Types</span>
          </div>
          <p className="text-2xl font-bold text-white">{totalTypes}</p>
        </div>

        <div className="p-4 bg-white/[0.02] border border-white/10 rounded-xl">
          <div className="flex items-center gap-2 mb-2">
            <Calendar size={14} className="text-purple-400" />
            <span className="text-xs text-white/40">Timeline Events</span>
          </div>
          <p className="text-2xl font-bold text-white">{timelineEvents ?? "—"}</p>
        </div>
      </div>

      {sortedTypes.length > 0 && (
        <div className="bg-white/[0.02] border border-white/10 rounded-xl p-4">
          <h2 className="text-xs font-semibold text-white/40 mb-3">Memory Type Distribution</h2>
          <div className="space-y-2">
            {sortedTypes.map(([type, count]) => {
              const pct = ((count / maxCount) * 100).toFixed(0);
              return (
                <div key={type} className="flex items-center gap-3">
                  <span
                    className={`w-20 text-[10px] px-1.5 py-0.5 rounded text-center ${
                      MEMORY_TYPE_COLORS[type] || "bg-white/5 text-white/40"
                    }`}
                  >
                    {MEMORY_TYPE_LABELS[type] || type}
                  </span>
                  <div className="flex-1 h-4 bg-white/5 rounded-full overflow-hidden">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${pct}%` }}
                      transition={{ duration: 0.8, ease: "easeOut" }}
                      className="h-full rounded-full bg-gradient-to-r from-amber-500/40 to-cyan-500/40"
                    />
                  </div>
                  <span className="text-xs text-white/40 w-8 text-right">{count}</span>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {totalMemories === 0 && (
        <div className="flex flex-col items-center gap-3 py-16 text-center">
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-white/5">
            <Brain size={20} className="text-white/30" />
          </div>
          <p className="text-sm text-white/50">No memories yet</p>
          <p className="text-xs text-white/30 max-w-sm">
            Insights will appear once you start adding memories.
          </p>
        </div>
      )}
    </motion.div>
  );
}
