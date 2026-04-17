# 프론트엔드

React 19 + TypeScript + Vite 8 + Tailwind CSS v4 기반 프론트엔드입니다.

## 개발 서버 실행

```bash
npm install
npm run dev
```

http://localhost:5173 에서 실행됩니다.

## 빌드

```bash
# 프로덕션 빌드
npm run build

# GitHub Pages 데모 빌드 (mock 데이터 사용)
npm run build:demo
```

## 주요 구성

- `src/pages/InputPage.tsx` — 입력 폼 (출발 지역, 터미널, cut-off 시간)
- `src/pages/ResultPage.tsx` — 결과 표시 (리스크 점수, 확률, 시뮬레이션)
- `src/components/` — 재사용 가능한 UI 컴포넌트
- `src/api/client.ts` — API 클라이언트 (데모 모드 시 mock 전환)
- `src/api/mock.ts` — 클라이언트사이드 mock 엔진
