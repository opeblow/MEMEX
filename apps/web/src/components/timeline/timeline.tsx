"use client";

import type { TimelineEvent } from "@memex/types";
import { motion } from "framer-motion";
import { Archive, Plus, RefreshCw, RotateCcw, Search, Trash2 } from "lucide-react";
import React, { useMemo } from "react";

const EVENT_ICONS: Record<string, typeof Plus> = {
  "memory.created": Plus,
  "memory.recalled": Search,
  "memory.improved": RefreshCw,
  "memory.deleted": Trash2,
  "memory.archived": Archive,
  "memory.restored": RotateCcw,
};

const EVENT_COLORS: Record<string, string> = {
  "memory.created": "text-emerald-400 border-emerald-500/30",
  "memory.recalled": "text-sky-400 border-sky-500/30",
  "memory.improved": "text-purple-400 border-purple-500/30",
  "memory.deleted": "text-red-400 border-red-500/30",
  "memory.archived": "text-amber-400 border-amber-500/30",
  "memory.restored": "text-blue-400 border-blue-500/30",
};

interface TimelineProps {
  events: TimelineEvent[];
  onEventClick?: (event: TimelineEvent) => void;
}

export const Timeline = React.memo(function Timeline({ events, onEventClick }: TimelineProps) {
  const eventItems = useMemo(
    () =>
      events.map((event, index) => {
        const Icon = EVENT_ICONS[event.event_type] || Plus;
        const colorClass = EVENT_COLORS[event.event_type] || "text-white/40 border-white/10";
        return { event, index, Icon, colorClass };
      }),
    [events],
  );

  if (events.length === 0) {
    return (
      <div className="text-center py-12" aria-live="polite">
        <p className="text-sm text-white/30">No timeline events yet</p>
      </div>
    );
  }

  return (
    <ol className="relative" aria-label="Memory timeline">
      <div className="absolute left-[19px] top-2 bottom-2 w-px bg-white/5" />
      <div className="space-y-0">
        {eventItems.map(({ event, index, Icon, colorClass }) => {
          return (
            <motion.button
              key={event.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.03 }}
              onClick={() => onEventClick?.(event)}
              className="relative flex items-start gap-4 w-full py-3 px-4 hover:bg-white/5 rounded-lg transition-colors text-left"
            >
              <div
                className={`relative z-10 flex items-center justify-center w-10 h-10 rounded-full border bg-black/50 ${colorClass}`}
              >
                <Icon size={14} />
              </div>
              <div className="flex-1 min-w-0 pt-1.5">
                <p className="text-sm text-white/80 capitalize">
                  {event.event_type.replace(/memory\./, "").replace(/_/g, " ")}
                </p>
                {event.data && Object.keys(event.data).length > 0 && (
                  <p className="text-xs text-white/40 truncate mt-0.5">
                    {JSON.stringify(event.data).slice(0, 100)}
                  </p>
                )}
              </div>
              <span className="text-xs text-white/20 shrink-0 pt-1.5 font-mono">
                {new Date(event.created_at).toLocaleTimeString([], {
                  hour: "2-digit",
                  minute: "2-digit",
                })}
              </span>
            </motion.button>
          );
        })}
      </div>
    </ol>
  );
});
