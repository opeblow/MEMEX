"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api/client";
import type { ImportJob, ImportJobListResponse, ImportResponse, Source, SourceListResponse } from "@memex/types";

export function useImport(projectId: string) {
  return useMutation({
    mutationFn: async (data: { source_type: string; data?: string; url?: string; display_name?: string }) => {
      return api.post<ImportResponse>("/api/v1/memex/imports", {
        project_id: projectId,
        ...data,
      });
    },
  });
}

export function useUploadImport() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({ file, projectId, sourceType }: { file: File; projectId: string; sourceType: string }) => {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("project_id", projectId);
      formData.append("source_type", sourceType);
      const accessToken = localStorage.getItem("memex_access_token");
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/v1/memex/imports/upload`,
        {
          method: "POST",
          headers: accessToken ? { Authorization: `Bearer ${accessToken}` } : {},
          body: formData,
        },
      );
      if (!res.ok) throw new Error("Upload failed");
      return res.json() as Promise<ImportResponse>;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["importJobs"] });
    },
  });
}

export function useImportJobs(projectId: string, limit = 20) {
  return useQuery({
    queryKey: ["importJobs", projectId, limit],
    queryFn: () =>
      api.get<ImportJobListResponse>(
        `/api/v1/memex/imports?project_id=${projectId}&limit=${limit}`,
      ),
    enabled: !!projectId,
    refetchInterval: (query) => {
      const data = query.state.data;
      if (!data) return 3000;
      const hasActive = data.jobs.some((j: ImportJob) => j.status === "running" || j.status === "queued");
      return hasActive ? 2000 : false;
    },
  });
}

export function useCancelImport() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (jobId: string) => {
      return api.delete<{ status: string }>(`/api/v1/memex/imports/${jobId}`);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["importJobs"] });
    },
  });
}

export function useSources(projectId: string, limit = 50) {
  return useQuery({
    queryKey: ["sources", projectId, limit],
    queryFn: () =>
      api.get<SourceListResponse>(
        `/api/v1/memex/sources?project_id=${projectId}&limit=${limit}`,
      ),
    enabled: !!projectId,
  });
}

export function useSource(sourceId: string | null) {
  return useQuery({
    queryKey: ["source", sourceId],
    queryFn: () =>
      api.get<Source>(`/api/v1/memex/sources/${sourceId}`),
    enabled: !!sourceId,
  });
}

export function useSourceMemories(sourceId: string | null) {
  return useQuery({
    queryKey: ["sourceMemories", sourceId],
    queryFn: () =>
      api.get(`/api/v1/memex/sources/${sourceId}/memories`),
    enabled: !!sourceId,
  });
}
