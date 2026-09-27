import React, { useState, useEffect } from "react";
import { Navbar } from "./components/Navbar";
import { Hero } from "./components/Hero";
import { AnalyzerWorkspace } from "./components/AnalyzerWorkspace";
import { ResultsDashboard } from "./components/ResultsDashboard";
import { Footer } from "./components/Footer";
import type { AnalysisReport } from "./types";
import { analyzeJob, fetchSample, checkHealth, fetchHtmlReport, ApiError } from "./services/api";

function downloadBlob(blob: Blob, filename: string): void {
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  window.setTimeout(() => URL.revokeObjectURL(url), 1000);
}

export const App: React.FC = () => {
  const [jobDescription, setJobDescription] = useState<string>("");
  const [candidateSkills, setCandidateSkills] = useState<string>("");
  const [compareEnabled, setCompareEnabled] = useState<boolean>(true);
  const [report, setReport] = useState<AnalysisReport | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [loadingStep, setLoadingStep] = useState<string>("");
  const [error, setError] = useState<string | null>(null);
  const [backendConnected, setBackendConnected] = useState<boolean>(true);

  // Check health on mount
  useEffect(() => {
    checkHealth().then(setBackendConnected);
    const interval = setInterval(() => {
      checkHealth().then(setBackendConnected);
    }, 15000);
    return () => clearInterval(interval);
  }, []);

  const scrollToWorkspace = () => {
    const el = document.getElementById("workspace");
    el?.scrollIntoView({ behavior: "smooth" });
  };

  const scrollToResults = () => {
    setTimeout(() => {
      const el = document.getElementById("results");
      el?.scrollIntoView({ behavior: "smooth" });
    }, 100);
  };

  const handleLoadSample = async () => {
    setError(null);
    try {
      const sample = await fetchSample();
      setJobDescription(sample.job_description);
      setCandidateSkills(sample.candidate_skills);
      setCompareEnabled(true);
      scrollToWorkspace();
    } catch {
      // Local fallback in case backend is offline
      setJobDescription(
        "Senior Backend & Platform Engineer\n\n" +
        "We are seeking an experienced Backend Engineer to scale our distributed microservices. " +
        "You will design asynchronous APIs using Python and FastAPI, optimizing relational data models " +
        "in PostgreSQL. The role requires containerizing services with Docker and orchestrating deployments " +
        "via Kubernetes. You will manage cloud infrastructure on AWS, leveraging EC2, S3, and Lambda functions. " +
        "Experience with REST API design, Git version control, and automated CI/CD pipelines using GitHub Actions " +
        "is required. Familiarity with Redis caching and Machine Learning fundamentals is a strong plus."
      );
      setCandidateSkills("Python, FastAPI, PostgreSQL, Docker, Git, REST API, Redis");
      setCompareEnabled(true);
      scrollToWorkspace();
    }
  };

  const handleAnalyze = async () => {
    if (!jobDescription.trim()) {
      setError("Please paste a job description before analyzing.");
      return;
    }

    setIsLoading(true);
    setError(null);
    setLoadingStep("Running the deterministic skill analysis...");

    try {
      const res = await analyzeJob({
        job_description: jobDescription,
        candidate_skills: compareEnabled && candidateSkills.trim() ? candidateSkills : undefined,
      });

      setReport(res);
      scrollToResults();
    } catch (err: unknown) {
      if (err instanceof ApiError) {
        setError(err.message);
      } else {
        setError("An unexpected error occurred during analysis.");
      }
    } finally {
      setIsLoading(false);
      setLoadingStep("");
    }
  };

  const handleDownloadJson = () => {
    if (!report) return;
    const blob = new Blob([JSON.stringify(report, null, 2)], { type: "application/json" });
    downloadBlob(blob, `job_skill_analysis_${Date.now()}.json`);
  };

  const handleDownloadHtml = async () => {
    if (!report) return;
    try {
      const htmlText = await fetchHtmlReport({
        job_description: jobDescription,
        candidate_skills: compareEnabled && candidateSkills.trim() ? candidateSkills : undefined,
      });
      const blob = new Blob([htmlText], { type: "text/html;charset=utf-8" });
      downloadBlob(blob, `job_skill_report_${Date.now()}.html`);
    } catch {
      setError("Failed to export HTML report.");
    }
  };

  const handleReset = () => {
    setReport(null);
    setJobDescription("");
    setCandidateSkills("");
    setCompareEnabled(true);
    setError(null);
    scrollToWorkspace();
  };

  return (
    <div className="min-h-screen bg-navy text-cream flex flex-col font-sans selection:bg-orange-burnt selection:text-cream">
      <Navbar
        backendConnected={backendConnected}
        onLoadSample={handleLoadSample}
        onScrollToWorkspace={scrollToWorkspace}
      />

      <main className="flex-1">
        <Hero onStartAnalysis={scrollToWorkspace} onLoadSample={handleLoadSample} />

        <AnalyzerWorkspace
          jobDescription={jobDescription}
          setJobDescription={setJobDescription}
          candidateSkills={candidateSkills}
          setCandidateSkills={setCandidateSkills}
          compareEnabled={compareEnabled}
          setCompareEnabled={setCompareEnabled}
          onAnalyze={handleAnalyze}
          onLoadSample={handleLoadSample}
          isLoading={isLoading}
          loadingStep={loadingStep}
          error={error}
          onClearError={() => setError(null)}
        />

        {report && (
          <ResultsDashboard
            report={report}
            onReset={handleReset}
            onDownloadHtml={handleDownloadHtml}
            onDownloadJson={handleDownloadJson}
          />
        )}
      </main>

      <Footer />
    </div>
  );
};

export default App;
