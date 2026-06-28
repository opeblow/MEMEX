"use client";

import type { MemoryDetail } from "@memex/types";
import { AnimatePresence, motion } from "framer-motion";
import { Archive, Calendar, FileText, Globe, Tag, Trash2, X } from "lucide-react";

interface MemoryDetailPanelProps {
  memory: MemoryDetail | null;
  onClose: () => void;
  onDelete: (id: string) => void;
  onArchive: (id: string) => void;
}

export function MemoryDetailPanel({
  memory,
  onClose,
  onDelete,
  onArchive,
}: MemoryDetailPanelProps) {
  return (
    <AnimatePresence>
      {memory && (
        <motion.div
          initial={{ opacity: 0, x: 300 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: 300 }}
          transition={{ type: "spring", damping: 25, stiffness: 200 }}
          className="fixed right-0 top-0 h-full w-full md:w-96 bg-black/90 backdrop-blur-xl border-l border-white/10 z-50 overflow-y-auto"
        >
          <div className="p-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-lg font-semibold text-white truncate pr-4">
                {memory.title || "Untitled"}
              </h2>
              <button
                type="button"
                onClick={onClose}
                className="text-white/40 hover:text-white transition-colors"
              >
                <X size={18} />
              </button>
            </div>

            <div className="space-y-4">
              <div className="flex items-center gap-2 text-sm text-white/50">
                <FileText size={14} />
                <span className="capitalize">{memory.memory_type}</span>
              </div>

              <div className="flex items-center gap-2 text-sm text-white/50">
                <Globe size={14} />
                <span>{memory.source || "direct_input"}</span>
              </div>

              <div className="flex items-center gap-2 text-sm text-white/50">
                <Calendar size={14} />
                <span>{new Date(memory.created_at).toLocaleDateString()}</span>
              </div>

              <div className="flex items-center gap-2 text-sm text-white/50">
                <span className="font-mono text-xs">ID:</span>
                <span className="font-mono text-xs truncate">{memory.id.slice(0, 8)}...</span>
              </div>

              {memory.tags && memory.tags.length > 0 && (
                <div className="flex items-start gap-2">
                  <Tag size={14} className="mt-0.5 text-white/50" />
                  <div className="flex flex-wrap gap-1.5">
                    {memory.tags.map((tag) => (
                      <span
                        key={tag}
                        className="px-2 py-0.5 text-xs rounded-full bg-white/5 text-white/60 border border-white/10"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              <div className="flex items-center gap-3 text-sm">
                <span className="text-white/50">Importance</span>
                <div className="flex-1 h-1.5 bg-white/10 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-amber-400 rounded-full transition-all"
                    style={{ width: `${memory.importance * 100}%` }}
                  />
                </div>
                <span className="text-white/60 font-mono text-xs">
                  {Math.round(memory.importance * 100)}%
                </span>
              </div>

              {memory.content_preview && (
                <div className="pt-4 border-t border-white/10">
                  <p className="text-sm text-white/70 leading-relaxed whitespace-pre-wrap">
                    {memory.content_preview}
                  </p>
                </div>
              )}
            </div>

            <div className="mt-8 flex gap-3">
              <button
                type="button"
                onClick={() => onArchive(memory.id)}
                className="flex-1 flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg border border-white/10 text-white/60 hover:text-white hover:border-white/30 transition-all text-sm"
              >
                <Archive size={14} />
                Archive
              </button>
              <button
                type="button"
                onClick={() => onDelete(memory.id)}
                className="flex-1 flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg border border-red-500/20 text-red-400 hover:text-red-300 hover:border-red-500/40 transition-all text-sm"
              >
                <Trash2 size={14} />
                Delete
              </button>
            </div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
