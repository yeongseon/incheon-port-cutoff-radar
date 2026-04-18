# 인천항 Cut-off 리스크 레이더

[![React](https://img.shields.io/badge/React-19-61DAFB?logo=react)](https://react.dev)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?logo=typescript)](https://typescriptlang.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![Vite](https://img.shields.io/badge/Vite-8-646CFF?logo=vite)](https://vitejs.dev)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql)](https://postgresql.org)
[![License](https://img.shields.io/badge/License-MIT-green)](https://github.com/yeongseon/incheon-port-cutoff-radar)

**인천항 반입 cut-off 리스크 예측 MVP**

> 혼잡 가시화에서 배차 의사결정까지.

**[라이브 데모](../app/)** · **[API 문서](guide/api.md)** · **[빠른 시작](guide/quickstart.md)**

---

## 문제 정의

| 문제 유형 | 설명 |
|-----------|------|
| Cut-off 초과 | gate-in 마감 시간 초과로 선적 지연 |
| 분산된 정보 | 교통/터미널/게이트 데이터를 수동 조합 |
| 재계획 비용 | 미스 시 재배차 + 추가 비용 발생 |
| 선적 누락 | 최악의 경우 해당 선편 누락 |

!!! danger "핵심 과제"

    cut-off 미스는 단순 지연이 아니라 선적 누락, 재계획 비용, 고객 신뢰 하락으로 이어진다. '상태 모니터링'이 아니라 '의사결정 지원'이 목표다.

## 프로젝트 목표

1. 실시간 교통·터미널·게이트 신호를 결합해 반입 cut-off 충족 가능성을 빠르게 판단합니다.
2. 배차 담당자가 출발 시각 조정, 보수적 운행, 재계획 여부를 즉시 결정할 수 있도록 지원합니다.
3. cut-off 미스에 따른 선적 누락과 추가 운영비를 줄이는 방향으로 리스크를 시각화합니다.

## 프로젝트 소개

인천항 반입 cut-off 리스크 예측 시스템은 컨테이너 반입 작업의 gate-in cut-off 충족 가능 여부를 판단하는 의사결정 지원 웹 서비스입니다.

### 주요 기능

- **정시 도착 확률** — 현재 출발 시 cut-off를 충족할 확률
- **리스크 점수** — 0~100점 기반 위험도 (낮음 / 보통 / 높음)
- **최적 출발 시각** — cut-off를 안전하게 충족하는 최늦 출발 시각
- **원인 분석** — 교통, 터미널 혼잡도, 게이트 진입량 등 기여도 분해
- **시뮬레이션** — 출발 시각별 what-if 비교

## 빠른 시작

### Docker Compose

```bash
docker compose up --build
```

| 서비스 | URL |
|--------|-----|
| 프론트엔드 | [http://localhost:3000](http://localhost:3000) |
| 백엔드 API | [http://localhost:8000](http://localhost:8000) |
| API 문서 (Swagger) | [http://localhost:8000/docs](http://localhost:8000/docs) |

### 로컬 개발

=== "백엔드"

    ```bash
    cd backend
    pip install fastapi uvicorn pydantic pydantic-settings sqlalchemy redis httpx python-dotenv
    cp .env.example .env
    uvicorn app.main:app --reload --port 8000
    ```

=== "프론트엔드"

    ```bash
    cd frontend
    npm install
    npm run dev
    ```

    프론트엔드: [http://localhost:5173](http://localhost:5173)

### 테스트

```bash
cd backend
python3 -m pytest tests/ -v
```

## 아키텍처

```
사용자 브라우저
  → 프론트엔드 (React 19 + TypeScript + Tailwind)
    → 백엔드 API (FastAPI + Pydantic v2)
      → 데이터 집계 계층
      → 리스크 엔진 (규칙 기반 v1.0.0)
      → Redis (캐시) + PostgreSQL (영구 저장)
      → 외부 공공 API
```

## 기술 스택

| 계층 | 스택 |
|------|------|
| 프론트엔드 | React 19, TypeScript, Vite 8, Tailwind CSS v4, Recharts |
| 백엔드 | Python 3.10+, FastAPI, Pydantic v2, SQLAlchemy |
| 데이터베이스 | PostgreSQL 16, Redis 7 |
| 인프라 | Docker Compose |
| 문서 | MkDocs Material |
| CI/CD | GitHub Actions → GitHub Pages |

## 문서

전체 스펙 문서는 [스펙 문서](specs/00_project_overview.md) 섹션에서 확인할 수 있습니다.

## 라이브 데모

[데모 페이지](demo.md)에서 mock 데이터 기반 데모를 확인할 수 있습니다.

## 라이선스

MIT
