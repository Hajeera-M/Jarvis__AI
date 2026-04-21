"use client";

import { useState, useRef, useEffect } from "react";
import { useRouter } from "next/navigation";
import { AssistantHeader } from "./components/AssistantHeader";
import { ChatMessage } from "./components/ChatMessage";
import { VoiceOrb } from "./components/VoiceOrb";
import { MetricsSidebar } from "./components/MetricsSidebar";
import { ChatInput } from "./components/ChatInput";
import { SettingsModal } from "./components/SettingsModal";
import { HistoryModal } from "./components/HistoryModal";
import { initVoices, getPreferredVoice } from "../lib/voiceHelper";

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
  const [imageUrl, setImageUrl] = useState(""); // Kept for state compatibility
  const chatEndRef = useRef<HTMLDivElement>(null);

  // Modal States
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [isHistoryOpen, setIsHistoryOpen] = useState(false);

  // Auto-scroll chat
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  useEffect(() => {
    const savedMessages = localStorage.getItem("jarvis_messages");
    if (savedMessages) {
      try {
        const parsed = JSON.parse(savedMessages);
        const hydrated = parsed.map((m: any) => ({
          ...m,
          timestamp: new Date(m.timestamp)
        }));
        setMessages(hydrated);
      } catch (e) {
        console.error("Failed to load history:", e);
      }
    }
  }, []);

  useEffect(() => {
    if (messages.length > 0) {
      localStorage.setItem("jarvis_messages", JSON.stringify(messages));
    }
  }, [messages]);

  // ─── Auth Guard ────────────────────────────────────────
  const router = useRouter();
  const [authChecked, setAuthChecked] = useState(false);
  useEffect(() => {
    const user = localStorage.getItem("jarvis_user");
    if (!user) {
      router.replace("/signin");
    } else {
      setAuthChecked(true);
    }
    // Initialize voices
    initVoices();
  }, [router]);

  // ─── API Call ───────────────────────────────────────────
  async function sendToJarvis(text: string) {
    try {
      const res = await fetch("http://127.0.0.1:8000/jarvis", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ input: text }),
      });
      return await res.json();
    } catch (e) {
      console.error("JARVIS API Error:", e);
      return { response: "Connection lost. Please try again.", status: "failed", source: "error" };
    }
  }

  // ─── Process a query (shared by voice + text) ──────────
  async function processQuery(text: string) {
    if (!text.trim()) return;
    // Add user message
    setMessages((prev) => [...prev, { role: "user", text, timestamp: new Date() }]);
    setState("thinking");
    setImageUrl("");

    const data = await sendToJarvis(text);
    const reply = data.response || data.message || "No response received.";
    const spokenReply = data.spoken_response || reply;
    const source = data.source || "ai";
    const imgUrl = data.image_url || "";
    const status = data.status || "success";

    // Add JARVIS message
    setMessages((prev) => [
      ...prev,
      { role: "jarvis", text: reply, source, imageUrl: imgUrl, status, timestamp: new Date() },
    ]);
    setImageUrl(imgUrl);

    // ─── TTS Stability Hardening ───────────────────────────
    if (typeof window !== "undefined" && window.speechSynthesis) {
      window.speechSynthesis.cancel(); // Interrupt any ongoing speech immediately
      
      const speechText = data.spoken_response || reply; // Ensure full text source
      const utterance = new SpeechSynthesisUtterance(speechText);
      
      utterance.rate = 0.95; // Slightly slower for better professional clarity
      utterance.pitch = 1.0;  // Natural pitch anchor
      
      const picked = getPreferredVoice(data.language || "en");
      if (picked) utterance.voice = picked;
      
      utterance.onend = () => setState("idle");
      utterance.onerror = () => setState("idle");

      setState("speaking");
      // 200ms buffer delay allows the browser audio context to stabilize
      setTimeout(() => {
        window.speechSynthesis.speak(utterance);
      }, 200);
    } else {
      setTimeout(() => setState("idle"), 2000);
    }
  }

  // ─── Voice Mic Handler ─────────────────────────────────
  const handleMicClick = () => {
    // Instant interrupt
    if (typeof window !== "undefined" && window.speechSynthesis) {
      window.speechSynthesis.cancel();
    }
    if (state === "speaking") {
      setState("idle");
      return;
    }
    if (state !== "idle") return;

    const SpeechRecognition =
      (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert("Speech recognition is not supported. Use Chrome or Edge.");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    setState("listening");

    recognition.onresult = async (event: any) => {
      const transcript = event.results[0][0].transcript;
      processQuery(transcript);
    };

    recognition.onerror = () => {
      setState("idle");
    };

    recognition.onend = () => {
      setState((prev) => (prev === "listening" ? "idle" : prev));
    };

    recognition.onspeechend = () => recognition.stop();
    recognition.start();
  };

  // ─── Text Submit ───────────────────────────────────────
  const handleTextSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!textInput.trim() || state !== "idle") return;
    processQuery(textInput.trim());
    setTextInput("");
  };

  // ─── Stop Speaking ─────────────────────────────────────
  const handleStop = () => {
    if (typeof window !== "undefined" && window.speechSynthesis) {
      window.speechSynthesis.cancel();
    }
    setState("idle");
  };

  // ─── Clear Chat ────────────────────────────────────────
  const handleClear = () => {
    setMessages([]);
    localStorage.removeItem("jarvis_messages");
    setImageUrl("");
    setState("idle");
  };

  const sendPredefinedText = (text: string) => {
    if (state !== "idle") return;
    processQuery(text);
  };

  // Metrics Logic
  const jarvisMessages = messages.filter((m) => m.role === "jarvis").length;
  const jarvisImages = messages.filter((m) => m.imageUrl && m.imageUrl !== "").length;

  // Prevent flash of dashboard before redirect
  if (!authChecked) return null;

  return (
    <div className="bg-jarvis min-h-screen flex justify-center p-4 lg:p-8">
      
      {/* Front-End Only Modals */}
      <SettingsModal isOpen={isSettingsOpen} onClose={() => setIsSettingsOpen(false)} onClearMemory={handleClear} />
      <HistoryModal isOpen={isHistoryOpen} onClose={() => setIsHistoryOpen(false)} messages={messages} />

      {/* Structural constraint container */}
      <div className="w-full max-w-7xl h-[calc(100vh-4rem)] flex gap-6">
        
        {/* Left/Center Panel: Main Interaction Area */}
        <div className="flex-1 flex flex-col h-full relative border border-indigo-50/50 rounded-3xl overflow-hidden shadow-[0_0_50px_rgba(165,180,252,0.1)]">
          <div className="absolute inset-0 bg-white/40 backdrop-blur-3xl z-0 pointer-events-none"></div>
          
          <AssistantHeader state={state} />

          {/* Main Chat Feed */}
          <main className="flex-1 flex flex-col overflow-hidden relative z-10 w-full max-w-3xl mx-auto h-full">
            
            <div className="flex-1 overflow-y-auto px-4 sm:px-8 py-4 space-y-2 relative custom-scrollbar">
              
              {messages.length === 0 && (
                <div className="flex flex-col items-center justify-center h-full opacity-60 gap-4 pt-4 animate-fade-in text-center">
                  <div className="text-5xl drop-shadow-sm mb-2" style={{color: "var(--accent-lavender)"}}>✧</div>
                  <h2 className="text-xl sm:text-2xl font-bold tracking-tight text-slate-700">How can I help you today?</h2>
                  <p className="text-xs font-semibold uppercase tracking-widest text-indigo-300">
                    Voice • Image • Search • Stock
                  </p>
                </div>
              )}

              {/* Render Messages */}
              {messages.map((msg, i) => (
                <ChatMessage key={i} msg={msg} />
              ))}

              {/* Thinking Indicator */}
              {state === "thinking" && (
                <div className="flex justify-start my-3">
                   <div className="glass-card-sm px-5 py-4 rounded-3xl rounded-bl-sm flex items-center gap-3 bg-white/70 shadow-sm animate-fade-in border border-indigo-100">
                      <div className="flex gap-1.5">
                        <span className="text-lg animate-spin">⚙️</span>
                      </div>
                      <span className="text-[13px] font-bold text-indigo-500 uppercase tracking-widest">
                        JARVIS is thinking...
                      </span>
                   </div>
                </div>
              )}

              <div ref={chatEndRef} className="h-6" />
            </div>
            
            {/* Proper Bottom Action Dock */}
            <div className="flex-none w-full bg-white/30 backdrop-blur-2xl border-t border-indigo-50/50 pt-3 pb-2 px-4 shadow-[0_-10px_30px_rgba(165,180,252,0.05)]">
               
               {/* Fixed Dock Row: Left Action | Center Mic | Right Action */}
               <div className="flex justify-between items-center max-w-lg mx-auto mb-1">
                 
                 {/* Left: Clear Command */}
                 <div className="flex-1 flex justify-start">
                    {messages.length > 0 && state === "idle" ? (
                      <button onClick={handleClear} className="bg-white/80 backdrop-blur-md px-4 py-2 rounded-2xl text-[10px] font-bold text-slate-500 uppercase tracking-widest hover:bg-white shadow-sm border border-slate-200 transition-all hover:scale-105 active:scale-95">
                        ✕ Clear Output
                      </button>
                    ) : (
                      <div className="w-[100px]"></div> /* Placeholder to balance flex */
                    )}
                 </div>
                 
                 {/* Center: Explicit Voice Orb placement */}
                 <div className="flex-none flex items-center justify-center h-[110px] w-[110px]">
                   <VoiceOrb state={state} onClick={handleMicClick} />
                 </div>
                 
                 {/* Right: Interrupt / Stop Command */}
                 <div className="flex-1 flex justify-end">
                    {state === "speaking" ? (
                      <button onClick={handleStop} className="bg-rose-50/90 backdrop-blur-md px-4 py-2 rounded-2xl text-[10px] font-bold text-rose-500 uppercase tracking-widest hover:bg-rose-100/90 shadow-sm border border-rose-200 transition-all hover:scale-105 active:scale-95 animate-pulse">
                        ⏹ Interrupt
                      </button>
                    ) : (
                      <div className="w-[100px]"></div> /* Placeholder to balance flex */
                    )}
                 </div>

               </div>
               
               {/* Chat Input Integrated into Dock */}
               <div className="max-w-xl mx-auto align-bottom -mt-2">
                 <ChatInput
                    textInput={textInput}
                    setTextInput={setTextInput}
                    handleTextSubmit={handleTextSubmit}
                    isDisabled={state !== "idle"}
                 />
               </div>

            </div>
          </main>
        </div>

        {/* Right Sidebar: Context & Actions */}
        <div className="w-[320px] lg:w-[350px] flex-shrink-0 relative hidden md:block z-50">
          <MetricsSidebar 
             msgCount={jarvisMessages} 
             imgCount={jarvisImages} 
             sendPredefinedText={sendPredefinedText}
             onOpenSettings={() => setIsSettingsOpen(true)}
             onOpenHistory={() => setIsHistoryOpen(true)}
          />
        </div>

      </div>
    </div>
  );
}
