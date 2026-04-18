import { useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import type { DispatchRiskResult, DispatchJobInput } from '../types';
import { RiskBadge } from '../components/RiskBadge';
import { ReasonChart } from '../components/ReasonChart';
import { ReasonCards } from '../components/ReasonCards';
import { SimulationView } from '../components/SimulationView';
import { FreshnessIndicator } from '../components/FreshnessIndicator';

function formatTime(iso: string | null): string {
  if (!iso) return '—';
  return new Date(iso).toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit', hour12: false });
}

function formatDateTime(iso: string | null): string {
  if (!iso) return '—';
  return new Date(iso).toLocaleString('ko-KR', {
    month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit', hour12: false,
  });
}

function probabilityColor(p: number): string {
  if (p >= 0.7) return 'text-green-600';
  if (p >= 0.4) return 'text-yellow-600';
  return 'text-red-600';
}

function riskScoreColor(s: number): string {
  if (s <= 34) return 'text-green-600';
  if (s <= 69) return 'text-yellow-600';
  return 'text-red-600';
}

function riskAccent(level: 'LOW' | 'MEDIUM' | 'HIGH'): string {
  if (level === 'LOW') return 'border-l-green-500';
  if (level === 'MEDIUM') return 'border-l-yellow-500';
  return 'border-l-red-500';
}

function probabilityTone(probability: number): string {
  if (probability >= 0.7) return 'border-green-200 bg-linear-to-br from-green-50 to-white';
  if (probability >= 0.4) return 'border-yellow-200 bg-linear-to-br from-yellow-50 to-white';
  return 'border-red-200 bg-linear-to-br from-red-50 to-white';
}

function probabilityAccent(probability: number): string {
  if (probability >= 0.7) return 'bg-green-500';
  if (probability >= 0.4) return 'bg-yellow-500';
  return 'bg-red-500';
}

function riskTone(level: 'LOW' | 'MEDIUM' | 'HIGH'): string {
  if (level === 'LOW') return 'border-green-200 bg-linear-to-br from-green-50 to-white';
  if (level === 'MEDIUM') return 'border-yellow-200 bg-linear-to-br from-yellow-50 to-white';
  return 'border-red-200 bg-linear-to-br from-red-50 to-white';
}

function riskAccentBar(level: 'LOW' | 'MEDIUM' | 'HIGH'): string {
  if (level === 'LOW') return 'bg-green-500';
  if (level === 'MEDIUM') return 'bg-yellow-500';
  return 'bg-red-500';
}

function sectionHeading(icon: string, title: string) {
  return (
    <div className="mb-5 flex items-center gap-3">
      <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-blue-50 text-lg text-blue-700">{icon}</span>
      <div className="flex-1">
        <p className="text-base font-semibold text-slate-900">{title}</p>
        <div className="mt-2 h-px w-full bg-linear-to-r from-blue-200 via-slate-200 to-transparent" />
      </div>
    </div>
  );
}

export function ResultPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const state = location.state as { result: DispatchRiskResult; input: DispatchJobInput } | null;

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, []);

  if (!state) {
    return (
      <div className="flex min-h-[calc(100vh-12rem)] items-center justify-center px-4 py-12">
        <div className="rounded-3xl border border-slate-200 bg-white/90 p-10 text-center shadow-xl shadow-slate-950/5">
          <p className="text-slate-500 mb-4">📭 평가 결과가 없습니다.</p>
          <button onClick={() => navigate('/')} className="text-blue-600 hover:underline">
            ← 입력 화면으로 돌아가기
          </button>
        </div>
      </div>
    );
  }

  const { result, input } = state;

  return (
    <div className="px-4 py-8 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-5xl space-y-6 animate-fade-in">
        <div className="flex flex-col gap-3 rounded-2xl border border-white/70 bg-white/85 px-5 py-4 shadow-lg shadow-slate-950/5 backdrop-blur-sm sm:flex-row sm:items-center sm:justify-between">
          <div className="flex items-center gap-2 text-sm text-slate-500">
            <button onClick={() => navigate('/')} className="font-medium text-blue-600 transition-colors hover:text-blue-700 hover:underline">
              홈
            </button>
            <span className="text-slate-300">&gt;</span>
            <span className="font-medium text-slate-700">리스크 평가 결과</span>
          </div>
          <div className="flex items-center justify-between gap-3 sm:justify-end">
            <button onClick={() => navigate('/')} className="text-sm font-medium text-blue-600 transition-colors hover:text-blue-700 hover:underline">
              ← 새로운 평가
            </button>
            <span className="text-xs text-slate-400">
            🔧 엔진 {result.engine_version} · {formatDateTime(result.evaluated_at)}
          </span>
          </div>
        </div>

        {result.result_status === 'FAILED' && (
          <div className="rounded-3xl border border-red-300 bg-red-50 p-6 text-center shadow-sm">
            <p className="text-red-700 font-semibold text-lg">🚫 {result.verdict}</p>
          </div>
        )}

        {result.result_status !== 'FAILED' && (
          <>
            {result.result_status === 'DEGRADED' && (
              <div className="rounded-2xl border border-yellow-300 bg-yellow-50 px-4 py-3 shadow-sm">
                <p className="text-yellow-800 text-sm font-medium">⚠️ 부분 결과 — 일부 데이터 소스를 사용할 수 없습니다</p>
                {result.warnings.map((w, i) => (
                  <p key={i} className="text-yellow-700 text-xs mt-1">{w.message}</p>
                ))}
              </div>
            )}

            <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
              <div className={`rounded-3xl border p-6 text-center shadow-sm shadow-slate-900/5 ${probabilityTone(result.on_time_probability)}`}>
                <div className={`-mx-6 -mt-6 mb-5 h-1 rounded-t-3xl ${probabilityAccent(result.on_time_probability)}`} />
                <p className="mb-2 text-sm text-slate-500">🎯 정시 도착 확률</p>
                <p className={`text-5xl font-semibold tracking-tight ${probabilityColor(result.on_time_probability)}`}>
                  {Math.round(result.on_time_probability * 100)}%
                </p>
                <p className="mt-2 text-xs text-slate-400">예상 데이터 기반 도착 성공 확률</p>
              </div>

              <div className={`rounded-3xl border p-6 text-center shadow-sm shadow-slate-900/5 ${riskTone(result.risk_level)}`}>
                <div className={`-mx-6 -mt-6 mb-5 h-1 rounded-t-3xl ${riskAccentBar(result.risk_level)}`} />
                <p className="mb-2 text-sm text-slate-500">📊 리스크 점수</p>
                <p className={`text-5xl font-semibold tracking-tight ${riskScoreColor(result.risk_score)}`}>
                  {result.risk_score}
                </p>
                <div className="mt-3 flex justify-center">
                  <RiskBadge level={result.risk_level} />
                </div>
              </div>

              <div className="rounded-3xl border border-sky-200 bg-linear-to-br from-sky-50 to-white p-6 text-center shadow-sm shadow-sky-900/5">
                <div className="-mx-6 -mt-6 mb-5 h-1 rounded-t-3xl bg-sky-500" />
                <p className="mb-2 text-sm text-slate-500">🕐 최늦 출발 시각</p>
                <p className="text-4xl font-semibold tracking-tight text-slate-800">
                  {formatTime(result.latest_safe_dispatch_at)}
                </p>
                <p className="mt-2 text-xs text-slate-400">
                  ⏱️ 총 소요시간: {result.estimated_total_minutes}분
                </p>
              </div>
            </div>

            <div className={`rounded-3xl border border-slate-200 border-l-4 bg-white/95 p-6 shadow-sm ${riskAccent(result.risk_level)}`}>
              <p className="mb-2 text-lg font-semibold text-slate-800">📋 종합 판단</p>
              <p className="text-base leading-7 text-slate-600">{result.verdict}</p>
            </div>

            <div className="rounded-3xl border border-slate-200 bg-white/95 p-6 shadow-sm">
              {sectionHeading('🔎', '리스크 요인 분석')}
              <ReasonChart reasons={result.reason_items} />
              <div className="mt-4">
                <ReasonCards reasons={result.reason_items} />
              </div>
            </div>

            <div className="rounded-3xl border border-slate-200 bg-white/95 p-6 shadow-sm">
              {sectionHeading('📈', '출발 시각 시뮬레이션')}
              <SimulationView jobInput={input} />
            </div>

            <div className="rounded-3xl border border-slate-200 bg-white/95 p-6 shadow-sm">
              {sectionHeading('📡', '데이터 신선도')}
              <FreshnessIndicator items={result.source_freshness} />
            </div>
          </>
        )}
      </div>
    </div>
  );
}
