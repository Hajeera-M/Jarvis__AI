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
      ai: { label: "🧠 AI", cls: "bg-indigo-50/50 text-indigo-500 border-indigo-200" },
      stock: { label: "📈 STOCK", cls: "bg-emerald-50/50 text-emerald-600 border-emerald-200" },
      search: { label: "🔍 SEARCH", cls: "bg-sky-50/50 text-sky-500 border-sky-200" },
      automation: { label: "⚡ AUTO", cls: "bg-amber-50/50 text-amber-600 border-amber-200" },
      image: { label: "🎨 IMAGE", cls: "bg-fuchsia-50/50 text-fuchsia-500 border-fuchsia-200" },
      weather: { label: "🌤 WEATHER", cls: "bg-cyan-50/50 text-cyan-600 border-cyan-200" },
      tool: { label: "🔧 TOOL", cls: "bg-slate-50/50 text-slate-500 border-slate-200" },
    };
    const badge = map[source] || map.ai;
    return (
      <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold border backdrop-blur-md ${badge.cls}`}>
        {badge.label}
      </span>
    );
  };

  const isFailed = msg.status === "failed";
  const isUser = msg.role === "user";

  return (
    <div className={`flex w-full ${isUser ? "justify-end" : "justify-start"} animate-fade-in my-3`}>
      <div 
        className={`relative max-w-[85%] sm:max-w-[75%] px-5 py-4 rounded-3xl ${
          isUser 
            ? "bg-gradient-to-br from-indigo-50 to-indigo-100/50 border border-indigo-100/50 rounded-br-sm shadow-sm" 
            : isFailed
              ? "bg-gradient-to-br from-rose-50/80 to-rose-100/50 border border-rose-200/60 rounded-bl-sm shadow-sm"
              : "glass-card rounded-bl-sm"
        }`}
      >
        {/* Assistant Header inside message */}
        {!isUser && (
          <div className="flex items-center gap-2 mb-2 pb-2 border-b border-black/5">
            <div className="w-6 h-6 rounded-full bg-gradient-to-br from-indigo-300 to-indigo-400 flex items-center justify-center text-[10px] text-white shadow-sm font-bold">
              J
            </div>
            {msg.source && getBadge(msg.source)}
            {isFailed && (
              <span className="px-2 py-0.5 rounded-full text-[10px] font-bold border border-rose-200 bg-rose-50 text-rose-500 animate-pulse">
                ⚠️ FAILED FALLBACK
              </span>
            )}
            {!isFailed && msg.source && msg.status && (
              <span className="px-2 py-0.5 rounded-full text-[10px] font-bold border border-emerald-200 bg-emerald-50 text-emerald-500">
                ✓ SUCCESS
              </span>
            )}
          </div>
        )}

        {/* Message Text */}
        <p className={`text-[14px] leading-relaxed whitespace-pre-wrap font-medium ${isFailed ? "text-rose-900" : "text-slate-700"}`}>
          {msg.text}
        </p>

        {/* Image Attachment Rendering */}
        {msg.imageUrl && (
          <div className="mt-4 rounded-xl overflow-hidden border-2 border-indigo-50/50 shadow-md relative group">
            <div className="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent z-10 pointer-events-none"></div>
            <img
              src={msg.imageUrl}
              alt="Generated Content"
              className="w-full h-auto max-h-[300px] object-cover transition-transform duration-700 group-hover:scale-105"
              onError={(e) => { (e.target as HTMLImageElement).style.display = "none"; }}
            />
          </div>
        )}

        {/* Timestamp */}
        <span className={`text-[9px] block mt-2 font-semibold uppercase tracking-wider ${isUser ? "text-indigo-300 text-right" : "text-slate-400"}`}>
          {msg.timestamp.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
        </span>
      </div>
    </div>
  );
}
