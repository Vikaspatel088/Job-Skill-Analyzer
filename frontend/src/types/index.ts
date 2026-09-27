export type PriorityLevel = "High" | "Medium" | "Low";

export interface ExtractedSkill {
  name: string;
  category: string;
  matched_terms: string[];
  frequency: number;
}

export interface CandidateComparison {
  provided: boolean;
  candidate_skills: string[];
  matched_skills: string[];
  missing_skills: string[];
  match_percentage: number;
}

export interface PrioritizedSkill {
  skill: string;
  category: string;
  priority: PriorityLevel;
  reason: string;
  is_missing: boolean;
}

export interface AnalysisReport {
  total_skills: number;
  skills: ExtractedSkill[];
  category_counts: Record<string, number>;
  candidate_comparison: CandidateComparison;
  priorities: PrioritizedSkill[];
}

export interface AnalyzePayload {
  job_description: string;
  candidate_skills?: string | string[];
}

export interface SampleData {
  job_description: string;
  candidate_skills: string;
  role_title: string;
}
