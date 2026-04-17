import { useLocation, useNavigate } from 'react-router-dom';
import type { DispatchRiskResult, DispatchJobInput } from '../types';
import { RiskBadge } from '../components/RiskBadge';
import { ReasonChart } from '../components/ReasonChart';
import { ReasonCards } from '../components/ReasonCards';
import { SimulationView } from '../components/SimulationView';
import { FreshnessIndicator } from '../components/FreshnessIndicator';

function formatTime(iso: string | null): string {
  if (!iso) return '—';
  return new Date(iso).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: false });
}

function formatDateTime(iso: string | null): string {
  if (!iso) return '—';
  return new Date(iso).toLocaleString('en-US', {
    month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit', hour12: false,
  });
}

function probabilityColor(p: number): string {
  if (p >= 0.7) return 'text-green-600';
  if (p >= 0.4) return 'text-yellow-600';
  return 'text-red-600';
}

function riskScoreColor(s: number): string {
  if (s <= 34) return 'text-green-600';
  if (s <= 69) return 'text-yellow-600';
  return 'text-red-600';
}

export function ResultPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const state = location.state as { result: DispatchRiskResult; input: DispatchJobInput } | null;

  if (!state) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="text-slate-500 mb-4">No evaluation result found.</p>
          <button onClick={() => navigate('/')} className="text-blue-600 hover:underline">
            Go back to input
          </button>
        </div>
      </div>
    );
  }

  const { result, input } = state;

  return (
    <div className="min-h-screen bg-slate-50 py-8 px-4">
      <div className="max-w-3xl mx-auto space-y-6">
        <div className="flex items-center justify-between">
          <button onClick={() => navigate('/')} className="text-blue-600 hover:underline text-sm">
            ← New evaluation
          </button>
          <span className="text-xs text-slate-400">
            Engine {result.engine_version} · {formatDateTime(result.evaluated_at)}
          </span>
        </div>

        {result.result_status === 'FAILED' && (
          <div className="bg-red-50 border border-red-300 rounded-xl p-6 text-center">
            <p className="text-red-700 font-semibold text-lg">{result.verdict}</p>
          </div>
        )}

        {result.result_status !== 'FAILED' && (
          <>
            {result.result_status === 'DEGRADED' && (
              <div className="bg-yellow-50 border border-yellow-300 rounded-xl px-4 py-3">
                <p className="text-yellow-800 text-sm font-medium">⚠ Degraded result — some data sources are unavailable</p>
                {result.warnings.map((w, i) => (
                  <p key={i} className="text-yellow-700 text-xs mt-1">{w.message}</p>
                ))}
              </div>
            )}

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div className="bg-white rounded-xl shadow-sm p-6 text-center">
                <p className="text-sm text-slate-500 mb-1">On-time Probability</p>
                <p className={`text-4xl font-bold ${probabilityColor(result.on_time_probability)}`}>
                  {Math.round(result.on_time_probability * 100)}%
                </p>
              </div>

              <div className="bg-white rounded-xl shadow-sm p-6 text-center">
                <p className="text-sm text-slate-500 mb-1">Risk Score</p>
                <p className={`text-4xl font-bold ${riskScoreColor(result.risk_score)}`}>
                  {result.risk_score}
                </p>
                <div className="mt-2">
                  <RiskBadge level={result.risk_level} />
                </div>
              </div>

              <div className="bg-white rounded-xl shadow-sm p-6 text-center">
                <p className="text-sm text-slate-500 mb-1">Latest Safe Dispatch</p>
                <p className="text-3xl font-bold text-slate-800">
                  {formatTime(result.latest_safe_dispatch_at)}
                </p>
                <p className="text-xs text-slate-400 mt-1">
                  Total lead: {result.estimated_total_minutes} min
                </p>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-sm p-6">
              <p className="text-lg font-semibold text-slate-800 mb-1">Verdict</p>
              <p className="text-slate-600">{result.verdict}</p>
            </div>

            <div className="bg-white rounded-xl shadow-sm p-6">
              <p className="text-lg font-semibold text-slate-800 mb-4">Risk Factor Analysis</p>
              <ReasonChart reasons={result.reason_items} />
              <div className="mt-4">
                <ReasonCards reasons={result.reason_items} />
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-sm p-6">
              <p className="text-lg font-semibold text-slate-800 mb-4">Dispatch Time Simulation</p>
              <SimulationView jobInput={input} />
            </div>

            <div className="bg-white rounded-xl shadow-sm p-4">
              <p className="text-sm font-medium text-slate-600 mb-2">Data Freshness</p>
              <FreshnessIndicator items={result.source_freshness} />
            </div>
          </>
        )}
      </div>
    </div>
  );
}
