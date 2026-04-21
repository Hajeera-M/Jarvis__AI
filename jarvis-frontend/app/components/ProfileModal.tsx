import React from "react";
import { useRouter } from "next/navigation";

interface ProfileModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export function ProfileModal({ isOpen, onClose }: ProfileModalProps) {
  const router = useRouter();
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[110] flex items-center justify-center p-4 sm:p-6 animate-fade-in pointer-events-auto">
      {/* Backdrop */}
      <div className="absolute inset-0 bg-slate-900/40 backdrop-blur-sm" onClick={onClose}></div>
      
      {/* Modal */}
      <div className="relative w-full max-w-sm bg-white/95 backdrop-blur-3xl rounded-3xl shadow-[0_20px_60px_rgba(165,180,252,0.3)] border border-indigo-100/50 flex flex-col overflow-hidden">
        
        {/* Header / Avatar Banner */}
        <div className="relative h-24 bg-gradient-to-r from-indigo-300 via-purple-300 to-pink-300">
           <button 
              onClick={onClose}
              className="absolute top-4 right-4 w-8 h-8 rounded-full bg-black/10 hover:bg-black/20 text-white flex items-center justify-center transition-colors shadow-sm"
            >
              ✕
            </button>
        </div>

        {/* Profile Info */}
        <div className="px-6 pb-6 pt-0 relative flex-1">
           {/* Overlapping Avatar */}
           <div className="w-20 h-20 rounded-full bg-white border-4 border-white shadow-md flex items-center justify-center overflow-hidden -mt-10 mx-auto z-10 relative">
              <img src="https://ui-avatars.com/api/?name=HJ&background=A5B4FC&color=fff&size=128" alt="Hajeera" className="w-full h-full object-cover" />
           </div>

           <div className="text-center mt-3 mb-6">
              <h2 className="text-xl font-bold text-slate-800 tracking-tight">Hajeera</h2>
              <p className="text-xs font-semibold text-indigo-500 uppercase tracking-widest mt-0.5">App Owner</p>
           </div>

           {/* Config Badges */}
           <div className="space-y-3">
              <div className="flex items-center justify-between bg-slate-50 border border-slate-100 rounded-xl p-3">
                 <div className="flex items-center gap-2 text-slate-500 font-semibold text-xs uppercase tracking-wide">
                    <span>🌐</span> Languages
                 </div>
                 <span className="text-sm font-bold text-slate-700">En / Hi / Hinglish</span>
              </div>
              
              <div className="flex items-center justify-between bg-slate-50 border border-slate-100 rounded-xl p-3">
                 <div className="flex items-center gap-2 text-slate-500 font-semibold text-xs uppercase tracking-wide">
                    <span>⚙️</span> Demo Mode
                 </div>
                 <div className="px-2.5 py-1 bg-mint-50/50 text-emerald-600 border border-emerald-100 rounded-lg text-xs font-bold uppercase">
                    Enabled
                 </div>
              </div>
           </div>
        </div>

        {/* Footer Actions */}
        <div className="p-4 bg-slate-50 border-t border-slate-100 flex gap-3">
           <button 
             onClick={() => {
               localStorage.removeItem("jarvis_user");
               onClose();
               router.replace("/signin");
             }}
             className="flex-1 py-2.5 rounded-xl text-xs font-bold text-rose-500 bg-rose-50 border border-rose-200 hover:bg-rose-100 transition-colors uppercase tracking-wider shadow-sm"
           >
             Logout
           </button>
           <button 
             onClick={onClose}
             className="flex-1 py-2.5 rounded-xl text-xs font-bold text-white transition-all shadow-sm uppercase tracking-wider hover:opacity-90"
             style={{ background: "var(--gradient-orb)" }}
           >
             Close
           </button>
        </div>

      </div>
    </div>
  );
}
