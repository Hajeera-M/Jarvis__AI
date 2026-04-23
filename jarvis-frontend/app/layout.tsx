import type { Metadata } from "next";
import type { ReactNode } from "react";
import "./globals.css";

export const metadata: Metadata = {
    title: "JARVIS | Core Operator: Hajeera",
    description:
        "JARVIS — Superior Agentic AI System. Authorized Operator: Hajeera.",
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

