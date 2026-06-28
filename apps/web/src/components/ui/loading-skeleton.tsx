"use client";

import React from "react";

interface SkeletonProps {
  className?: string;
}

function Skeleton({ className = "" }: SkeletonProps) {
  return <div className={`animate-pulse bg-white/5 rounded ${className}`} aria-hidden="true" />;
}

export function PageSkeleton() {
  return (
    <div className="space-y-6 p-6 max-w-3xl mx-auto">
      <div className="flex items-center justify-between">
        <div className="space-y-2">
          <Skeleton className="h-5 w-32" />
          <Skeleton className="h-3 w-56" />
        </div>
        <Skeleton className="h-8 w-24 rounded-lg" />
      </div>
      <div className="flex gap-2">
        <Skeleton className="h-7 w-16 rounded-lg" />
        <Skeleton className="h-7 w-20 rounded-lg" />
        <Skeleton className="h-7 w-14 rounded-lg" />
      </div>
      <div className="space-y-2">
        {Array.from({ length: 4 }).map((_, i) => (
          // biome-ignore lint/suspicious/noArrayIndexKey: static skeleton list
          <Skeleton key={i} className="h-16 w-full rounded-xl" />
        ))}
      </div>
    </div>
  );
}

export function ChatSkeleton() {
  return (
    <div className="flex flex-col h-full bg-black/40 backdrop-blur-md border-l border-white/10">
      <div className="flex items-center gap-2 px-4 py-3 border-b border-white/10">
        <Skeleton className="h-4 w-4 rounded" />
        <Skeleton className="h-4 w-32" />
      </div>
      <div className="flex-1 p-4 space-y-4">
        {Array.from({ length: 3 }).map((_, i) => (
          // biome-ignore lint/suspicious/noArrayIndexKey: static skeleton list
          <div key={i} className={`flex ${i % 2 === 0 ? "justify-end" : "justify-start"}`}>
            <div
              className={`rounded-lg p-3 ${i % 2 === 0 ? "bg-purple-500/20" : "bg-white/5"} max-w-[80%]`}
            >
              <Skeleton className={`h-3 ${i % 2 === 0 ? "w-48" : "w-36"} mb-2`} />
              <Skeleton className={`h-3 ${i % 2 === 0 ? "w-32" : "w-44"}`} />
            </div>
          </div>
        ))}
      </div>
      <div className="p-4 border-t border-white/10">
        <Skeleton className="h-9 w-full rounded-lg" />
      </div>
    </div>
  );
}

export function UniverseSkeleton() {
  return (
    <div className="relative w-full h-[calc(100vh-4rem)] overflow-hidden bg-black/20 flex items-center justify-center">
      <div className="flex flex-col items-center gap-3">
        <Skeleton className="h-16 w-16 rounded-full" />
        <Skeleton className="h-3 w-40" />
        <Skeleton className="h-3 w-56" />
      </div>
    </div>
  );
}

export function TimelineSkeleton() {
  return (
    <div className="p-6 space-y-4">
      <div className="flex items-center gap-3">
        <Skeleton className="h-10 w-10 rounded-full shrink-0" />
        <div className="space-y-1.5 flex-1">
          <Skeleton className="h-3 w-32" />
          <Skeleton className="h-2 w-48" />
        </div>
      </div>
      {Array.from({ length: 5 }).map((_, i) => (
        // biome-ignore lint/suspicious/noArrayIndexKey: static skeleton list
        <div key={i} className="flex items-center gap-3">
          <Skeleton className="h-10 w-10 rounded-full shrink-0" />
          <div className="space-y-1.5 flex-1">
            <Skeleton className={`h-3 ${i % 2 === 0 ? "w-28" : "w-36"}`} />
            <Skeleton className={`h-2 ${i % 2 === 0 ? "w-44" : "w-32"}`} />
          </div>
        </div>
      ))}
    </div>
  );
}
