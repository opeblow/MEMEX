"use client";

import { OrbitControls } from "@react-three/drei";
import { useThree } from "@react-three/fiber";
import { useEffect } from "react";
import * as THREE from "three";

interface UniverseControlsProps {
  target: [number, number, number];
  onTargetChange: (target: [number, number, number]) => void;
  selectedId: string | null;
}

export function UniverseControls({ target, selectedId }: UniverseControlsProps) {
  const { camera } = useThree();

  useEffect(() => {
    if (selectedId) {
      const end = new THREE.Vector3(target[0], target[1], target[2]);
      const start = camera.position.clone();
      const duration = 1000;
      const startTime = Date.now();

      function animate() {
        const elapsed = Date.now() - startTime;
        const t = Math.min(elapsed / duration, 1);
        const ease = 1 - (1 - t) ** 3;

        camera.position.lerpVectors(start, end.clone().add(new THREE.Vector3(0, 0, 3)), ease);
        camera.lookAt(end);

        if (t < 1) {
          requestAnimationFrame(animate);
        }
      }

      animate();
    }
  }, [selectedId, target, camera]);

  return (
    <OrbitControls
      enableDamping
      dampingFactor={0.05}
      rotateSpeed={0.5}
      zoomSpeed={0.8}
      minDistance={2}
      maxDistance={30}
      autoRotate={!selectedId}
      autoRotateSpeed={0.3}
    />
  );
}
