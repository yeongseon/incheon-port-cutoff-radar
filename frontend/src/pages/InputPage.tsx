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

  return (
    <div className="px-4 py-8 sm:px-6 lg:px-8">
      <div className="mx-auto grid w-full max-w-6xl gap-6 lg:grid-cols-[1.05fr_0.95fr] lg:items-start">
        <section className="animate-slide-up space-y-6">
          <div className="overflow-hidden rounded-[28px] border border-white/70 bg-white/80 p-6 shadow-xl shadow-slate-950/5 backdrop-blur-sm sm:p-8">
            <div className="inline-flex items-center gap-2 rounded-full border border-blue-200 bg-blue-50 px-3 py-1 text-xs font-semibold text-blue-700">
              반입 배차 리스크 평가
            </div>
            <h2 className="mt-4 text-3xl font-semibold tracking-tight text-slate-900 sm:text-4xl">
              Cut-off 마감 전에<br className="hidden sm:block" />
              가장 안전한 출발 시점을 빠르게 판단합니다.
            </h2>
            <p className="mt-4 max-w-2xl text-sm leading-7 text-slate-600 sm:text-base">
              교통, 터미널, 게이트, 버퍼 데이터를 종합해 인천항 반입 배차의 정시 도착 가능성과 최늦 출발 시각을 한 번에 제공합니다.
            </p>

            <div className="mt-6 grid grid-cols-2 gap-3">
              {[
                ['교', '교통', '실시간 이동 여건 반영'],
                ['터', '터미널', '혼잡도와 운영 상태 확인'],
                ['게', '게이트', '진입 흐름과 대기 편차 반영'],
                ['버', '버퍼', '보수적 여유시간 설정'],
              ].map(([icon, title, description]) => (
                <div
                  key={title}
                  className="rounded-2xl border border-slate-200/80 bg-linear-to-br from-white to-slate-50 p-4 shadow-sm transition-transform duration-300 hover:-translate-y-1"
                >
                  <div className="mb-3 flex h-10 w-10 items-center justify-center rounded-xl bg-blue-600/10 text-lg">{icon}</div>
                  <p className="text-sm font-semibold text-slate-800">{title}</p>
                  <p className="mt-1 text-xs leading-5 text-slate-500">{description}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        <form
          onSubmit={async (e) => {
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
          }}
          className="animate-fade-in rounded-[28px] border border-white/70 bg-white/90 p-6 shadow-xl shadow-slate-950/8 backdrop-blur-sm transition-all duration-300 hover:-translate-y-1 hover:shadow-2xl hover:shadow-blue-950/10 sm:p-7"
        >
          <div className="mb-6 flex items-start justify-between gap-4">
            <div>
              <p className="text-sm font-semibold text-blue-700">평가 입력</p>
              <h3 className="mt-1 text-2xl font-semibold text-slate-900">배차 조건 설정</h3>
              <p className="mt-2 text-sm text-slate-500">현재 조건을 기준으로 정시 도착 리스크를 분석합니다.</p>
            </div>
          </div>

          <div className="space-y-4">
            <div className="rounded-2xl border border-slate-200 border-l-4 border-l-blue-500 bg-white p-5 shadow-sm transition-all duration-300 hover:border-blue-200 hover:shadow-md">
              <label className="mb-2 block text-sm font-medium text-slate-700">출발 지역</label>
              <select
                value={origin}
                onChange={(e) => setOrigin(e.target.value)}
                className="w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-slate-800 outline-none transition-all duration-200 hover:border-blue-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
              >
                {ORIGIN_ZONES.map((z) => (
                  <option key={z.id} value={z.id}>{z.label} ({z.id})</option>
                ))}
              </select>
            </div>

            <div className="rounded-2xl border border-slate-200 border-l-4 border-l-sky-500 bg-white p-5 shadow-sm transition-all duration-300 hover:border-sky-200 hover:shadow-md">
              <label className="mb-2 block text-sm font-medium text-slate-700">도착 터미널</label>
              <select
                value={terminal}
                onChange={(e) => setTerminal(e.target.value)}
                className="w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-slate-800 outline-none transition-all duration-200 hover:border-sky-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
              >
                {TERMINALS.map((t) => (
                  <option key={t.code} value={t.code}>{t.name} ({t.code})</option>
                ))}
              </select>
            </div>

            <div className="rounded-2xl border border-slate-200 border-l-4 border-l-cyan-500 bg-white p-5 shadow-sm transition-all duration-300 hover:border-cyan-200 hover:shadow-md">
              <label className="mb-2 block text-sm font-medium text-slate-700">Cut-off 시간</label>
              <input
                type="datetime-local"
                value={cutoff}
                onChange={(e) => setCutoff(e.target.value)}
                className="w-full rounded-xl border border-slate-300 px-4 py-3 text-slate-800 outline-none transition-all duration-200 hover:border-cyan-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
                required
              />
            </div>

            <div className="rounded-2xl border border-slate-200 border-l-4 border-l-indigo-500 bg-white p-5 shadow-sm transition-all duration-300 hover:border-indigo-200 hover:shadow-md">
              <div className="flex items-center justify-between gap-4">
                <div>
                  <label className="text-sm font-medium text-slate-700">보수적 모드</label>
                  <p className="mt-1 text-xs text-slate-400">예상 편차를 더 넉넉하게 반영합니다.</p>
                </div>
                <button
                  type="button"
                  onClick={() => setConservative(!conservative)}
                  className={`relative inline-flex h-7 w-12 items-center rounded-full transition-all duration-300 ${
                    conservative ? 'bg-blue-600 shadow-lg shadow-blue-600/25' : 'bg-slate-300'
                  }`}
                >
                  <span
                    className={`inline-block h-5 w-5 rounded-full bg-white transition-transform duration-300 ${
                      conservative ? 'translate-x-6' : 'translate-x-1'
                    }`}
                  />
                </button>
              </div>
            </div>

            <div className="rounded-2xl border border-slate-200 border-l-4 border-l-blue-400 bg-white p-5 shadow-sm transition-all duration-300 hover:border-blue-200 hover:shadow-md">
              <label className="mb-2 block text-sm font-medium text-slate-700">
                수동 버퍼 (분, 선택사항)
              </label>
              <input
                type="number"
                min="0"
                max="120"
                value={buffer}
                onChange={(e) => setBuffer(e.target.value)}
                placeholder="자동"
                className="w-full rounded-xl border border-slate-300 px-4 py-3 text-slate-800 outline-none transition-all duration-200 hover:border-blue-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
              />
            </div>
          </div>

          {error && (
            <div className="mt-4 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700 animate-fade-in">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="mt-6 flex w-full items-center justify-center rounded-2xl bg-linear-to-r from-blue-600 to-blue-700 px-4 py-3.5 text-white shadow-lg shadow-blue-700/25 transition-all duration-200 hover:-translate-y-0.5 hover:shadow-xl hover:shadow-blue-700/30 active:scale-[0.985] disabled:translate-y-0 disabled:cursor-not-allowed disabled:from-blue-300 disabled:to-blue-400"
          >
            {loading ? (
              <span className="relative inline-flex items-center justify-center px-4 py-0.5 text-sm font-semibold sm:text-base">
                <span className="button-ring absolute inset-0 rounded-full border border-white/40" />
                <span className="relative">리스크 평가</span>
              </span>
            ) : (
              <span className="text-sm font-semibold sm:text-base">리스크 평가</span>
            )}
          </button>
        </form>
      </div>
    </div>
  );
}
