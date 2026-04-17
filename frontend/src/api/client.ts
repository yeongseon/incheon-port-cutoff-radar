import axios from 'axios';
import type { DispatchJobInput, DispatchRiskResult, SimulationInput, SimulationResult, TerminalInfo } from '../types';

const api = axios.create({
  baseURL: '/api/v1',
  headers: { 'Content-Type': 'application/json' },
});

export async function evaluateRisk(input: DispatchJobInput): Promise<DispatchRiskResult> {
  const { data } = await api.post<DispatchRiskResult>('/risk/evaluate', input);
  return data;
}

export async function simulateRisk(input: SimulationInput): Promise<SimulationResult> {
  const { data } = await api.post<SimulationResult>('/risk/simulate', input);
  return data;
}

export async function getTerminals(): Promise<TerminalInfo[]> {
  const { data } = await api.get<TerminalInfo[]>('/terminals');
  return data;
}

export async function healthCheck(): Promise<{ status: string }> {
  const { data } = await api.get('/health');
  return data;
}
