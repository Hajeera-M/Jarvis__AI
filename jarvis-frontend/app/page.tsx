import { VoiceInterface } from "./voice-interface";

export default function Home() {
    return (
        <main className="relative w-full h-screen flex flex-col items-center justify-center overflow-hidden">
            {/* Background grid effect */}
            <div
                className="absolute inset-0 opacity-[0.03]"
                style={{
                    backgroundImage: "linear-gradient(rgba(0,240,255,0.3) 1px, transparent 1px), linear-gradient(90deg, rgba(0,240,255,0.3) 1px, transparent 1px)",
                    backgroundSize: "60px 60px",
                }}
            />

            {/* Title */}
            <div className="absolute top-8 left-1/2 -translate-x-1/2 text-center animate-fade-in z-10">
                <h1 className="text-xl font-semibold tracking-[0.3em] text-jarvis-cyan/80 uppercase">
                    JARVIS-X
                </h1>
                <p className="text-[0.65rem] tracking-[0.2em] text-jarvis-cyan/30 mt-1 uppercase">
                    Voice AI Assistant
                </p>
            </div>

            {/* Core Voice Interface */}
            <VoiceInterface />

            {/* Bottom branding */}
            <div className="absolute bottom-6 text-center animate-fade-in z-10">
                <p className="text-[0.6rem] tracking-[0.15em] text-jarvis-cyan/20 uppercase">
                    Powered by Groq • HuggingFace • Edge TTS
                </p>
            </div>
        </main>
    );
}
