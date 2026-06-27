"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api/client";
import type {
  MemoryDetail,
  SearchRequest,
  SearchResponse,
} from "@memex/types";

export function useMemory(memoryId: string | null) {
  return useQuery({
    queryKey: ["memory", memoryId],
    queryFn: () =>
      api.get<MemoryDetail>(`/api/v1/memex/memory/${memoryId}`),
    enabled: !!memoryId,
  });
}

export function useMemories(projectId: string, limit = 50, offset = 0) {
  return useQuery({
    queryKey: ["memories", projectId, limit, offset],
    queryFn: () =>
      api.get<MemoryDetail[]>(
        `/api/v1/memex/memory?project_id=${projectId}&limit=${limit}&offset=${offset}`,
      ),
    enabled: !!projectId,
  });
}

export function useSearchMemories() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (params: SearchRequest) => {
      return api.post<SearchResponse>("/api/v1/memex/memory/search", params);
    },
    onSuccess: (data) => {
      (data.results || []).forEach((mem) => {
        queryClient.setQueryData(["memory", mem.id], mem);
      });
    },
  });
}

export function useDeleteMemory() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({
      memoryId,
      permanent = false,
    }: {
      memoryId: string;
      permanent?: boolean;
    }) => {
      return api.delete<{ status: string }>(
        `/api/v1/memex/memory/${memoryId}?permanent=${permanent}`,
      );
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["memories"] });
    },
  });
}

export function useArchiveMemory() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (memoryId: string) => {
      return api.post<{ status: string }>(
        `/api/v1/memex/memory/${memoryId}/archive`,
      );
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["memories"] });
    },
  });
}

export function useRestoreMemory() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (memoryId: string) => {
      return api.post<{ status: string }>(
        `/api/v1/memex/memory/${memoryId}/restore`,
      );
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["memories"] });
    },
  });
}

export function useUpdateMemory() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({
      memoryId,
      ...data
    }: {
      memoryId: string;
      title?: string;
      tags?: string[];
      importance?: number;
    }) => {
      return api.patch<MemoryDetail>(
        `/api/v1/memex/memory/${memoryId}`,
        data,
      );
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["memories"] });
      queryClient.invalidateQueries({ queryKey: ["memory"] });
    },
  });
}
