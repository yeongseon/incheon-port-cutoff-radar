# 🔌 내부 API 명세서
## 🚢 인천항 반입 Cut-off 리스크 레이더

## 1. 📮 POST /api/v1/risk/evaluate

### 설명

하나의 반입 배차 작업을 평가합니다.

### 요청 본문

```json
{
  "origin_text": "Songdo Warehouse",
  "terminal_code": "TERMINAL_A",
  "cut_off_at": "2026-07-10T17:00:00+09:00",
  "conservative_mode": true,
  "manual_buffer_minutes": 20
}
```

### 응답 본문

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
      "summary": "도로 이동 시간이 높게 형성되어 있습니다."
    },
    {
      "code": "TERMINAL_CONGESTION",
      "label": "터미널 혼잡",
      "contribution_percent": 34,
      "summary": "터미널 혼잡도가 높은 상태입니다."
    },
    {
      "code": "GATE_FLOW",
      "label": "Gate 진입 흐름",
      "contribution_percent": 28,
      "summary": "진입 흐름이 평소보다 높은 편입니다."
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

!!! info "핵심 응답 값"
    클라이언트는 `risk_score`, `on_time_probability`, `latest_safe_dispatch_at`를 최우선 표시 값으로 사용해야 합니다.

## 2. 🧪 POST /api/v1/risk/simulate

### 설명

배차 시각 변경에 따른 what-if 시뮬레이션을 실행합니다.

### 요청 본문

```json
{
  "origin_text": "Songdo Warehouse",
  "terminal_code": "TERMINAL_A",
  "cut_off_at": "2026-07-10T17:00:00+09:00",
  "scenario_offsets_minutes": [0, -15, -30, -60]
}
```

### 응답 본문

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

## 3. 🏷️ GET /api/v1/terminals

### 설명

지원되는 인천항 터미널 목록을 반환합니다.

## 4. ❤️ GET /api/v1/health

### 설명

백엔드와 의존 구성요소의 상태를 확인하기 위한 단순 health endpoint입니다.

!!! tip "프론트엔드 연동 팁"
    `simulate` 응답은 표 형태나 막대 그래프로 표현하면 사용자가 배차 시각 변화에 따른 위험도 차이를 직관적으로 이해하기 쉽습니다.

!!! warning "API 설계 주의"
    외부 원천 데이터가 불완전할 수 있으므로, 성공 응답이라도 `data_freshness`나 warning 메시지를 함께 제공하는 설계가 바람직합니다.

!!! danger "핵심 과제"
    API의 핵심 과제는 단순 계산 결과 반환이 아니라, 프론트엔드가 즉시 의사결정을 표현할 수 있도록 **설명 가능한 구조화 응답**을 제공하는 것입니다.
