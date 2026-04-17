# Database Schema
## Incheon Port Cut-off Miss Risk Radar

## 1. Tables

### 1.1 terminals

| Column | Type |
|--------|------|
| id | serial PK |
| terminal_code | varchar |
| terminal_name | varchar |
| is_active | boolean |
| created_at | timestamp |
| updated_at | timestamp |

### 1.2 source_snapshots_terminal_congestion

| Column | Type |
|--------|------|
| id | serial PK |
| terminal_code | varchar |
| congestion_status | varchar |
| congestion_time_minutes | float |
| observed_at | timestamp |
| fetched_at | timestamp |
| raw_payload_json | jsonb |

### 1.3 source_snapshots_terminal_operation

| Column | Type |
|--------|------|
| id | serial PK |
| terminal_code | varchar |
| available_time | timestamp |
| expected_arrival_applied | boolean |
| raw_status_note | text |
| observed_at | timestamp |
| fetched_at | timestamp |
| raw_payload_json | jsonb |

### 1.4 source_snapshots_gate_entry

| Column | Type |
|--------|------|
| id | serial PK |
| terminal_name | varchar |
| lane_code | varchar |
| entry_type | varchar |
| vehicle_count | integer |
| observed_at | timestamp |
| fetched_at | timestamp |
| raw_payload_json | jsonb |

### 1.5 source_snapshots_traffic

| Column | Type |
|--------|------|
| id | serial PK |
| route_key | varchar |
| average_speed_kph | float |
| estimated_travel_minutes | float |
| observed_at | timestamp |
| fetched_at | timestamp |
| raw_payload_json | jsonb |

### 1.6 dispatch_evaluations

| Column | Type |
|--------|------|
| id | serial PK |
| origin_text | varchar |
| terminal_code | varchar |
| cut_off_at | timestamp |
| conservative_mode | boolean |
| manual_buffer_minutes | integer |
| risk_score | integer |
| risk_level | varchar |
| on_time_probability | float |
| latest_safe_dispatch_at | timestamp |
| estimated_total_minutes | integer |
| created_at | timestamp |

### 1.7 dispatch_reason_items

| Column | Type |
|--------|------|
| id | serial PK |
| dispatch_evaluation_id | integer FK |
| code | varchar |
| label | varchar |
| contribution_percent | integer |
| summary | text |

## 2. Cache keys (Redis)

| Key pattern | Purpose |
|-------------|---------|
| `source:terminal_congestion:{terminal_code}` | Terminal congestion snapshot |
| `source:terminal_operation:{terminal_code}` | Terminal operation snapshot |
| `source:gate_entry:{terminal_name}` | Gate entry snapshot |
| `source:traffic:{route_key}` | Traffic snapshot |
