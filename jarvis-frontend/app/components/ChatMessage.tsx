import React from "react";

export interface ChatMessageProps {
  msg: {
    role: "user" | "jarvis";
    text: string;
    source?: string;
    imageUrl?: string;
    status?: "success" | "failed";
    timestamp: Date;
  };
}

export function ChatMessage({ msg }: ChatMessageProps) {
  // Source Badges Style Mapper
  const getBadge = (source: string) => {
    const map: Record<string, { label: string; cls: string }> = {
      ai: { label: "🧠 AI", cls: "bg-indigo-500/10 text-indigo-400 border-indigo-500/20" },
      stock: { label: "📈 STOCK", cls: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20" },
      search: { label: "🔍 SEARCH", cls: "bg-sky-500/10 text-sky-400 border-sky-500/20" },
      automation: { label: "⚡ AUTO", cls: "bg-amber-500/10 text-amber-400 border-amber-500/20" },
      image: { label: "🎨 IMAGE", cls: "bg-fuchsia-500/10 text-fuchsia-400 border-fuchsia-500/20" },
      weather: { label: "🌤 WEATHER", cls: "bg-cyan-500/10 text-cyan-400 border-cyan-500/20" },
      tool: { label: "🔧 TOOL", cls: "bg-slate-500/10 text-slate-400 border-slate-500/20" },
    };
    const badge = map[source] || map.ai;
    return (
      <span className={`px-2.5 py-0.5 rounded-full text-[9px] font-bold border backdrop-blur-md ${badge.cls}`}>
        {badge.label}
      </span>
    );
  };

  const isFailed = msg.status === "failed";
  const isUser = msg.role === "user";

  return (
    <div className={`flex w-full ${isUser ? "justify-end" : "justify-start"} animate-fade-in my-3 font-mono`}>
      <div 
        className={`relative max-w-[90%] px-4 py-3 rounded-2xl ${
          isUser 
            ? "bg-cyan-500/10 border border-cyan-500/20 rounded-tr-none text-cyan-100" 
            : isFailed
              ? "bg-rose-500/10 border border-rose-500/20 rounded-tl-none text-rose-400"
              : "bg-white/5 border border-white/10 rounded-tl-none text-slate-300"
        }`}
      >
        {/* Assistant Header inside message */}
        {!isUser && (
          <div className="flex items-center gap-2 mb-2 pb-2 border-b border-white/5">
            <div className="w-5 h-5 rounded-full bg-gradient-to-br from-cyan-500 to-indigo-600 flex items-center justify-center text-[9px] text-white shadow-sm font-bold">
              J
            </div>
            {msg.source && getBadge(msg.source)}
            {isFailed && (
              <span className="px-2 py-0.5 rounded-full text-[9px] font-bold border border-rose-500/30 bg-rose-500/10 text-rose-400 animate-pulse">
                FAILURE
              </span>
            )}
          </div>
        )}

        {/* Message Text */}
        <p className={`text-[13px] leading-relaxed whitespace-pre-wrap ${isUser ? "font-bold tracking-tight" : "font-sans font-medium"}`}>
          {msg.text}
        </p>

        {/* Image Attachment Rendering */}
        {msg.imageUrl && (
          <div className="mt-4 rounded-xl overflow-hidden border border-white/10 shadow-2xl relative group">
            <img
              src={msg.imageUrl}
              alt="Generated Content"
              className="w-full h-auto max-h-[400px] object-cover transition-transform duration-700 group-hover:scale-105"
              onError={(e) => { (e.target as HTMLImageElement).style.top = "-9999px"; }}
            />
          </div>
        )}

        {/* Timestamp */}
        <span className={`text-[8px] block mt-2 font-bold uppercase tracking-tighter ${isUser ? "text-cyan-600 text-right" : "text-slate-600"}`}>
          {msg.role === "user" ? "Operator" : "Core"} • {msg.timestamp.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
        </span>
      </div>
    </div>
  );
}

