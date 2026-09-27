import React, { useState } from "react";
import { FileText, UserCheck, Sparkles, Trash2, ArrowRight, Loader2, Check } from "lucide-react";

interface AnalyzerWorkspaceProps {
  jobDescription: string;
  setJobDescription: (val: string) => void;
  candidateSkills: string;
  setCandidateSkills: (val: string) => void;
  compareEnabled: boolean;
  setCompareEnabled: (val: boolean) => void;
  onAnalyze: () => void;
  onLoadSample: () => void;
  isLoading: boolean;
  loadingStep: string;
  error: string | null;
  onClearError: () => void;
}

const PRESET_SKILLS = [
  { label: "Backend Python", skills: "Python, FastAPI, PostgreSQL, Docker, Git, REST API, Redis" },
  { label: "Full-Stack React", skills: "JavaScript, TypeScript, React, Node.js, HTML, CSS, Git, REST API" },
  { label: "DevOps & Cloud", skills: "Docker, Kubernetes, AWS, Terraform, CI/CD, Linux, Git, GitHub Actions" },
];

export const AnalyzerWorkspace: React.FC<AnalyzerWorkspaceProps> = ({
  jobDescription,
  setJobDescription,
  candidateSkills,
  setCandidateSkills,
  compareEnabled,
  setCompareEnabled,
  onAnalyze,
  onLoadSample,
  isLoading,
  loadingStep,
  error,
  onClearError,
}) => {
  const [copiedPreset, setCopiedPreset] = useState<string | null>(null);

  const wordCount = jobDescription.trim() ? jobDescription.trim().split(/\s+/).length : 0;
  const charCount = jobDescription.length;

  const handleApplyPreset = (skills: string, label: string) => {
    setCandidateSkills(skills);
    setCopiedPreset(label);
    setTimeout(() => setCopiedPreset(null), 1500);
  };

  const handleClear = () => {
    setJobDescription("");
    onClearError();
  };

  return (
    <section id="workspace" className="py-12 sm:py-16 bg-navy relative">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row md:items-end justify-between mb-8 pb-4 border-b border-slate">
          <div>
            <span className="text-xs font-mono uppercase tracking-wider text-gray-muted">Analysis Workspace</span>
            <h2 className="text-2xl sm:text-3xl font-bold text-cream mt-1">Submit Role Requirements</h2>
          </div>
          <p className="text-xs sm:text-sm text-gray-muted mt-2 md:mt-0 max-w-md">
            Paste an unformatted job posting. Our engine handles multi-word technologies, aliases, and punctuation boundaries.
          </p>
        </div>

        {/* Error notification banner */}
        {error && (
          <div role="alert" className="mb-6 p-4 rounded-md bg-slate-dark border border-orange-burnt/80 flex items-center justify-between text-cream shadow-card animate-fadeIn">
            <div className="flex items-center space-x-3">
              <span className="w-2.5 h-2.5 rounded-full bg-orange-burnt animate-pulse" />
              <p className="text-sm font-medium">{error}</p>
            </div>
            <button
              type="button"
              onClick={onClearError}
              className="text-xs text-gray-muted hover:text-cream px-2 py-1 rounded bg-slate/40 hover:bg-slate/80 transition"
            >
              Dismiss
            </button>
          </div>
        )}

        {/* Main 2-column workspace */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
          {/* Left: Job Description input (7 cols) */}
          <div className="lg:col-span-7 bg-slate-dark border border-slate rounded-lg p-5 shadow-panel flex flex-col">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center space-x-2">
                <FileText className="w-4 h-4 text-cream" />
                <label htmlFor="job-description-input" className="text-sm font-semibold text-cream">
                  Job Description <span className="text-orange-burnt">*</span>
                </label>
              </div>

              <div className="flex items-center space-x-2 text-xs text-gray-muted">
                <button
                  type="button"
                  onClick={onLoadSample}
                  className="inline-flex items-center space-x-1 hover:text-cream px-2 py-1 rounded bg-slate/30 hover:bg-slate/60 transition"
                >
                  <Sparkles className="w-3 h-3 text-cream" />
                  <span>Sample</span>
                </button>
                {jobDescription && (
                  <button
                    type="button"
                    onClick={handleClear}
                    className="inline-flex items-center space-x-1 hover:text-cream px-2 py-1 rounded bg-slate/30 hover:bg-slate/60 transition"
                  >
                    <Trash2 className="w-3 h-3" />
                    <span>Clear</span>
                  </button>
                )}
              </div>
            </div>

            <textarea
              id="job-description-input"
              rows={11}
              value={jobDescription}
              onChange={(e) => {
                setJobDescription(e.target.value);
                if (error) onClearError();
              }}
              placeholder="Paste job description text here (responsibilities, technical stack, qualifications)..."
              className="w-full p-4 rounded-md bg-navy/90 border border-slate text-cream placeholder-gray-muted/60 text-sm font-normal focus:outline-none focus:ring-1 focus:ring-cream focus:border-cream resize-y leading-relaxed transition"
            />

            <div className="mt-3 flex items-center justify-between text-xs text-gray-muted font-mono">
              <span>{wordCount} words &bull; {charCount} characters</span>
              <span className="text-[11px] text-gray-muted">Markdown & plain text supported</span>
            </div>
          </div>

          {/* Right: Candidate Skills Comparison (5 cols) */}
          <div className="lg:col-span-5 bg-slate-dark border border-slate rounded-lg p-5 shadow-panel flex flex-col">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-2">
                <UserCheck className="w-4 h-4 text-cream" />
                <span className="text-sm font-semibold text-cream">Candidate Skill Gap</span>
              </div>

              {/* Toggle comparison */}
              <label className="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  aria-label="Compare my skills"
                  checked={compareEnabled}
                  onChange={(e) => setCompareEnabled(e.target.checked)}
                  className="sr-only peer"
                />
                <div className="w-9 h-5 bg-slate peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-cream after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-orange-burnt"></div>
                <span className="ml-2 text-xs font-medium text-cream">
                  {compareEnabled ? "Enabled" : "Disabled"}
                </span>
              </label>
            </div>

            {compareEnabled ? (
              <div className="space-y-4">
                <p className="text-xs text-gray-muted leading-relaxed">
                  Provide your competencies to compare your profile against the role.
                  We calculate matched skills, identify gaps, and prioritize what to learn.
                </p>

                <label htmlFor="candidate-skills-input" className="sr-only">Your skills</label>
                <textarea
                  id="candidate-skills-input"
                  rows={4}
                  value={candidateSkills}
                  onChange={(e) => setCandidateSkills(e.target.value)}
                  placeholder="e.g. Python, Docker, PostgreSQL, React, AWS, Git..."
                  className="w-full p-3.5 rounded-md bg-navy/90 border border-slate text-cream placeholder-gray-muted/60 text-sm focus:outline-none focus:ring-1 focus:ring-cream focus:border-cream resize-none transition"
                />

                {/* Quick Presets */}
                <div>
                  <span className="text-[11px] font-mono uppercase tracking-wider text-gray-muted block mb-2">
                    Quick Preset Profiles
                  </span>
                  <div className="flex flex-wrap gap-1.5">
                    {PRESET_SKILLS.map((preset) => (
                      <button
                        key={preset.label}
                        type="button"
                        onClick={() => handleApplyPreset(preset.skills, preset.label)}
                        className="inline-flex items-center space-x-1 px-2.5 py-1 text-xs rounded-sm bg-navy/80 hover:bg-slate border border-slate text-cream transition"
                      >
                        {copiedPreset === preset.label ? (
                          <Check className="w-3 h-3 text-cream" />
                        ) : null}
                        <span>{preset.label}</span>
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            ) : (
              <div className="py-8 px-4 text-center rounded-md bg-navy/50 border border-slate/60 flex flex-col items-center justify-center space-y-2">
                <UserCheck className="w-8 h-8 text-gray-muted/50 mb-1" />
                <p className="text-sm font-medium text-cream">Candidate comparison is disabled</p>
                <p className="text-xs text-gray-muted max-w-xs leading-relaxed">
                  Toggle on to enter your skills and perform gap analysis with personalized learning priorities.
                </p>
                <button
                  type="button"
                  onClick={() => setCompareEnabled(true)}
                  className="mt-2 text-xs font-semibold text-cream underline decoration-slate hover:text-cream/80"
                >
                  Enable Profile Comparison
                </button>
              </div>
            )}
          </div>
        </div>

        {/* Action button bar */}
        <div className="mt-8 flex flex-col sm:flex-row items-center justify-end gap-4">
          {isLoading && (
            <div role="status" aria-live="polite" className="flex items-center space-x-2 text-xs font-mono text-cream/90 bg-slate-dark px-3 py-2 rounded-sm border border-slate">
              <Loader2 className="w-3.5 h-3.5 animate-spin text-cream" />
              <span>{loadingStep || "Processing NLP pipeline..."}</span>
            </div>
          )}

          <button
            type="button"
            disabled={isLoading || !jobDescription.trim()}
            onClick={onAnalyze}
            className="w-full sm:w-auto inline-flex items-center justify-center space-x-2.5 px-8 py-3.5 rounded-sm bg-orange-burnt hover:bg-orange-hover disabled:bg-slate-dark disabled:border disabled:border-slate disabled:text-gray-muted disabled:cursor-not-allowed text-cream font-semibold text-sm shadow-card transition transform active:scale-[0.99]"
          >
            {isLoading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin text-cream" />
                <span>Running Engine...</span>
              </>
            ) : (
              <>
                <span>Analyze Requirements</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </div>
      </div>
    </section>
  );
};
