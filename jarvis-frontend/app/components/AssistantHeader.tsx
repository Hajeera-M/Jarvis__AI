"use client";

import React, { useState } from "react";
import { ProfileModal } from "./ProfileModal";

export function AssistantHeader({ state }: { state: string }) {
  const [isProfileOpen, setIsProfileOpen] = useState(false);

  const statusLabel = {
    idle: "Ready",
    listening: "Listening...",
    thinking: "Thinking...",
    speaking: "Speaking...",
  }[state as keyof typeof statusLabel] || "Ready";

  return (
    <>
      <ProfileModal isOpen={isProfileOpen} onClose={() => setIsProfileOpen(false)} />
      
      <header className="flex items-center justify-between px-6 py-5 glass-card-sm mb-6 z-10 w-full relative">
        <div className="flex items-center gap-4">
          {/* Modern minimal logo/icon */}
          <div 
            className="w-10 h-10 rounded-xl flex items-center justify-center text-white font-bold text-lg shadow-sm"
            style={{ background: "var(--gradient-orb)" }}
          >
            J.
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-tight" style={{ color: "var(--text-primary)" }}>
              JARVIS
            </h1>
            <p className="text-xs font-medium" style={{ color: "var(--text-muted)", letterSpacing: "0.08em" }}>
              SMART VOICE ASSISTANT
            </p>
          </div>
        </div>

        <div className="flex items-center gap-5">
          {/* Status Indicator */}
          <div className="hidden sm:flex items-center gap-2 bg-white/50 px-3 py-1.5 rounded-full border border-[var(--border-light)] shadow-sm">
            <span className={`status-dot status-${state}`}></span>
            <span className="text-xs font-semibold uppercase tracking-wider" style={{ color: "var(--text-secondary)" }}>
              {statusLabel}
            </span>
          </div>

          {/* Profile Avatar */}
          <div 
            onClick={() => setIsProfileOpen(true)}
            className="relative z-50 cursor-pointer pointer-events-auto w-10 h-10 rounded-full bg-indigo-100 border-2 border-white shadow-sm flex items-center justify-center overflow-hidden hover:scale-105 transition-transform"
          >
             <img src="https://ui-avatars.com/api/?name=HJ&background=A5B4FC&color=fff" alt="User" className="w-full h-full object-cover pointer-events-none" />
          </div>
        </div>
      </header>
    </>
  );
}
