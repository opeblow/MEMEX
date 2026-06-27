"use client";

import { useRef } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";

interface RelationshipLineProps {
  start: [number, number, number];
  end: [number, number, number];
  weight: number;
  isActive: boolean;
}

export function RelationshipLine({ start, end, isActive }: RelationshipLineProps) {
  const ref = useRef<THREE.Mesh>(null);

  const mid = [
    (start[0] + end[0]) / 2,
    (start[1] + end[1]) / 2,
    (start[2] + end[2]) / 2,
  ] as [number, number, number];

  const direction = [
    end[0] - start[0],
    end[1] - start[1],
    end[2] - start[2],
  ] as [number, number, number];

  const length = Math.sqrt(
    direction[0] ** 2 + direction[1] ** 2 + direction[2] ** 2,
  );

  useFrame((state) => {
    if (!ref.current) return;
    if (isActive) {
      (ref.current.material as THREE.MeshBasicMaterial).opacity =
        0.3 + Math.sin(state.clock.elapsedTime * 2) * 0.2;
    }
  });

  return (
    <mesh
      ref={ref}
      position={mid}
      rotation={[
        Math.atan2(direction[1], direction[2]),
        0,
        Math.atan2(direction[0], Math.sqrt(direction[1] ** 2 + direction[2] ** 2)),
      ]}
    >
      <cylinderGeometry args={[0.01, 0.01, length, 4]} />
      <meshBasicMaterial
        color={isActive ? "#f59e0b" : "#ffffff"}
        transparent
        opacity={isActive ? 0.5 : 0.1}
      />
    </mesh>
  );
}
