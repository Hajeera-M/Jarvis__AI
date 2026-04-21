"use client";

import React, { useState, useRef, useCallback, useEffect } from "react";
import { MicButton } from "@/components/mic-button";
import { VoiceWave } from "@/components/voice-wave";
import { sendVoiceCommand } from "@/lib/api";

type AppState = "idle" | "listening" | "processing" | "speaking";

export function VoiceInterface() {
    const [state, setState] = useState<AppState>("idle");
    const [transcript, setTranscript] = useState("");
    const [response, setResponse] = useState("");
    const [error, setError] = useState("");

    const mediaRecorderRef = useRef<MediaRecorder | null>(null);
    const audioChunksRef = useRef<Blob[]>([]);
    const audioRef = useRef<HTMLAudioElement | null>(null);

    // Status text based on state
    const statusText: Record<AppState, string> = {
        idle: "Tap to speak",
        listening: "Listening...",
        processing: "Thinking...",
        speaking: "Speaking...",
    };

    // Start recording
    const startListening = useCallback(async () => {
        try {
            setError("");
            setTranscript("");
            setResponse("");

            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            const mediaRecorder = new MediaRecorder(stream, {
                mimeType: MediaRecorder.isTypeSupported("audio/webm;codecs=opus")
                    ? "audio/webm;codecs=opus"
                    : "audio/webm",
            });

            audioChunksRef.current = [];
            mediaRecorderRef.current = mediaRecorder;

            mediaRecorder.ondataavailable = (event: BlobEvent) => {
                if (event.data.size > 0) {
                    audioChunksRef.current.push(event.data);
                }
            };

            mediaRecorder.onstop = async () => {
                // Stop all tracks
                stream.getTracks().forEach((t) => t.stop());

                const audioBlob = new Blob(audioChunksRef.current, {
                    type: "audio/webm",
                });

                if (audioBlob.size === 0) {
                    setState("idle");
                    return;
                }

                // Send to backend
                setState("processing");
                try {
                    const result = await sendVoiceCommand(audioBlob);

                    if (result.transcript) setTranscript(result.transcript);
                    if (result.response) setResponse(result.response);

                    // Play audio response
                    if (result.audioBlob) {
                        setState("speaking");
                        const audioUrl = URL.createObjectURL(result.audioBlob);
                        const audio = new Audio(audioUrl);
                        audioRef.current = audio;

                        audio.onended = () => {
                            setState("idle");
                            URL.revokeObjectURL(audioUrl);
                        };
                        audio.onerror = () => {
                            setState("idle");
                            URL.revokeObjectURL(audioUrl);
                        };
                        audio.play();
                    } else {
                        setState("idle");
                    }
                } catch (err: unknown) {
                    setError(
                        err instanceof Error ? err.message : "Something went wrong"
                    );
                    setState("idle");
                }
            };

            mediaRecorder.start(250); // collect data every 250ms
            setState("listening");
        } catch (_err: unknown) {
            setError("Microphone access denied. Please allow microphone access.");
            setState("idle");
        }
    }, []);

    // Stop recording
    const stopListening = useCallback(() => {
        if (mediaRecorderRef.current?.state === "recording") {
            mediaRecorderRef.current.stop();
        }
    }, []);

    // Handle mic button click
    const handleMicClick = useCallback(() => {
        if (state === "listening") {
            stopListening();
        } else if (state === "idle") {
            startListening();
        } else if (state === "speaking") {
            // Stop playback
            if (audioRef.current) {
                audioRef.current.pause();
                audioRef.current = null;
            }
            setState("idle");
        }
    }, [state, startListening, stopListening]);

    // Keyboard shortcut: Space to toggle
    useEffect(() => {
        const handleKeyDown = (e: KeyboardEvent) => {
            if (e.code === "Space" && e.target === document.body) {
                e.preventDefault();
                handleMicClick();
            }
        };
        window.addEventListener("keydown", handleKeyDown);
        return () => window.removeEventListener("keydown", handleKeyDown);
    }, [handleMicClick]);

    return (
        <div className="relative flex flex-col items-center gap-10 z-10">
            {/* Voice Wave (shown when listening or speaking) */}
            <div className="h-16 flex items-center">
                {(state === "listening" || state === "speaking") && (
                    <VoiceWave isActive={true} />
                )}
            </div>

            {/* Mic Button */}
            <MicButton state={state} onClick={handleMicClick} />

            {/* Status */}
            <div className="text-center space-y-3 min-h-[80px]">
                <p className="status-text animate-fade-in">{statusText[state]}</p>

                {/* Transcript */}
                {transcript && (
                    <p className="text-sm text-jarvis-cyan/50 max-w-md animate-fade-in font-light">
                        &ldquo;{transcript}&rdquo;
                    </p>
                )}

                {/* Response preview */}
                {response && state !== "processing" && (
                    <p className="text-sm text-jarvis-cyan/70 max-w-lg animate-fade-in font-light leading-relaxed">
                        {response}
                    </p>
                )}

                {/* Error */}
                {error && (
                    <p className="text-sm text-red-400/80 max-w-md animate-fade-in">
                        {error}
                    </p>
                )}
            </div>
        </div>
    );
}

