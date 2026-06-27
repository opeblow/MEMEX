"use client";

import { useState, useEffect, useCallback } from "react";
import dynamic from "next/dynamic";
import { Search, Command, Brain } from "lucide-react";
import { CommandPalette } from "@/components/search/command-palette";
import { useMemories, useDeleteMemory, useArchiveMemory } from "@/hooks/use-memory";
import { useTimeline } from "@/hooks/use-timeline";
import type { MemoryDetail, TimelineEvent } from "@memex/types";
import { useUIStore } from "@/lib/stores/ui-store";
import { useRouter } from "next/navigation";

const MemoryUniverse = dynamic(
  () => import("@/components/memory-universe/memory-universe").then((m) => m.MemoryUniverse),
  { ssr: false },
);

const Timeline = dynamic(
  () => import("@/components/timeline/timeline").then((m) => m.Timeline),
  { ssr: false },
);

export default function RecallPage() {
  const router = useRouter();
  const [view, setView] = useState<"universe" | "timeline">("universe");
  const [commandOpen, setCommandOpen] = useState(false);
  const [, setSelectedMemory] = useState<MemoryDetail | null>(null);
  const activeProjectId = useUIStore((s) => s.activeProjectId);
  const projectId = activeProjectId || "default";

  const { data: memories = [] } = useMemories(projectId);
  const { data: timelineData } = useTimeline({
    projectId,
    limit: 50,
  });
  const deleteMemory = useDeleteMemory();
  const archiveMemory = useArchiveMemory();

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();
        setCommandOpen(true);
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  const handleDelete = useCallback(
    (id: string) => {
      deleteMemory.mutate({ memoryId: id });
    },
    [deleteMemory],
  );

  const handleArchive = useCallback(
    (id: string) => {
      archiveMemory.mutate(id);
    },
    [archiveMemory],
  );

  const handleSelectMemory = useCallback((memory: MemoryDetail) => {
    setSelectedMemory(memory);
  }, []);

  const handleTimelineEventClick = useCallback(
    (event: TimelineEvent) => {
      const memoryId = event.data?.memory_id as string | undefined;
      if (memoryId) {
        const memory = memories.find((m) => m.id === memoryId);
        if (memory) {
          handleSelectMemory(memory);
        }
      }
    },
    [memories, handleSelectMemory],
  );

  return (
    <div className="relative w-full h-[calc(100vh-4rem)] overflow-hidden">
      <div className="absolute top-4 left-4 z-10 flex items-center gap-3">
        <button
          onClick={() => setCommandOpen(true)}
          className="flex items-center gap-2 px-3 py-2 bg-black/50 backdrop-blur-md border border-white/10 rounded-lg text-sm text-white/50 hover:text-white/80 transition-colors"
        >
          <Search size={14} />
          <span>Search memories...</span>
          <kbd className="hidden sm:inline-flex items-center gap-1 px-1.5 py-0.5 text-xs text-white/30 bg-white/10 rounded">
            <Command size={10} />
            K
          </kbd>
        </button>
      </div>

      <div className="absolute top-4 right-4 z-10 flex items-center gap-2">
        <div className="flex bg-black/50 backdrop-blur-md border border-white/10 rounded-lg overflow-hidden">
          <button
            onClick={() => setView("universe")}
            className={`px-3 py-2 text-xs transition-colors ${
              view === "universe"
                ? "text-white bg-white/10"
                : "text-white/40 hover:text-white/60"
            }`}
          >
            Universe
          </button>
          <button
            onClick={() => setView("timeline")}
            className={`px-3 py-2 text-xs transition-colors ${
              view === "timeline"
                ? "text-white bg-white/10"
                : "text-white/40 hover:text-white/60"
            }`}
          >
            Timeline
          </button>
        </div>
        <button
          onClick={() => router.push("/chat")}
          className="flex items-center gap-2 px-3 py-2 bg-purple-500/10 border border-purple-500/30 rounded-lg text-xs text-purple-400 hover:bg-purple-500/20 transition-colors"
        >
          <Brain size={14} />
          Reason
        </button>
      </div>

      {view === "universe" ? (
        <MemoryUniverse
          memories={memories || []}
          onDelete={handleDelete}
          onArchive={handleArchive}
        />
      ) : (
        <div className="p-6 h-full overflow-y-auto">
          <Timeline
            events={(timelineData?.events || []) as TimelineEvent[]}
            onEventClick={handleTimelineEventClick}
          />
        </div>
      )}

      <CommandPalette
        isOpen={commandOpen}
        onClose={() => setCommandOpen(false)}
        onSelectMemory={handleSelectMemory}
        projectId={projectId}
        onOpenChat={() => router.push("/chat")}
      />
    </div>
  );
}
