# Incheon Port Cut-off Miss Risk Radar

A web-based decision-support tool that estimates whether an inbound container job can meet terminal gate-in cut-off at Incheon Port.

**From congestion visibility to dispatch decision.**

📖 **Documentation**: [https://yeongseon.github.io/incheon-port-cutoff-radar/](https://yeongseon.github.io/incheon-port-cutoff-radar/)

🚀 **Live Demo**: [https://yeongseon.github.io/incheon-port-cutoff-radar/demo/](https://yeongseon.github.io/incheon-port-cutoff-radar/demo/)

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
| Frontend | React 19, TypeScript, Vite 8, Tailwind CSS v4, Recharts |
| Backend | Python 3.10+, FastAPI, Pydantic v2, SQLAlchemy |
| Database | PostgreSQL 16, Redis 7 |
| Docs | MkDocs Material (white theme) |
| Infra | Docker Compose |
| CI/CD | GitHub Actions → GitHub Pages |

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

46 tests passing (23 unit-engine + 13 unit-normalizers + 10 integration-api).

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
│   │   ├── api/          # FastAPI routes + middleware
│   │   ├── engine/        # Risk calculation engine + config
│   │   ├── models/        # Pydantic schemas + ORM models
│   │   ├── services/      # Business logic orchestration
│   │   ├── clients/       # External API clients
│   │   ├── normalizers/   # Source data normalization
│   │   ├── repositories/  # DB/cache access
│   │   └── scheduler/     # Data ingestion scheduler
│   ├── tests/
│   └── alembic/           # DB migrations
├── frontend/
│   └── src/
│       ├── api/           # API client + mock engine
│       ├── components/    # Reusable UI components
│       └── pages/         # Input + Result pages
├── docs/                  # MkDocs documentation source
│   ├── specs/             # 13 spec documents (00-12)
│   └── guide/             # Quick start, API ref, engine docs
├── mkdocs.yml             # MkDocs configuration
├── docker-compose.yml
└── .github/workflows/     # CI/CD for GitHub Pages
```

## Documentation

Full spec documents available at the [docs site](https://yeongseon.github.io/incheon-port-cutoff-radar/):

| Doc | Title |
|-----|-------|
| 00 | Project Overview |
| 01 | PRD |
| 02 | MVP Spec |
| 03 | Architecture |
| 04 | Data Spec |
| 05 | API Spec |
| 06 | DB Schema |
| 07 | Frontend Spec |
| 08 | Backend Spec |
| 09 | 7-Month Dev Plan |
| 10 | Test Plan |
| 11 | Risks & Decisions |
| 12 | Pitch One-Pager |

## License

MIT
