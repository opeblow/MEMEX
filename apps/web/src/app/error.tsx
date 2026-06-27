"use client";

import { useEffect } from "react";
import { ErrorState } from "@memex/ui";

interface ErrorProps {
  error: Error & { digest?: string };
  reset: () => void;
}

export default function Error({ error, reset }: ErrorProps) {
  useEffect(() => {
    console.error("Application error:", error);
  }, [error]);

  return (
    <div className="flex min-h-screen items-center justify-center p-8">
      <ErrorState
        title="Something went wrong"
        message={error.message ?? "An unexpected error occurred."}
        onRetry={reset}
      />
    </div>
  );
}
