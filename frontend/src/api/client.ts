import axios from 'axios';
import type { DispatchJobInput, DispatchRiskResult, SimulationInput, SimulationResult, TerminalInfo } from '../types';
import { TERMINALS } from '../types';
import { evaluateRiskMock, simulateRiskMock } from './mock';

const IS_DEMO = import.meta.env.VITE_DEMO_MODE === 'true' || import.meta.env.MODE === 'demo';

const api = axios.create({
  baseURL: '/api/v1',
  headers: { 'Content-Type': 'application/json' },
});

export async function evaluateRisk(input: DispatchJobInput): Promise<DispatchRiskResult> {
  if (IS_DEMO) return evaluateRiskMock(input);
  const { data } = await api.post<DispatchRiskResult>('/risk/evaluate', input);
  return data;
}

export async function simulateRisk(input: SimulationInput): Promise<SimulationResult> {
  if (IS_DEMO) return simulateRiskMock(input);
  const { data } = await api.post<SimulationResult>('/risk/simulate', input);
  return data;
}

export async function getTerminals(): Promise<TerminalInfo[]> {
  if (IS_DEMO) {
    return TERMINALS.map((t) => ({
      terminal_code: t.code,
      terminal_name: t.name,
      is_active: true,
    }));
  }
  const { data } = await api.get<TerminalInfo[]>('/terminals');
  return data;
}

export async function healthCheck(): Promise<{ status: string }> {
  if (IS_DEMO) return { status: 'demo' };
  const { data } = await api.get('/health');
  return data;
}
