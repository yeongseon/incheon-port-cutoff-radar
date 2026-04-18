import type { ReasonItem } from '../types';

const CODE_ICONS: Record<string, string> = {
  TRAFFIC: '교통',
  TERMINAL_CONGESTION: '터미널',
  GATE_FLOW: '게이트',
  BUFFER: '버퍼',
};

export function ReasonCards({ reasons }: { reasons: ReasonItem[] }) {
  return (
    <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
      {reasons.map((r) => (
        <div
          key={r.code}
          className="group rounded-2xl border border-slate-200 bg-white/90 p-4 shadow-sm transition-all duration-300 hover:-translate-y-1 hover:border-blue-300 hover:shadow-xl hover:shadow-blue-950/5"
        >
          <div className="mb-1 flex items-center justify-between gap-3">
            <span className="font-medium text-slate-800">{CODE_ICONS[r.code] ?? '항목'} {r.label}</span>
            <span className="text-sm text-blue-600 font-semibold">+{r.impact_minutes.toFixed(0)}분</span>
          </div>
          <p className="text-sm text-slate-500">{r.summary}</p>
          <div className="mt-3 h-2.5 w-full overflow-hidden rounded-full bg-slate-200">
            <div
              className="h-2.5 rounded-full bg-linear-to-r from-blue-500 via-sky-500 to-cyan-400 transition-all duration-500"
              style={{ width: `${r.contribution_percent}%` }}
            />
          </div>
          <span className="mt-2 inline-block text-xs text-slate-400">기여도 {r.contribution_percent}%</span>
        </div>
      ))}
    </div>
  );
}
