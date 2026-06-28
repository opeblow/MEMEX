"use client";

import { Canvas, useFrame, useThree } from "@react-three/fiber";
import { useEffect, useMemo, useRef, useState } from "react";
import * as THREE from "three";

const NEURON_COUNT = 200;
const CLUSTER_COUNT = 6;
const CONNECTION_DISTANCE = 2.8;
const CLUSTER_RADIUS = 2.8;

interface ClusterCenter {
  x: number;
  y: number;
  z: number;
}

function generateClusterCenters(): ClusterCenter[] {
  const centers: ClusterCenter[] = [];
  for (let c = 0; c < CLUSTER_COUNT; c++) {
    const angle = (c / CLUSTER_COUNT) * Math.PI * 2 + 0.2;
    const r = CLUSTER_RADIUS * (0.7 + Math.random() * 0.6);
    centers.push({
      x: Math.cos(angle) * r,
      y: (Math.random() - 0.5) * 2.5,
      z: Math.sin(angle) * r,
    });
  }
  return centers;
}

function generateNeuronData(): {
  positions: Float32Array;
  colors: Float32Array;
  sizes: Float32Array;
  phases: Float32Array;
  connections: number[][];
} {
  const centers = generateClusterCenters();
  const positions = new Float32Array(NEURON_COUNT * 3);
  const colors = new Float32Array(NEURON_COUNT * 3);
  const sizes = new Float32Array(NEURON_COUNT);
  const phases = new Float32Array(NEURON_COUNT);
  const basePositions: { x: number; y: number; z: number }[] = [];

  const amber = new THREE.Color(0xf59e0b);
  const cyan = new THREE.Color(0x22d3ee);
  const warm = new THREE.Color(0xffd6a0);

  for (let i = 0; i < NEURON_COUNT; i++) {
    const center = centers[i % CLUSTER_COUNT];
    if (!center) {
      positions[i * 3] = 0;
      positions[i * 3 + 1] = 0;
      positions[i * 3 + 2] = 0;
      basePositions.push({ x: 0, y: 0, z: 0 });
    } else {
      const spread = 0.5 + Math.random() * 0.5;
      const px = center.x + (Math.random() - 0.5) * spread;
      const py = center.y + (Math.random() - 0.5) * spread;
      const pz = center.z + (Math.random() - 0.5) * spread;
      positions[i * 3] = px;
      positions[i * 3 + 1] = py;
      positions[i * 3 + 2] = pz;
      basePositions.push({ x: px, y: py, z: pz });
    }

    const mix = Math.random();
    const color = amber
      .clone()
      .lerp(cyan, mix * 0.6)
      .lerp(warm, mix * 0.2);
    colors[i * 3] = color.r;
    colors[i * 3 + 1] = color.g;
    colors[i * 3 + 2] = color.b;

    sizes[i] = 0.03 + Math.random() * 0.08;
    phases[i] = Math.random() * Math.PI * 2;
  }

  const connections: number[][] = [];
  for (let i = 0; i < NEURON_COUNT; i++) {
    const matches = Math.floor(3 + Math.random() * 5);
    const i3 = i * 3;
    const px = positions[i3];
    const py = positions[i3 + 1];
    const pz = positions[i3 + 2];
    if (px === undefined || py === undefined || pz === undefined) continue;
    for (
      let attempt = 0;
      attempt < NEURON_COUNT && connections.length < i + matches + 1;
      attempt++
    ) {
      const j = Math.floor(Math.random() * NEURON_COUNT);
      if (j === i) continue;
      const j3 = j * 3;
      const jx = positions[j3];
      const jy = positions[j3 + 1];
      const jz = positions[j3 + 2];
      if (jx === undefined || jy === undefined || jz === undefined) continue;
      const dx = px - jx;
      const dy = py - jy;
      const dz = pz - jz;
      const dist = Math.sqrt(dx * dx + dy * dy + dz * dz);
      if (dist < CONNECTION_DISTANCE) {
        connections.push([i, j]);
      }
    }
  }

  return { positions, colors, sizes, phases, connections };
}

