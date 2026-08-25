"""
broker.py
Owner: Shreya V R

POST /broker/evaluate — the core ZTNA decision endpoint. Takes a user's
device trust score plus login context (hour, geo), runs a simple
rule-based risk score, checks it against the policies table, issues a
JWT if allowed, and logs the decision to risk_logs.
"""
from fastapi import APIRouter
from .database import get_db
from .security import generate_token
from .models import BrokerEvaluateRequest, BrokerEvaluateResponse

router = APIRouter()

UNFAMILIAR_GEO_RISK = 0.3
ODD_HOUR_RISK = 0.2
KNOWN_GEO = {"Bengaluru", "Mysuru"}  # placeholder — treat these as familiar


def calculate_context_risk(login_hour: int, geo: str) -> tuple[float, list[str]]:
    """Simple rule-based risk scoring from login context."""
    risk = 0.0
    reasons = []

    if geo not in KNOWN_GEO:
        risk += UNFAMILIAR_GEO_RISK
        reasons.append(f"Unfamiliar login location: {geo}")

    if login_hour < 6 or login_hour > 22:
        risk += ODD_HOUR_RISK
        reasons.append(f"Unusual login hour: {login_hour}:00")

    return round(min(risk, 1.0), 3), reasons


@router.post("/broker/evaluate", response_model=BrokerEvaluateResponse)
def evaluate_broker_request(data: BrokerEvaluateRequest):
    context_risk, reasons = calculate_context_risk(data.login_hour, data.geo)

    device_risk = round(1.0 - data.device_trust_score, 3)
    final_risk = round((0.5 * device_risk) + (0.5 * context_risk), 3)

    conn = get_db()
    cur = conn.cursor()

    policy = cur.execute(
        "SELECT min_trust_score FROM policies WHERE resource = ?",
        ("/broker/evaluate",),
    ).fetchone()

    min_trust_score = policy["min_trust_score"] if policy else 0.5
    trust_score = round(1.0 - final_risk, 3)

    if trust_score >= min_trust_score:
        decision = "grant"
    elif trust_score >= min_trust_score - 0.2:
        decision = "step_up"
    else:
        decision = "deny"

    token = None
    if decision == "grant":
        token = generate_token(data.user_id, extra_claims={"risk_score": final_risk})

    cur.execute(
        """
        INSERT INTO risk_logs (user_id, session_id, identity_risk, device_risk, final_risk, decision, reason)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (data.user_id, None, context_risk, device_risk, final_risk, decision,
         "; ".join(reasons) or "No elevated risk factors"),
    )
    conn.commit()
    conn.close()

    return BrokerEvaluateResponse(
        decision=decision,
        risk_score=final_risk,
        token=token,
    )
