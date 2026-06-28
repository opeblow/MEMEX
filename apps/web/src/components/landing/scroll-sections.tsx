"use client";

import { useReducedMotion } from "@memex/hooks";
import { motion, useScroll, useTransform } from "framer-motion";
import { useRef } from "react";

interface SectionProps {
  title: string;
  subtitle: string;
  body: string;
  index: number;
  accentColor: string;
}

function StorySection({ title, subtitle, body, index, accentColor }: SectionProps) {
  const ref = useRef<HTMLElement>(null);
  const reducedMotion = useReducedMotion();

  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start end", "end start"],
  });

  const opacity = useTransform(scrollYProgress, [0, 0.3, 0.6, 1], [0, 1, 1, 0]);
  const y = useTransform(scrollYProgress, [0, 0.3, 0.7, 1], [80, 0, 0, -40]);
  const scale = useTransform(scrollYProgress, [0, 0.3, 0.7, 1], [0.92, 1, 1, 0.97]);
  const clipIn = useTransform(scrollYProgress, [0, 0.25], ["inset(0 0 100% 0)", "inset(0 0 0% 0)"]);

  const isEven = index % 2 === 0;

  return (
    <motion.section
      ref={ref}
      className="relative z-10 flex min-h-dvh items-center justify-center overflow-hidden px-6 py-32"
      style={reducedMotion ? {} : { opacity, y: reducedMotion ? 0 : y, scale }}
    >
      <div className="relative w-full max-w-6xl mx-auto">
        <motion.div className="mx-auto max-w-3xl" style={reducedMotion ? {} : { clipPath: clipIn }}>
          <motion.p
            className="mb-4 text-xs font-semibold tracking-[0.3em] uppercase"
            style={{ color: accentColor }}
          >
            {subtitle}
          </motion.p>
          <h2 className="mb-6 text-4xl font-bold leading-tight tracking-tight md:text-6xl lg:text-7xl">
            {title.split(" ").map((word) => (
              <span key={word}>
                <span
                  className="bg-clip-text text-transparent"
                  style={{
                    backgroundImage: `linear-gradient(135deg, ${accentColor}, ${accentColor}88)`,
                  }}
                >
                  {word}
                </span>{" "}
              </span>
            ))}
          </h2>
          <p className="text-base leading-relaxed text-white/30 md:text-lg max-w-2xl mx-auto">
            {body}
          </p>
        </motion.div>

        <div
          className="pointer-events-none absolute -inset-32 opacity-[0.03]"
          style={{
            background: `radial-gradient(ellipse at ${isEven ? "30%" : "70%"} 50%, ${accentColor} 0%, transparent 70%)`,
          }}
        />
      </div>
    </motion.section>
  );
}

const SECTIONS = [
  {
    subtitle: "01 — Birth of Memory",
    title: "Memories are born in an instant. They live forever.",
    body: "Every experience creates a trace. A spark fires. A connection forms. MEMEX captures that moment — the first breath of a memory — and preserves it with perfect fidelity. Nothing is lost. Nothing fades.",
    accentColor: "#f59e0b",
  },
  {
    subtitle: "02 — The Web of Connections",
    title: "No memory exists alone. Each one weaves into the next.",
    body: "Like neurons in a living brain, your memories form an intricate web. A conversation today links to a thought from years ago. Concepts merge. Patterns emerge. MEMEX maps every relationship, revealing the hidden structure of your knowledge.",
    accentColor: "#22d3ee",
  },
  {
    subtitle: "03 — Knowledge Becomes Intelligence",
    title: "From raw data to living understanding.",
    body: "Memories are not just stored — they evolve. MEMEX continuously refines connections, abstracts patterns, and surfaces insights you didn't know you had. Your knowledge grows organically, becoming more than the sum of its parts.",
    accentColor: "#fbbf24",
  },
  {
    subtitle: "04 — AI Never Forgets",
    title: "Your artificial memory is permanent. Eternal. Unbreakable.",
    body: "Every insight, every discovery, every forgotten thought — preserved across time. MEMEX gives AI a permanent memory foundation. Not a chat log. Not a cache. A living, breathing knowledge system that remembers everything, understands everything.",
    accentColor: "#67e8f9",
  },
];

export function ScrollSections() {
  return (
    <>
      {SECTIONS.map((section, index) => (
        <StorySection key={section.title} {...section} index={index} />
      ))}

      <section className="relative z-10 flex min-h-dvh items-center justify-center overflow-hidden px-6">
        <div className="relative w-full max-w-4xl mx-auto text-center">
          <motion.p
            className="mb-4 text-xs font-semibold tracking-[0.3em] uppercase text-amber-500/60"
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            05 — Call to Action
          </motion.p>
          <motion.h2
            className="mb-8 text-4xl font-bold leading-tight tracking-tight md:text-6xl lg:text-7xl"
            initial={{ opacity: 0, y: 30, filter: "blur(8px)" }}
            whileInView={{ opacity: 1, y: 0, filter: "blur(0px)" }}
            viewport={{ once: true }}
            transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
          >
            <span className="bg-clip-text text-transparent bg-gradient-to-r from-amber-400 via-white to-cyan-400">
              Enter the Operating System
            </span>
          </motion.h2>
          <motion.p
            className="mx-auto mb-12 max-w-xl text-base text-white/30 md:text-lg"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.3, duration: 0.6 }}
          >
            Your artificial memory is waiting. Start preserving, connecting, and discovering like
            never before.
          </motion.p>
          <motion.div
            className="flex flex-col items-center gap-4 sm:flex-row sm:justify-center"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.5, duration: 0.6 }}
          >
            <a
              href="/login"
              className="group relative inline-flex h-14 items-center justify-center rounded-lg px-8 text-sm font-medium text-black transition-all duration-300 hover:scale-105"
            >
              <span className="absolute inset-0 rounded-lg bg-gradient-to-r from-amber-400 via-amber-500 to-amber-400 bg-[length:200%_100%] animate-energy-flow" />
              <span className="absolute inset-[1px] rounded-[7px] bg-black transition-all duration-300 group-hover:bg-black/80" />
              <span className="relative z-10 flex items-center gap-2 text-white">
                Enter MEMEX
                <svg
                  width="16"
                  height="16"
                  viewBox="0 0 16 16"
                  fill="none"
                  className="transition-transform duration-300 group-hover:translate-x-1"
                >
                  <title>Arrow icon</title>
                  <path
                    d="M1 8H15M15 8L8 1M15 8L8 15"
                    stroke="currentColor"
                    strokeWidth="1.5"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
              </span>
            </a>
          </motion.div>
        </div>
      </section>

      <footer className="relative z-10 border-t border-white/5 py-8 text-center text-xs text-white/10">
        <p>MEMEX — The Operating System for Artificial Memory</p>
      </footer>
    </>
  );
}
