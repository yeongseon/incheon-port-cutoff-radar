# System Architecture
## Incheon Port Cut-off Miss Risk Radar

## 1. High-level architecture

```
User Browser
  → Frontend Web App
    → Backend API
      → Data Aggregation Layer
      → Risk Engine
      → Cache / Database
      → External Public APIs
```

## 2. Components

### 2.1 Frontend

Responsibilities:

- collect user input
- render result cards
- show simulation view
- display reason breakdown

Stack:

- React 19, TypeScript, Vite
- Tailwind CSS v4
- Recharts

### 2.2 Backend API

Responsibilities:

- receive job input
- orchestrate data fetch
- normalize source payloads
- call risk engine
- return structured response

Stack:

- Python 3.10+
- FastAPI
- Pydantic v2

### 2.3 Data Aggregation Layer

Responsibilities:

- fetch data from public APIs
- map source payloads into common schema
- apply fallback logic
- annotate data freshness

### 2.4 Risk Engine

Responsibilities:

- estimate total lead time
- compute risk score
- compute probability band
- compute latest safe dispatch time
- compute reason contribution

### 2.5 Storage

#### Cache

- Redis 7
- short TTL for external API data

#### Persistent DB

- PostgreSQL 16
- scenario logs
- normalized snapshots
- simulation history

## 3. Request flow

1. user submits input
2. backend validates input
3. data layer reads cache
4. if cache miss, fetch from source APIs
5. normalize payloads
6. risk engine evaluates job
7. backend stores request/result log
8. frontend renders result

## 4. Failure handling

- if one source fails, use cache if available
- if a non-critical source is missing, continue with degraded confidence
- if critical sources fail, return partial result with warning
