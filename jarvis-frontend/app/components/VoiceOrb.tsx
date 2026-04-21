import React from "react";

export function VoiceOrb({
  state,
  onClick,
}: {
  state: "idle" | "listening" | "thinking" | "speaking";
  onClick: () => void;
}) {
  const getIcon = () => {
    switch (state) {
      case "listening":
        return (
          <svg className="w-8 h-8 text-white drop-shadow-md" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
          </svg>
        );
      case "thinking":
        return <span className="text-2xl drop-shadow-md text-white">⚙️</span>;
      case "speaking":
        return <span className="text-2xl drop-shadow-md text-white">〰️</span>;
      default:
        return (
          <svg className="w-8 h-8 text-white/90 drop-shadow-sm" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
          </svg>
        );
    }
  };

  return (
    <div className="relative flex flex-col items-center justify-center p-2 w-full mt-1">
      <button
        onClick={onClick}
        className={`voice-orb ${state} z-10 flex flex-col items-center justify-center relative`}
        aria-label="Toggle microphone"
        id="voice-orb-btn"
      >
        {/* Aura Wave Rings (Only visible in listening state) */}
        {state === "listening" && (
          <div className="absolute inset-0 flex items-center justify-center pointer-events-none z-[-1]">
            <div className="ripple-ring delay-0"></div>
            <div className="ripple-ring delay-300"></div>
            <div className="ripple-ring delay-600"></div>
          </div>
        )}
        
        {/* Inner Icon container with breathing scale logic */}
        <div className={`z-10 transition-transform duration-500 transform ${state === 'listening' ? 'scale-125' : 'scale-110'}`}>
          {getIcon()}
        </div>
      </button>

      {/* Helper text under mic */}
      <div className="mt-4 text-center w-full">
        <span className="text-[10px] font-semibold tracking-wider uppercase text-slate-400 opacity-60">
           {state === "idle" ? "TAP TO SPEAK" : state}
        </span>
      </div>
    </div>
  );
}
