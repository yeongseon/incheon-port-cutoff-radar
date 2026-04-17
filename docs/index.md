# 인천항 Cut-off 리스크 레이더

**인천항 반입 cut-off 리스크 예측 MVP**

> 혼잡 가시화에서 배차 의사결정까지.

---

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
