from fastapi import FastAPI

from .auth import router as auth_router
from .gateway import router as gateway_router
from .broker import router as broker_router

app = FastAPI(
    title="ZTNA Backend",
    version="1.0"
)

@app.get("/health")
def health():
    return {
        "status": "Server is running"
    }

app.include_router(auth_router)
app.include_router(
    broker_router,
    tags=["Broker"]
)
app.include_router(
    gateway_router,
    prefix="/gateway",
    tags=["Gateway"]
)
