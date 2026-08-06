from fastapi import FastAPI
from .auth import router as auth_router

app = FastAPI(title="ZTNA Backend")

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(auth_router)