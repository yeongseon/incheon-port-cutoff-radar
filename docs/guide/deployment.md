# 배포 가이드

인천항 반입 컨테이너 cut-off 리스크 예측 MVP는 **문서/데모 공개용 정적 배포**와 **로컬 통합 검증용 Docker Compose 배포**를 함께 지원합니다. 문서는 GitHub Pages에, 전체 스택 실행은 Docker Compose에 최적화되어 있습니다.

## 배포 모드 비교

| 구분 | GitHub Pages 정적 배포 | Docker Compose Full-Stack |
|------|-------------------------|----------------------------|
| 목적 | 문서 공개, 데모 공유, 발표 시연 | 로컬 통합 개발, API 검증, 백엔드 연동 확인 |
| 실행 방식 | GitHub Actions가 자동 빌드 후 Pages 배포 | `docker compose up --build` |
| 프론트엔드 데이터 | mock 데이터 기반 demo mode | FastAPI 백엔드 + PostgreSQL + Redis |
| 접속 주소 | 문서: `https://yeongseon.github.io/incheon-port-cutoff-radar/`<br>데모: `https://yeongseon.github.io/incheon-port-cutoff-radar/app/` | 프론트엔드: `http://localhost:3000`<br>백엔드: `http://localhost:8000` |
| 적합한 상황 | 외부 공유, 심사 제출, 빠른 확인 | 기능 개발, API 테스트, 장애 재현 |

## GitHub Pages 배포

`deploy-pages.yml` 워크플로는 `main` 브랜치에 push될 때마다 자동으로 실행됩니다. 문서와 데모 앱을 각각 빌드한 뒤 하나의 Pages 아티팩트로 묶어 배포합니다.

### 자동화 흐름

```mermaid
graph LR
    A[Push to main] --> B[GitHub Actions]
    B --> C[Lint]
    C --> D[Build Frontend]
    D --> E[Build MkDocs]
    E --> F[Deploy to gh-pages]
```

!!! info "GitHub Pages 산출물 구성"
    - 문서 빌드: `mkdocs build --strict`
    - 프론트엔드 데모 빌드: `npm run build:demo`
    - 데모 정적 파일은 `site/app/` 아래로 복사되어 문서와 함께 배포됩니다.

### 배포 URL

| 산출물 | URL |
|--------|-----|
| MkDocs 문서 | `https://yeongseon.github.io/incheon-port-cutoff-radar/` |
| React 데모 앱 | `https://yeongseon.github.io/incheon-port-cutoff-radar/app/` |

### 워크플로 핵심 포인트

1. `main` push 시 GitHub Actions 실행
2. MkDocs를 strict 모드로 빌드하여 문서 링크 오류를 조기에 차단
3. 프론트엔드를 demo mode로 빌드하여 mock 데이터 기반 시연 환경 생성
4. `frontend/dist` 결과물을 `site/app`으로 복사
5. 최종적으로 GitHub Pages에 문서 + 데모를 함께 배포

```yaml
on:
  push:
    branches: [main]

steps:
  - name: Build MkDocs
    run: mkdocs build --strict

  - name: Build frontend demo
    working-directory: frontend
    run: npm run build:demo
```

## Docker Compose 배포

백엔드 API, 프론트엔드, PostgreSQL, Redis를 함께 실행하려면 루트 디렉터리에서 아래 명령을 사용합니다.

```bash
docker compose up --build
```

실행 후 기본 접속 주소는 다음과 같습니다.

| 서비스 | 주소 |
|--------|------|
| 프론트엔드 | `http://localhost:3000` |
| 백엔드 API | `http://localhost:8000` |
| Swagger UI | `http://localhost:8000/docs` |

Docker Compose는 **실제 FastAPI 백엔드와 캐시/DB 계층을 함께 검증**할 때 적합합니다. 발표용 공개 링크가 아니라, 개발자 로컬 환경에서 종단 간 동작을 확인하는 데 초점이 있습니다.

## Vite base 설정

GitHub Pages 하위 경로 배포를 위해 프론트엔드는 demo mode에서 다음 base 값을 사용합니다.

```ts
base: '/incheon-port-cutoff-radar/app/'
```

이 설정 덕분에 정적 자산 경로가 `/app/` 하위로 고정되며, Pages 환경에서도 CSS·JS·라우팅 리소스를 올바르게 찾을 수 있습니다.

!!! warning "base 경로 주의"
    GitHub Pages에서 데모 앱은 도메인 루트가 아니라 `/incheon-port-cutoff-radar/app/` 경로 아래에 배포됩니다.
    `base` 값이 `/`로 남아 있으면 JS 번들, CSS, 라우팅 경로가 모두 깨져 화면이 비정상적으로 보일 수 있습니다.

## 로컬 개발

정적 배포와 별개로, 기능 개발은 백엔드와 프론트엔드를 분리 실행하는 방식이 가장 빠릅니다.

=== "백엔드 터미널"

    ```bash
    cd backend
    cp .env.example .env
    pip install fastapi uvicorn pydantic pydantic-settings sqlalchemy redis httpx python-dotenv
    uvicorn app.main:app --reload --port 8000
    ```

=== "프론트엔드 터미널"

    ```bash
    cd frontend
    npm install
    npm run dev
    ```

로컬 개발 시 프론트엔드는 Vite 개발 서버(`http://localhost:5173`)로 실행되며, demo mode가 아닌 경우 `/api` 요청을 백엔드로 프록시합니다.

## 환경 변수

운영/개발 환경에서 자주 확인하는 핵심 변수는 아래와 같습니다.

| 변수 | 설명 | 예시 값 |
|------|------|---------|
| `DATABASE_URL` | PostgreSQL 연결 문자열. 앱 설정 문서에서는 일반적으로 이 이름으로 설명합니다. | `postgresql+asyncpg://radar:radar@localhost:5432/cutoff_radar` |
| `REDIS_URL` | Redis 캐시 연결 문자열 | `redis://localhost:6379/0` |
| `INGESTION_INTERVAL_SECONDS` | 데이터 수집/갱신 주기(초) | `180` |

!!! note "프로젝트 구현 메모"
    현재 예시 환경 파일과 Docker Compose에서는 `RADAR_DATABASE_URL`, `RADAR_REDIS_URL` 형태의 접두사 기반 이름을 사용합니다.
    문서 설계 관점에서는 `DATABASE_URL`, `REDIS_URL`처럼 역할 중심 이름으로 이해하면 됩니다.

## 배포 전략 선택 가이드

- **문서, 데모 링크, 발표 시연이 필요하다면** → GitHub Pages
- **API 포함 전체 기능을 검증해야 한다면** → Docker Compose
- **빠른 프론트엔드 확인만 필요하다면** → `npm run dev`

!!! info "MVP 범위 외"
    현재 저장소는 공개 데모와 로컬 통합 실행을 우선으로 한 MVP 구조입니다.
    실서비스 수준의 배포를 위해서는 비밀 정보 관리, HTTPS 종단, 관측성, 무중단 배포, 백그라운드 스케줄러 분리, 외부 API 장애 복구 전략 등이 추가로 필요합니다.
