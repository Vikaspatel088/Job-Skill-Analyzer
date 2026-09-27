import React, { useState, useMemo } from "react";
import {
  Download,
  Copy,
  CheckCircle2,
  XCircle,
  BarChart3,
  Layers,
  ArrowUpRight,
  Filter,
  Search,
  Check,
  RotateCcw,
  Sparkles,
} from "lucide-react";
import type { AnalysisReport, PriorityLevel } from "../types";

interface ResultsDashboardProps {
  report: AnalysisReport;
  onReset: () => void;
  onDownloadHtml: () => void;
  onDownloadJson: () => void;
}

export const ResultsDashboard: React.FC<ResultsDashboardProps> = ({
  report,
  onReset,
  onDownloadHtml,
  onDownloadJson,
}) => {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState<string>("ALL");
  const [selectedPriority, setSelectedPriority] = useState<string>("ALL");
  const [statusFilter, setStatusFilter] = useState<"ALL" | "MATCHED" | "MISSING">("ALL");
  const [copiedNotification, setCopiedNotification] = useState(false);

  const comp = report.candidate_comparison;

  // Compute dominant categories for factual role snapshot
  const roleSnapshot = useMemo(() => {
    if (!report.category_counts || Object.keys(report.category_counts).length === 0) {
      return "No specific technical domain concentration detected.";
    }
    const sorted = Object.entries(report.category_counts).sort((a, b) => b[1] - a[1]);
    const topCategories = sorted.slice(0, 2).map(([cat]) => cat);
    if (topCategories.length === 1) {
      return `This role is heavily focused on ${topCategories[0]}.`;
    }
    return `This role strongly emphasizes ${topCategories[0]} and ${topCategories[1]}, supported by adjacent operational tooling.`;
  }, [report.category_counts]);

  // Priority mapping lookup
  const priorityBySkill = useMemo(() => {
    const map = new Map<string, { priority: PriorityLevel; reason: string }>();
    for (const p of report.priorities) {
      map.set(p.skill.toLowerCase(), { priority: p.priority, reason: p.reason });
    }
    return map;
  }, [report.priorities]);

  // Filter skills
  const filteredSkills = useMemo(() => {
    return report.skills.filter((skill) => {
      // Search
      if (
        searchQuery &&
        !skill.name.toLowerCase().includes(searchQuery.toLowerCase()) &&
        !skill.category.toLowerCase().includes(searchQuery.toLowerCase())
      ) {
        return false;
      }
      // Category filter
      if (selectedCategory !== "ALL" && skill.category !== selectedCategory) {
        return false;
      }
      // Status filter
      if (comp.provided) {
        const isMatched = comp.matched_skills.some(
          (m) => m.toLowerCase() === skill.name.toLowerCase()
        );
        if (statusFilter === "MATCHED" && !isMatched) return false;
        if (statusFilter === "MISSING" && isMatched) return false;
      }
      // Priority filter
      if (selectedPriority !== "ALL") {
        const prioInfo = priorityBySkill.get(skill.name.toLowerCase());
        if (!prioInfo || prioInfo.priority !== selectedPriority) return false;
      }
      return true;
    });
  }, [report.skills, searchQuery, selectedCategory, statusFilter, selectedPriority, comp, priorityBySkill]);

  const handleCopySummary = async () => {
    const lines = [
      `JOB SKILL ANALYSIS SUMMARY`,
      `Total Skills Detected: ${report.total_skills}`,
      `Role Focus: ${roleSnapshot}`,
      "",
    ];

    if (comp.provided) {
      lines.push(
        `Candidate Coverage: ${comp.match_percentage.toFixed(1)}%`,
        `Matched (${comp.matched_skills.length}): ${comp.matched_skills.join(", ") || "None"}`,
        `Missing (${comp.missing_skills.length}): ${comp.missing_skills.join(", ") || "None"}`,
        ""
      );
    }

    lines.push(`Top Priority Skills:`);
    for (const p of report.priorities.slice(0, 5)) {
      lines.push(`• [${p.priority.toUpperCase()}] ${p.skill} — ${p.reason}`);
    }

    try {
      await navigator.clipboard.writeText(lines.join("\n"));
      setCopiedNotification(true);
      setTimeout(() => setCopiedNotification(false), 2500);
    } catch {
      // fallback
    }
  };

  const categories = Object.keys(report.category_counts);

  return (
    <section id="results" className="py-12 sm:py-16 bg-navy/95 border-t border-slate">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-10">
        {/* Results Header & Actions */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-slate">
          <div>
            <div className="flex items-center space-x-2">
              <span className="text-xs font-mono uppercase tracking-wider text-gray-muted">Analysis Output</span>
              <span className="px-2 py-0.5 text-[10px] font-mono rounded bg-slate-dark border border-slate text-cream">
                Engine Completed
              </span>
            </div>
            <h2 className="text-2xl sm:text-3xl font-bold text-cream mt-1">Intelligence Breakdown</h2>
          </div>

          <div className="flex flex-wrap items-center gap-2.5">
            <button
              type="button"
              onClick={handleCopySummary}
              className="inline-flex items-center space-x-1.5 px-3 py-2 text-xs font-medium rounded-sm bg-slate-dark hover:bg-slate border border-slate text-cream transition"
            >
              {copiedNotification ? <Check className="w-3.5 h-3.5 text-cream" /> : <Copy className="w-3.5 h-3.5" />}
              <span>{copiedNotification ? "Copied!" : "Copy Summary"}</span>
            </button>

            <button
              type="button"
              onClick={onDownloadJson}
              className="inline-flex items-center space-x-1.5 px-3 py-2 text-xs font-medium rounded-sm bg-slate-dark hover:bg-slate border border-slate text-cream transition"
            >
              <Download className="w-3.5 h-3.5" />
              <span>Export JSON</span>
            </button>

            <button
              type="button"
              onClick={onDownloadHtml}
              className="inline-flex items-center space-x-1.5 px-3 py-2 text-xs font-medium rounded-sm bg-slate-dark hover:bg-slate border border-slate text-cream transition"
            >
              <ArrowUpRight className="w-3.5 h-3.5 text-cream" />
              <span>HTML Report</span>
            </button>

            <button
              type="button"
              onClick={onReset}
              className="inline-flex items-center space-x-1.5 px-3 py-2 text-xs font-medium rounded-sm bg-slate/30 hover:bg-slate/70 border border-slate text-gray-muted hover:text-cream transition"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span>New Analysis</span>
            </button>
          </div>
        </div>

        {/* 1. Top Summary Metric Cards */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="p-5 rounded-lg bg-slate-dark border border-slate shadow-card flex flex-col justify-between">
            <span className="text-xs font-mono uppercase tracking-wider text-gray-muted">Skills Detected</span>
            <div className="mt-3 flex items-baseline justify-between">
              <span className="text-3xl sm:text-4xl font-extrabold text-cream">{report.total_skills}</span>
              <span className="text-xs text-gray-muted font-mono">{categories.length} domains</span>
            </div>
          </div>

          <div className="p-5 rounded-lg bg-slate-dark border border-slate shadow-card flex flex-col justify-between">
            <span className="text-xs font-mono uppercase tracking-wider text-gray-muted">Matched Profile</span>
            <div className="mt-3 flex items-baseline justify-between">
              <span className="text-3xl sm:text-4xl font-extrabold text-cream">
                {comp.provided ? comp.matched_skills.length : "—"}
              </span>
              <span className="text-xs text-gray-muted font-mono">
                {comp.provided ? "skills matched" : "no profile"}
              </span>
            </div>
          </div>

          <div className="p-5 rounded-lg bg-slate-dark border border-slate shadow-card flex flex-col justify-between">
            <span className="text-xs font-mono uppercase tracking-wider text-gray-muted">Skill Gaps</span>
            <div className="mt-3 flex items-baseline justify-between">
              <span className="text-3xl sm:text-4xl font-extrabold text-cream">
                {comp.provided ? comp.missing_skills.length : "—"}
              </span>
              <span className="text-xs text-gray-muted font-mono">
                {comp.provided ? "to acquire" : "no profile"}
              </span>
            </div>
          </div>

          <div className="p-5 rounded-lg bg-slate-dark border border-slate shadow-card flex flex-col justify-between">
            <span className="text-xs font-mono uppercase tracking-wider text-gray-muted">Role Coverage</span>
            <div className="mt-3 flex items-baseline justify-between">
              <span className="text-3xl sm:text-4xl font-extrabold text-cream">
                {comp.provided ? `${comp.match_percentage.toFixed(0)}%` : "—"}
              </span>
              {comp.provided && (
                <div className="w-16 bg-navy rounded-full h-2 overflow-hidden border border-slate">
                  <div
                    className="bg-cream h-full rounded-full transition-all duration-500"
                    style={{ width: `${Math.min(100, Math.max(0, comp.match_percentage))}%` }}
                  />
                </div>
              )}
            </div>
          </div>
        </div>

        {/* 2. Role Snapshot & Category Distribution */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-stretch">
          {/* Factual Role Snapshot (5 cols) */}
          <div className="lg:col-span-5 p-6 rounded-lg bg-slate-dark border border-slate shadow-card flex flex-col justify-between">
            <div>
              <div className="flex items-center space-x-2 text-cream mb-2">
                <Sparkles className="w-4 h-4 text-cream" />
                <h3 className="text-sm font-semibold tracking-wide uppercase font-mono">Role Profile Snapshot</h3>
              </div>
              <p className="text-sm sm:text-base text-cream/90 leading-relaxed font-normal mt-3">
                {roleSnapshot}
              </p>
              <div className="mt-5 pt-4 border-t border-slate text-xs text-gray-muted leading-relaxed">
                Deterministic synthesis derived from token frequency counts across technical pillars.
                No generative guesswork.
              </div>
            </div>

            <div className="mt-6 flex flex-wrap gap-2">
              {categories.slice(0, 4).map((cat) => (
                <span
                  key={cat}
                  className="px-2.5 py-1 text-xs rounded-sm bg-navy border border-slate text-cream/80"
                >
                  {cat} ({report.category_counts[cat]})
                </span>
              ))}
            </div>
          </div>

          {/* Interactive Category Breakdown (7 cols) */}
          <div className="lg:col-span-7 p-6 rounded-lg bg-slate-dark border border-slate shadow-card flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center space-x-2 text-cream">
                  <BarChart3 className="w-4 h-4 text-cream" />
                  <h3 className="text-sm font-semibold tracking-wide uppercase font-mono">Domain Composition</h3>
                </div>
                {selectedCategory !== "ALL" && (
                  <button
                    type="button"
                    onClick={() => setSelectedCategory("ALL")}
                    className="text-xs text-cream hover:underline"
                  >
                    Clear Filter
                  </button>
                )}
              </div>

              <div className="space-y-3">
                {Object.entries(report.category_counts).map(([category, count]) => {
                  const pct = report.total_skills > 0 ? (count / report.total_skills) * 100 : 0;
                  const isSelected = selectedCategory === category;
                  return (
                    <button
                      key={category}
                      type="button"
                      aria-pressed={isSelected}
                      onClick={() => setSelectedCategory(isSelected ? "ALL" : category)}
                      className={`w-full text-left cursor-pointer p-2 rounded-sm transition ${
                        isSelected ? "bg-navy border border-cream/50" : "hover:bg-navy/50"
                      }`}
                    >
                      <div className="flex justify-between items-center text-xs mb-1.5 font-medium">
                        <span className={isSelected ? "text-cream font-bold" : "text-cream/90"}>
                          {category}
                        </span>
                        <span className="font-mono text-gray-muted">
                          {count} skill{count > 1 ? "s" : ""} &bull; {pct.toFixed(0)}%
                        </span>
                      </div>
                      <div className="w-full bg-navy rounded-full h-2 overflow-hidden border border-slate">
                        <div
                          className="bg-slate-light hover:bg-cream h-full rounded-full transition-all duration-300"
                          style={{ width: `${pct}%` }}
                        />
                      </div>
                    </button>
                  );
                })}
              </div>
            </div>
          </div>
        </div>

        {/* 3. Skill Gap Split View (Matched vs Missing) */}
        {comp.provided ? (
          <div className="p-6 rounded-lg bg-slate-dark border border-slate shadow-panel">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-6 pb-4 border-b border-slate">
              <div>
                <h3 className="text-lg font-bold text-cream">Candidate Gap Analysis</h3>
                <p className="text-xs text-gray-muted mt-0.5">
                  Comparison between the posting's technical requirements and your supplied profile.
                </p>
              </div>
              <span className="text-xs font-mono px-3 py-1 rounded bg-navy border border-slate text-cream self-start sm:self-auto">
                {comp.match_percentage.toFixed(1)}% Profile Coverage
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Matched */}
              <div className="p-4 rounded-md bg-navy/60 border border-slate">
                <div className="flex items-center space-x-2 text-cream mb-3">
                  <CheckCircle2 className="w-4 h-4 text-cream" />
                  <h4 className="text-sm font-semibold">Matched Competencies ({comp.matched_skills.length})</h4>
                </div>
                {comp.matched_skills.length > 0 ? (
                  <div className="flex flex-wrap gap-2">
                    {comp.matched_skills.map((skill) => (
                      <span
                        key={skill}
                        className="inline-flex items-center space-x-1.5 px-3 py-1 rounded-sm text-xs font-medium bg-slate-dark border border-slate text-cream"
                      >
                        <Check className="w-3 h-3 text-cream" />
                        <span>{skill}</span>
                      </span>
                    ))}
                  </div>
                ) : (
                  <p className="text-xs text-gray-muted italic">No skills in your profile matched this role yet.</p>
                )}
              </div>

              {/* Missing */}
              <div className="p-4 rounded-md bg-navy/60 border border-slate">
                <div className="flex items-center space-x-2 text-cream mb-3">
                  <XCircle className="w-4 h-4 text-orange-burnt" />
                  <h4 className="text-sm font-semibold">Skills to Acquire ({comp.missing_skills.length})</h4>
                </div>
                {comp.missing_skills.length > 0 ? (
                  <div className="flex flex-wrap gap-2">
                    {comp.missing_skills.map((skill) => {
                      const prio = priorityBySkill.get(skill.toLowerCase());
                      const isHigh = prio?.priority === "High";
                      return (
                        <span
                          key={skill}
                          className={`inline-flex items-center space-x-1.5 px-3 py-1 rounded-sm text-xs font-medium border ${
                            isHigh
                              ? "bg-orange-soft/40 border-orange-burnt text-cream"
                              : "bg-slate-dark border-slate text-cream/90"
                          }`}
                        >
                          <span className="w-1.5 h-1.5 rounded-full bg-orange-burnt" />
                          <span>{skill}</span>
                          {prio && (
                            <span className="text-[10px] font-mono text-gray-muted ml-1">
                              [{prio.priority}]
                            </span>
                          )}
                        </span>
                      );
                    })}
                  </div>
                ) : (
                  <p className="text-xs text-cream font-medium">100% matched! You cover every identified requirement.</p>
                )}
              </div>
            </div>
          </div>
        ) : (
          <div className="p-6 rounded-lg bg-slate-dark/70 border border-slate text-center">
            <h3 className="text-base font-bold text-cream">Want personalized gap analysis?</h3>
            <p className="text-xs text-gray-muted max-w-md mx-auto mt-1 mb-4 leading-relaxed">
              We never invent false claims about what you're missing. Toggle on "Compare My Skills" above to see your exact match percentage.
            </p>
            <button
              type="button"
              onClick={() => {
                const el = document.getElementById("workspace");
                el?.scrollIntoView({ behavior: "smooth" });
              }}
              className="inline-flex items-center space-x-2 px-4 py-2 text-xs font-semibold rounded-sm bg-slate-dark hover:bg-slate border border-slate text-cream transition"
            >
              <span>Compare My Skills</span>
            </button>
          </div>
        )}

        {/* 4. Priority Intelligence Section */}
        <div className="p-6 rounded-lg bg-slate-dark border border-slate shadow-card">
          <div className="mb-6 pb-4 border-b border-slate">
            <div className="flex items-center space-x-2 text-cream">
              <Layers className="w-4 h-4 text-cream" />
              <h3 className="text-lg font-bold">Priority Intelligence & Explanations</h3>
            </div>
            <p className="text-xs text-gray-muted mt-1">
              Transparent, deterministic evaluation calculated from mention frequency, core architectural importance, and profile gap status.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {(["High", "Medium", "Low"] as PriorityLevel[]).map((level) => {
              const skillsAtLevel = report.priorities.filter((p) => p.priority === level);
              return (
                <div key={level} className="p-4 rounded-md bg-navy/60 border border-slate flex flex-col">
                  <div className="flex items-center justify-between pb-3 mb-3 border-b border-slate/60">
                    <span
                      className={`text-xs font-mono font-bold uppercase tracking-wider px-2 py-0.5 rounded ${
                        level === "High"
                          ? "bg-orange-burnt text-cream"
                          : level === "Medium"
                          ? "bg-slate text-cream"
                          : "bg-navy border border-slate text-gray-muted"
                      }`}
                    >
                      {level} Priority
                    </span>
                    <span className="text-xs font-mono text-gray-muted">
                      {skillsAtLevel.length} skill{skillsAtLevel.length !== 1 ? "s" : ""}
                    </span>
                  </div>

                  <div className="space-y-3 flex-1">
                    {skillsAtLevel.length > 0 ? (
                      skillsAtLevel.map((p) => (
                        <div
                          key={p.skill}
                          className="p-3 rounded-sm bg-slate-dark/90 border border-slate text-xs space-y-1 hover:border-slate-light transition"
                        >
                          <div className="flex items-center justify-between">
                            <strong className="text-cream text-sm">{p.skill}</strong>
                            <span className="text-[10px] font-mono text-gray-muted">{p.category}</span>
                          </div>
                          <p className="text-gray-muted text-[11px] leading-relaxed">{p.reason}</p>
                        </div>
                      ))
                    ) : (
                      <p className="text-xs text-gray-muted italic py-4 text-center">No {level.toLowerCase()} priority skills.</p>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* 5. Filterable Skills Explorer */}
        <div className="p-6 rounded-lg bg-slate-dark border border-slate shadow-panel space-y-6">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate">
            <div>
              <h3 className="text-lg font-bold text-cream">Extracted Skills Directory</h3>
              <p className="text-xs text-gray-muted mt-0.5">
                Showing {filteredSkills.length} of {report.total_skills} detected technologies.
              </p>
            </div>

            {/* Search input */}
            <div className="relative w-full md:w-72">
              <Search className="w-4 h-4 text-gray-muted absolute left-3 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                aria-label="Search skills or domain"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search skills or domain..."
                className="w-full pl-9 pr-4 py-2 text-xs rounded-sm bg-navy border border-slate text-cream placeholder-gray-muted/60 focus:outline-none focus:border-cream"
              />
            </div>
          </div>

          {/* Filter Pills */}
          <div className="flex flex-wrap items-center gap-2 text-xs">
            <span className="text-gray-muted font-mono flex items-center space-x-1 mr-1">
              <Filter className="w-3.5 h-3.5" />
              <span>Filters:</span>
            </span>

            {/* Category Filter */}
            <select
              aria-label="Filter by category"
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="bg-navy border border-slate rounded-sm px-2.5 py-1.5 text-cream text-xs focus:outline-none"
            >
              <option value="ALL">All Categories</option>
              {categories.map((cat) => (
                <option key={cat} value={cat}>
                  {cat} ({report.category_counts[cat]})
                </option>
              ))}
            </select>

            {/* Priority Filter */}
            <select
              aria-label="Filter by priority"
              value={selectedPriority}
              onChange={(e) => setSelectedPriority(e.target.value)}
              className="bg-navy border border-slate rounded-sm px-2.5 py-1.5 text-cream text-xs focus:outline-none"
            >
              <option value="ALL">All Priorities</option>
              <option value="High">High Priority</option>
              <option value="Medium">Medium Priority</option>
              <option value="Low">Low Priority</option>
            </select>

            {/* Status Filter if candidate provided */}
            {comp.provided && (
              <div role="group" aria-label="Filter by match status" className="inline-flex rounded-sm border border-slate bg-navy p-0.5">
                {(["ALL", "MATCHED", "MISSING"] as const).map((st) => (
                  <button
                    key={st}
                    type="button"
                    aria-pressed={statusFilter === st}
                    onClick={() => setStatusFilter(st)}
                    className={`px-2.5 py-1 text-xs rounded-sm font-medium transition ${
                      statusFilter === st ? "bg-slate-dark text-cream font-bold" : "text-gray-muted hover:text-cream"
                    }`}
                  >
                    {st === "ALL" ? "All" : st === "MATCHED" ? "Matched" : "Missing"}
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Skill Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3.5 pt-2">
            {filteredSkills.map((skill) => {
              const isMatched = comp.provided && comp.matched_skills.some(
                (m) => m.toLowerCase() === skill.name.toLowerCase()
              );
              const prioInfo = priorityBySkill.get(skill.name.toLowerCase());

              return (
                <div
                  key={skill.name}
                  className="p-4 rounded-md bg-navy/70 border border-slate hover:border-slate-light transition flex flex-col justify-between"
                >
                  <div className="flex items-start justify-between">
                    <div>
                      <div className="flex items-center space-x-2">
                        <strong className="text-sm font-semibold text-cream">{skill.name}</strong>
                        {skill.frequency > 1 && (
                          <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-slate-dark border border-slate text-cream/90">
                            ×{skill.frequency}
                          </span>
                        )}
                      </div>
                      <span className="text-xs text-gray-muted block mt-0.5">{skill.category}</span>
                    </div>

                    {comp.provided && (
                      <span
                        className={`text-[10px] font-mono px-2 py-0.5 rounded border ${
                          isMatched
                            ? "bg-slate-dark border-slate text-cream"
                            : "bg-orange-soft/40 border-orange-burnt text-cream"
                        }`}
                      >
                        {isMatched ? "Matched" : "Missing"}
                      </span>
                    )}
                  </div>

                  {prioInfo && (
                    <div className="mt-3 pt-2.5 border-t border-slate/60 text-[11px] text-gray-muted flex items-center justify-between">
                      <span className="font-mono">Priority: {prioInfo.priority}</span>
                      <span className="truncate max-w-[150px]" title={prioInfo.reason}>
                        {prioInfo.reason}
                      </span>
                    </div>
                  )}
                </div>
              );
            })}
          </div>

          {filteredSkills.length === 0 && (
            <div className="py-12 text-center text-gray-muted text-sm italic">
              No technical skills matched your filter criteria.
            </div>
          )}
        </div>
      </div>
    </section>
  );
};
