"use client";

import { useState, useRef, useEffect } from "react";
import { useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import { 
  Plus, Database, History, User, Terminal, 
  Settings, Mic, Square, Trash2, Globe, Cpu 
} from "lucide-react";

import dynamic from "next/dynamic";
import { SettingsModal } from "./components/SettingsModal";
import { HistoryModal } from "./components/HistoryModal";
import { ChatMessage } from "./components/ChatMessage";
import { initVoices, getPreferredVoice } from "../lib/voiceHelper";

const ParticleGlobe = dynamic(() => import("./components/ParticleGlobe"), { 
  ssr: false, 
  loading: () => <div className="w-[420px] h-[420px] flex items-center justify-center text-cyan-500/20 tracking-widest text-[10px]">INITIALIZING CORE...</div>
});

interface ChatMessageObj {
  role: "user" | "jarvis";
  text: string;
  source?: string;
  imageUrl?: string;
  status?: "success" | "failed";
  timestamp: Date;
}

export default function Home() {
  const [state, setState] = useState<"idle" | "listening" | "thinking" | "speaking">("idle");
  const [messages, setMessages] = useState<ChatMessageObj[]>([]);
  const [textInput, setTextInput] = useState("");
  const [interimText, setInterimText] = useState("");
  const chatEndRef = useRef<HTMLDivElement>(null);
  
  // Modal States
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [isHistoryOpen, setIsHistoryOpen] = useState(false);
  const [isContinuous, setIsContinuous] = useState(true);
  const recognitionRef = useRef<any>(null);
  const isContinuousRef = useRef(true);
  const processingRef = useRef(false);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, interimText]);

  useEffect(() => {
    const saved = localStorage.getItem("jarvis_messages");
    if (saved) {
      try {
        setMessages(JSON.parse(saved).map((m: any) => ({ ...m, timestamp: new Date(m.timestamp) })));
      } catch (e) {}
    }
    initVoices();
  }, []);

  useEffect(() => {
    if (messages.length > 0) localStorage.setItem("jarvis_messages", JSON.stringify(messages));
  }, [messages]);

  const router = useRouter();
  const [authChecked, setAuthChecked] = useState(false);
  useEffect(() => {
    if (!localStorage.getItem("jarvis_user")) router.replace("/signin");
    else setAuthChecked(true);
  }, [router]);

  async function processQuery(text: string) {
    if (!text.trim()) return;
    
    // 1. Force stop and disable recognition before processing starts
    if (recognitionRef.current) {
        try {
            recognitionRef.current.onend = null;
            recognitionRef.current.stop();
        } catch(e) {}
    }
    
    processingRef.current = true;
    setMessages(prev => [...prev, { role: "user", text, timestamp: new Date() }]);
    setState("thinking");
    setInterimText("");

    try {
      const controller = new AbortController();
      const id = setTimeout(() => controller.abort(), 30000); // 30s timeout for safety

      const res = await fetch("http://127.0.0.1:8000/jarvis", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ input: text }),
        signal: controller.signal
      });
      clearTimeout(id);
      const data = await res.json();
      
      const reply = data.response || "System online. No change detected.";
      const spoken = data.spoken_response || reply;
      
      setMessages(prev => [...prev, { 
        role: "jarvis", 
        text: reply, 
        source: data.source || "ai", 
        imageUrl: data.image_url, 
        status: data.status || "success", 
        timestamp: new Date() 
      }]);

      if (typeof window !== "undefined" && window.speechSynthesis) {
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(spoken);
        utterance.rate = 1.18; // Sharp, fast, professional
        const voice = getPreferredVoice(data.language || "en");
        if (voice) utterance.voice = voice;
        
        utterance.onstart = () => setState("speaking");
        utterance.onend = () => {
          setState("idle");
          processingRef.current = false;
          
          if (data.source === "exit") {
            setTimeout(() => {
                window.close();
                localStorage.removeItem("jarvis_user");
                window.location.href = "/signin";
            }, 500);
            return;
          }

          // Only resume if we are STILL in continuous mode
          if (isContinuousRef.current) {
            setTimeout(startListening, 600); // Increased buffer to avoid hearing trailing audio
          }
        };
        utterance.onerror = () => {
          setState("idle");
          processingRef.current = false;
          if (isContinuousRef.current) setTimeout(startListening, 600);
        };
        
        window.speechSynthesis.speak(utterance);
      } else {
        setState("idle");
        processingRef.current = false;
        
        if (data.source === "exit") {
          window.close();
          localStorage.removeItem("jarvis_user");
          window.location.href = "/signin";
          return;
        }

        if (isContinuousRef.current) setTimeout(startListening, 600);
      }
    } catch (err: any) {
      if (err.name === 'AbortError') {
        console.error("JARVIS: Request timed out.");
        setMessages(prev => [...prev, { role: "jarvis", text: "I'm sorry, the request timed out. My communication link might be slow.", timestamp: new Date() }]);
      } else {
        console.error("JARVIS: Search/Automation Error:", err);
      }
      setState("idle");
      processingRef.current = false;
      if (isContinuousRef.current) setTimeout(startListening, 600);
    }
  }

  const startListening = () => {
    if (processingRef.current) return;
    if (state === "listening" || state === "speaking" || state === "thinking") return;
    
    // Stop previous if exists
    const Recognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!Recognition) {
        console.error("Critical: Speech Recognition API not supported in this browser.");
        alert("Your browser does not support Speech Recognition. Please use Chrome or Edge.");
        return;
    }

    // Ensure we clear previous instance properly
    if (recognitionRef.current) {
        try { 
            recognitionRef.current.onend = null;
            recognitionRef.current.stop(); 
        } catch(e) {}
    }

    const recognition = new Recognition();
    recognition.lang = "en-US";
    recognition.interimResults = true;
    recognition.continuous = false; 

    recognition.onstart = () => {
        console.log("JARVIS: Mic Link Active.");
        setState("listening");
    };

    recognition.onresult = (e: any) => {
      const transcript = Array.from(e.results).map((r: any) => r[0].transcript).join("");
      setInterimText(transcript);
      if (e.results[0].isFinal) {
          recognition.stop();
          processQuery(transcript);
      }
    };

    recognition.onerror = (event: any) => {
        const error = event.error;
        if (error !== 'no-speech' && error !== 'aborted') {
            console.error("Speech Recognition Error:", error);
        }
        
        // On network error, stop retrying — speech service is unavailable
        if (error === 'network') {
            console.error("JARVIS: Speech service network error. Retrying in 3s...");
            setState("idle");
            if (isContinuousRef.current && !processingRef.current) {
                setTimeout(startListening, 3000);
            }
            return;
        }
        
        if (error === 'not-allowed') {
            console.error("JARVIS: Microphone permission denied.");
            setIsContinuous(false);
            isContinuousRef.current = false;
            setState("idle");
            return;
        }
        
        if (isContinuousRef.current && !processingRef.current) {
            setTimeout(startListening, 500);
        }
    };

    recognition.onend = () => { 
        if (!processingRef.current && isContinuousRef.current) {
            setTimeout(startListening, 200);
        } else if (!processingRef.current) {
            setState("idle");
        }
    };
    
    recognitionRef.current = recognition;
    try {
        recognition.start();
    } catch(e) {}
  };

  const handleMicClick = () => {
    console.log("JARVIS: User triggered mic protocol.");
    if (state === "speaking") {
      window.speechSynthesis.cancel();
      processingRef.current = false;
      setState("idle");
      return;
    }
    
    const nextContinuous = !isContinuous;
    setIsContinuous(nextContinuous);
    isContinuousRef.current = nextContinuous;

    if (nextContinuous) {
        // Request mic permission explicitly if needed
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(() => {
                startListening();
                if (!document.fullscreenElement) {
                    document.documentElement.requestFullscreen().catch(() => {});
                }
            })
            .catch(err => {
                console.error("Mic Permission Denied:", err);
                setIsContinuous(false);
                isContinuousRef.current = false;
                alert("Microphone access is required for JARVIS. Please enable it in your browser settings.");
            });
    } else {
        if (recognitionRef.current) {
            recognitionRef.current.onend = null;
            recognitionRef.current.stop();
        }
        setState("idle");
    }
  };

  const handleStop = () => {
    if (typeof window !== "undefined" && window.speechSynthesis) {
      window.speechSynthesis.cancel();
    }
    setState("idle");
  };

  if (!authChecked) return null;

  return (
    <div className="bg-[#050608] h-screen w-screen text-white font-mono selection:bg-cyan-500/30 overflow-hidden flex">
      <SettingsModal isOpen={isSettingsOpen} onClose={() => setIsSettingsOpen(false)} onClearMemory={() => setMessages([])} />
      <HistoryModal isOpen={isHistoryOpen} onClose={() => setIsHistoryOpen(false)} messages={messages} />

      {/* ─── LEFT DOCK ─────────────────────────────────────── */}
      <nav className="w-20 border-r border-white/5 flex flex-col items-center py-8 gap-8 bg-black/40 backdrop-blur-xl">
         <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-cyan-500 to-purple-600 flex items-center justify-center shadow-lg shadow-cyan-500/20 mb-4">
            <Cpu className="text-white w-6 h-6" />
         </div>
         
         <div className="flex flex-col gap-6 flex-1">
            <button title="System History" onClick={() => setIsHistoryOpen(true)} className="p-3 rounded-xl hover:bg-white/5 transition-colors group">
               <History className="w-6 h-6 text-slate-400 group-hover:text-cyan-400 transition-colors" />
            </button>
         </div>

         <button onClick={() => setIsSettingsOpen(true)} className="p-3 rounded-xl hover:bg-white/5 transition-colors group">
            <Settings className="w-6 h-6 text-slate-400 group-hover:text-white transition-colors" />
         </button>
      </nav>

      {/* ─── MAIN VISUAL HUB ──────────────────────────────── */}
      <main className="flex-1 flex flex-col relative overflow-hidden bg-[#050608] min-w-0">
         {/* Futuristic Gradient & Noise Overlay */}
         <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_0%,rgba(6,182,212,0.1)_0%,transparent_70%),radial-gradient(circle_at_0%_100%,rgba(139,92,246,0.05)_0%,transparent_50%)] pointer-events-none"></div>
         
         {/* Grid System */}
         <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808008_1px,transparent_1px),linear-gradient(to_bottom,#80808008_1px,transparent_1px)] bg-[size:40px_40px] pointer-events-none"></div>
         
         {/* Scanline Effect */}
         <div className="absolute inset-0 pointer-events-none opacity-[0.03] bg-[linear-gradient(rgba(18,16,16,0)_50%,rgba(0,0,0,0.25)_50%),linear-gradient(90deg,rgba(255,0,0,0.06),rgba(0,255,0,0.02),rgba(0,0,255,0.06))] bg-[size:100%_2px,3px_100%]"></div>

         {/* Header area */}
         <div className="flex items-center justify-between px-12 py-6 relative z-10">
            <div className="flex items-center gap-6">
               <div>
                  <h2 className="text-[10px] font-bold tracking-[0.4em] text-cyan-500/60 uppercase">Primary Core</h2>
                  <h1 className="text-xl font-bold tracking-tighter text-white">SYSTEM_ACTIVE</h1>
               </div>
               <button 
                onClick={() => document.documentElement.requestFullscreen()}
                className="mt-2 p-2 rounded-lg border border-white/5 hover:bg-white/5 text-slate-500 hover:text-cyan-400 transition-all"
                title="Enter Fullscreen"
               >
                <Globe size={16} />
               </button>
            </div>
            <div className="flex items-center gap-4">
               <div className="flex flex-col items-end">
                  <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Operator Identity</span>
                  <span className="text-sm font-bold text-white tracking-wide">Hajeera</span>
               </div>
               <div className="w-10 h-10 rounded-full border border-white/10 p-0.5 shadow-xl shadow-purple-500/10 bg-black">
                  <img src={`https://ui-avatars.com/api/?name=Hajeera&background=020617&color=00f2ff`} className="w-full h-full rounded-full object-cover" />
               </div>
            </div>
         </div>

         {/* 3D Central Visualization */}
         <div className="flex-1 relative flex items-center justify-center overflow-hidden">
            <div className="relative w-[420px] h-[420px] z-50">
               <ParticleGlobe state={state} />
            </div>
            
            {/* HUD Rings */}
            <div className="absolute w-[450px] h-[450px] border border-indigo-500/5 rounded-full pointer-events-none"></div>
            <div className="absolute w-[600px] h-[600px] border border-white rounded-full pointer-events-none animate-spin-slow opacity-20"></div>

            {/* Visual Voice Waveform (Active when listening/speaking) */}
            <AnimatePresence>
               {(state === 'listening' || state === 'speaking') && (
                  <motion.div 
                     initial={{ opacity: 0, scale: 0.8 }}
                     animate={{ opacity: 1, scale: 1 }}
                     exit={{ opacity: 0, scale: 0.8 }}
                     className="absolute flex items-center gap-1 h-32 pointer-events-none"
                  >
                     {[...Array(12)].map((_, i) => (
                        <motion.div
                           key={i}
                           animate={{ 
                              height: [20, Math.random() * 80 + 20, 20],
                              backgroundColor: state === 'listening' ? '#22d3ee' : '#8b5cf6'
                           }}
                           transition={{ 
                              repeat: Infinity, 
                              duration: 0.5 + Math.random() * 0.5,
                              ease: "easeInOut"
                           }}
                           className="w-1 rounded-full shadow-[0_0_15px_rgba(34,211,238,0.5)]"
                        />
                     ))}
                  </motion.div>
               )}
            </AnimatePresence>
            
            {/* Status Radar Overlay */}
            <div className="absolute bottom-16 flex flex-col items-center gap-8">
               <AnimatePresence mode="wait">
                  <motion.div 
                     key={state}
                     initial={{ opacity: 0, y: 10 }}
                     animate={{ opacity: 1, y: 0 }}
                     exit={{ opacity: 0, y: -10 }}
                     className="px-8 py-3 rounded-full border border-cyan-500/20 bg-black/40 backdrop-blur-xl flex items-center gap-4 shadow-2xl shadow-cyan-500/10"
                  >
                     <div className={`w-2.5 h-2.5 rounded-full shadow-[0_0_15px_rgba(0,242,255,0.8)] ${
                        state === 'listening' ? 'bg-cyan-400 animate-pulse' : 
                        state === 'thinking' ? 'bg-amber-400 animate-spin' : 
                        state === 'speaking' ? 'bg-purple-400 scale-125' : 'bg-slate-600'
                     }`}></div>
                     <span className="text-[11px] font-bold uppercase tracking-[0.3em] text-cyan-100">
                        {state === 'idle' ? 'Jarvis Protocol Alpha' : `System is ${state}`}
                     </span>
                  </motion.div>
               </AnimatePresence>

               <div className="flex items-center gap-4">
                  {state === 'idle' ? (
                     <button onClick={handleMicClick} className="w-20 h-20 rounded-full bg-white/5 border border-white/10 flex items-center justify-center hover:bg-cyan-500/10 hover:border-cyan-500/30 transition-all group active:scale-95 shadow-2xl shadow-cyan-500/10">
                        <Mic className="w-8 h-8 text-slate-400 group-hover:text-cyan-400" />
                     </button>
                  ) : (
                     <button onClick={() => { if(state === 'speaking') handleStop(); else window.location.reload(); }} className="w-20 h-20 rounded-full bg-rose-500/10 border border-rose-500/30 flex items-center justify-center hover:bg-rose-500/20 transition-all active:scale-95 shadow-2xl shadow-rose-500/10">
                        <Square className="w-6 h-6 text-rose-500 fill-rose-500" />
                     </button>
                  )}
                  
                  {isContinuous && (
                      <div className="flex flex-col">
                          <span className="text-[10px] text-cyan-500 font-bold tracking-widest uppercase">Live Link</span>
                          <span className="text-[9px] text-cyan-500/40 font-bold uppercase">Always Listening</span>
                      </div>
                  )}
               </div>
            </div>
         </div>
      </main>

      {/* ─── SYSTEM TRANSCRIPTION PANEL ───────────────────── */}
      <aside className="w-[400px] shrink-0 border-l border-white/5 bg-black/20 backdrop-blur-3xl flex flex-col relative z-50">
         <div className="p-8 border-b border-white/5">
            <div className="flex items-center justify-between mb-2">
               <h3 className="text-xs font-bold tracking-[0.3em] text-cyan-400 uppercase">Communications</h3>
               <div className="flex gap-2">
                  <button onClick={() => {localStorage.removeItem("jarvis_messages"); setMessages([]);}} className="p-1.5 hover:bg-white/5 rounded-md text-slate-500 hover:text-rose-400 transition-colors">
                     <Trash2 size={14} />
                  </button>
               </div>
            </div>
            <h1 className="text-lg font-bold text-white tracking-tighter">System_Transcription</h1>
         </div>

         {/* Chat Feed */}
         <div className="flex-1 overflow-y-auto px-6 space-y-6 custom-scrollbar scroll-smooth">
            {messages.length === 0 && (
               <div className="h-full flex flex-col items-center justify-center opacity-20 gap-4 text-center px-8">
                  <Terminal size={40} className="text-cyan-500" />
                  <p className="text-xs uppercase tracking-widest leading-loose text-slate-500">Waiting for encrypted signal data...</p>
               </div>
            )}
            
            {messages.map((msg, i) => (
               <div key={i} className={`flex flex-col ${msg.role === 'user' ? 'items-end' : 'items-start'}`}>
                  <div className={`px-4 py-3 rounded-2xl text-[13px] leading-relaxed max-w-[90%] shadow-2xl ${
                     msg.role === 'user' 
                     ? 'bg-cyan-500/10 border border-cyan-500/20 text-cyan-100 rounded-tr-none'
                     : 'bg-white/5 border border-white/10 text-slate-300 rounded-tl-none font-sans'
                  }`}>
                     {msg.text}
                     {msg.imageUrl && (
                        <div className="mt-4 rounded-xl overflow-hidden border border-white/10 shadow-2xl">
                           <img src={msg.imageUrl} alt="Generated" className="w-full h-auto" />
                        </div>
                     )}
                  </div>
                  <span className="text-[9px] uppercase tracking-tighter text-slate-600 mt-2">
                     {msg.role === 'user' ? 'Operator' : 'Jarvis Core'} • {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </span>
               </div>
            ))}

            {interimText && (
               <div className="flex flex-col items-end opacity-50">
                  <div className="px-4 py-3 rounded-2xl bg-cyan-500/5 border border-dashed border-cyan-500/30 text-cyan-200 text-[13px] rounded-tr-none">
                     {interimText}
                  </div>
               </div>
            )}

            <div ref={chatEndRef} className="h-12" />
         </div>

         {/* Bottom Action Area */}
         <div className="p-6 bg-black/40 border-t border-white/5">
            <form onSubmit={(e) => { e.preventDefault(); if(textInput.trim()) processQuery(textInput); setTextInput(""); }} className="relative group">
               <input 
                  type="text" 
                  value={textInput}
                  onChange={(e) => setTextInput(e.target.value)}
                  placeholder="TYPE_COMMAND_HERE..."
                  className="w-full bg-white/5 border border-white/10 rounded-xl px-12 py-4 text-xs font-bold tracking-widest text-cyan-400 placeholder:text-slate-700 focus:outline-none focus:border-cyan-500/50 transition-all uppercase"
               />
               <Terminal className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-700 group-focus-within:text-cyan-500 transition-colors" />
            </form>
         </div>
      </aside>
    </div>
  );
}

