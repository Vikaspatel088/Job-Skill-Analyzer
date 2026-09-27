import React from "react";
import { Terminal, Cpu, Sparkles, AlertCircle } from "lucide-react";

interface NavbarProps {
  backendConnected: boolean;
  onLoadSample: () => void;
  onScrollToWorkspace: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  backendConnected,
  onLoadSample,
  onScrollToWorkspace,
}) => {
  return (
    <header className="sticky top-0 z-50 backdrop-blur-md bg-navy/85 border-b border-slate">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand identity */}
        <div className="flex items-center space-x-3 cursor-pointer" onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })}>
          <div className="w-9 h-9 rounded-sm bg-slate-dark border border-slate flex items-center justify-center text-cream shadow-sm">
            <Cpu className="w-5 h-5 text-cream" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-semibold text-cream text-base tracking-tight">Job Skill Analyzer</span>
              <span className="text-[10px] uppercase font-mono px-1.5 py-0.5 rounded bg-slate-dark border border-slate text-cream/80">v1.0</span>
            </div>
            <p className="text-[11px] text-gray-muted hidden sm:block">Deterministic Career Intelligence</p>
          </div>
        </div>

        {/* Engine status & actions */}
        <div className="flex items-center space-x-3 sm:space-x-4">
          <div
            className={`hidden md:flex items-center space-x-2 px-2.5 py-1 rounded-full text-xs font-mono border ${
              backendConnected
                ? "bg-slate-dark/70 border-slate text-cream/90"
                : "bg-orange-soft/40 border-orange-burnt text-cream/90"
            }`}
          >
            {backendConnected ? (
              <>
                <span className="w-2 h-2 rounded-full bg-cream animate-pulse" />
                <span>NLP Engine Ready</span>
              </>
            ) : (
              <>
                <AlertCircle className="w-3.5 h-3.5 text-cream" />
                <span>Engine Reconnecting</span>
              </>
            )}
          </div>

          <button
            type="button"
            onClick={onLoadSample}
            className="hidden sm:inline-flex items-center space-x-1.5 px-3 py-1.5 text-xs font-medium text-cream bg-slate-dark hover:bg-slate border border-slate rounded-sm transition"
          >
            <Sparkles className="w-3.5 h-3.5 text-cream" />
            <span>Load Sample</span>
          </button>

          <button
            type="button"
            onClick={onScrollToWorkspace}
            className="inline-flex items-center space-x-1.5 px-4 py-1.5 text-xs font-semibold text-cream bg-orange-burnt hover:bg-orange-hover border border-orange-burnt rounded-sm shadow-sm transition"
          >
            <Terminal className="w-3.5 h-3.5" />
            <span>Analyze Job</span>
          </button>
        </div>
      </div>
    </header>
  );
};
