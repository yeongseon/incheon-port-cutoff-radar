from __future__ import annotations

from datetime import datetime, timezone

from app.normalizers.source_normalizer import (
    normalize_congestion,
    normalize_gate_entry,
    normalize_operation,
    normalize_traffic,
)


class TestNormalizeCongestion:
    def test_korean_status_mapped(self):
        result = normalize_congestion(
            {"congestion_status": "혼잡", "observed_at": "2026-01-01T00:00:00Z"}
        )
        assert result is not None
        assert result["congestion_status"] == "congested"

    def test_english_status_passthrough(self):
        result = normalize_congestion({"congestion_status": "severe"})
        assert result is not None
        assert result["congestion_status"] == "severe"

    def test_explicit_time_preserved(self):
        result = normalize_congestion(
            {"congestion_status": "normal", "congestion_time_minutes": 42}
        )
        assert result is not None
        assert result["congestion_time_minutes"] == 42.0

    def test_none_returns_none(self):
        assert normalize_congestion(None) is None

    def test_unknown_status_defaults_to_normal(self):
        result = normalize_congestion({"congestion_status": "unknown_value"})
        assert result is not None
        assert result["congestion_status"] == "normal"


class TestNormalizeGateEntry:
    def test_camel_case_count(self):
        result = normalize_gate_entry({"vehicleCount": "25"})
        assert result is not None
        assert result["vehicle_count"] == 25

    def test_snake_case_count(self):
        result = normalize_gate_entry({"vehicle_count": 30})
        assert result is not None
        assert result["vehicle_count"] == 30

    def test_none_returns_none(self):
        assert normalize_gate_entry(None) is None

    def test_invalid_count_becomes_none(self):
        result = normalize_gate_entry({"vehicle_count": "not_a_number"})
        assert result is not None
        assert result["vehicle_count"] is None


class TestNormalizeTraffic:
    def test_speed_from_avgSpeed(self):
        result = normalize_traffic({"avgSpeed": "45.5"})
        assert result is not None
        assert result["average_speed_kph"] == 45.5

    def test_travel_from_travelTime(self):
        result = normalize_traffic({"travelTime": "30"})
        assert result is not None
        assert result["estimated_travel_minutes"] == 30.0

    def test_none_returns_none(self):
        assert normalize_traffic(None) is None


class TestNormalizeOperation:
    def test_camel_case_fields(self):
        result = normalize_operation(
            {
                "expectedArrival": True,
                "statusNote": "Delayed",
            }
        )
        assert result is not None
        assert result["expected_arrival_applied"] is True
        assert result["raw_status_note"] == "Delayed"

    def test_none_returns_none(self):
        assert normalize_operation(None) is None
