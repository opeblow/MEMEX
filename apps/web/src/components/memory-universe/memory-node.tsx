"use client";

import type { MemoryDetail } from "@memex/types";
import { Text } from "@react-three/drei";
import { useFrame } from "@react-three/fiber";
import React, { useRef, useState, useMemo } from "react";
import * as THREE from "three";

const TYPE_COLORS: Record<string, string> = {
  text: "#f59e0b",
  code: "#22d3ee",
  conversation: "#a78bfa",
  meeting_note: "#34d399",
  research: "#f472b6",
  decision: "#fb923c",
  url: "#38bdf8",
  file: "#818cf8",
  image: "#e879f9",
  github_issue: "#94a3b8",
  support_ticket: "#fbbf24",
  default: "#6b7280",
};

interface MemoryNodeProps {
  memory: MemoryDetail;
  position: [number, number, number];
  isSelected: boolean;
  onSelect: (id: string) => void;
}

const colorMap = new Map(Object.entries(TYPE_COLORS));

export const MemoryNode = React.memo(function MemoryNode({
  memory,
  position,
  isSelected,
  onSelect,
}: MemoryNodeProps) {
  const meshRef = useRef<THREE.Mesh>(null);
  const [hovered, setHovered] = useState(false);

  const color = colorMap.get(memory.memory_type) || colorMap.get("default") || "#6b7280";
  const size = useMemo(
    () => Math.max(0.3, Math.min(1.5, memory.importance * 1.5)),
    [memory.importance],
  );

  useFrame((state) => {
    if (!meshRef.current) return;
    meshRef.current.rotation.y += 0.005;
    if (isSelected) {
      meshRef.current.position.y = position[1] + Math.sin(state.clock.elapsedTime * 2) * 0.1;
    }
  });

  return (
    <group position={position}>
      {/* biome-ignore lint/a11y/useKeyWithClickEvents: R3F mesh uses pointer events */}
      <mesh
        ref={meshRef}
        onClick={(e) => {
          e.stopPropagation();
          onSelect(memory.id);
        }}
        onPointerOver={() => setHovered(true)}
        onPointerOut={() => setHovered(false)}
      >
        <sphereGeometry args={[size, 32, 32]} />
        <meshPhysicalMaterial
          color={color}
          emissive={color}
          emissiveIntensity={isSelected ? 0.8 : hovered ? 0.4 : 0.15}
          metalness={0.1}
          roughness={0.3}
          transparent
          opacity={memory.status === "archived" ? 0.5 : 1}
        />
        {hovered && (
          <Text
            position={[0, size + 0.5, 0]}
            fontSize={0.2}
            color="white"
            anchorX="center"
            anchorY="middle"
          >
            {memory.title || memory.memory_type}
          </Text>
        )}
      </mesh>
      {isSelected && (
        <mesh>
          <ringGeometry args={[size * 1.3, size * 1.5, 64]} />
          <meshBasicMaterial color={color} transparent opacity={0.3} side={THREE.DoubleSide} />
        </mesh>
      )}
    </group>
  );
});
