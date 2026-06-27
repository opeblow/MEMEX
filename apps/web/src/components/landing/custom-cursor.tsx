"use client";

import { useEffect, useRef, useCallback } from "react";
import { motion, useMotionValue, useSpring } from "framer-motion";

export function CustomCursor() {
  const cursorX = useMotionValue(-200);
  const cursorY = useMotionValue(-200);
  const isHovering = useRef(false);

  const springX = useSpring(cursorX, { stiffness: 300, damping: 25 });
  const springY = useSpring(cursorY, { stiffness: 300, damping: 25 });

  const handleMouseMove = useCallback(
    (e: MouseEvent) => {
      cursorX.set(e.clientX);
      cursorY.set(e.clientY);
    },
    [cursorX, cursorY],
  );

  const handleMouseOver = useCallback((e: MouseEvent) => {
    const target = e.target as HTMLElement;
    if (
      target.closest("a") ||
      target.closest("button") ||
      target.closest("[data-cursor-hover]")
    ) {
      isHovering.current = true;
      document.documentElement.style.setProperty("--cursor-scale", "1.5");
    }
  }, []);

  const handleMouseOut = useCallback(() => {
    isHovering.current = false;
    document.documentElement.style.setProperty("--cursor-scale", "1");
  }, []);

  useEffect(() => {
    document.documentElement.style.cursor = "none";
    document.documentElement.style.setProperty("--cursor-scale", "1");

    window.addEventListener("mousemove", handleMouseMove);
    window.addEventListener("mouseover", handleMouseOver);
    window.addEventListener("mouseout", handleMouseOut);

    const style = document.createElement("style");
    style.textContent = `
      a, button, [data-cursor-hover] { cursor: none; }
    `;
    document.head.appendChild(style);

    return () => {
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("mouseover", handleMouseOver);
      window.removeEventListener("mouseout", handleMouseOut);
      document.documentElement.style.cursor = "";
      document.head.removeChild(style);
    };
  }, [handleMouseMove, handleMouseOver, handleMouseOut]);

  return (
    <>
      <motion.div
        className="fixed top-0 left-0 pointer-events-none z-[9999]"
        style={{ x: springX, y: springY }}
      >
        <div
          className="-translate-x-1/2 -translate-y-1/2 rounded-full bg-amber-500/20 blur-xl transition-all duration-300"
          style={{
            width: "calc(32px * var(--cursor-scale, 1))",
            height: "calc(32px * var(--cursor-scale, 1))",
          }}
        />
        <div className="absolute -translate-x-1/2 -translate-y-1/2 top-0 left-0 w-2 h-2 rounded-full bg-amber-400/70" />
      </motion.div>
      <motion.div
        className="fixed top-0 left-0 pointer-events-none z-[9998]"
        style={{ x: springX, y: springY }}
      >
        <div
          className="-translate-x-1/2 -translate-y-1/2 rounded-full border border-amber-500/20 transition-all duration-300"
          style={{
            width: "calc(48px * var(--cursor-scale, 1))",
            height: "calc(48px * var(--cursor-scale, 1))",
          }}
        />
      </motion.div>
    </>
  );
}
