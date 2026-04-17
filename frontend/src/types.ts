export interface DispatchJobInput {
  origin_zone_id: string;
  terminal_code: string;
  cut_off_at: string;
  conservative_mode: boolean;
  manual_buffer_minutes: number | null;
}

export interface SimulationInput {
  origin_zone_id: string;
  terminal_code: string;
  cut_off_at: string;
  scenario_offsets_minutes: number[];
}

export interface ReasonItem {
  code: string;
  label: string;
  contribution_percent: number;
  impact_minutes: number;
  direction: string;
  summary: string;
}

export interface SourceFreshness {
  source_name: string;
  observed_at: string | null;
  status: 'LIVE' | 'CACHED' | 'STALE' | 'UNAVAILABLE';
  freshness_seconds: number | null;
}

export interface Warning {
  code: string;
  message: string;
  affected_source: string | null;
}

export interface DispatchRiskResult {
  evaluation_id: string;
  result_status: 'FULL' | 'DEGRADED' | 'FAILED';
  risk_score: number;
  risk_level: 'LOW' | 'MEDIUM' | 'HIGH';
  on_time_probability: number;
  latest_safe_dispatch_at: string | null;
  estimated_total_minutes: number;
  verdict: string;
  reason_items: ReasonItem[];
  source_freshness: SourceFreshness[];
  warnings: Warning[];
  engine_version: string;
  evaluated_at: string;
}

export interface ScenarioResult {
  offset_minutes: number;
  dispatch_at: string;
  risk_score: number;
  risk_level: 'LOW' | 'MEDIUM' | 'HIGH';
  on_time_probability: number;
  latest_safe_dispatch_at: string | null;
  verdict: string;
}

export interface SimulationResult {
  base_scenario: ScenarioResult;
  scenarios: ScenarioResult[];
  source_freshness: SourceFreshness[];
  warnings: Warning[];
  engine_version: string;
  evaluated_at: string;
}

export interface TerminalInfo {
  terminal_code: string;
  terminal_name: string;
  is_active: boolean;
}

export const ORIGIN_ZONES = [
  { id: 'SONGDO', label: 'Songdo' },
  { id: 'NAMDONG', label: 'Namdong' },
  { id: 'SEOGU', label: 'Seo-gu' },
  { id: 'YEONSU', label: 'Yeonsu' },
  { id: 'BUPYEONG', label: 'Bupyeong' },
  { id: 'SIHEUNG', label: 'Siheung' },
  { id: 'ANSAN', label: 'Ansan' },
] as const;

export const TERMINALS = [
  { code: 'ICT', name: 'Incheon Container Terminal' },
  { code: 'E1', name: 'E1 Container Terminal' },
  { code: 'SNCT', name: 'Sun Kwang New Container Terminal' },
  { code: 'HJIT', name: 'Hanjin Incheon Terminal' },
  { code: 'SGT', name: 'Sungmin Terminal' },
] as const;