function NeuralField() {
  const { mouse } = useThree();
  const groupRef = useRef<THREE.Group>(null);
  const pointsRef = useRef<THREE.Points>(null);
  const linesRef = useRef<THREE.LineSegments>(null);
  const glowPointsRef = useRef<THREE.Points>(null);

  const data = useMemo(() => generateNeuronData(), []);

  const basePositions = useMemo(() => {
    const base = new Float32Array(NEURON_COUNT * 3);
    for (let i = 0; i < NEURON_COUNT * 3; i++) {
      base[i] = data.positions[i] ?? 0;
    }
    return base;
  }, [data.positions]);

  const connectionPositions = useMemo(() => {
    const verts = new Float32Array(data.connections.length * 6);
    for (let k = 0; k < data.connections.length; k++) {
      const conn = data.connections[k];
      if (!conn || conn.length < 2) continue;
      const i = conn[0];
      const j = conn[1];
      if (i === undefined || j === undefined) continue;
      const i3 = i * 3;
      const j3 = j * 3;
      verts[k * 6] = data.positions[i3] ?? 0;
      verts[k * 6 + 1] = data.positions[i3 + 1] ?? 0;
      verts[k * 6 + 2] = data.positions[i3 + 2] ?? 0;
      verts[k * 6 + 3] = data.positions[j3] ?? 0;
      verts[k * 6 + 4] = data.positions[j3 + 1] ?? 0;
      verts[k * 6 + 5] = data.positions[j3 + 2] ?? 0;
    }
    return verts;
  }, [data]);

  const [pointsGeometry, glowGeometry, linesGeometry] = useMemo(() => {
    const pg = new THREE.BufferGeometry();
    pg.setAttribute("position", new THREE.BufferAttribute(data.positions.slice(), 3));
    pg.setAttribute("color", new THREE.BufferAttribute(data.colors.slice(), 3));
    pg.setAttribute("size", new THREE.BufferAttribute(data.sizes.slice(), 1));

    const gg = new THREE.BufferGeometry();
    gg.setAttribute("position", new THREE.BufferAttribute(data.positions.slice(), 3));

    const lg = new THREE.BufferGeometry();
    lg.setAttribute("position", new THREE.BufferAttribute(connectionPositions.slice(), 3));

    return [pg, gg, lg];
  }, [data, connectionPositions]);

  useFrame((state) => {
    const time = state.clock.getElapsedTime();

    if (groupRef.current) {
      groupRef.current.rotation.x = mouse.y * 0.04;
      groupRef.current.rotation.y = mouse.x * 0.04;
    }

    if (pointsRef.current) {
      const pos = pointsRef.current.geometry.attributes.position;
      if (!pos) return;
      const arr = pos.array as Float32Array;
      if (!arr) return;
      for (let i = 0; i < NEURON_COUNT; i++) {
        const i3 = i * 3;
        const phase = data.phases[i] ?? 0;
        const bx = basePositions[i3] ?? 0;
        const by = basePositions[i3 + 1] ?? 0;
        const bz = basePositions[i3 + 2] ?? 0;
        arr[i3] = bx + Math.sin(time * 0.3 + phase) * 0.03;
        arr[i3 + 1] = by + Math.cos(time * 0.4 + phase * 1.1) * 0.03;
        arr[i3 + 2] = bz + Math.sin(time * 0.2 + phase * 0.9) * 0.03;
      }
      pos.needsUpdate = true;

      const sAttr = pointsRef.current.geometry.attributes.size;
      if (!sAttr) return;
      const sArr = sAttr.array as Float32Array;
      if (!sArr) return;
      for (let i = 0; i < NEURON_COUNT; i++) {
        const phase = data.phases[i] ?? 0;
        const baseSize = data.sizes[i] ?? 0.05;
        sArr[i] = baseSize * (1 + Math.sin(time * 0.5 + phase) * 0.3);
      }
      sAttr.needsUpdate = true;
    }

    if (linesRef.current) {
      const pos = linesRef.current.geometry.attributes.position;
      if (!pos) return;
      const arr = pos.array as Float32Array;
      if (!arr) return;
      for (let k = 0; k < data.connections.length; k++) {
        const conn = data.connections[k];
        if (!conn || conn.length < 2) continue;
        const i = conn[0];
        const j = conn[1];
        if (i === undefined || j === undefined) continue;
        const i3 = i * 3;
        const j3 = j * 3;
        const k6 = k * 6;
        const phaseI = data.phases[i] ?? 0;
        const phaseJ = data.phases[j] ?? 0;
        const t = time * 0.3;
        const bix = basePositions[i3] ?? 0;
        const biy = basePositions[i3 + 1] ?? 0;
        const biz = basePositions[i3 + 2] ?? 0;
        const bjx = basePositions[j3] ?? 0;
        const bjy = basePositions[j3 + 1] ?? 0;
        const bjz = basePositions[j3 + 2] ?? 0;
        arr[k6] = bix + Math.sin(t + phaseI) * 0.03;
        arr[k6 + 1] = biy + Math.cos(t * 1.1 + phaseI * 1.1) * 0.03;
        arr[k6 + 2] = biz + Math.sin(t * 0.9 + phaseI * 0.9) * 0.03;
        arr[k6 + 3] = bjx + Math.sin(t + phaseJ) * 0.03;
        arr[k6 + 4] = bjy + Math.cos(t * 1.1 + phaseJ * 1.1) * 0.03;
        arr[k6 + 5] = bjz + Math.sin(t * 0.9 + phaseJ * 0.9) * 0.03;
      }
      pos.needsUpdate = true;

      const lineMat = linesRef.current.material;
      if (lineMat && !Array.isArray(lineMat)) {
        (lineMat as THREE.LineBasicMaterial).opacity = 0.06 + Math.sin(time * 0.2) * 0.04;
      }
    }

    if (glowPointsRef.current) {
      const glowMat = glowPointsRef.current.material;
      if (glowMat && !Array.isArray(glowMat)) {
        (glowMat as THREE.PointsMaterial).opacity = 0.15 + Math.sin(time * 0.3) * 0.1;
      }
    }
  });

  return (
    <group ref={groupRef}>
      <points ref={pointsRef} geometry={pointsGeometry}>
        <pointsMaterial
          size={0.08}
          vertexColors
          transparent
          opacity={1}
          sizeAttenuation
          blending={THREE.AdditiveBlending}
          depthWrite={false}
        />
      </points>
      <points ref={glowPointsRef} geometry={glowGeometry}>
        <pointsMaterial
          size={0.18}
          color={0xf59e0b}
          transparent
          opacity={0.15}
          sizeAttenuation
          blending={THREE.AdditiveBlending}
          depthWrite={false}
        />
      </points>
      <lineSegments ref={linesRef} geometry={linesGeometry}>
        <lineBasicMaterial
          color={0x22d3ee}
          transparent
          opacity={0.06}
          blending={THREE.AdditiveBlending}
          depthWrite={false}
        />
      </lineSegments>
    </group>
  );
}

export function NeuralBackground() {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return <div className="fixed inset-0 z-0 bg-surface" />;
  }

  return (
    <div className="fixed inset-0 z-0 pointer-events-none">
      <Canvas
        camera={{ position: [0, 0, 9], fov: 55 }}
        dpr={[1, 1.5]}
        gl={{ antialias: false, alpha: true }}
        style={{ background: "transparent" }}
      >
        <NeuralField />
      </Canvas>
    </div>
  );
}
