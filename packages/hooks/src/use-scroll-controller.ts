"use client";

import { useEffect, useRef, useState } from "react";

export interface ScrollState {
  progress: number;
  velocity: number;
  direction: "up" | "down";
}

export function useScrollController() {
  const [scrollState, setScrollState] = useState<ScrollState>({
    progress: 0,
    velocity: 0,
    direction: "down",
  });
  const rafRef = useRef<number | null>(null);
  const lastYRef = useRef(0);
  const lastTimeRef = useRef(0);

  useEffect(() => {
    const handleScroll = () => {
      if (rafRef.current) return;

      rafRef.current = requestAnimationFrame(() => {
        const now = performance.now();
        const currentY = window.scrollY;
        const deltaY = currentY - lastYRef.current;
        const deltaTime = now - lastTimeRef.current;

        const maxScroll = document.documentElement.scrollHeight - window.innerHeight;

        setScrollState({
          progress: maxScroll > 0 ? currentY / maxScroll : 0,
          velocity: deltaTime > 0 ? Math.abs(deltaY / deltaTime) : 0,
          direction: deltaY > 0 ? "down" : "up",
        });

        lastYRef.current = currentY;
        lastTimeRef.current = now;
        rafRef.current = null;
      });
    };

    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => {
      window.removeEventListener("scroll", handleScroll);
      if (rafRef.current) cancelAnimationFrame(rafRef.current);
    };
  }, []);

  return scrollState;
}
