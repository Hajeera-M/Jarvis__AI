"use client";

import React, { useRef, useMemo, useEffect } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import * as THREE from "three";

function NeuralParticles({ state }: { state: string }) {
  const pointsRef = useRef<THREE.Points>(null!);
  const count = 4000;
  
  const positions = useMemo(() => {
    const pos = new Float32Array(count * 3);
    for (let i = 0; i < count; i++) {
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(2 * Math.random() - 1);
      const r = 2.0;
      
      pos[i * 3] = r * Math.sin(phi) * Math.cos(theta);
      pos[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta);
      pos[i * 3 + 2] = r * Math.cos(phi);
    }
    return pos;
  }, []);

  useFrame((clockState, delta) => {
    if (!pointsRef.current) return;
    
    let speed = 0.15;
    if (state === "thinking") speed = 0.8;
    if (state === "listening") speed = 0.4;
    if (state === "speaking") speed = 0.2;
    
    pointsRef.current.rotation.y += delta * speed;
    pointsRef.current.rotation.x += delta * speed * 0.3;
    
    // Scale pulse
    const time = clockState.clock.getElapsedTime();
    const s = 1 + Math.sin(time * 2) * 0.05;
    pointsRef.current.scale.set(s, s, s);
  });

  return (
    <points ref={pointsRef}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={count}
          array={positions}
          itemSize={3}
        />
      </bufferGeometry>
      <pointsMaterial
        size={0.015}
        color={state === "thinking" ? "#f59e0b" : state === "listening" ? "#06b6d4" : "#8b5cf6"}
        transparent
        opacity={0.6}
        sizeAttenuation={true}
        blending={THREE.AdditiveBlending}
      />
    </points>
  );
}

function InnerCore({ state }: { state: string }) {
    const meshRef = useRef<THREE.Mesh>(null!);
    
    useFrame((clockState) => {
        if (!meshRef.current) return;
        const time = clockState.clock.getElapsedTime();
        const s = 1.2 + Math.sin(time * 4) * 0.1;
        meshRef.current.scale.set(s, s, s);
    });

    return (
        <mesh ref={meshRef}>
            <sphereGeometry args={[0.6, 32, 32]} />
            <meshStandardMaterial 
                color={state === "thinking" ? "#f59e0b" : "#06b6d4"} 
                emissive={state === "thinking" ? "#d97706" : "#0891b2"}
                emissiveIntensity={3}
                transparent 
                opacity={0.2} 
                wireframe
            />
        </mesh>
    );
}

function ScanningRings({ state }: { state: string }) {
    const groupRef = useRef<THREE.Group>(null!);
    
    useFrame((clockState, delta) => {
        if (!groupRef.current) return;
        groupRef.current.rotation.z += delta * 0.5;
        groupRef.current.rotation.x += delta * 0.2;
    });

    return (
        <group ref={groupRef}>
            {[1.8, 2.2, 2.6].map((r, i) => (
                <mesh key={i} rotation={[Math.random() * Math.PI, Math.random() * Math.PI, 0]}>
                    <torusGeometry args={[r, 0.01, 16, 100]} />
                    <meshBasicMaterial 
                        color={state === "listening" ? "#22d3ee" : "#1e293b"} 
                        transparent 
                        opacity={0.1} 
                    />
                </mesh>
            ))}
        </group>
    );
}

export default function ParticleGlobe({ state }: { state: string }) {
  const [mounted, setMounted] = React.useState(false);
  
  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) return null;

  return (
    <div className="w-full h-full flex items-center justify-center bg-transparent">
      <Canvas 
        camera={{ position: [0, 0, 5.5], fov: 40 }}
        gl={{ antialias: true, alpha: true }}
      >
        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} intensity={1.5} color="#06b6d4" />
        
        <NeuralParticles state={state} />
        <InnerCore state={state} />
        <ScanningRings state={state} />
      </Canvas>

      {/* Radial Glow Overlay */}
      <div className="absolute inset-0 pointer-events-none flex items-center justify-center">
        <div className={`w-[350px] h-[350px] rounded-full blur-[90px] transition-all duration-700 ${
            state === 'thinking' ? 'bg-amber-500/10' : 
            state === 'listening' ? 'bg-cyan-500/15' : 
            state === 'speaking' ? 'bg-purple-500/10' : 'bg-cyan-500/5'
        }`}></div>
      </div>
    </div>
  );
}
