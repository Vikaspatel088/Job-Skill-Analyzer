import React from "react";
import { ArrowRight, Sparkles, ShieldCheck, Zap, Layers } from "lucide-react";

interface HeroProps {
  onStartAnalysis: () => void;
  onLoadSample: () => void;
}

export const Hero: React.FC<HeroProps> = ({ onStartAnalysis, onLoadSample }) => {
  return (
    <section className="relative overflow-hidden border-b border-slate bg-navy">
      {/* Background image with layered dark gradients */}
      <div
        className="absolute inset-0 z-0 bg-cover bg-center bg-no-repeat opacity-25 mix-blend-luminosity filter contrast-125"
        style={{ backgroundImage: `url('/hero-bg.jpg')` }}
      />
      <div className="absolute inset-0 z-0 bg-gradient-to-b from-navy/90 via-navy/95 to-navy" />
      <div className="absolute inset-0 z-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-slate-dark/40 via-transparent to-transparent" />

      <div className="relative z-10 max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 pt-16 pb-20 sm:pt-24 sm:pb-28 text-center">
        {/* Eyebrow badge */}
        <div className="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-slate-dark/90 border border-slate text-xs font-mono tracking-wider text-cream uppercase mb-8 shadow-sm">
          <span className="w-1.5 h-1.5 rounded-full bg-cream" />
          <span>Career Intelligence Platform</span>
        </div>

        {/* Primary headline */}
        <h1 className="text-4xl sm:text-5xl md:text-6xl font-extrabold text-cream tracking-tight leading-[1.15] mb-6">
          Understand what the job <br className="hidden sm:inline" />
          <span className="text-cream underline decoration-slate decoration-2 underline-offset-8">
            actually asks for.
          </span>
        </h1>

        {/* Subtitle */}
        <p className="max-w-2xl mx-auto text-base sm:text-lg text-gray-muted leading-relaxed mb-10">
          Turn messy job descriptions into a clear map of skills, gaps, priorities and opportunities.
          Powered by transparent, deterministic NLP with zero hallucinations.
        </p>

        {/* CTAs */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-16">
          <button
            type="button"
            onClick={onStartAnalysis}
            className="w-full sm:w-auto inline-flex items-center justify-center space-x-2.5 px-7 py-3.5 rounded-sm bg-orange-burnt hover:bg-orange-hover text-cream font-semibold text-sm shadow-card transition transform active:scale-[0.99]"
          >
            <span>Analyze a Job</span>
            <ArrowRight className="w-4 h-4" />
          </button>

          <button
            type="button"
            onClick={onLoadSample}
            className="w-full sm:w-auto inline-flex items-center justify-center space-x-2 px-6 py-3.5 rounded-sm bg-slate-dark hover:bg-slate border border-slate text-cream font-medium text-sm transition"
          >
            <Sparkles className="w-4 h-4 text-cream" />
            <span>Try Sample Job</span>
          </button>
        </div>

        {/* Pillars / Trust indicators */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 pt-10 border-t border-slate/60 text-left">
          <div className="flex items-start space-x-3.5">
            <div className="p-2 rounded-sm bg-slate-dark border border-slate text-cream shrink-0 mt-0.5">
              <Zap className="w-4 h-4" />
            </div>
            <div>
              <h2 className="text-sm font-semibold text-cream">Punctuation-Safe NLP</h2>
              <p className="text-xs text-gray-muted mt-1 leading-normal">
                Properly identifies C++, C#, .NET, Node.js, and CI/CD without tokenizer fragmentation.
              </p>
            </div>
          </div>

          <div className="flex items-start space-x-3.5">
            <div className="p-2 rounded-sm bg-slate-dark border border-slate text-cream shrink-0 mt-0.5">
              <ShieldCheck className="w-4 h-4" />
            </div>
            <div>
              <h2 className="text-sm font-semibold text-cream">Objective Gap Analysis</h2>
              <p className="text-xs text-gray-muted mt-1 leading-normal">
                Never invents false candidate gaps. Evaluates alignment only when profile skills are supplied.
              </p>
            </div>
          </div>

          <div className="flex items-start space-x-3.5">
            <div className="p-2 rounded-sm bg-slate-dark border border-slate text-cream shrink-0 mt-0.5">
              <Layers className="w-4 h-4" />
            </div>
            <div>
              <h2 className="text-sm font-semibold text-cream">Explainable Priorities</h2>
              <p className="text-xs text-gray-muted mt-1 leading-normal">
                Deterministic High, Medium, and Low rankings grounded in posting frequency and architectural roles.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
