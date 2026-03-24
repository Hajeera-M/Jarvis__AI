# JARVIS-X AI Assistant 🎙️🛸

A modular, multi-lingual, and local-first AI voice assistant integrated with Groq LLM and customized for responsive human-like interactions.

## 🏗️ Project Structure

- **`/jarvis`**: The primary Python-based backend handling voice processing (STT/TTS), agent orchestration, and Groq-based reasoning.
- **`/jarvis-frontend`**: A modern Next.js dashboard/UI for visual feedback and character interaction.
- **`/jarvis-backend`**: Supporting tools and legacy backend components.

## 🚀 Key Features

- **Natural Neural Voice**: Integrated with Microsoft Edge TTS for high-quality, human-like speech.
- **Multi-Lingual Support**: Automatically matches the user's language (English, Hindi, Hinglish).
- **Local Automation**: Commands for searching YouTube, playing music, opening local apps, and WhatsApp messaging.
- **Stable Interruption**: Real-time voice interruption and request-ID tracking to prevent race conditions.

## 🛠️ Tech Stack

- **Reasoning**: Groq (LLaMA-3/Mixtral)
- **STT**: Google Speech Recognition
- **TTS**: Microsoft Edge Neural TTS / pyttsx3
- **Frontend**: Next.js, Tailwind CSS, Framer Motion
- **Database**: SQLite (Local Memory)

## 📋 Prerequisites

- Python 3.10+
- Node.js 18+
- Groq API Key

---
*Created and maintained by Hajeera-M.*
