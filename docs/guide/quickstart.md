# 빠른 시작 가이드

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
| 프론트엔드 | http://localhost:3000 |
| 백엔드 API | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |

## 로컬 개발 환경

### 백엔드

```bash
cd backend
pip install fastapi uvicorn pydantic pydantic-settings sqlalchemy redis httpx python-dotenv
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

### 프론트엔드

```bash
cd frontend
npm install
npm run dev
```

프론트엔드는 http://localhost:5173 에서 실행되며, Vite 프록시를 통해 백엔드와 통신합니다.

## 테스트 실행

```bash
cd backend
python3 -m pytest tests/ -v
```

현재 46개 테스트 전부 통과:

- 단위 테스트 - 리스크 엔진: 23개
- 단위 테스트 - 정규화: 13개
- 통합 테스트 - API: 10개

## 환경 변수

`backend/.env.example` 파일을 참고하여 `.env`를 설정합니다.

주요 변수:

| 변수 | 설명 | 기본값 |
|------|------|--------|
| `DATABASE_URL` | PostgreSQL 연결 문자열 | `postgresql+asyncpg://...` |
| `REDIS_URL` | Redis 연결 문자열 | `redis://localhost:6379/0` |
| `API_KEY` | API 인증 키 | (없으면 인증 비활성화) |
| `INGESTION_INTERVAL_SECONDS` | 데이터 수집 주기 (초) | `180` |
