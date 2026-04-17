import type { SourceFreshness } from '../types';

const STATUS_COLORS: Record<string, string> = {
  LIVE: 'bg-green-500',
  CACHED: 'bg-yellow-500',
  STALE: 'bg-orange-500',
  UNAVAILABLE: 'bg-red-500',
};

export function FreshnessIndicator({ items }: { items: SourceFreshness[] }) {
  return (
    <div className="flex flex-wrap gap-3">
      {items.map((s) => (
        <div key={s.source_name} className="flex items-center gap-1.5 text-sm text-slate-600">
          <span className={`inline-block w-2 h-2 rounded-full ${STATUS_COLORS[s.status] ?? 'bg-gray-400'}`} />
          <span>{s.source_name.replace(/_/g, ' ')}</span>
          <span className="text-xs text-slate-400">({s.status})</span>
        </div>
      ))}
    </div>
  );
}
