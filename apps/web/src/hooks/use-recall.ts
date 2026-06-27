"use client";

import { useMutation } from "@tanstack/react-query";
import { api, ApiError } from "@/lib/api/client";
import type { RecallRequest, RecallResponse } from "@memex/types";

export function useRecall() {
  return useMutation({
    mutationFn: async (params: RecallRequest) => {
      return api.post<RecallResponse>("/api/v1/memex/recall", params);
    },
  });
}

export function useStreamingRecall() {
  return useMutation({
    mutationFn: async ({
      params,
      onToken,
      onDone,
      signal,
    }: {
      params: RecallRequest;
      onToken: (token: string) => void;
      onDone: (result: RecallResponse) => void;
      signal: AbortSignal;
    }) => {
      const response = await api.stream(
        "/api/v1/memex/recall",
        { ...params, stream: true },
        signal,
      );

      if (!response.ok) {
        throw new ApiError(
          response.status,
          "STREAM_ERROR",
          "Failed to start streaming recall",
        );
      }

      const reader = response.body?.getReader();
      if (!reader) throw new Error("No reader available");

      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n");
        buffer = lines.pop() ?? "";

        for (const line of lines) {
          if (line.startsWith("event: ")) continue;
          if (!line.startsWith("data: ")) continue;

          const data = JSON.parse(line.slice(6));

          if (data.token) {
            onToken(data.token);
          }
          if (data.done) {
            onDone(data);
          }
        }
      }
    },
  });
}
