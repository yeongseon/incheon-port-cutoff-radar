# Data Specification
## Incheon Port Cut-off Miss Risk Radar

## 1. Core source groups

### 1.1 Terminal congestion

Purpose: estimate terminal waiting pressure

### 1.2 Terminal operational info

Purpose: reflect terminal-side inbound operational hints

### 1.3 Vehicle entry statistics

Purpose: estimate gate-side traffic pressure

### 1.4 Road traffic data

Purpose: estimate origin-to-terminal travel time

## 2. Internal normalized model

### TerminalCongestionSnapshot

| Field | Type |
|-------|------|
| terminal_code | string |
| terminal_name | string |
| congestion_status | string |
| congestion_time_minutes | number \| null |
| observed_at | datetime |
| source_name | string |

### TerminalOperationSnapshot

| Field | Type |
|-------|------|
| terminal_code | string |
| terminal_name | string |
| available_time | datetime \| null |
| expected_arrival_applied | boolean \| null |
| raw_status_note | string \| null |
| observed_at | datetime |
| source_name | string |

### GateEntrySnapshot

| Field | Type |
|-------|------|
| terminal_name | string |
| lane_code | string \| null |
| entry_type | string \| null |
| vehicle_count | integer \| null |
| observed_at | datetime |
| source_name | string |

### TrafficSnapshot

| Field | Type |
|-------|------|
| route_key | string |
| average_speed_kph | number \| null |
| congestion_level | string \| null |
| estimated_travel_minutes | number \| null |
| observed_at | datetime |
| source_name | string |

## 3. User input model

### DispatchJobInput

| Field | Type |
|-------|------|
| origin_text | string |
| terminal_code | string |
| cut_off_at | datetime |
| conservative_mode | boolean |
| manual_buffer_minutes | integer \| null |

## 4. Result model

### DispatchRiskResult

| Field | Type |
|-------|------|
| risk_score | integer |
| risk_level | string |
| on_time_probability | number |
| latest_safe_dispatch_at | datetime |
| estimated_total_minutes | integer |
| reason_items | list[ReasonItem] |
| data_freshness | list[SourceFreshness] |

### ReasonItem

| Field | Type |
|-------|------|
| code | string |
| label | string |
| contribution_percent | integer |
| summary | string |

### SourceFreshness

| Field | Type |
|-------|------|
| source_name | string |
| observed_at | datetime \| null |
| status | string |
