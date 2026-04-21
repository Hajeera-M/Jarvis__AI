"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";

export default function SignIn() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSignIn = (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setTimeout(() => {
      localStorage.setItem("jarvis_user", "true");
      router.push("/");
    }, 800);
  };

  const handleGuestLogin = () => {
    setIsSubmitting(true);
    setTimeout(() => {
      localStorage.setItem("jarvis_user", "true");
      router.push("/");
    }, 500);
  };

  return (
    <div className="bg-jarvis min-h-screen flex items-center justify-center p-4 relative overflow-hidden">
      
      {/* Decorative Floating Orbs */}
      <div className="absolute top-1/4 left-1/4 w-32 h-32 bg-indigo-300 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-pulse"></div>
      <div className="absolute bottom-1/4 right-1/4 w-32 h-32 bg-mint-300 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-pulse" style={{ animationDelay: '1s', backgroundColor: 'var(--accent-mint)' }}></div>

      <div className="w-full max-w-md relative z-10 animate-fade-in">
        <div className="glass-card p-8 sm:p-10 shadow-[0_20px_50px_rgba(165,180,252,0.15)] flex flex-col items-center">
          
          {/* JARVIS Logo / Header */}
          <div className="flex flex-col items-center justify-center mb-10 w-full">
            <div 
              className="w-16 h-16 rounded-2xl flex items-center justify-center text-white font-black text-3xl shadow-lg mb-5 transform transition-transform hover:scale-105"
              style={{ background: "var(--gradient-orb)" }}
            >
              J.
            </div>
            <h1 className="text-3xl font-black tracking-tight text-slate-800">
              JARVIS
            </h1>
            <p className="text-sm font-semibold uppercase tracking-widest text-indigo-400 mt-1">
              Sign in to continue
            </p>

            {/* Demo Hint Badge */}
            <div className="mt-5 w-full bg-indigo-50/80 border border-indigo-100 rounded-2xl px-4 py-3 text-center">
              <p className="text-[11px] font-bold text-indigo-400 uppercase tracking-widest mb-1">🔑 Demo Credentials</p>
              <p className="text-xs text-slate-500 font-medium">Email: <span className="font-bold text-slate-700">demo@jarvis.ai</span></p>
              <p className="text-xs text-slate-500 font-medium mt-0.5">Password: <span className="font-bold text-slate-700">any password works</span></p>
            </div>
          </div>

          {/* Form */}
          <form onSubmit={handleSignIn} className="w-full space-y-5">
            
            <div className="space-y-1">
              <label className="block text-xs font-bold text-slate-500 uppercase tracking-wide px-1">Email</label>
              <input 
                type="email" 
                required
                disabled={isSubmitting}
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="hello@example.com"
                className="w-full bg-white/60 border border-indigo-100/60 rounded-2xl px-4 py-3.5 text-sm font-medium text-slate-700 outline-none placeholder:text-slate-400 focus:border-indigo-300 focus:ring-4 focus:ring-indigo-100/50 transition-all disabled:opacity-50"
              />
            </div>

            <div className="space-y-1 relative">
              <label className="block text-xs font-bold text-slate-500 uppercase tracking-wide px-1">Password</label>
              <div className="relative">
                <input 
                  type={showPassword ? "text" : "password"} 
                  required
                  disabled={isSubmitting}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="w-full bg-white/60 border border-indigo-100/60 rounded-2xl pl-4 pr-12 py-3.5 text-sm font-medium text-slate-700 outline-none placeholder:text-slate-400 focus:border-indigo-300 focus:ring-4 focus:ring-indigo-100/50 transition-all disabled:opacity-50"
                />
                <button 
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 p-2 text-slate-400 hover:text-indigo-500 transition-colors focus:outline-none"
                >
                  {showPassword ? "👁️" : "👁‍🗨"}
                </button>
              </div>
            </div>

            <div className="flex items-center justify-between pt-1">
               <label className="flex items-center gap-2 cursor-pointer group">
                  <input type="checkbox" className="w-4 h-4 rounded border-indigo-200 text-indigo-500 focus:ring-indigo-500/30 transition-colors cursor-pointer" />
                  <span className="text-xs font-semibold text-slate-500 group-hover:text-slate-700 transition-colors">Remember me</span>
               </label>
               <a href="#" className="text-xs font-bold text-indigo-500 hover:text-indigo-600 transition-colors">Forgot password?</a>
            </div>

            <button 
              type="submit"
              disabled={isSubmitting}
              className="w-full py-4 mt-6 rounded-2xl text-sm font-bold text-white uppercase tracking-widest transition-all shadow-md hover:shadow-lg disabled:opacity-70 disabled:cursor-not-allowed hover:-translate-y-0.5 active:translate-y-0 flex items-center justify-center gap-2"
              style={{ background: "var(--gradient-orb)" }}
            >
              {isSubmitting ? (
                <><span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span> Authenticating...</>
              ) : (
                "Sign In"
              )}
            </button>
          </form>

          {/* Guest Breakless Route */}
          <div className="w-full mt-6 pt-6 border-t border-indigo-50/60 text-center">
             <button 
               onClick={handleGuestLogin}
               disabled={isSubmitting}
               className="w-full py-3.5 rounded-2xl bg-slate-50/60 border border-slate-200 text-slate-600 text-xs font-bold uppercase tracking-widest hover:bg-white hover:text-indigo-500 transition-all shadow-sm"
             >
               Continue as Guest
             </button>
          </div>

          <p className="mt-8 text-xs font-semibold text-slate-400">
            Don't have an account? <a href="#" className="text-indigo-500 hover:text-indigo-600 ml-1">Sign up</a>
          </p>

        </div>
      </div>
    </div>
  );
}
