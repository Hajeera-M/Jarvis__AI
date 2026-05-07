/**
 * JARVIS-X — API Client
 * Handles communication with the FastAPI backend.
 */

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface VoiceCommandResult {
    transcript: string;
    response: string;
    audioBlob: Blob | null;
    imageUrl?: string;
}

/**
 * Send a voice command (audio blob) to the backend.
 * Returns transcript, response text, and audio blob for playback.
 */
export async function sendVoiceCommand(
    audioBlob: Blob
): Promise<VoiceCommandResult> {
    const formData = new FormData();
    formData.append("audio", audioBlob, "recording.webm");

    // Try the full endpoint first (returns JSON with audio as base64)
    const res = await fetch(`${API_BASE}/voice-command-full`, {
        method: "POST",
        body: formData,
    });

    if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(
            errorData.detail || `Server error: ${res.status} ${res.statusText}`
        );
    }

    const data = await res.json();

    // Decode base64 audio to blob
    let responseAudioBlob: Blob | null = null;
    if (data.audio_base64) {
        const binaryString = atob(data.audio_base64);
        const bytes = new Uint8Array(binaryString.length);
        for (let i = 0; i < binaryString.length; i++) {
            bytes[i] = binaryString.charCodeAt(i);
        }
        responseAudioBlob = new Blob([bytes], { type: "audio/mpeg" });
    }

    return {
        transcript: data.transcript || "",
        response: data.response || "",
        audioBlob: responseAudioBlob,
        imageUrl: data.image_url,
    };
}

/**
 * Send a text command (for testing without microphone).
 */
export async function sendTextCommand(
    text: string
): Promise<{ transcript: string; response: string }> {
    const res = await fetch(`${API_BASE}/text-command`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
    });

    if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(
            errorData.detail || `Server error: ${res.status} ${res.statusText}`
        );
    }

    return res.json();
}
