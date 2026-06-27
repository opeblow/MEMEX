"use client";

import { useMutation } from "@tanstack/react-query";
import { api } from "@/lib/api/client";

interface RememberParams {
  data: string | File;
  projectId: string;
  sessionId?: string;
  memoryType?: string;
  title?: string;
  tags?: string[];
  runInBackground?: boolean;
}

interface RememberResponse {
  memoryId: string;
  datasetId: string;
  chunkCount: number;
  tokenCount: number;
  processingTimeMs: number;
  status: string;
}

export function useRemember() {
  return useMutation({
    mutationFn: async (params: RememberParams) => {
      const formData = new FormData();

      if (typeof params.data === "string") {
        formData.append("data", params.data);
      } else {
        formData.append("file", params.data);
      }

      formData.append("project_id", params.projectId);
      if (params.sessionId) formData.append("session_id", params.sessionId);
      if (params.memoryType) formData.append("memory_type", params.memoryType);
      if (params.title) formData.append("title", params.title);
      if (params.tags) formData.append("tags", JSON.stringify(params.tags));
      if (params.runInBackground) {
        formData.append("run_in_background", "true");
      }

      return api.post<RememberResponse>("/api/v1/memex/remember", formData);
    },
  });
}
