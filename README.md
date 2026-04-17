# 인천항 Cut-off 리스크 레이더

인천항 반입 컨테이너가 터미널 gate-in cut-off를 충족할 수 있는지 예측하는 웹 기반 의사결정 지원 도구입니다.

**혼잡 가시화에서 배차 의사결정까지.**

📖 **문서 사이트**: [https://yeongseon.github.io/incheon-port-cutoff-radar/](https://yeongseon.github.io/incheon-port-cutoff-radar/)

🚀 **라이브 데모**: [https://yeongseon.github.io/incheon-port-cutoff-radar/app/](https://yeongseon.github.io/incheon-port-cutoff-radar/app/)

## 주요 기능

출발 지역, 도착 터미널, cut-off 시간을 입력하면:
- 정시 도착 확률
- Cut-off 초과 리스크 점수 (0-100)
- 최늦 안전 출발 시각
- 리스크 요인별 기여도 분석
- 출발 시각별 시뮬레이션 (현재 vs -15/-30/-60분)

## 기술 스택

| 계층 | 스택 |
|------|------|
| 프론트엔드 | React 19, TypeScript, Vite 8, Tailwind CSS v4, Recharts |
| 백엔드 | Python 3.10+, FastAPI, Pydantic v2, SQLAlchemy |
| 데이터베이스 | PostgreSQL 16, Redis 7 |
| 문서 | MkDocs Material (화이트 테마) |
| 인프라 | Docker Compose |
| CI/CD | GitHub Actions → GitHub Pages |

## 빠른 시작

### Docker Compose

```bash
docker compose up --build
```

- 프론트엔드: http://localhost:3000
- 백엔드 API: http://localhost:8000
- API 문서: http://localhost:8000/docs

### 로컬 개발

**백엔드:**
```bash
cd backend
pip install fastapi uvicorn pydantic pydantic-settings sqlalchemy redis httpx apscheduler python-dotenv
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

**프론트엔드:**
```bash
cd frontend
npm install
npm run dev
```

프론트엔드는 http://localhost:5173 에서 실행되며 API 프록시로 백엔드와 통신합니다.

### 테스트 실행

```bash
cd backend
python3 -m pytest tests/ -v
```

46개 테스트 전부 통과 (엔진 단위 23 + 정규화 단위 13 + API 통합 10).

## API 엔드포인트

| 메서드 | 경로 | 설명 |
|--------|------|------|
| POST | `/api/v1/risk/evaluate` | 단일 반입 작업 리스크 평가 |
| POST | `/api/v1/risk/simulate` | 출발 시각별 시뮬레이션 |
| GET | `/api/v1/terminals` | 지원 터미널 목록 조회 |
| GET | `/api/v1/health` | 상태 확인 |

## 프로젝트 구조

```
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI 라우트 + 미들웨어
│   │   ├── engine/        # 리스크 계산 엔진 + 설정
│   │   ├── models/        # Pydantic 스키마 + ORM 모델
│   │   ├── services/      # 비즈니스 로직 조율
│   │   ├── clients/       # 외부 API 클라이언트
│   │   ├── normalizers/   # 소스 데이터 정규화
│   │   ├── repositories/  # DB/캐시 접근
│   │   └── scheduler/     # 데이터 수집 스케줄러
│   ├── tests/
│   └── alembic/           # DB 마이그레이션
├── frontend/
│   └── src/
│       ├── api/           # API 클라이언트 + mock 엔진
│       ├── components/    # 재사용 가능 UI 컴포넌트
│       └── pages/         # 입력 + 결과 페이지
├── docs/                  # MkDocs 문서 소스
│   ├── specs/             # 13개 스펙 문서 (00-12)
│   └── guide/             # 빠른 시작, API 참조, 엔진 설명
├── mkdocs.yml             # MkDocs 설정
├── docker-compose.yml
└── .github/workflows/     # GitHub Pages CI/CD
```

## 문서

전체 스펙 문서는 [문서 사이트](https://yeongseon.github.io/incheon-port-cutoff-radar/)에서 확인할 수 있습니다:

| 번호 | 제목 |
|------|------|
| 00 | 프로젝트 개요 |
| 01 | 제품 요구사항 정의서 (PRD) |
| 02 | MVP 스펙 |
| 03 | 아키텍처 |
| 04 | 데이터 스펙 |
| 05 | API 스펙 |
| 06 | DB 스키마 |
| 07 | 프론트엔드 스펙 |
| 08 | 백엔드 스펙 |
| 09 | 7개월 개발 계획 |
| 10 | 테스트 계획 |
| 11 | 리스크 & 의사결정 |
| 12 | 피치 원페이저 |

## 라이선스

MIT
