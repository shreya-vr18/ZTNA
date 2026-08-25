"""
identity_risk.py
Owner: Shreya V R

Scores how risky a user's IDENTITY and CREDENTIALS look for this login
attempt — separate from device/location risk (Vaishnavi) and the final
aggregated decision (Akash's risk_engine.py).

Signals used:
  - Repeated failed login attempts (credential stuffing / brute force signal)
  - Account age (brand-new accounts are inherently less trusted)
  - Password strength (weak passwords raise baseline risk even after a
    successful login, since they're easier to have been compromised)

Score is 0.0 (no identity risk) -> 1.0 (very high identity risk).
"""

from ..models import IdentityRiskInput, IdentityRiskOutput

FAILED_LOGIN_THRESHOLD = 3
NEW_ACCOUNT_DAYS_THRESHOLD = 7

FAILED_LOGIN_WEIGHT = 0.4
NEW_ACCOUNT_WEIGHT = 0.2
WEAK_PASSWORD_WEIGHT = 0.4


def score_identity_risk(data: IdentityRiskInput) -> IdentityRiskOutput:
    risk = 0.0
    reasons: list[str] = []

    if data.failed_login_count >= FAILED_LOGIN_THRESHOLD:
        excess = min(data.failed_login_count - FAILED_LOGIN_THRESHOLD, 5)
        contribution = FAILED_LOGIN_WEIGHT * (1 + excess * 0.1)
        risk += contribution
        reasons.append(
            f"{data.failed_login_count} failed login attempts "
            f"(threshold: {FAILED_LOGIN_THRESHOLD})"
        )

    if data.account_age_days < NEW_ACCOUNT_DAYS_THRESHOLD:
        risk += NEW_ACCOUNT_WEIGHT
        reasons.append(
            f"Account is only {data.account_age_days} day(s) old "
            f"(threshold: {NEW_ACCOUNT_DAYS_THRESHOLD})"
        )

    weak_password_contribution = WEAK_PASSWORD_WEIGHT * (1 - data.password_strength_score)
    if data.password_strength_score < 0.5:
        reasons.append(
            f"Password strength score is low ({data.password_strength_score:.2f})"
        )
    risk += weak_password_contribution

    risk = max(0.0, min(risk, 1.0))

    if not reasons:
        reasons.append("No identity risk signals detected")

    return IdentityRiskOutput(identity_risk_score=round(risk, 3), reasons=reasons)
