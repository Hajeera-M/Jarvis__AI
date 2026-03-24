"use client";

import React from "react";

type AppState = "idle" | "listening" | "processing" | "speaking";

interface MicButtonProps {
    state: AppState;
    onClick: () => void;
}

/* ── Inline SVG Icons (no external dependency) ─────────────── */

function MicIcon({ className }: { className?: string }) {
    return (
        <svg
            xmlns="http://www.w3.org/2000/svg"
            width="32"
            height="32"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            className={className}
        >
            <path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z" />
            <path d="M19 10v2a7 7 0 0 1-14 0v-2" />
            <line x1="12" x2="12" y1="19" y2="22" />
        </svg>
    );
}

function SpinnerIcon({ className }: { className?: string }) {
    return (
        <svg
            xmlns="http://www.w3.org/2000/svg"
            width="32"
            height="32"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            className={className}
        >
            <path d="M21 12a9 9 0 1 1-6.219-8.56" />
        </svg>
    );
}

function VolumeIcon({ className }: { className?: string }) {
    return (
        <svg
            xmlns="http://www.w3.org/2000/svg"
            width="32"
            height="32"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            className={className}
        >
            <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5" />
            <path d="M15.54 8.46a5 5 0 0 1 0 7.07" />
            <path d="M19.07 4.93a10 10 0 0 1 0 14.14" />
        </svg>
    );
}

/* ── Mic Button Component ──────────────────────────────────── */

export function MicButton({ state, onClick }: MicButtonProps) {
    const isActive = state === "listening";
    const isProcessing = state === "processing";
    const isSpeaking = state === "speaking";

    return (
        <button
            id="mic-button"
            onClick={onClick}
            disabled={isProcessing}
            className={`
        relative w-24 h-24 rounded-full flex items-center justify-center
        transition-all duration-500 ease-out
        focus:outline-none focus:ring-2 focus:ring-jarvis-cyan/30 focus:ring-offset-4 focus:ring-offset-jarvis-dark
        ${isProcessing ? "cursor-wait" : "cursor-pointer"}
        ${isActive
                    ? "bg-jarvis-cyan/20 scale-110"
                    : isSpeaking
                        ? "bg-jarvis-blue/20"
                        : "bg-white/5 hover:bg-white/10 hover:scale-105"
                }
      `}
            aria-label={
                isActive
                    ? "Stop listening"
                    : isProcessing
                        ? "Processing"
                        : isSpeaking
                            ? "Stop speaking"
                            : "Start listening"
            }
        >
            {/* Outer ring */}
            <div
                className={`mic-ring transition-all duration-500 ${isActive || isSpeaking ? "mic-ring-active" : ""
                    }`}
            />

            {/* Ripple rings when active */}
            {isActive && (
                <>
                    <div className="ripple-ring" />
                    <div className="ripple-ring" />
                    <div className="ripple-ring" />
                </>
            )}

            {/* Icon */}
            <div className="relative z-10">
                {isProcessing ? (
                    <SpinnerIcon className="text-jarvis-cyan/80 animate-spin" />
                ) : isSpeaking ? (
                    <VolumeIcon className="text-jarvis-cyan animate-pulse" />
                ) : (
                    <MicIcon
                        className={`transition-colors duration-300 ${isActive ? "text-jarvis-cyan" : "text-jarvis-cyan/60"
                            }`}
                    />
                )}
            </div>
        </button>
    );
}
