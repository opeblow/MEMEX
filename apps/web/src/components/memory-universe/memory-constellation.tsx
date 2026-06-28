"use client";

import type { MemoryDetail } from "@memex/types";
import { useMemo } from "react";
import { MemoryNode } from "./memory-node";
import { RelationshipLine } from "./relationship-line";

interface ConstellationProps {
  memories: MemoryDetail[];
  selectedId: string | null;
  onSelect: (id: string) => void;
}

export function MemoryConstellation({ memories, selectedId, onSelect }: ConstellationProps) {
  const positions = useMemo(() => {
    const map = new Map<string, [number, number, number]>();
    const count = memories.length;
    memories.forEach((mem, i) => {
      const theta = (i / count) * Math.PI * 2;
      const phi = Math.acos(2 * (i / count) - 1);
      const r = 3 + Math.random() * 2;
      map.set(mem.id, [
        r * Math.sin(phi) * Math.cos(theta),
        r * Math.cos(phi),
        r * Math.sin(phi) * Math.sin(theta),
      ]);
    });
    return map;
  }, [memories]);

  return (
    <group>
      {memories.map((mem) => {
        const pos = positions.get(mem.id);
        if (!pos) return null;
        return (
          <MemoryNode
            key={mem.id}
            memory={mem}
            position={pos}
            isSelected={mem.id === selectedId}
            onSelect={onSelect}
          />
        );
      })}
      {memories.map((mem, i) => {
        const start = positions.get(mem.id);
        const nextMem = memories[(i + 1) % memories.length];
        if (!nextMem) return null;
        const next = positions.get(nextMem.id);
        if (!start || !next) return null;
        return (
          <RelationshipLine
            key={`edge-${mem.id}`}
            start={start}
            end={next}
            weight={0.5}
            isActive={mem.id === selectedId || nextMem.id === selectedId}
          />
        );
      })}
    </group>
  );
}
