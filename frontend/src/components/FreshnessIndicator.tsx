import type { SourceFreshness } from '../types';

const STATUS_COLORS: Record<string, string> = {
  LIVE: 'bg-green-500',
  CACHED: 'bg-yellow-500',
  STALE: 'bg-orange-500',
  UNAVAILABLE: 'bg-red-500',
};

const STATUS_LABELS: Record<string, string> = {
  LIVE: '실시간',
  CACHED: '캐시',
  STALE: '오래됨',
  UNAVAILABLE: '사용불가',
};

const SOURCE_LABELS: Record<string, string> = {
  terminal_congestion: '터미널 혼잡도',
  terminal_operation: '터미널 운영',
  gate_entry: '게이트 진입',
  traffic: '교통',
};

export function FreshnessIndicator({ items }: { items: SourceFreshness[] }) {
  return (
    <div className="flex flex-wrap gap-3">
      {items.map((s) => (
        <div key={s.source_name} className="flex items-center gap-1.5 text-sm text-slate-600">
          <span className={`inline-block w-2 h-2 rounded-full ${STATUS_COLORS[s.status] ?? 'bg-gray-400'}`} />
          <span>{SOURCE_LABELS[s.source_name] ?? s.source_name.replace(/_/g, ' ')}</span>
          <span className="text-xs text-slate-400">({STATUS_LABELS[s.status] ?? s.status})</span>
        </div>
      ))}
    </div>
  );
}
