from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from app.engine.risk import (
    build_reason_items,
    compute_buffer_minutes,
    compute_gate_adjustment_minutes,
    compute_terminal_wait_minutes,
    compute_travel_minutes,
    evaluate,
    risk_score_to_level,
    slack_to_risk_and_probability,
)


class TestComputeTravelMinutes:
    def test_known_zone_no_traffic(self):
        minutes, fallback = compute_travel_minutes("SONGDO", None)
        assert minutes == 25.0
        assert fallback is True

    def test_known_zone_with_fast_traffic(self):
        minutes, fallback = compute_travel_minutes("SONGDO", {"average_speed_kph": 65})
        assert minutes == 25.0
        assert fallback is False

    def test_known_zone_with_slow_traffic(self):
        minutes, fallback = compute_travel_minutes("SONGDO", {"average_speed_kph": 15})
        assert minutes == pytest.approx(25 * 2.5, rel=0.1)
        assert fallback is False

    def test_unknown_zone_uses_default(self):
        minutes, _ = compute_travel_minutes("UNKNOWN", None)
        assert minutes == 40.0


class TestComputeTerminalWait:
    def test_no_snapshot(self):
        minutes, fallback = compute_terminal_wait_minutes(None)
        assert minutes == 15.0
        assert fallback is True

    def test_congested(self):
        minutes, fallback = compute_terminal_wait_minutes({"congestion_status": "congested"})
        assert minutes == 30.0
        assert fallback is False

    def test_explicit_time_overrides_status(self):
        snap = {"congestion_status": "smooth", "congestion_time_minutes": 42}
        minutes, fallback = compute_terminal_wait_minutes(snap)
        assert minutes == 42.0


class TestComputeGateAdjustment:
    def test_no_snapshot(self):
        minutes, fallback = compute_gate_adjustment_minutes(None)
        assert minutes == 5.0
        assert fallback is True

    def test_low_count(self):
        minutes, fallback = compute_gate_adjustment_minutes({"vehicle_count": 5})
        assert minutes == 0.0

    def test_very_busy(self):
        minutes, fallback = compute_gate_adjustment_minutes({"vehicle_count": 70})
        assert minutes == 25.0


class TestBuffer:
    def test_default(self):
        assert compute_buffer_minutes(False, None, False) == 15.0

    def test_conservative(self):
        assert compute_buffer_minutes(True, None, False) == 35.0

    def test_manual_override(self):
        assert compute_buffer_minutes(True, 10, True) == 10.0

    def test_stale_penalty(self):
        assert compute_buffer_minutes(False, None, True) == 25.0


class TestSlackMapping:
    def test_high_slack_low_risk(self):
        score, prob = slack_to_risk_and_probability(120)
        assert score == 5
        assert prob == 0.97

    def test_negative_slack_high_risk(self):
        score, prob = slack_to_risk_and_probability(-10)
        assert score == 98
        assert prob == 0.05


class TestRiskLevel:
    def test_low(self):
        assert risk_score_to_level(20) == "LOW"

    def test_medium(self):
        assert risk_score_to_level(50) == "MEDIUM"

    def test_high(self):
        assert risk_score_to_level(80) == "HIGH"


class TestBuildReasonItems:
    def test_four_items_sorted_by_impact(self):
        items = build_reason_items(30, 20, 10, 15)
        assert len(items) == 4
        assert items[0]["code"] == "TRAFFIC"
        assert sum(i["contribution_percent"] for i in items) in range(98, 102)


class TestEvaluateEndToEnd:
    def test_low_risk_scenario(self):
        now = datetime(2026, 7, 10, 10, 0, tzinfo=timezone.utc)
        cutoff = datetime(2026, 7, 10, 17, 0, tzinfo=timezone.utc)

        result = evaluate(
            origin_zone_id="SONGDO",
            terminal_code="ICT",
            cut_off_at=cutoff,
            now=now,
            traffic_snapshot={"average_speed_kph": 60},
            congestion_snapshot={"congestion_status": "smooth"},
            gate_snapshot={"vehicle_count": 5},
        )

        assert result["risk_level"] == "LOW"
        assert result["on_time_probability"] > 0.9

    def test_high_risk_scenario(self):
        now = datetime(2026, 7, 10, 16, 0, tzinfo=timezone.utc)
        cutoff = datetime(2026, 7, 10, 17, 0, tzinfo=timezone.utc)

        result = evaluate(
            origin_zone_id="ANSAN",
            terminal_code="ICT",
            cut_off_at=cutoff,
            now=now,
            traffic_snapshot={"average_speed_kph": 15},
            congestion_snapshot={"congestion_status": "severe"},
            gate_snapshot={"vehicle_count": 70},
        )

        assert result["risk_level"] == "HIGH"
        assert result["on_time_probability"] < 0.3

    def test_all_fallback_scenario(self):
        now = datetime(2026, 7, 10, 14, 0, tzinfo=timezone.utc)
        cutoff = datetime(2026, 7, 10, 17, 0, tzinfo=timezone.utc)

        result = evaluate(
            origin_zone_id="SONGDO",
            terminal_code="ICT",
            cut_off_at=cutoff,
            now=now,
        )

        assert result["used_fallbacks"]["traffic"] is True
        assert result["used_fallbacks"]["congestion"] is True
        assert "risk_score" in result
