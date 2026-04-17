# API 참조

## 기본 URL

```
http://localhost:8000/api/v1
```

## 인증

API 키 인증 (선택적). `X-API-Key` 헤더로 전달.

```bash
curl -H "X-API-Key: your-key" http://localhost:8000/api/v1/health
```

API 키가 설정되지 않은 경우 인증 없이 접근 가능.

## 요청 제한

IP 기반 분당 60회 요청.

---

## POST /risk/evaluate

단일 반입 작업의 리스크를 평가합니다.

### 요청

```json
{
  "origin_zone_id": "SONGDO",
  "terminal_code": "ICT",
  "cut_off_at": "2026-07-10T17:00:00+09:00",
  "conservative_mode": false,
  "manual_buffer_minutes": null
}
```

### 응답

```json
{
  "risk_score": 74,
  "risk_level": "HIGH",
  "on_time_probability": 0.41,
  "latest_safe_dispatch_at": "2026-07-10T14:20:00+09:00",
  "estimated_total_minutes": 145,
  "reason_items": [
    {
      "code": "TRAFFIC",
      "label": "도로 교통",
      "contribution_percent": 38,
      "summary": "도로 교통 요인으로 이동 시간이 증가했습니다."
    }
  ],
  "data_freshness": [
    {
      "source_name": "terminal_congestion",
      "observed_at": "2026-07-10T13:05:00+09:00",
      "status": "LIVE"
    }
  ],
  "result_status": "FULL",
  "warnings": []
}
```

### 필드 설명

| 필드 | 타입 | 설명 |
|------|------|------|
| `risk_score` | int | 0-100 리스크 점수 |
| `risk_level` | string | LOW / MEDIUM / HIGH |
| `on_time_probability` | float | 정시 도착 확률 (0-1) |
| `latest_safe_dispatch_at` | datetime | 최늦 안전 출발 시각 |
| `result_status` | string | FULL / DEGRADED / FAILED |

---

## POST /risk/simulate

출발 시각별 what-if 시뮬레이션을 실행합니다.

### 요청

```json
{
  "origin_zone_id": "SONGDO",
  "terminal_code": "ICT",
  "cut_off_at": "2026-07-10T17:00:00+09:00",
  "scenario_offsets_minutes": [0, -15, -30, -60]
}
```

### 응답

```json
{
  "scenarios": [
    {
      "offset_minutes": 0,
      "risk_score": 74,
      "risk_level": "HIGH",
      "on_time_probability": 0.41
    },
    {
      "offset_minutes": -30,
      "risk_score": 51,
      "risk_level": "MEDIUM",
      "on_time_probability": 0.67
    }
  ]
}
```

---

## GET /terminals

지원하는 인천항 터미널 목록을 반환합니다.

### 응답

```json
[
  {"code": "ICT", "name": "인천컨테이너터미널"},
  {"code": "E1", "name": "E1컨테이너터미널"},
  {"code": "SNCT", "name": "선광신컨테이너터미널"},
  {"code": "HJIT", "name": "한진인천터미널"},
  {"code": "SGT", "name": "성민터미널"}
]
```

---

## GET /health

상태 확인 엔드포인트.

### 응답

```json
{
  "status": "ok",
  "version": "0.1.0"
}
```
