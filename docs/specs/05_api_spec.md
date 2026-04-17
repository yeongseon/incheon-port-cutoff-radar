# Internal API Specification
## Incheon Port Cut-off Miss Risk Radar

## 1. POST /api/v1/risk/evaluate

### Description

Evaluate one inbound dispatch job.

### Request body

```json
{
  "origin_text": "Songdo Warehouse",
  "terminal_code": "TERMINAL_A",
  "cut_off_at": "2026-07-10T17:00:00+09:00",
  "conservative_mode": true,
  "manual_buffer_minutes": 20
}
```

### Response body

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
    },
    {
      "code": "TERMINAL_CONGESTION",
      "label": "Terminal congestion",
      "contribution_percent": 34,
      "summary": "Terminal congestion is high."
    },
    {
      "code": "GATE_FLOW",
      "label": "Gate entry flow",
      "contribution_percent": 28,
      "summary": "Entry flow is above normal."
    }
  ],
  "data_freshness": [
    {
      "source_name": "terminal_congestion",
      "observed_at": "2026-07-10T13:05:00+09:00",
      "status": "LIVE"
    }
  ]
}
```

## 2. POST /api/v1/risk/simulate

### Description

Run dispatch-time what-if simulation.

### Request body

```json
{
  "origin_text": "Songdo Warehouse",
  "terminal_code": "TERMINAL_A",
  "cut_off_at": "2026-07-10T17:00:00+09:00",
  "scenario_offsets_minutes": [0, -15, -30, -60]
}
```

### Response body

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

## 3. GET /api/v1/terminals

### Description

Return supported Incheon terminal list.

## 4. GET /api/v1/health

### Description

Simple health endpoint for backend and dependencies.
