from fastapi import FastAPI
from app.gateway import router as gateway_router

app = FastAPI(
    title="ZTNA Gateway API",
    version="1.0"
)

app.include_router(
    gateway_router,
    prefix="/gateway",
    tags=["Gateway"]
)

@app.get("/health")
def health():
    return {
        "status": "Server is running"
    }