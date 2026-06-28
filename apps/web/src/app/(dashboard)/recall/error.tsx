"use client";

import { Button } from "@memex/ui";
import { AlertTriangle, MessageSquare, Upload } from "lucide-react";
import Link from "next/link";
import { useEffect } from "react";

interface ErrorProps {
  error: Error & { digest?: string };
  reset: () => void;
}

export default function RecallError({ error, reset }: ErrorProps) {
  useEffect(() => {
    console.error("Recall page error:", error);
  }, [error]);

  return (
    <div className="flex min-h-[calc(100vh-4rem)] items-center justify-center p-8">
      <div className="flex flex-col items-center gap-6 text-center" aria-live="assertive">
        <div className="flex h-16 w-16 items-center justify-center rounded-full bg-red-500/10">
          <AlertTriangle className="h-8 w-8 text-red-400" />
        </div>
        <div>
          <h2 className="text-xl font-semibold text-white/90">Memory Universe Unavailable</h2>
          <p className="mt-2 max-w-md text-sm text-white/50">
            {error.message ?? "Failed to load your memories."}
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Button variant="secondary" size="sm" onClick={reset}>
            Try Again
          </Button>
          <Link href="/chat">
            <Button variant="ghost" size="sm" leftIcon={<MessageSquare size={14} />}>
              Go to Chat
            </Button>
          </Link>
          <Link href="/ingest">
            <Button variant="ghost" size="sm" leftIcon={<Upload size={14} />}>
              Go to Ingest
            </Button>
          </Link>
        </div>
      </div>
    </div>
  );
}
