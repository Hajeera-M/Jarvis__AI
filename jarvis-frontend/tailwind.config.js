/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./app/**/*.{js,ts,jsx,tsx,mdx}",
        "./components/**/*.{js,ts,jsx,tsx,mdx}",
        "./lib/**/*.{js,ts,jsx,tsx,mdx}",
    ],
    theme: {
        extend: {
            colors: {
                jarvis: {
                    cyan: "#00f0ff",
                    blue: "#0066ff",
                    dark: "#050a14",
                    panel: "#0a1628",
                    glow: "#00f0ff33",
                },
            },
            fontFamily: {
                sans: ["Inter", "system-ui", "sans-serif"],
                mono: ["JetBrains Mono", "monospace"],
            },
            animation: {
                "pulse-glow": "pulse-glow 2s ease-in-out infinite",
                "wave-bar": "wave-bar 1.2s ease-in-out infinite",
                "spin-slow": "spin 3s linear infinite",
                "fade-in": "fade-in 0.5s ease-out",
                "scale-in": "scale-in 0.3s ease-out",
                "ripple": "ripple 1.5s ease-out infinite",
            },
            keyframes: {
                "pulse-glow": {
                    "0%, 100%": {
                        boxShadow: "0 0 20px #00f0ff33, 0 0 60px #00f0ff11",
                    },
                    "50%": {
                        boxShadow: "0 0 40px #00f0ff66, 0 0 100px #00f0ff22",
                    },
                },
                "wave-bar": {
                    "0%, 100%": { height: "12px" },
                    "50%": { height: "40px" },
                },
                "fade-in": {
                    "0%": { opacity: "0", transform: "translateY(10px)" },
                    "100%": { opacity: "1", transform: "translateY(0)" },
                },
                "scale-in": {
                    "0%": { opacity: "0", transform: "scale(0.9)" },
                    "100%": { opacity: "1", transform: "scale(1)" },
                },
                "ripple": {
                    "0%": { transform: "scale(1)", opacity: "0.4" },
                    "100%": { transform: "scale(2.5)", opacity: "0" },
                },
            },
        },
    },
    plugins: [],
};
