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
      label: 'Road traffic',
      contribution_percent: Math.round((travel / total) * 100),
      impact_minutes: travel,
      direction: 'increase',
      summary: `Road travel time estimated at ${travel.toFixed(0)} min based on current traffic conditions.`,
    },
    {
      code: 'TERMINAL_CONGESTION',
      label: 'Terminal congestion',
      contribution_percent: Math.round((terminal / total) * 100),
      impact_minutes: terminal,
      direction: 'increase',
      summary: `Terminal wait time estimated at ${terminal.toFixed(0)} min due to current congestion level.`,
    },
    {
      code: 'GATE_FLOW',
      label: 'Gate entry flow',
      contribution_percent: Math.round((gate / total) * 100),
      impact_minutes: gate,
      direction: 'increase',
      summary: `Gate entry adjustment adds ${gate.toFixed(0)} min based on vehicle queue.`,
    },
    {
      code: 'BUFFER',
      label: 'Safety buffer',
      contribution_percent: Math.round((buffer / total) * 100),
      impact_minutes: buffer,
      direction: 'increase',
      summary: `Safety buffer of ${buffer.toFixed(0)} min applied for operational uncertainty.`,
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
  if (risk_score <= 34) verdict = 'Safe to dispatch now.';
  else if (risk_score <= 69) verdict = 'Dispatch is possible but tight. Consider dispatching earlier.';
  else verdict = 'High risk of missing cut-off. Dispatch immediately or reschedule.';

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
