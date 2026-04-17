# Backend Specification
## Incheon Port Cut-off Miss Risk Radar

## 1. Modules

### app/api

- request routing
- validation
- response shaping

### app/services

- orchestration layer
- scenario evaluation flow

### app/clients

- external API clients
- source-specific adapters

### app/normalizers

- source payload → internal schema conversion

### app/engine

- risk calculation engine
- recommendation engine
- reason attribution engine

### app/repositories

- database access
- cache access

### app/models

- pydantic schemas
- ORM models

## 2. Core service flow

### evaluate_dispatch_job()

1. validate request
2. fetch source data
3. normalize payloads
4. compute travel estimate
5. compute terminal wait estimate
6. compute gate adjustment
7. add safety buffer
8. compute score / probability / recommendation
9. save log
10. return result

## 3. Engineering principles

- keep engine deterministic in MVP
- log every source freshness timestamp
- isolate each external source behind a client adapter
- keep calculations testable as pure functions

## 4. Tech stack

- Python 3.10+
- FastAPI
- Pydantic v2
- SQLAlchemy (async)
- Redis (aioredis)
- httpx (async HTTP client)
