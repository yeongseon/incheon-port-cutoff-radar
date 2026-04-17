import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { evaluateRisk } from '../api/client';
import { ORIGIN_ZONES, TERMINALS } from '../types';
import type { DispatchJobInput } from '../types';

function getDefaultCutoff(): string {
  const d = new Date();
  d.setHours(d.getHours() + 4);
  d.setMinutes(0, 0, 0);
  return d.toISOString().slice(0, 16);
}

export function InputPage() {
  const navigate = useNavigate();
  const [origin, setOrigin] = useState<string>(ORIGIN_ZONES[0].id);
  const [terminal, setTerminal] = useState<string>(TERMINALS[0].code);
  const [cutoff, setCutoff] = useState(getDefaultCutoff);
  const [conservative, setConservative] = useState(false);
  const [buffer, setBuffer] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const input: DispatchJobInput = {
      origin_zone_id: origin,
      terminal_code: terminal,
      cut_off_at: new Date(cutoff).toISOString(),
      conservative_mode: conservative,
      manual_buffer_minutes: buffer ? parseInt(buffer, 10) : null,
    };

    try {
      const result = await evaluateRisk(input);
      navigate('/result', { state: { result, input } });
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : '평가에 실패했습니다';
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="w-full max-w-lg">
        <div className="text-center mb-8">
          <div className="inline-flex items-center gap-2 mb-4">
            <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
              <span className="text-white text-xl">⚓</span>
            </div>
            <h1 className="text-2xl font-bold text-slate-800">⚓ Cut-off 리스크 레이더</h1>
          </div>
          <p className="text-slate-500">🚢 인천항 — 반입 배차 리스크 평가</p>
          {import.meta.env.VITE_DEMO_MODE === 'true' && (
            <span className="inline-block mt-2 px-3 py-1 bg-amber-100 text-amber-800 text-xs font-medium rounded-full border border-amber-300">
              🧪 데모 모드 — 시뮬레이션 데이터 사용 중
            </span>
          )}
        </div>

        <form onSubmit={handleSubmit} className="bg-white rounded-2xl shadow-lg p-6 space-y-5">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">📍 출발 지역</label>
            <select
              value={origin}
              onChange={(e) => setOrigin(e.target.value)}
              className="w-full border border-slate-300 rounded-lg px-3 py-2.5 text-slate-800 bg-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
            >
              {ORIGIN_ZONES.map((z) => (
                <option key={z.id} value={z.id}>{z.label} ({z.id})</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">🏗️ 도착 터미널</label>
            <select
              value={terminal}
              onChange={(e) => setTerminal(e.target.value)}
              className="w-full border border-slate-300 rounded-lg px-3 py-2.5 text-slate-800 bg-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
            >
              {TERMINALS.map((t) => (
                <option key={t.code} value={t.code}>{t.name} ({t.code})</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">⏰ Cut-off 시간</label>
            <input
              type="datetime-local"
              value={cutoff}
              onChange={(e) => setCutoff(e.target.value)}
              className="w-full border border-slate-300 rounded-lg px-3 py-2.5 text-slate-800 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
              required
            />
          </div>

          <div className="flex items-center justify-between">
            <label className="text-sm font-medium text-slate-700">🛡️ 보수적 모드</label>
            <button
              type="button"
              onClick={() => setConservative(!conservative)}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                conservative ? 'bg-blue-600' : 'bg-slate-300'
              }`}
            >
              <span
                className={`inline-block h-4 w-4 rounded-full bg-white transition-transform ${
                  conservative ? 'translate-x-6' : 'translate-x-1'
                }`}
              />
            </button>
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">
              ⏱️ 수동 버퍼 (분, 선택사항)
            </label>
            <input
              type="number"
              min="0"
              max="120"
              value={buffer}
              onChange={(e) => setBuffer(e.target.value)}
              placeholder="자동"
              className="w-full border border-slate-300 rounded-lg px-3 py-2.5 text-slate-800 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
            />
          </div>

          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 rounded-lg px-4 py-3 text-sm">
              ❌ {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-300 text-white font-semibold rounded-lg py-3 transition-colors"
          >
            {loading ? '⏳ 평가 중...' : '🔍 리스크 평가'}
          </button>
        </form>
      </div>
    </div>
  );
}
