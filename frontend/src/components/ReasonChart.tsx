import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import type { ReasonItem } from '../types';

const COLORS = ['#3b82f6', '#0ea5e9', '#6366f1', '#8b5cf6'];

export function ReasonChart({ reasons }: { reasons: ReasonItem[] }) {
  const data = reasons.map((r) => ({
    name: r.label,
    percent: r.contribution_percent,
    minutes: r.impact_minutes,
  }));

  return (
    <div className="w-full h-64">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} layout="vertical" margin={{ left: 20, right: 20 }}>
          <XAxis type="number" domain={[0, 100]} tickFormatter={(v) => `${v}%`} />
          <YAxis type="category" dataKey="name" width={130} tick={{ fontSize: 13 }} />
          <Tooltip formatter={(value) => `${value}%`} />
          <Bar dataKey="percent" radius={[0, 6, 6, 0]}>
            {data.map((_, i) => (
              <Cell key={i} fill={COLORS[i % COLORS.length]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
