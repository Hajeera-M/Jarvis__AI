import React from "react";

export function MetricsSidebar({ 
  msgCount, 
  imgCount, 
  sendPredefinedText,
  onOpenSettings,
  onOpenHistory
}: { 
  msgCount: number;
  imgCount: number;
  sendPredefinedText: (text: string) => void;
  onOpenSettings: () => void;
  onOpenHistory: () => void;
}) {
  
  const suggestions = [
    { text: "What is the Tesla stock price?", icon: "📈" },
    { text: "Convert Apple stock into INR", icon: "🇮🇳" },
    { text: "What is the weather in Bangalore?", icon: "🌤" },
    { text: "Generate an image of a futuristic city", icon: "🎨" },
    { text: "Tell me about Karnataka", icon: "🏛" },
    { text: "What is happening in the world today?", icon: "🌐" },
    { text: "Remember that my favorite color is blue", icon: "🧠" },
    { text: "What is the latest update on Iran?", icon: "📰" },
  ];

  return (
    <div className="hidden lg:flex flex-col w-full gap-6 h-full p-2 overflow-hidden">
      
      {/* Metrics Card - Fixed Top */}
      <div className="flex-none glass-card-sm p-5 border-t-4 border-t-indigo-300">
        <h3 className="text-sm font-bold uppercase tracking-wider text-slate-500 mb-4 flex items-center gap-2">
          <span>📊</span> Today's Metrics
        </h3>
        
        <div className="grid grid-cols-2 gap-3">
          <div className="bg-slate-50/50 border border-slate-100 rounded-2xl p-4 flex flex-col items-center justify-center text-center shadow-sm">
            <span className="text-2xl font-black text-indigo-500 mb-1">{msgCount}</span>
            <span className="text-[10px] font-bold text-slate-400 uppercase">Commands</span>
          </div>
          
          <div className="bg-slate-50/50 border border-slate-100 rounded-2xl p-4 flex flex-col items-center justify-center text-center shadow-sm">
            <span className="text-2xl font-black text-fuchsia-500 mb-1">{imgCount}</span>
            <span className="text-[10px] font-bold text-slate-400 uppercase">Images</span>
          </div>
        </div>
      </div>

      {/* Suggested Prompts - Flexible & Scrollable Middle */}
      <div className="flex-1 glass-card-sm p-5 border-t-4 border-t-mint-300 overflow-hidden flex flex-col" style={{ borderTopColor: "var(--accent-mint)" }}>
        <h3 className="text-sm font-bold uppercase tracking-wider text-slate-500 mb-4 flex items-center gap-2">
          <span>💡</span> Try Asking
        </h3>
        
        <div className="flex-1 overflow-y-auto pr-2 custom-scrollbar space-y-2">
          {suggestions.map((s, idx) => (
             <button
                key={idx}
                onClick={() => sendPredefinedText(s.text)}
                className="w-full text-left bg-white/40 hover:bg-white/80 border border-indigo-100/30 rounded-xl p-3 text-xs font-semibold text-slate-600 transition-all hover:shadow-sm hover:-translate-y-0.5 flex items-center gap-3"
             >
               <span className="text-base bg-indigo-50/50 w-7 h-7 rounded-lg flex flex-shrink-0 items-center justify-center">{s.icon}</span>
               <span className="flex-1 truncate">{s.text}</span>
             </button>
          ))}
        </div>
      </div>

      {/* Quick Nav / Footer - Pinned Bottom */}
      <div className="flex-none glass-card-sm p-4 flex items-center justify-between text-xs font-bold text-slate-400 opacity-80 border-dashed border-indigo-100">
        <span onClick={onOpenSettings} className="flex items-center gap-1.5 hover:text-indigo-500 cursor-pointer transition-colors">⚙️ Settings</span>
        <span onClick={onOpenHistory} className="flex items-center gap-1.5 hover:text-indigo-500 cursor-pointer transition-colors">📄 History</span>
      </div>
      
    </div>
  );
}
