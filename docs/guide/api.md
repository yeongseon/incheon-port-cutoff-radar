# API Reference

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

API key 인증 (선택적). `X-API-Key` 헤더로 전달.

```bash
curl -H "X-API-Key: your-key" http://localhost:8000/api/v1/health
```

API key가 설정되지 않은 경우 인증 없이 접근 가능.

## Rate Limiting

IP 기반 60 requests/minute.

---

## POST /risk/evaluate

단일 반입 작업의 리스크를 평가합니다.

### Request

```json
{
  "origin_zone_id": "SONGDO",
  "terminal_code": "ICT",
  "cut_off_at": "2026-07-10T17:00:00+09:00",
  "conservative_mode": false,
  "manual_buffer_minutes": null
}
```

### Response

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
      "label": "Road traffic",
      "contribution_percent": 38,
      "summary": "Road travel time is elevated."
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

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `risk_score` | int | 0-100 리스크 점수 |
| `risk_level` | string | LOW / MEDIUM / HIGH |
| `on_time_probability` | float | 정시 도착 확률 (0-1) |
| `latest_safe_dispatch_at` | datetime | 최적 출발 시각 |
| `result_status` | string | FULL / DEGRADED / FAILED |

---

## POST /risk/simulate

출발 시각별 what-if 시뮬레이션을 실행합니다.

### Request

```json
{
  "origin_zone_id": "SONGDO",
  "terminal_code": "ICT",
  "cut_off_at": "2026-07-10T17:00:00+09:00",
  "scenario_offsets_minutes": [0, -15, -30, -60]
}
```

### Response

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

### Response

```json
[
  {"code": "ICT", "name": "Incheon Container Terminal"},
  {"code": "E1", "name": "E1 Container Terminal"},
  {"code": "SNCT", "name": "Sun Kwang New Container Terminal"},
  {"code": "HJIT", "name": "Hanjin Incheon Terminal"},
  {"code": "SGT", "name": "Sungmin Terminal"}
]
```

---

## GET /health

헬스 체크 엔드포인트.

### Response

```json
{
  "status": "ok",
  "version": "0.1.0"
}
```
