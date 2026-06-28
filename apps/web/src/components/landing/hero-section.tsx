"use client";

import { useReducedMotion } from "@memex/hooks";
import { motion } from "framer-motion";
import { useEffect, useRef, useState } from "react";

const LINES = ["THE OPERATING SYSTEM", "FOR", "ARTIFICIAL MEMORY"];

export function HeroSection() {
  const reducedMotion = useReducedMotion();
  const [startAnimation, setStartAnimation] = useState(false);
  const sectionRef = useRef<HTMLElement>(null);

  useEffect(() => {
    const timer = setTimeout(() => setStartAnimation(true), 400);
    return () => clearTimeout(timer);
  }, []);

  return (
    <section
      ref={sectionRef}
      className="relative z-10 flex min-h-dvh items-center justify-center overflow-hidden"
    >
      <div className="relative px-6 text-center">
        <h1 className="flex flex-col items-center gap-2 md:gap-4">
          {LINES.map((line, lineIdx) => (
            <span key={line} className="block overflow-hidden">
              <span className="flex flex-wrap justify-center">
                {line.split("").map((char, charIdx) => (
                  <motion.span
                    key={`${line}-${char}`}
                    className="inline-block font-bold tracking-tighter text-white"
                    style={{
                      fontSize: "clamp(2.5rem, 12vw, 8rem)",
                      lineHeight: "1.05",
                      letterSpacing: "-0.04em",
                    }}
                    initial={
                      reducedMotion
                        ? { opacity: 1, scale: 1, filter: "blur(0px)" }
                        : { opacity: 0, scale: 0.4, filter: "blur(12px)", y: 30 }
                    }
                    animate={
                      startAnimation ? { opacity: 1, scale: 1, filter: "blur(0px)", y: 0 } : {}
                    }
                    transition={{
                      delay: lineIdx * 0.3 + charIdx * 0.025,
                      duration: 0.6,
                      ease: [0.16, 1, 0.3, 1],
                    }}
                  >
                    {char === " " ? "\u00A0" : char}
                  </motion.span>
                ))}
              </span>
            </span>
          ))}
        </h1>

        <motion.p
          className="mx-auto mt-8 max-w-2xl text-sm tracking-wide text-white/20 md:text-base"
          initial={{ opacity: 0, y: 20 }}
          animate={startAnimation ? { opacity: 1, y: 0 } : {}}
          transition={{ delay: 2.2, duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
        >
          Enter the artificial brain. Every memory, every connection, every thought — preserved,
          interconnected, alive.
        </motion.p>

        <motion.div
          className="absolute bottom-8 left-1/2 -translate-x-1/2"
          initial={{ opacity: 0 }}
          animate={startAnimation ? { opacity: 1 } : {}}
          transition={{ delay: 3, duration: 0.6 }}
        >
          <motion.div
            className="h-12 w-px bg-gradient-to-b from-amber-500/60 to-transparent"
            animate={{ opacity: [0.3, 0.8, 0.3] }}
            transition={{ duration: 2, repeat: Number.POSITIVE_INFINITY, ease: "easeInOut" }}
          />
        </motion.div>
      </div>
    </section>
  );
}
