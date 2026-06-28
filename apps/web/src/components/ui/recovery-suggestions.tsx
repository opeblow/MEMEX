"use client";

import { Button } from "@memex/ui";
import { AnimatePresence, motion } from "framer-motion";
import { AlertTriangle, RefreshCw } from "lucide-react";

interface RecoverySuggestionsProps {
  error: Error;
  suggestions?: string[];
  onRetry?: () => void;
}

export function RecoverySuggestions({ error, suggestions, onRetry }: RecoverySuggestionsProps) {
  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: 10 }}
        transition={{ duration: 0.3, ease: "easeOut" }}
        className="flex flex-col items-center gap-5 py-16 text-center"
        aria-live="assertive"
      >
        <motion.div
          initial={{ scale: 0.8 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.1, type: "spring", stiffness: 200 }}
          className="flex h-14 w-14 items-center justify-center rounded-full bg-red-500/10"
        >
          <AlertTriangle className="h-7 w-7 text-red-400" />
        </motion.div>

        <div>
          <p className="text-lg font-medium text-white/80">Something went wrong</p>
          <p className="mt-1 max-w-sm text-sm text-white/40">
            {error.message || "An unexpected error occurred."}
          </p>
        </div>

        {suggestions && suggestions.length > 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2 }}
            className="flex flex-col gap-2"
          >
            <p className="text-xs font-medium uppercase tracking-wider text-white/30">
              You could try
            </p>
            <ul className="flex flex-col gap-1.5">
              {suggestions.map((suggestion, i) => (
                <li
                  // biome-ignore lint/suspicious/noArrayIndexKey: static suggestions list
                  key={i}
                  className="rounded-lg border border-amber-500/20 bg-amber-500/5 px-4 py-2 text-sm text-amber-300/80"
                >
                  {suggestion}
                </li>
              ))}
            </ul>
          </motion.div>
        )}

        {onRetry && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.3 }}>
            <Button variant="energy" size="sm" onClick={onRetry} leftIcon={<RefreshCw size={14} />}>
              Retry
            </Button>
          </motion.div>
        )}
      </motion.div>
    </AnimatePresence>
  );
}
