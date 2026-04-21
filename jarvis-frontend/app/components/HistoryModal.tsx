import React from "react";

interface HistoryModalProps {
  isOpen: boolean;
  onClose: () => void;
  messages: Array<any>;
}

export function HistoryModal({ isOpen, onClose, messages }: HistoryModalProps) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 sm:p-6 animate-fade-in pointer-events-auto">
      {/* Backdrop */}
      <div className="absolute inset-0 bg-slate-900/40 backdrop-blur-sm" onClick={onClose}></div>
      
      {/* Modal */}
      <div className="relative w-full max-w-2xl bg-white/90 backdrop-blur-2xl rounded-3xl shadow-[0_20px_60px_rgba(165,180,252,0.3)] border border-indigo-100/50 flex flex-col max-h-[85vh] overflow-hidden">
        
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-5 border-b border-indigo-50/50 bg-white/50">
          <h2 className="text-xl font-bold text-slate-700 flex items-center gap-2">
            <span>📄</span> Session History
          </h2>
          <button 
            onClick={onClose}
            className="w-8 h-8 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-500 flex items-center justify-center transition-colors"
          >
            ✕
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-6 custom-scrollbar bg-slate-50/30">
          
          {messages.length === 0 ? (
            <div className="text-center py-12 text-slate-400 font-medium tracking-wide">
              No history found for this session.
            </div>
          ) : (
            <div className="space-y-6">
              {messages.map((msg, idx) => (
                <div key={idx} className="bg-white/80 border border-slate-100 rounded-2xl p-4 shadow-sm">
                   
                   <div className="flex justify-between items-start mb-2">
                     <span className={`px-2.5 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider ${msg.role === 'user' ? 'bg-indigo-50 text-indigo-500' : 'bg-slate-100 text-slate-600'}`}>
                        {msg.role === 'user' ? '👤 User Command' : '🧠 JARVIS Response'}
                     </span>
                     <span className="text-[10px] font-semibold text-slate-400">
                        {msg.timestamp?.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                     </span>
                   </div>

                   <p className="text-sm text-slate-700 font-medium whitespace-pre-wrap leading-relaxed">
                     {msg.text}
                   </p>

                   {msg.imageUrl && (
                      <div className="mt-3 overflow-hidden rounded-xl border border-indigo-50">
                        <img src={msg.imageUrl} alt="Generated graphic" className="w-full max-h-[250px] object-cover" />
                      </div>
                   )}
                </div>
              ))}
            </div>
          )}

        </div>

      </div>
    </div>
  );
}
