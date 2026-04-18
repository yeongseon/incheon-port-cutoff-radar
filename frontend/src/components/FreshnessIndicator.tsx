import type { SourceFreshness } from '../types';

const STATUS_COLORS: Record<string, string> = {
  LIVE: 'bg-green-500',
  CACHED: 'bg-yellow-500',
  STALE: 'bg-orange-500',
  UNAVAILABLE: 'bg-red-500',
};

const STATUS_LABELS: Record<string, string> = {
  LIVE: '🟢 실시간',
  CACHED: '🟡 캐시',
  STALE: '🟠 오래됨',
  UNAVAILABLE: '🔴 사용불가',
};

const SOURCE_LABELS: Record<string, string> = {
  terminal_congestion: '🏗️ 터미널 혼잡도',
  terminal_operation: '⚙️ 터미널 운영',
  gate_entry: '🚧 게이트 진입',
  traffic: '🚗 교통',
};

export function FreshnessIndicator({ items }: { items: SourceFreshness[] }) {
  return (
    <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 xl:grid-cols-4">
      {items.map((s) => (
        <div
          key={s.source_name}
          className="rounded-2xl border border-slate-200 bg-white px-4 py-3 shadow-sm transition-all duration-300 hover:-translate-y-0.5 hover:border-blue-200 hover:shadow-lg hover:shadow-blue-950/5"
        >
          <div className="flex items-start justify-between gap-3">
            <div>
              <p className="text-sm font-semibold text-slate-800">{SOURCE_LABELS[s.source_name] ?? s.source_name.replace(/_/g, ' ')}</p>
              <p className="mt-1 text-xs text-slate-400">{STATUS_LABELS[s.status] ?? s.status}</p>
            </div>
            <span
              className={`inline-block h-3 w-3 rounded-full ${STATUS_COLORS[s.status] ?? 'bg-gray-400'} ${s.status === 'LIVE' ? 'status-live-pulse' : ''}`}
            />
          </div>
        </div>
      ))}
    </div>
  );
}
