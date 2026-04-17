# Risk Engine

## 개요

Rule-based deterministic engine (v1.0.0)으로 반입 작업의 cut-off 충족 리스크를 계산합니다.

## 계산 흐름

```
Total Lead Time = road_travel + terminal_wait + gate_adjustment + safety_buffer
Slack = cut_off_at - now - total_lead_time
Slack → Risk Score (lookup table)
Slack → On-time Probability (lookup table)
Risk Score → Risk Level (LOW / MEDIUM / HIGH)
Latest Safe Dispatch = cut_off_at - total_lead_time
```

## 구성 요소

### 1. Road Travel Time

출발 zone별 기본 소요시간 + 교통 데이터 기반 보정:

| Zone | Base (min) |
|------|-----------|
| SONGDO | 25 |
| NAMDONG | 35 |
| SEOGU | 20 |
| YEONSU | 30 |
| BUPYEONG | 40 |
| SIHEUNG | 45 |
| ANSAN | 55 |

교통 데이터가 있으면 속도 기반 multiplier 적용:

- `speed ≥ 50 kph` → ×1.0
- `speed 30-49 kph` → ×1.5
- `speed < 30 kph` → ×2.5

### 2. Terminal Wait Time

터미널 혼잡도 기반:

| Status | Minutes |
|--------|---------|
| smooth | 10 |
| normal | 15 |
| congested | 30 |
| severe | 45 |

`congestion_time_minutes`가 있으면 직접 사용.

### 3. Gate Adjustment

게이트 차량 수 기반:

| Vehicle Count | Adjustment (min) |
|--------------|------------------|
| 0-9 | 0 |
| 10-29 | 5 |
| 30-49 | 15 |
| 50+ | 25 |

### 4. Safety Buffer

| Condition | Buffer (min) |
|-----------|-------------|
| Default | 15 |
| Conservative mode | 35 |
| Stale data penalty | +10 |
| Manual override | 사용자 입력값 |

## Slack → Risk 매핑

| Slack (min) | Risk Score | Probability |
|-------------|-----------|-------------|
| ≥ 90 | 5 | 0.97 |
| 60-89 | 20 | 0.90 |
| 30-59 | 45 | 0.72 |
| 15-29 | 65 | 0.50 |
| 0-14 | 82 | 0.28 |
| < 0 | 98 | 0.05 |

## Risk Level

| Score Range | Level |
|------------|-------|
| 0-34 | LOW |
| 35-69 | MEDIUM |
| 70-100 | HIGH |

## Reason Attribution

4가지 요소(traffic, terminal wait, gate, buffer)의 분 단위 기여도를 퍼센트로 환산하여 `reason_items`로 반환합니다. 기여도가 높은 순으로 정렬됩니다.
