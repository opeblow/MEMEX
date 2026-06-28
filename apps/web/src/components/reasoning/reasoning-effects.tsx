"use client";

import { useFrame } from "@react-three/fiber";
import { useMemo, useRef } from "react";
import * as THREE from "three";

interface ReasoningTrailProps {
  memoryPositions: [number, number, number][];
  active: boolean;
}

export function ReasoningTrail({ memoryPositions, active }: ReasoningTrailProps) {
  const lineRef = useRef<THREE.LineSegments>(null);

  const geometry = useMemo(() => {
    if (!memoryPositions || memoryPositions.length < 2) return null;
    const pts = memoryPositions;
    const generated: number[] = [];
    for (let i = 0; i < pts.length - 1; i++) {
      const a = pts[i];
      const b = pts[i + 1];
      if (a && b) {
        generated.push(a[0], a[1], a[2], b[0], b[1], b[2]);
      }
    }
    const geo = new THREE.BufferGeometry();
    geo.setAttribute("position", new THREE.Float32BufferAttribute(generated, 3));
    return geo;
  }, [memoryPositions]);

  useFrame(() => {
    if (!lineRef.current || !geometry) return;
    const opacity = active ? 0.8 : 0;
    if (lineRef.current.material instanceof THREE.LineBasicMaterial) {
      lineRef.current.material.opacity = opacity;
    }
  });

  if (!geometry) return null;

  return (
    <lineSegments ref={lineRef} geometry={geometry}>
      <lineBasicMaterial color="#a78bfa" transparent opacity={0} linewidth={2} />
    </lineSegments>
  );
}

interface IlluminatedMemoryProps {
  position: [number, number, number];
  active: boolean;
  color?: string;
}

export function IlluminatedMemory({ position, active, color = "#22d3ee" }: IlluminatedMemoryProps) {
  const meshRef = useRef<THREE.Mesh>(null);
  const glowRef = useRef<THREE.Mesh>(null);

  useFrame(() => {
    if (!meshRef.current || !glowRef.current) return;
    if (active) {
      const intensity = 0.5 + Math.sin(Date.now() * 0.003) * 0.3;
      meshRef.current.scale.setScalar(1 + intensity * 0.3);
      glowRef.current.scale.setScalar(1.5 + intensity);
      if (glowRef.current.material instanceof THREE.MeshBasicMaterial) {
        glowRef.current.material.opacity = 0.3 + intensity * 0.2;
      }
    } else {
      meshRef.current.scale.setScalar(1);
      glowRef.current.scale.setScalar(0.01);
      if (glowRef.current.material instanceof THREE.MeshBasicMaterial) {
        glowRef.current.material.opacity = 0;
      }
    }
  });

  return (
    <group position={position}>
      <mesh ref={meshRef}>
        <sphereGeometry args={[0.3, 16, 16]} />
        <meshBasicMaterial color={color} />
      </mesh>
      <mesh ref={glowRef} scale={[0.01, 0.01, 0.01]}>
        <sphereGeometry args={[0.5, 16, 16]} />
        <meshBasicMaterial color={color} transparent opacity={0} />
      </mesh>
    </group>
  );
}
