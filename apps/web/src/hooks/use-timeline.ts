"use client";

import { api } from "@/lib/api/client";
import type { TimelineQuery, TimelineResponse } from "@memex/types";
import { useQuery } from "@tanstack/react-query";

export function useTimeline(query: TimelineQuery) {
  return useQuery({
    queryKey: ["timeline", query],
    queryFn: () => api.post<TimelineResponse>("/api/v1/memex/timeline", query),
    enabled: !!query.projectId,
  });
}

export function useTimelineSummary(projectId: string | null) {
  return useQuery({
    queryKey: ["timeline-summary", projectId],
    queryFn: () => api.get<Record<string, unknown>>(`/api/v1/memex/timeline/summary/${projectId}`),
    enabled: !!projectId,
  });
}
