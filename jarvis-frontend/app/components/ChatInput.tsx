import React from "react";

export function ChatInput({
  textInput,
  setTextInput,
  handleTextSubmit,
  isDisabled
}: {
  textInput: string;
  setTextInput: (v: string) => void;
  handleTextSubmit: (e: React.FormEvent) => void;
  isDisabled: boolean;
}) {
  return (
    <form onSubmit={handleTextSubmit} className="w-full relative mt-auto px-4 py-4" id="text-input-form">
      <div className="glass-card-sm flex items-center pr-2 pl-4 py-2 border-2 border-transparent focus-within:border-indigo-200/50 transition-colors shadow-lg">
        <span className="text-xl mr-3 opacity-40">✨</span>
        <input
          type="text"
          value={textInput}
          onChange={(e) => setTextInput(e.target.value)}
          placeholder="Type a command for JARVIS..."
          disabled={isDisabled}
          className="flex-1 bg-transparent outline-none text-sm font-medium placeholder-slate-400 py-2 h-10 disabled:opacity-60"
          style={{ color: "var(--text-primary)" }}
          id="text-input"
        />
        <button
          type="submit"
          disabled={isDisabled || !textInput.trim()}
          className="ml-2 px-6 py-2.5 rounded-full text-xs font-bold text-white transition-all hover:scale-105 hover:shadow-md disabled:opacity-40 disabled:hover:scale-100 disabled:shadow-none flex items-center gap-2 uppercase tracking-wide"
          style={{ background: "var(--gradient-orb)" }}
          id="send-btn"
        >
          Send <span className="text-lg leading-none">🚀</span>
        </button>
      </div>
    </form>
  );
}
