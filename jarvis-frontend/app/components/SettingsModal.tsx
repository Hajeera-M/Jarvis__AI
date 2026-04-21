import React, { useState } from "react";

interface SettingsModalProps {
  isOpen: boolean;
  onClose: () => void;
  onClearMemory: () => void;
}

export function SettingsModal({ isOpen, onClose, onClearMemory }: SettingsModalProps) {
  const [demoMode, setDemoMode] = useState(true);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 sm:p-6 animate-fade-in pointer-events-auto">
      {/* Backdrop */}
      <div className="absolute inset-0 bg-slate-900/40 backdrop-blur-sm" onClick={onClose}></div>
      
      {/* Modal */}
      <div className="relative w-full max-w-md bg-white/95 backdrop-blur-3xl rounded-3xl shadow-[0_20px_60px_rgba(165,180,252,0.3)] border border-indigo-100/50 flex flex-col overflow-hidden">
        
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-5 border-b border-indigo-50/50 bg-white/50">
          <h2 className="text-xl font-bold text-slate-700 flex items-center gap-2">
            <span>⚙️</span> Assistant Settings
          </h2>
          <button 
            onClick={onClose}
            className="w-8 h-8 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-500 flex items-center justify-center transition-colors"
          >
            ✕
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          
          {/* Language / Voice */}
          <div className="space-y-4">
             <div>
                <label className="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">Primary Language</label>
                <select className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-2.5 text-sm font-medium text-slate-700 outline-none focus:border-indigo-300 focus:ring-2 focus:ring-indigo-100 transition-all">
                  <option>English</option>
                  <option>Hindi</option>
                  <option>Telugu</option>
                  <option>Kannada</option>
                </select>
             </div>
             
             <div>
                <label className="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">Voice Model</label>
                <select className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-2.5 text-sm font-medium text-slate-700 outline-none focus:border-indigo-300 focus:ring-2 focus:ring-indigo-100 transition-all">
                  <option>Female (Default, Indian)</option>
                  <option>Male (British)</option>
                  <option>Female (US)</option>
                </select>
             </div>

             <div>
                <label className="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">Active Theme</label>
                <div className="w-full bg-indigo-50/50 border border-indigo-100 rounded-xl px-4 py-2.5 text-sm font-bold text-indigo-500 flex items-center justify-between">
                  <span>Soft Pastel Glassmorphism</span>
                  <span className="w-3 h-3 rounded-full bg-indigo-300 animate-pulse"></span>
                </div>
             </div>
          </div>

          <div className="w-full h-px bg-slate-100"></div>

          {/* Toggles */}
          <div className="flex items-center justify-between bg-slate-50/50 p-4 rounded-xl border border-slate-100">
             <div>
               <p className="text-sm font-bold text-slate-700">Demo Safe Mode</p>
               <p className="text-[10px] font-semibold text-slate-400 uppercase tracking-wider mt-0.5">Blocks unstable endpoints</p>
             </div>
             <button 
                onClick={() => setDemoMode(!demoMode)}
                className={`w-12 h-6 rounded-full p-1 transition-colors duration-300 ease-in-out ${demoMode ? 'bg-indigo-400' : 'bg-slate-300'}`}
             >
                <div className={`w-4 h-4 bg-white rounded-full transition-transform duration-300 ease-in-out ${demoMode ? 'translate-x-6' : 'translate-x-0'}`}></div>
             </button>
          </div>

        </div>

        {/* Footer */}
        <div className="p-4 bg-slate-50 border-t border-slate-100 flex justify-between items-center">
           <button 
             onClick={() => {
               onClearMemory();
               onClose();
             }}
             className="px-4 py-2.5 rounded-xl text-xs font-bold text-rose-500 bg-rose-50 border border-rose-200 hover:bg-rose-100 transition-colors uppercase tracking-wider"
           >
             Clear Memory
           </button>
           
           <button 
             onClick={onClose}
             className="px-6 py-2.5 rounded-xl text-xs font-bold text-white transition-transform hover:scale-105 shadow-sm uppercase tracking-wider"
             style={{ background: "var(--gradient-orb)" }}
           >
             Save & Close
           </button>
        </div>

      </div>
    </div>
  );
}
