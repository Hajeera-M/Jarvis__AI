"use client";

import React from "react";

interface VoiceWaveProps {
    isActive: boolean;
    barCount?: number;
}

export function VoiceWave({ isActive, barCount = 24 }: VoiceWaveProps) {
    return (
        <div
            className="flex items-center gap-[3px] h-12 animate-fade-in"
            role="presentation"
            aria-hidden="true"
        >
            {Array.from({ length: barCount }).map((_, i) => {
                // Create a wave pattern — bars in the middle are taller
                const center = barCount / 2;
                const distFromCenter = Math.abs(i - center) / center;
                const maxHeight = 40 - distFromCenter * 28;
                const delay = i * 0.06;

                return (
                    <div
                        key={i}
                        className="rounded-full transition-all duration-300"
                        style={{
                            width: "2.5px",
                            height: isActive ? `${8 + Math.random() * maxHeight}px` : "4px",
                            backgroundColor: isActive
                                ? `rgba(0, 240, 255, ${0.4 + (1 - distFromCenter) * 0.5})`
                                : "rgba(0, 240, 255, 0.15)",
                            animation: isActive
                                ? `wave-bar 0.8s ease-in-out ${delay}s infinite alternate`
                                : "none",
                            boxShadow: isActive
                                ? `0 0 6px rgba(0, 240, 255, ${0.2 + (1 - distFromCenter) * 0.3
                                })`
                                : "none",
                        }}
                    />
                );
            })}
        </div>
    );
}

