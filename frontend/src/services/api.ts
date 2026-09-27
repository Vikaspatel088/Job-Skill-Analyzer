import type { AnalysisReport, AnalyzePayload, SampleData } from "../types";

const API_BASE_URL = import.meta.env.VITE_API_URL || "";

export class ApiError extends Error {
  override message: string;
  status?: number;

  constructor(message: string, status?: number) {
    super(message);
    this.name = "ApiError";
    this.message = message;
    this.status = status;
  }
}

export async function analyzeJob(payload: AnalyzePayload): Promise<AnalysisReport> {
  try {
    const res = await fetch(`${API_BASE_URL}/api/analyze`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      let errorMsg = "Failed to analyze job description.";
      try {
        const errJson = await res.json();
        errorMsg = errJson.detail || errJson.message || errorMsg;
      } catch {
        // use default
      }
      throw new ApiError(errorMsg, res.status);
    }

    const json = await res.json();
    return json.data;
  } catch (err: unknown) {
    if (err instanceof ApiError) throw err;
    const msg = err instanceof Error ? err.message : "Network error connecting to backend.";
    throw new ApiError(`Service unreachable: ${msg}. Please ensure the backend is running.`);
  }
}

export async function fetchSample(): Promise<SampleData> {
  const res = await fetch(`${API_BASE_URL}/api/sample`);
  if (!res.ok) {
    throw new ApiError("Failed to fetch sample data.", res.status);
  }
  return res.json();
}

export async function checkHealth(): Promise<boolean> {
  try {
    const res = await fetch(`${API_BASE_URL}/api/health`, { method: "GET" });
    return res.ok;
  } catch {
    return false;
  }
}

export async function fetchHtmlReport(payload: AnalyzePayload): Promise<string> {
  const res = await fetch(`${API_BASE_URL}/api/report/html`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    throw new ApiError("Failed to generate HTML report.", res.status);
  }
  return res.text();
}
