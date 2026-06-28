"use client";

import { Button } from "@memex/ui";
import { AlertTriangle } from "lucide-react";
import { useEffect } from "react";

interface ErrorProps {
  error: Error & { digest?: string };
  reset: () => void;
}

export default function ChatError({ error, reset }: ErrorProps) {
  useEffect(() => {
    console.error("Chat page error:", error);
  }, [error]);

  return (
    <div className="flex h-[calc(100vh-4rem)] items-center justify-center p-8">
      <div className="flex flex-col items-center gap-6 text-center" aria-live="assertive">
        <div className="flex h-16 w-16 items-center justify-center rounded-full bg-red-500/10">
          <AlertTriangle className="h-8 w-8 text-red-400" />
        </div>
        <div>
          <h2 className="text-xl font-semibold text-white/90">Chat Unavailable</h2>
          <p className="mt-2 max-w-md text-sm text-white/50">
            {error.message ?? "Failed to load the chat interface."}
          </p>
        </div>
        <Button variant="secondary" size="sm" onClick={reset}>
          Try Again
        </Button>
      </div>
    </div>
  );
}
