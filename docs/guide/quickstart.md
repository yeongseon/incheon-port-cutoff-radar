# Quick Start Guide

## 사전 요구사항

- Docker & Docker Compose (권장)
- 또는: Python 3.10+, Node.js 20+, PostgreSQL 16, Redis 7

## Docker Compose로 실행

```bash
git clone https://github.com/yeongseon/incheon-port-cutoff-radar.git
cd incheon-port-cutoff-radar
docker compose up --build
```

서비스 접속:

| 서비스 | URL |
|--------|-----|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |

## 로컬 개발 환경

### Backend

```bash
cd backend
pip install fastapi uvicorn pydantic pydantic-settings sqlalchemy redis httpx python-dotenv
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend는 http://localhost:5173 에서 실행되며, Vite proxy를 통해 backend와 통신합니다.

## 테스트 실행

```bash
cd backend
python3 -m pytest tests/ -v
```

현재 46개 테스트 전부 통과:

- Unit - Risk Engine: 23 tests
- Unit - Normalizers: 13 tests
- Integration - API: 10 tests

## 환경 변수

`backend/.env.example` 파일을 참고하여 `.env`를 설정합니다.

주요 변수:

| 변수 | 설명 | 기본값 |
|------|------|--------|
| `DATABASE_URL` | PostgreSQL 연결 | `postgresql+asyncpg://...` |
| `REDIS_URL` | Redis 연결 | `redis://localhost:6379/0` |
| `API_KEY` | API 인증 키 | (없으면 인증 비활성화) |
| `INGESTION_INTERVAL_SECONDS` | 데이터 수집 주기 | `180` |
