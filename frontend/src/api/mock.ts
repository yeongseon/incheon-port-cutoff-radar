import type {
  DispatchJobInput,
  DispatchRiskResult,
  SimulationInput,
  SimulationResult,
  ScenarioResult,
  ReasonItem,
  SourceFreshness,
} from '../types';

function randomBetween(min: number, max: number): number {
  return Math.round((Math.random() * (max - min) + min) * 100) / 100;
}

function buildMockReasons(): ReasonItem[] {
  const travel = randomBetween(15, 50);
  const terminal = randomBetween(5, 40);
  const gate = randomBetween(3, 25);
  const buffer = randomBetween(10, 30);
  const total = travel + terminal + gate + buffer;

  return [
    {
      code: 'TRAFFIC',
      label: '도로 교통',
      contribution_percent: Math.round((travel / total) * 100),
      impact_minutes: travel,
      direction: 'increase',
      summary: `현재 교통 상황 기준 도로 이동시간 약 ${travel.toFixed(0)}분 소요 예상.`,
    },
    {
      code: 'TERMINAL_CONGESTION',
      label: '터미널 혼잡',
      contribution_percent: Math.round((terminal / total) * 100),
      impact_minutes: terminal,
      direction: 'increase',
      summary: `현재 혼잡도 기준 터미널 대기시간 약 ${terminal.toFixed(0)}분 예상.`,
    },
    {
      code: 'GATE_FLOW',
      label: '게이트 진입',
      contribution_percent: Math.round((gate / total) * 100),
      impact_minutes: gate,
      direction: 'increase',
      summary: `대기 차량 수 기준 게이트 진입 지연 약 ${gate.toFixed(0)}분 예상.`,
    },
    {
      code: 'BUFFER',
      label: '안전 버퍼',
      contribution_percent: Math.round((buffer / total) * 100),
      impact_minutes: buffer,
      direction: 'increase',
      summary: `운영 불확실성 대비 안전 버퍼 ${buffer.toFixed(0)}분 적용.`,
    },
  ];
}

function buildMockFreshness(): SourceFreshness[] {
  const now = new Date().toISOString();
  return [
    { source_name: 'terminal_congestion', observed_at: now, status: 'LIVE', freshness_seconds: 30 },
    { source_name: 'terminal_operation', observed_at: now, status: 'LIVE', freshness_seconds: 45 },
    { source_name: 'gate_entry', observed_at: now, status: 'CACHED', freshness_seconds: 120 },
    { source_name: 'traffic', observed_at: now, status: 'LIVE', freshness_seconds: 60 },
  ];
}

function computeMockResult(input: DispatchJobInput, dispatchOffset: number = 0): {
  risk_score: number;
  risk_level: 'LOW' | 'MEDIUM' | 'HIGH';
  on_time_probability: number;
  estimated_total_minutes: number;
  latest_safe_dispatch_at: string;
  verdict: string;
  reason_items: ReasonItem[];
} {
  const reasons = buildMockReasons();
  const totalMinutes = reasons.reduce((sum, r) => sum + r.impact_minutes, 0);
  const cutoff = new Date(input.cut_off_at);
  const now = new Date();
  now.setMinutes(now.getMinutes() + dispatchOffset);
  const remainingMinutes = (cutoff.getTime() - now.getTime()) / 60000;
  const slack = remainingMinutes - totalMinutes;

  let risk_score: number;
  let on_time_probability: number;

  if (slack >= 90) { risk_score = 5; on_time_probability = 0.97; }
  else if (slack >= 60) { risk_score = 15; on_time_probability = 0.92; }
  else if (slack >= 45) { risk_score = 25; on_time_probability = 0.82; }
  else if (slack >= 30) { risk_score = 40; on_time_probability = 0.68; }
  else if (slack >= 15) { risk_score = 60; on_time_probability = 0.48; }
  else if (slack >= 5) { risk_score = 78; on_time_probability = 0.28; }
  else if (slack >= 0) { risk_score = 88; on_time_probability = 0.15; }
  else { risk_score = 98; on_time_probability = 0.05; }

  if (input.conservative_mode) {
    risk_score = Math.min(100, risk_score + 10);
    on_time_probability = Math.max(0, on_time_probability - 0.08);
  }

  const risk_level = risk_score <= 34 ? 'LOW' : risk_score <= 69 ? 'MEDIUM' : 'HIGH';
  const latestSafe = new Date(cutoff.getTime() - totalMinutes * 60000);

  let verdict: string;
  if (risk_score <= 34) verdict = '지금 출발해도 안전합니다.';
  else if (risk_score <= 69) verdict = '배차 가능하지만 여유가 부족합니다. 조기 출발을 권장합니다.';
  else verdict = 'Cut-off 초과 위험이 높습니다. 즉시 출발하거나 일정을 재조정하세요.';

  return {
    risk_score,
    risk_level,
    on_time_probability: Math.round(on_time_probability * 100) / 100,
    estimated_total_minutes: Math.round(totalMinutes),
    latest_safe_dispatch_at: latestSafe.toISOString(),
    verdict,
    reason_items: reasons,
  };
}

function delay(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

export async function evaluateRiskMock(input: DispatchJobInput): Promise<DispatchRiskResult> {
  await delay(400 + Math.random() * 600);
  const mock = computeMockResult(input);

  return {
    evaluation_id: crypto.randomUUID(),
    result_status: 'FULL',
    risk_score: mock.risk_score,
    risk_level: mock.risk_level,
    on_time_probability: mock.on_time_probability,
    latest_safe_dispatch_at: mock.latest_safe_dispatch_at,
    estimated_total_minutes: mock.estimated_total_minutes,
    verdict: mock.verdict,
    reason_items: mock.reason_items,
    source_freshness: buildMockFreshness(),
    warnings: [],
    engine_version: 'v1.0.0-demo',
    evaluated_at: new Date().toISOString(),
  };
}

export async function simulateRiskMock(input: SimulationInput): Promise<SimulationResult> {
  await delay(300 + Math.random() * 500);

  const jobInput: DispatchJobInput = {
    origin_zone_id: input.origin_zone_id,
    terminal_code: input.terminal_code,
    cut_off_at: input.cut_off_at,
    conservative_mode: false,
    manual_buffer_minutes: null,
  };

  const scenarios: ScenarioResult[] = input.scenario_offsets_minutes.map((offset) => {
    const mock = computeMockResult(jobInput, offset);
    const dispatchAt = new Date();
    dispatchAt.setMinutes(dispatchAt.getMinutes() + offset);

    return {
      offset_minutes: offset,
      dispatch_at: dispatchAt.toISOString(),
      risk_score: mock.risk_score,
      risk_level: mock.risk_level,
      on_time_probability: mock.on_time_probability,
      latest_safe_dispatch_at: mock.latest_safe_dispatch_at,
      verdict: mock.verdict,
    };
  });

  const baseScenario = scenarios.find((s) => s.offset_minutes === 0) ?? scenarios[0];

  return {
    base_scenario: baseScenario,
    scenarios,
    source_freshness: buildMockFreshness(),
    warnings: [],
    engine_version: 'v1.0.0-demo',
    evaluated_at: new Date().toISOString(),
  };
}
