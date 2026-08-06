from fastapi import FastAPI

from app.database import init_db
from app.models import (
    LoginRequest,
    LoginResponse,
    IdentityRiskInput,
    IdentityRiskOutput,
    DeviceRiskInput,
    DeviceRiskOutput,
    RiskEvaluationRequest,
    RiskEvaluationResponse,
)
from app.auth import login
from app.risk.identity_risk import score_identity_risk
from app.risk.device_risk import score_device_risk
from app.risk.risk_engine import evaluate_final_risk

app = FastAPI(title="ZTNA Trust Broker")


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/auth/login", response_model=LoginResponse)
def auth_login(data: LoginRequest):
    return login(data)


@app.post("/risk/identity", response_model=IdentityRiskOutput)
def risk_identity(data: IdentityRiskInput):
    return score_identity_risk(data)


@app.post("/risk/device", response_model=DeviceRiskOutput)
def risk_device(data: DeviceRiskInput):
    return score_device_risk(data)


@app.post("/broker/evaluate", response_model=RiskEvaluationResponse)
def broker_evaluate(data: RiskEvaluationRequest):
    return evaluate_final_risk(data)
