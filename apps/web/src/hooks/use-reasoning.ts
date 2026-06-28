"use client";

import type { Explanation, ReasoningResponse, TrailStep } from "@memex/types";
import { useMutation } from "@tanstack/react-query";
import { useCallback, useRef, useState } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export function useReason() {
  const mutation = useMutation({
    mutationFn: async (params: {
      query: string;
      projectId: string;
      includeTrail?: boolean;
      includeExplanation?: boolean;
    }): Promise<ReasoningResponse> => {
      const res = await fetch(`${API_BASE}/api/v1/memex/reason`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          query: params.query,
          project_id: params.projectId,
          include_trail: params.includeTrail ?? true,
          include_explanation: params.includeExplanation ?? true,
          top_k: 20,
        }),
      });
      if (!res.ok) throw new Error("Reasoning failed");
      return res.json();
    },
  });

  const answer = mutation.data?.answer ?? null;
  const explanation = mutation.data?.explanation ?? null;
  const trail = mutation.data?.trail ?? null;
  const trailId = mutation.data?.trail_id ?? null;
  const confidence = explanation?.confidence ?? null;
  const processingTimeMs = mutation.data?.processing_time_ms ?? null;

  return {
    execute: mutation.mutate,
    answer,
    explanation,
    trail,
    trailId,
    confidence,
    isLoading: mutation.isPending,
    processingTimeMs,
  } as const;
}

export function useStreamReason() {
  const [answer, setAnswer] = useState("");
  const [steps, setSteps] = useState<TrailStep[]>([]);
  const [memoryIds, setMemoryIds] = useState<string[]>([]);
  const [isStreaming, setIsStreaming] = useState(false);
  const [isComplete, setIsComplete] = useState(false);
  const [trailId, setTrailId] = useState<string | null>(null);
  const [explanation, setExplanation] = useState<Explanation | null>(null);
  const abortRef = useRef<AbortController | null>(null);

  const streamReason = useCallback(async (query: string, projectId: string) => {
    abortRef.current?.abort();
    abortRef.current = new AbortController();
    setAnswer("");
    setSteps([]);
    setMemoryIds([]);
    setIsComplete(false);
    setIsStreaming(true);

    try {
      const res = await fetch(`${API_BASE}/api/v1/memex/reason/stream`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          query,
          project_id: projectId,
          include_trail: true,
          include_explanation: true,
          top_k: 20,
        }),
        signal: abortRef.current.signal,
      });

      if (!res.body) throw new Error("No response body");

      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n\n");
        buffer = lines.pop() ?? "";

        for (const line of lines) {
          if (!line.startsWith("data: ")) continue;
          try {
            const event = JSON.parse(line.slice(6));
            switch (event.event) {
              case "step":
                if (event.data.step && event.data.name) {
                  setSteps((prev) => [
                    ...prev,
                    {
                      step: event.data.step,
                      name: event.data.name,
                      description: event.data.status,
                      data: {},
                      memory_ids: event.data.memory_ids ?? [],
                      duration_ms: 0,
                    },
                  ]);
                }
                if (event.data.memory_ids) {
                  setMemoryIds(event.data.memory_ids);
                }
                break;
              case "token":
                setAnswer((prev) => prev + event.content);
                break;
              case "complete":
                setTrailId(event.data.trail_id ?? null);
                setExplanation(event.data.explanation ?? null);
                setIsComplete(true);
                setIsStreaming(false);
                break;
            }
          } catch {
            // Ignore parse errors
          }
        }
      }
    } catch {
      setIsStreaming(false);
    }
  }, []);

  return {
    streamReason,
    answer,
    steps,
    memoryIds,
    isStreaming,
    isComplete,
    trailId,
    explanation,
  } as const;
}
