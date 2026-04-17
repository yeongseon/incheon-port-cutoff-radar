const LEVEL_LABELS: Record<string, string> = {
  LOW: '✅ 낮음',
  MEDIUM: '⚠️ 보통',
  HIGH: '🔴 높음',
};

export function RiskBadge({ level }: { level: 'LOW' | 'MEDIUM' | 'HIGH' }) {
  const styles: Record<string, string> = {
    LOW: 'bg-green-100 text-green-800 border-green-300',
    MEDIUM: 'bg-yellow-100 text-yellow-800 border-yellow-300',
    HIGH: 'bg-red-100 text-red-800 border-red-300',
  };

  return (
    <span className={`inline-block px-3 py-1 rounded-full text-sm font-semibold border ${styles[level]}`}>
      {LEVEL_LABELS[level] ?? level}
    </span>
  );
}
