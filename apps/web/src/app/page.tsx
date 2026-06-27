"use client";

import { useState, useCallback } from "react";
import dynamic from "next/dynamic";
import { Loader } from "@/components/landing/loader";

const NeuralBackground = dynamic(
  () => import("@/components/landing/neural-background").then((m) => ({ default: m.NeuralBackground })),
  { ssr: false },
);

const CustomCursor = dynamic(
  () => import("@/components/landing/custom-cursor").then((m) => ({ default: m.CustomCursor })),
  { ssr: false },
);

const HeroSection = dynamic(
  () => import("@/components/landing/hero-section").then((m) => ({ default: m.HeroSection })),
  { ssr: false },
);

const ScrollSections = dynamic(
  () => import("@/components/landing/scroll-sections").then((m) => ({ default: m.ScrollSections })),
  { ssr: false },
);

export default function LandingPage() {
  const [loading, setLoading] = useState(true);

  const handleLoaderComplete = useCallback(() => {
    setLoading(false);
  }, []);

  return (
    <>
      {loading && <Loader onComplete={handleLoaderComplete} />}

      <NeuralBackground />
      <CustomCursor />

      <main className="relative">
        <HeroSection />
        <ScrollSections />
      </main>
    </>
  );
}
