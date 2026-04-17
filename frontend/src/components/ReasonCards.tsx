import type { ReasonItem } from '../types';

const CODE_ICONS: Record<string, string> = {
  TRAFFIC: '🚗',
  TERMINAL_CONGESTION: '🏗️',
  GATE_FLOW: '🚧',
  BUFFER: '🛡️',
};

export function ReasonCards({ reasons }: { reasons: ReasonItem[] }) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
      {reasons.map((r) => (
        <div key={r.code} className="bg-slate-50 rounded-lg p-4 border border-slate-200">
          <div className="flex items-center justify-between mb-1">
            <span className="font-medium text-slate-800">{CODE_ICONS[r.code] ?? '📌'} {r.label}</span>
            <span className="text-sm text-blue-600 font-semibold">+{r.impact_minutes.toFixed(0)}분</span>
          </div>
          <p className="text-sm text-slate-500">{r.summary}</p>
          <div className="mt-2 w-full bg-slate-200 rounded-full h-2">
            <div
              className="bg-blue-500 h-2 rounded-full transition-all"
              style={{ width: `${r.contribution_percent}%` }}
            />
          </div>
          <span className="text-xs text-slate-400 mt-1 inline-block">기여도 {r.contribution_percent}%</span>
        </div>
      ))}
    </div>
  );
}
