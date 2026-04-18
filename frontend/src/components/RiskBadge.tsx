const LEVEL_LABELS: Record<string, string> = {
  LOW: '🟢 낮음',
  MEDIUM: '🟠 보통',
  HIGH: '🔴 높음',
};

export function RiskBadge({ level }: { level: 'LOW' | 'MEDIUM' | 'HIGH' }) {
  const styles: Record<string, string> = {
    LOW: 'border-green-300 bg-green-50 text-green-800 shadow-green-500/10',
    MEDIUM: 'border-yellow-300 bg-yellow-50 text-yellow-800 shadow-yellow-500/10',
    HIGH: 'border-red-300 bg-red-50 text-red-800 shadow-red-500/20 risk-badge-pulse',
  };

  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full border px-3.5 py-1.5 text-sm font-semibold shadow-sm transition-transform duration-200 ${styles[level]}`}
    >
      {LEVEL_LABELS[level] ?? level}
    </span>
  );
}
