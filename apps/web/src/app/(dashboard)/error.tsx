"use client";

import { Button } from "@memex/ui";
import { AlertTriangle, Home } from "lucide-react";
import Link from "next/link";
import { useEffect } from "react";

interface ErrorProps {
  error: Error & { digest?: string };
  reset: () => void;
}

export default function DashboardError({ error, reset }: ErrorProps) {
  useEffect(() => {
    console.error("Dashboard error:", error);
  }, [error]);

  return (
    <div className="flex min-h-[calc(100vh-4rem)] items-center justify-center p-8">
      <div className="flex flex-col items-center gap-6 text-center" aria-live="assertive">
        <div className="flex h-16 w-16 items-center justify-center rounded-full bg-red-500/10">
          <AlertTriangle className="h-8 w-8 text-red-400" />
        </div>
        <div>
          <h2 className="text-xl font-semibold text-white/90">Dashboard Error</h2>
          <p className="mt-2 max-w-md text-sm text-white/50">
            {error.message ?? "Something went wrong loading this page."}
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Button variant="secondary" size="sm" onClick={reset}>
            Try Again
          </Button>
          <Link href="/">
            <Button variant="ghost" size="sm" leftIcon={<Home size={14} />}>
              Return to Dashboard
            </Button>
          </Link>
        </div>
      </div>
    </div>
  );
}
