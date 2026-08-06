"""
device_risk.py
Owner: Vaishnavi R D

TODO (Vaishnavi): Implement device & location risk scoring.
Signals to consider: unknown device_hash, unusual login_hour,
mismatched/unfamiliar login_location vs. user history.

Score should be 0.0 (low risk) -> 1.0 (high risk), same scale as
identity_risk.py, so risk_engine.py can combine them directly.
"""

from app.models import DeviceRiskInput, DeviceRiskOutput


def score_device_risk(data: DeviceRiskInput) -> DeviceRiskOutput:
    return DeviceRiskOutput(
        device_risk_score=0.2,
        known_device=True,
        reasons=["Placeholder: real device/location scoring not implemented yet"],
    )
