"use client";

import { AnimatePresence, motion } from "framer-motion";
import { useEffect, useState } from "react";

interface LoaderProps {
  onComplete: () => void;
}

export function Loader({ onComplete }: LoaderProps) {
  const [phase, setPhase] = useState<"nucleus" | "dendrites" | "connections" | "complete">(
    "nucleus",
  );

  useEffect(() => {
    const t1 = setTimeout(() => setPhase("dendrites"), 600);
    const t2 = setTimeout(() => setPhase("connections"), 1400);
    const t3 = setTimeout(() => {
      setPhase("complete");
      setTimeout(onComplete, 500);
    }, 2400);
    return () => {
      clearTimeout(t1);
      clearTimeout(t2);
      clearTimeout(t3);
    };
  }, [onComplete]);

  return (
    <AnimatePresence>
      {phase !== "complete" && (
        <motion.div
          className="fixed inset-0 z-[9997] flex items-center justify-center bg-black"
          exit={{ opacity: 0 }}
          transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
        >
          <svg width="120" height="120" viewBox="0 0 120 120" className="overflow-visible">
            <title>Loading animation</title>
            <defs>
              <radialGradient id="nucleus-glow" cx="50%" cy="50%" r="50%">
                <stop offset="0%" stopColor="#f59e0b" stopOpacity="0.8" />
                <stop offset="60%" stopColor="#f59e0b" stopOpacity="0.3" />
                <stop offset="100%" stopColor="#f59e0b" stopOpacity="0" />
              </radialGradient>
              <radialGradient id="nucleus-core" cx="50%" cy="50%" r="50%">
                <stop offset="0%" stopColor="#fbbf24" stopOpacity="1" />
                <stop offset="50%" stopColor="#f59e0b" stopOpacity="0.8" />
                <stop offset="100%" stopColor="#d97706" stopOpacity="0" />
              </radialGradient>
            </defs>

            <circle cx="60" cy="60" r="30" fill="url(#nucleus-glow)">
              <animate attributeName="r" values="20;35;20" dur="2s" repeatCount="indefinite" />
              <animate
                attributeName="opacity"
                values="0.3;0.8;0.3"
                dur="2s"
                repeatCount="indefinite"
              />
            </circle>

            <circle cx="60" cy="60" r="5" fill="url(#nucleus-core)">
              <animate attributeName="r" values="3;6;3" dur="2s" repeatCount="indefinite" />
            </circle>

            {phase === "nucleus" || phase === "dendrites" || phase === "connections" ? (
              <>
                <motion.line
                  x1="60"
                  y1="60"
                  x2="60"
                  y2="15"
                  stroke="#f59e0b"
                  strokeWidth="1"
                  strokeOpacity="0.6"
                  initial={{ pathLength: 0, opacity: 0 }}
                  animate={
                    phase === "nucleus"
                      ? { pathLength: 0, opacity: 0 }
                      : { pathLength: 1, opacity: 0.6 }
                  }
                  transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
                />
                <motion.line
                  x1="60"
                  y1="60"
                  x2="105"
                  y2="45"
                  stroke="#22d3ee"
                  strokeWidth="1"
                  strokeOpacity="0.5"
                  initial={{ pathLength: 0, opacity: 0 }}
                  animate={
                    phase === "nucleus"
                      ? { pathLength: 0, opacity: 0 }
                      : { pathLength: 1, opacity: 0.5 }
                  }
                  transition={{ duration: 0.6, delay: 0.1, ease: [0.16, 1, 0.3, 1] }}
                />
                <motion.line
                  x1="60"
                  y1="60"
                  x2="15"
                  y2="75"
                  stroke="#f59e0b"
                  strokeWidth="1"
                  strokeOpacity="0.4"
                  initial={{ pathLength: 0, opacity: 0 }}
                  animate={
                    phase === "nucleus"
                      ? { pathLength: 0, opacity: 0 }
                      : { pathLength: 1, opacity: 0.4 }
                  }
                  transition={{ duration: 0.6, delay: 0.2, ease: [0.16, 1, 0.3, 1] }}
                />
                <motion.line
                  x1="60"
                  y1="60"
                  x2="90"
                  y2="100"
                  stroke="#22d3ee"
                  strokeWidth="1"
                  strokeOpacity="0.5"
                  initial={{ pathLength: 0, opacity: 0 }}
                  animate={
                    phase === "nucleus"
                      ? { pathLength: 0, opacity: 0 }
                      : { pathLength: 1, opacity: 0.5 }
                  }
                  transition={{ duration: 0.6, delay: 0.15, ease: [0.16, 1, 0.3, 1] }}
                />
                <motion.line
                  x1="60"
                  y1="60"
                  x2="30"
                  y2="20"
                  stroke="#22d3ee"
                  strokeWidth="1"
                  strokeOpacity="0.4"
                  initial={{ pathLength: 0, opacity: 0 }}
                  animate={
                    phase === "nucleus"
                      ? { pathLength: 0, opacity: 0 }
                      : { pathLength: 1, opacity: 0.4 }
                  }
                  transition={{ duration: 0.6, delay: 0.25, ease: [0.16, 1, 0.3, 1] }}
                />
              </>
            ) : null}

            {phase === "connections" ? (
              <>
                <motion.line
                  x1="15"
                  y1="75"
                  x2="90"
                  y2="100"
                  stroke="#f59e0b"
                  strokeWidth="0.5"
                  strokeOpacity="0.3"
                  initial={{ pathLength: 0, opacity: 0 }}
                  animate={{ pathLength: 1, opacity: 0.3 }}
                  transition={{ duration: 0.5, delay: 0.1, ease: [0.16, 1, 0.3, 1] }}
                />
                <motion.line
                  x1="105"
                  y1="45"
                  x2="30"
                  y2="20"
                  stroke="#22d3ee"
                  strokeWidth="0.5"
                  strokeOpacity="0.3"
                  initial={{ pathLength: 0, opacity: 0 }}
                  animate={{ pathLength: 1, opacity: 0.3 }}
                  transition={{ duration: 0.5, delay: 0.2, ease: [0.16, 1, 0.3, 1] }}
                />
                <motion.line
                  x1="60"
                  y1="15"
                  x2="105"
                  y2="45"
                  stroke="#f59e0b"
                  strokeWidth="0.5"
                  strokeOpacity="0.25"
                  initial={{ pathLength: 0, opacity: 0 }}
                  animate={{ pathLength: 1, opacity: 0.25 }}
                  transition={{ duration: 0.5, delay: 0.35, ease: [0.16, 1, 0.3, 1] }}
                />
              </>
            ) : null}
          </svg>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
