# Incheon Port Cut-off Miss Risk Radar

A web-based decision-support tool that estimates whether an inbound container job can meet terminal gate-in cut-off at Incheon Port.

**From congestion visibility to dispatch decision.**

## What it does

Enter origin zone, destination terminal, and cut-off time → get:
- On-time arrival probability
- Cut-off miss risk score (0-100)
- Latest safe dispatch time
- Top contributing risk factors
- Dispatch-time simulation (now vs -15/-30/-60 min)

## Tech Stack

| Layer | Stack |
|-------|-------|
| Frontend | React 19, TypeScript, Vite, Tailwind CSS, Recharts |
| Backend | Python 3.10+, FastAPI, Pydantic v2 |
| Database | PostgreSQL 16, Redis 7 |
| Infra | Docker Compose |

## Quick Start

### With Docker Compose

```bash
docker compose up --build
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API docs: http://localhost:8000/docs

### Local Development

**Backend:**
```bash
cd backend
pip install fastapi uvicorn pydantic pydantic-settings sqlalchemy redis httpx apscheduler python-dotenv
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

Frontend runs at http://localhost:5173 with API proxy to backend.

### Run Tests

```bash
cd backend
python3 -m pytest tests/ -v
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/risk/evaluate` | Evaluate single dispatch job |
| POST | `/api/v1/risk/simulate` | What-if dispatch time simulation |
| GET | `/api/v1/terminals` | List supported terminals |
| GET | `/api/v1/health` | Health check |

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI routes
│   │   ├── engine/        # Risk calculation engine + config
│   │   ├── models/        # Pydantic schemas + ORM models
│   │   ├── services/      # Business logic orchestration
│   │   ├── clients/       # External API clients
│   │   ├── normalizers/   # Source data normalization
│   │   ├── repositories/  # DB/cache access
│   │   └── scheduler/     # Data ingestion scheduler
│   └── tests/
├── frontend/
│   └── src/
│       ├── api/           # API client
│       ├── components/    # Reusable UI components
│       └── pages/         # Input + Result pages
├── docker-compose.yml
└── README.md
```

## Supported Terminals

| Code | Name |
|------|------|
| ICT | Incheon Container Terminal |
| E1 | E1 Container Terminal |
| SNCT | Sun Kwang New Container Terminal |
| HJIT | Hanjin Incheon Terminal |
| SGT | Sungmin Terminal |

## Origin Zones

SONGDO, NAMDONG, SEOGU, YEONSU, BUPYEONG, SIHEUNG, ANSAN

## Risk Engine

Rule-based deterministic engine (v1.0.0):
- Total lead time = road travel + terminal wait + gate adjustment + safety buffer
- Slack = cut-off - now - total lead time
- Slack mapped to risk score and heuristic probability via lookup table
- Conservative mode adds extra buffer
- Stale data sources add freshness penalty

## License

MIT
