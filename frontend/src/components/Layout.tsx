import type { ReactNode } from 'react';

interface LayoutProps {
  children: ReactNode;
}

const IS_DEMO = import.meta.env.VITE_DEMO_MODE === 'true';
const APP_VERSION = 'v0.0.0';

export function Layout({ children }: LayoutProps) {
  return (
    <div className="relative min-h-screen overflow-hidden bg-slate-100 text-slate-900">
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_top,_rgba(59,130,246,0.14),_transparent_34%),radial-gradient(circle_at_bottom_right,_rgba(14,165,233,0.12),_transparent_28%)]" />

      <header className="sticky top-0 z-30 border-b border-white/60 bg-white/85 backdrop-blur-xl">
        <div className="mx-auto flex w-full max-w-6xl items-center justify-between gap-4 px-4 py-4 sm:px-6 lg:px-8">
          <div className="flex items-center gap-3">
            <div className="flex h-11 w-11 items-center justify-center rounded-lg bg-blue-600 shadow-lg shadow-blue-600/20">
              <span className="text-sm font-semibold text-white">IP</span>
            </div>
            <div>
              <p className="text-[11px] font-semibold tracking-[0.18em] text-blue-600">인천항 운송 인텔리전스</p>
              <h1 className="text-base font-semibold text-slate-900 sm:text-lg">인천항 Cut-off 리스크 레이더</h1>
            </div>
          </div>

          <div className="flex items-center gap-2 text-xs sm:text-sm">
            {IS_DEMO && (
              <span className="rounded-full border border-amber-300 bg-amber-50 px-3 py-1 font-medium text-amber-800 shadow-sm">
                데모 모드
              </span>
            )}
          </div>
        </div>
        <div className="h-px w-full bg-linear-to-r from-transparent via-blue-400/70 to-transparent" />
      </header>

      <main className="relative z-10">{children}</main>

      <footer className="relative z-10 mt-12 border-t border-slate-200/80 bg-white/80 backdrop-blur-sm">
        <div className="mx-auto flex w-full max-w-6xl flex-col gap-2 px-4 py-5 text-sm text-slate-500 sm:flex-row sm:items-center sm:justify-between sm:px-6 lg:px-8">
          <p>© 2025 인천항 Cut-off 리스크 레이더 · 멘토링 프로젝트</p>
          <p className="text-xs font-medium uppercase tracking-[0.22em] text-slate-400">버전 {APP_VERSION}</p>
        </div>
      </footer>
    </div>
  );
}
