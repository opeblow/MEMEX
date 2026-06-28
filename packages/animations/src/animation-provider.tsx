"use client";

import { Lenis as ReactLenis } from "lenis/react";
import { type ReactNode, createContext, useContext, useMemo } from "react";

interface AnimationContextValue {
  reducedMotion: boolean;
}

const AnimationContext = createContext<AnimationContextValue>({
  reducedMotion: false,
});

export function useAnimationContext(): AnimationContextValue {
  const ctx = useContext(AnimationContext);
  if (!ctx) {
    throw new Error("useAnimationContext must be used within AnimationProvider");
  }
  return ctx;
}

interface AnimationProviderProps {
  children: ReactNode;
  reducedMotion?: boolean;
}

export function AnimationProvider({ children, reducedMotion = false }: AnimationProviderProps) {
  const value = useMemo(() => ({ reducedMotion }), [reducedMotion]);

  if (reducedMotion) {
    return <AnimationContext.Provider value={value}>{children}</AnimationContext.Provider>;
  }

  return (
    <AnimationContext.Provider value={value}>
      <ReactLenis
        root
        options={{ duration: 1.2, easing: (t) => Math.min(1, 1.001 - 2 ** (-10 * t)) }}
      >
        {children}
      </ReactLenis>
    </AnimationContext.Provider>
  );
}
