"use client";

import { useState, useCallback, Suspense } from "react";
import { Canvas } from "@react-three/fiber";
import { Stars, Environment, ContactShadows } from "@react-three/drei";
import { MemoryConstellation } from "./memory-constellation";
import { MemoryDetailPanel } from "./memory-detail-panel";
import { UniverseControls } from "./universe-controls";
import { GalaxyBackground } from "./galaxy-background";
import type { MemoryDetail } from "@memex/types";

interface MemoryUniverseProps {
  memories: MemoryDetail[];
  onDelete?: (id: string) => void;
  onArchive?: (id: string) => void;
}

export function MemoryUniverse({ memories, onDelete, onArchive }: MemoryUniverseProps) {
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [cameraTarget, setCameraTarget] = useState<[number, number, number]>([0, 0, 0]);

  const selectedMemory = memories.find((m) => m.id === selectedId) || null;

  const handleSelect = useCallback((id: string) => {
    setSelectedId((prev) => (prev === id ? null : id));
  }, []);

  const handleClosePanel = useCallback(() => {
    setSelectedId(null);
  }, []);

  const handleDelete = useCallback(
    (id: string) => {
      onDelete?.(id);
      setSelectedId(null);
    },
    [onDelete],
  );

  const handleArchive = useCallback(
    (id: string) => {
      onArchive?.(id);
      setSelectedId(null);
    },
    [onArchive],
  );

  return (
    <div className="relative w-full h-full">
      <div className="absolute inset-0">
        <Canvas
          camera={{ position: [0, 0, 8], fov: 60, near: 0.1, far: 100 }}
          dpr={[1, 2]}
          gl={{ antialias: true, alpha: false }}
        >
          <color attach="background" args={["#000000"]} />
          <fog attach="fog" args={["#000000", 15, 30]} />

          <ambientLight intensity={0.2} />
          <pointLight position={[10, 10, 10]} intensity={0.8} />
          <pointLight position={[-10, -10, -10]} intensity={0.3} />

          <Suspense fallback={null}>
            <GalaxyBackground />
            <Stars radius={100} depth={50} count={3000} factor={4} saturation={0} fade speed={1} />
            <Environment preset="night" />
            <ContactShadows position={[0, -5, 0]} opacity={0.4} scale={20} blur={2} far={10} />
          </Suspense>

          <MemoryConstellation
            memories={memories}
            selectedId={selectedId}
            onSelect={handleSelect}
          />

          <UniverseControls
            target={cameraTarget}
            onTargetChange={setCameraTarget}
            selectedId={selectedId}
          />
        </Canvas>
      </div>

      <MemoryDetailPanel
        memory={selectedMemory}
        onClose={handleClosePanel}
        onDelete={handleDelete}
        onArchive={handleArchive}
      />
    </div>
  );
}
