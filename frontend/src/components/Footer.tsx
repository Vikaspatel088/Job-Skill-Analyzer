import React from "react";
import { Cpu } from "lucide-react";

export const Footer: React.FC = () => {
  return (
    <footer className="border-t border-slate bg-navy py-12 text-xs text-gray-muted">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8 pb-8 border-b border-slate">
          {/* Col 1: Identity */}
          <div className="space-y-3">
            <div className="flex items-center space-x-2">
              <div className="w-6 h-6 rounded-sm bg-slate-dark border border-slate flex items-center justify-center text-cream">
                <Cpu className="w-3.5 h-3.5" />
              </div>
              <span className="font-semibold text-cream text-sm">Job Skill Analyzer</span>
            </div>
            <p className="leading-relaxed">
              Transparent, deterministic rule-based natural language processing tool designed for career intelligence and objective candidate skill-gap analysis.
            </p>
          </div>

          {/* Col 2: Pipeline Architecture */}
          <div>
            <span className="font-mono uppercase font-bold text-cream block mb-3">NLP Engine</span>
            <ul className="space-y-1.5 font-mono text-[11px]">
              <li>&bull; Boundary-Aware Tokenizer</li>
              <li>&bull; Non-Overlapping Spans</li>
              <li>&bull; Canonical Normalization</li>
              <li>&bull; Deterministic Categorization</li>
              <li>&bull; Objective Gap Scoring</li>
            </ul>
          </div>

          {/* Col 3: Taxonomy Domains */}
          <div>
            <span className="font-mono uppercase font-bold text-cream block mb-3">Core Domains</span>
            <ul className="space-y-1.5">
              <li>Programming Languages & Frameworks</li>
              <li>Databases & Cloud Architecture</li>
              <li>DevOps & CI/CD Pipelines</li>
              <li>REST & Asynchronous APIs</li>
              <li>AI, Data Science & Tooling</li>
            </ul>
          </div>

          {/* Col 4: Design Tokens */}
          <div>
            <span className="font-mono uppercase font-bold text-cream block mb-3">Design System</span>
            <div className="space-y-1 font-mono text-[11px]">
              <div className="flex items-center space-x-2">
                <span className="w-3 h-3 rounded-full bg-[#14252C] border border-slate" />
                <span>#14252C &bull; Deep Navy</span>
              </div>
              <div className="flex items-center space-x-2">
                <span className="w-3 h-3 rounded-full bg-[#273C41] border border-slate" />
                <span>#273C41 &bull; Dark Slate</span>
              </div>
              <div className="flex items-center space-x-2">
                <span className="w-3 h-3 rounded-full bg-[#45575B] border border-slate" />
                <span>#45575B &bull; Slate</span>
              </div>
              <div className="flex items-center space-x-2">
                <span className="w-3 h-3 rounded-full bg-[#A3A39B] border border-slate" />
                <span>#A3A39B &bull; Muted Gray</span>
              </div>
              <div className="flex items-center space-x-2">
                <span className="w-3 h-3 rounded-full bg-[#E6CAB3] border border-slate" />
                <span>#E6CAB3 &bull; Warm Cream</span>
              </div>
              <div className="flex items-center space-x-2">
                <span className="w-3 h-3 rounded-full bg-[#82401D] border border-slate" />
                <span>#82401D &bull; Burnt Orange</span>
              </div>
            </div>
          </div>
        </div>

        <div className="flex flex-col sm:flex-row items-center justify-between text-[11px] text-gray-muted gap-2">
          <span>&copy; {new Date().getFullYear()} Job Skill Analyzer &bull; Senior Engineering Portfolio Edition</span>
          <span>Single-origin API & UI &bull; No account required</span>
        </div>
      </div>
    </footer>
  );
};
