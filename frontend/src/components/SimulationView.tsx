import { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { simulateRisk } from '../api/client';
import type { SimulationResult, DispatchJobInput } from '../types';
import { RiskBadge } from './RiskBadge';

interface Props {
  jobInput: DispatchJobInput;
}

export function SimulationView({ jobInput }: Props) {
  const [result, setResult] = useState<SimulationResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    setError(null);
    simulateRisk({
      origin_zone_id: jobInput.origin_zone_id,
      terminal_code: jobInput.terminal_code,
      cut_off_at: jobInput.cut_off_at,
      scenario_offsets_minutes: [0, -15, -30, -60],
    })
      .then(setResult)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [jobInput]);

  if (loading) {
    return (
      <div className="space-y-4 animate-fade-in">
        <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
          <div className="simulation-skeleton h-56 rounded-xl" />
        </div>
        <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
          <div className="space-y-3 p-4">
            {[1, 2, 3, 4].map((row) => (
              <div key={row} className="grid grid-cols-5 gap-3">
                {Array.from({ length: 5 }).map((_, cell) => (
                  <div key={cell} className="simulation-skeleton h-10 rounded-lg" />
                ))}
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }
  if (error) return <div className="text-center py-8 text-red-500">❌ 시뮬레이션 실패: {error}</div>;
  if (!result) return null;

  const chartData = result.scenarios.map((s) => ({
    label: s.offset_minutes === 0 ? '현재' : `${s.offset_minutes}분`,
    '🎯 정시 확률': Math.round(s.on_time_probability * 100),
    '📊 리스크': s.risk_score,
  }));

  return (
    <div className="space-y-4">
      <div className="h-56 w-full overflow-hidden rounded-2xl border border-slate-200 bg-white p-3 shadow-sm">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData}>
            <XAxis dataKey="label" />
            <YAxis domain={[0, 100]} />
            <Tooltip />
            <Legend />
            <Bar dataKey="🎯 정시 확률" fill="#3b82f6" radius={[4, 4, 0, 0]} />
            <Bar dataKey="📊 리스크" fill="#ef4444" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="overflow-x-auto rounded-2xl border border-slate-200 bg-white shadow-sm">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-slate-200 bg-slate-50/80 text-left text-slate-500">
              <th className="px-4 py-3">🕐 출발 시점</th>
              <th className="px-4 py-3">🎯 정시 확률</th>
              <th className="px-4 py-3">📊 리스크</th>
              <th className="px-4 py-3">🏷️ 등급</th>
              <th className="px-4 py-3">📋 판단</th>
            </tr>
          </thead>
          <tbody>
            {result.scenarios.map((s, index) => (
              <tr
                key={s.offset_minutes}
                className={`border-b border-slate-100 transition-colors hover:bg-blue-50/60 ${index % 2 === 0 ? 'bg-white' : 'bg-slate-50/50'}`}
              >
                <td className="px-4 py-3 font-medium">
                  {s.offset_minutes === 0 ? '현재' : `${s.offset_minutes}분`}
                </td>
                <td className="px-4 py-3">{Math.round(s.on_time_probability * 100)}%</td>
                <td className="px-4 py-3">{s.risk_score}</td>
                <td className="px-4 py-3"><RiskBadge level={s.risk_level} /></td>
                <td className="px-4 py-3 text-slate-600">{s.verdict}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
