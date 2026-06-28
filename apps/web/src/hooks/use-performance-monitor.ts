"use client";

import { useCallback, useEffect, useRef } from "react";

interface PerformanceMetrics {
  timeToInteractive: number | null;
  renderTime: number | null;
}

type MarkName = `${string}-start` | `${string}-end`;

const marks = new Map<string, number>();

export function mark(name: MarkName) {
  if (typeof performance === "undefined") return;
  performance.mark(name);
  marks.set(name, performance.now());
}

interface UsePerformanceMonitorOptions {
  featureName: string;
  report?: (metrics: PerformanceMetrics) => void;
}

export function usePerformanceMonitor({ featureName, report }: UsePerformanceMonitorOptions) {
  const startRef = useRef<number>(0);
  const reportedRef = useRef(false);

  useEffect(() => {
    startRef.current = performance.now();
    mark(`${featureName}-start`);
  }, [featureName]);

  useEffect(() => {
    const end = performance.now();
    const renderTime = end - startRef.current;
    mark(`${featureName}-end`);

    let timeToInteractive: number | null = null;
    try {
      performance.measure(featureName, `${featureName}-start`, `${featureName}-end`);
      const entries = performance.getEntriesByName(featureName);
      const lastEntry = entries[entries.length - 1];
      if (lastEntry) {
        timeToInteractive = lastEntry.duration;
      }
    } catch {
      // measure may fail if marks don't exist
    }

    const metrics: PerformanceMetrics = {
      timeToInteractive,
      renderTime,
    };

    if (!reportedRef.current) {
      reportedRef.current = true;
      report?.(metrics);
    }
  }, [featureName, report]);
}

export function useRenderTiming() {
  const renderStart = useRef(performance.now());

  const getMetrics = useCallback((): PerformanceMetrics => {
    const now = performance.now();
    return {
      timeToInteractive: null,
      renderTime: now - renderStart.current,
    };
  }, []);

  return { getMetrics };
}
