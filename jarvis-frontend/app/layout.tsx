import type { Metadata } from "next";
import type { ReactNode } from "react";
import "./globals.css";

export const metadata: Metadata = {
    title: "JARVIS-X | Voice AI Assistant",
    description:
        "JARVIS-X — A voice-based agentic AI assistant powered by Groq reasoning and HuggingFace generation.",
};

export default function RootLayout({ children }: { children: ReactNode }) {
    return (
        <html lang="en">
            <body className="bg-jarvis min-h-screen flex items-center justify-center">
                {children}
            </body>
        </html>
    );
}
