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
  { id: 'SONGDO', label: '송도' },
  { id: 'NAMDONG', label: '남동' },
  { id: 'SEOGU', label: '서구' },
  { id: 'YEONSU', label: '연수' },
  { id: 'BUPYEONG', label: '부평' },
  { id: 'SIHEUNG', label: '시흥' },
  { id: 'ANSAN', label: '안산' },
] as const;

export const TERMINALS = [
  { code: 'ICT', name: '인천컨테이너터미널' },
  { code: 'E1', name: 'E1컨테이너터미널' },
  { code: 'SNCT', name: '선광신컨테이너터미널' },
  { code: 'HJIT', name: '한진인천터미널' },
  { code: 'SGT', name: '성민터미널' },
] as const;
