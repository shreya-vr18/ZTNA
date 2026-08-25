"""
models.py
Shared request/response schemas — everyone imports from here so the
API contracts stay in sync with what's actually being sent/returned.
"""

from pydantic import BaseModel
from typing import Optional


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    status: str  # "success" | "fail" | "mfa_required"
    user_id: Optional[int] = None


class IdentityRiskInput(BaseModel):
    user_id: int
    failed_login_count: int
    account_age_days: int
    password_strength_score: float  # 0.0 (weak) - 1.0 (strong)


class IdentityRiskOutput(BaseModel):
    identity_risk_score: float  # 0.0 (low risk) - 1.0 (high risk)
    reasons: list[str]


class DeviceRiskInput(BaseModel):
    user_id: int
    device_hash: str
    browser: str
    os: str
    ip_address: str
    login_hour: int
    login_location: str


class DeviceRiskOutput(BaseModel):
    device_risk_score: float
    known_device: bool
    reasons: list[str]


class RiskEvaluationRequest(BaseModel):
    user_id: int
    identity_risk_score: float
    device_risk_score: float


class RiskEvaluationResponse(BaseModel):
    final_risk_score: float
    decision: str  # "grant" | "deny" | "step_up"
    token: Optional[str] = None

class BrokerEvaluateRequest(BaseModel):
    user_id: int
    device_trust_score: float  # 0.0 (untrusted) - 1.0 (fully trusted)
    login_hour: int
    geo: str


class BrokerEvaluateResponse(BaseModel):
    decision: str  # "grant" | "step_up" | "deny"
    risk_score: float
    token: Optional[str] = None
