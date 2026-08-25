"""
risk_engine.py
Owner: Akash P Bhat

TODO (Akash): Combine identity_risk_score + device_risk_score into a
final decision.

    final_risk = (0.5 * identity_risk_score) + (0.5 * device_risk_score)

    if final_risk < 0.3   -> "grant"
    elif final_risk < 0.6 -> "step_up"   (e.g. require MFA)
    else                  -> "deny"
"""

from ..models import RiskEvaluationRequest, RiskEvaluationResponse
GRANT_THRESHOLD = 0.3
STEP_UP_THRESHOLD = 0.6


def evaluate_final_risk(data: RiskEvaluationRequest) -> RiskEvaluationResponse:
    final_risk = (0.5 * data.identity_risk_score) + (0.5 * data.device_risk_score)
    final_risk = round(final_risk, 3)

    if final_risk < GRANT_THRESHOLD:
        decision = "grant"
    elif final_risk < STEP_UP_THRESHOLD:
        decision = "step_up"
    else:
        decision = "deny"

    token = None

    return RiskEvaluationResponse(
        final_risk_score=final_risk, decision=decision, token=token
    )
