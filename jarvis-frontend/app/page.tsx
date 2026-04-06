"use client";

import { useState, useCallback } from "react";
import Particles from "react-tsparticles";
import { loadSlim } from "tsparticles-slim";

export default function Home() {
  // state: "idle" | "listening" | "thinking" | "speaking" | "completed"
  const [state, setState] = useState("idle");
  const [response, setResponse] = useState("");

  const particlesInit = useCallback(async (engine: any) => {
    await loadSlim(engine);
  }, []);

  // Simple Synthesizer Beep for Mic Feedback
  const playBeep = () => {
    try {
      const audioCtx = new (window.AudioContext || (window as any).webkitAudioContext)();
      const oscillator = audioCtx.createOscillator();
      const gainNode = audioCtx.createGain();

      oscillator.type = "sine";
      oscillator.frequency.setValueAtTime(800, audioCtx.currentTime); // high pitch beep
      gainNode.gain.setValueAtTime(0.1, audioCtx.currentTime); // volume
      gainNode.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.1);

      oscillator.connect(gainNode);
      gainNode.connect(audioCtx.destination);
      oscillator.start();
      oscillator.stop(audioCtx.currentTime + 0.1);
    } catch {
      // Ignore if audio isn't supported or allowed yet
    }
  };

  async function sendToJarvis(text: string) {
    try {
      const res = await fetch("http://127.0.0.1:8000/jarvis", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ input: text }),
      });
      const data = await res.json();
      console.log("JARVIS API Reply:", data);
      
      // Defensive check: handle different response keys or raw strings
      return data.response || data.message || (typeof data === 'string' ? data : JSON.stringify(data));

    } catch (e) {
      console.error(e);
      throw e;
    }
  }

  // Real Sequence: Click -> Recording -> Fetching -> TTS -> Idle
  const handleMicClick = () => {
    if (state !== "idle") return; // Prevent clicking while active
    
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert("Speech recognition is not supported in this browser. Please use Chrome or Edge.");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";

    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    // INSTANT CONFIDENCE: Change UI immediately
    setState("listening");
    setResponse("Listening...");
    playBeep();

    recognition.onresult = async (event: any) => {
      const text = event.results[0][0].transcript;
      setState("thinking");
      setResponse(`"${text}" ... processing.`);
      
      // Safety Fallback: Let user know the backend isn't dead
      const thinkingTimeout = setTimeout(() => {
        setResponse("Still processing... JARVIS is thinking.");
      }, 5000);

      try {
        const backendResponse = await sendToJarvis(text);

        clearTimeout(thinkingTimeout); // Clear fallback
        setResponse(backendResponse);
        setState("speaking");

        speechSynthesis.cancel(); // Prevent overlapping audio bug
        const speech = new SpeechSynthesisUtterance(backendResponse);
        
        speech.onend = () => {
          setState("completed"); // Trigger the energy pulse
          setTimeout(() => {
             setState("idle");
          }, 800);
        };
        
        speechSynthesis.speak(speech);

      } catch (e) {
        clearTimeout(thinkingTimeout); // Clear fallback
        setResponse("Connection lost. Please try again.");
        setTimeout(() => setState("idle"), 3000);
      }
    };

    recognition.onerror = (event: any) => {
      console.error("Speech error", event);
      setResponse("Microphone resting.");
      setTimeout(() => setState("idle"), 1500);
    };

    recognition.onend = () => {
      // If recognition ends abruptly without entering thinking phase
      setState((prevState) => {
        if (prevState === "listening") {
          setResponse("No speech detected.");
          setTimeout(() => setState("idle"), 1500);
          return "idle"; 
        }
        return prevState;
      });
    };

    recognition.onspeechend = () => {
        recognition.stop();
    };

    recognition.start();
  };


  return (
    <div className="h-screen bg-black flex flex-col items-center justify-center text-white relative overflow-hidden">
      
      {/* Background Particles - Subtle and elegant */}
      <Particles
        id="tsparticles"
        init={particlesInit}
        options={{
          background: { color: { value: "transparent" } },
          fpsLimit: 60,
          particles: {
            color: { value: "#00f0ff" },
            links: {
              color: "#00f0ff",
              distance: 150,
              enable: true,
              opacity: 0.15,
              width: 1,
            },
            move: {
              enable: true,
              speed: 0.3,
              direction: "none",
              random: true,
              outModes: { default: "out" },
            },
            number: { density: { enable: true, area: 800 }, value: 40 },
            opacity: { value: 0.2 },
            shape: { type: "circle" },
            size: { value: { min: 1, max: 2 } },
          },
          detectRetina: true,
        }}
        className="absolute inset-0 z-0 pointer-events-none"
      />

      {/* Title */}
      <h1 className="text-cyan-400 text-xl font-light mb-12 tracking-[0.3em] z-10 opacity-80">
        JARVIS-X CORE
      </h1>

      {/* Outer Rotating Ring Assembly */}
      <div className="relative flex items-center justify-center z-10 my-4">

        {/* Ring 1 - Outer (Balanced Speed) */}
        <div className={`absolute border rounded-full transition-all duration-700 opacity-30 ${
          state === "thinking" 
            ? "w-80 h-80 animate-[spin_4s_linear_infinite] border-purple-500 scale-105" 
            : "w-72 h-72 animate-[spin_12s_linear_infinite] border-cyan-400"
        }`}></div>

        {/* Ring 2 - Inner (Balanced Speed) */}
        <div className={`absolute border rounded-full transition-all duration-700 opacity-30 ${
          state === "thinking" 
            ? "w-64 h-64 animate-[spin-reverse_3s_linear_infinite] border-cyan-400 scale-95" 
            : "w-56 h-56 animate-[spin-reverse_10s_linear_infinite] border-purple-500"
        }`}></div>

        {/* Ring 3 Glow Foundation */}
        <div className="absolute w-40 h-40 bg-cyan-500/10 blur-3xl rounded-full"></div>

        {/* Center UI Core */}
        <button
          onClick={handleMicClick}
          className={`relative z-10 flex items-center justify-center text-3xl shadow-[0_0_30px_rgba(0,240,255,0.4)] transition-all duration-500 w-28 h-28 rounded-full border border-cyan-400/30 ${
            state === "listening" 
              ? "animate-pulse bg-cyan-500/80 scale-105 shadow-[0_0_50px_rgba(0,240,255,0.6)]" 
              : state === "thinking" 
              ? "bg-purple-600/60 scale-95 shadow-[0_0_20px_rgba(168,85,247,0.5)]" 
              : state === "speaking"
              ? "bg-gradient-to-r from-cyan-500/80 to-emerald-400/80 animate-pulse shadow-[0_0_60px_rgba(0,240,255,0.6)] scale-110"
              : state === "completed"
              ? "animate-energy-pulse bg-cyan-400 shadow-[0_0_80px_rgba(0,240,255,0.8)]"
              : "bg-gradient-to-r from-cyan-500/20 to-purple-500/20 hover:scale-105 hover:bg-cyan-500/30"
          }`}
        >
          <span className="drop-shadow-[0_0_10px_rgba(255,255,255,0.8)]">
            {state === "idle" ? "🎤" : state === "listening" ? "🎧" : state === "thinking" ? "⚙️" : state === "completed" ? "✨" : "🔊"}
          </span>
        </button>
      </div>

      {/* Floating Response Text Box (Pro Readability) */}
      <div className="mt-10 max-w-sm w-full min-h-[4rem] z-10 flex flex-col items-center justify-start px-4">
        {response ? (
          <p className="text-cyan-100 text-center tracking-wide font-light text-lg 
                        drop-shadow-[0_0_8px_rgba(0,255,255,0.6)] 
                        bg-black/40 backdrop-blur-md rounded-xl p-4 
                        border border-cyan-500/20 w-full animate-fade-in shadow-xl">
            {response}
          </p>
        ) : (
          <p className="text-cyan-500/50 text-center tracking-widest text-sm font-light mt-4">
            AWAITING COMMAND
          </p>
        )}
      </div>

    </div>
  );
}
