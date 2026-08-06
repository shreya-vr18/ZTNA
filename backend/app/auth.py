from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import sqlite3
from .security import verify_password

router = APIRouter()

# Path to the local database file
DB_PATH = "ztna.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    # This line allows us to access columns by name (like a dictionary)
    conn.row_factory = sqlite3.Row 
    try:
        yield conn
    finally:
        conn.close()

class LoginRequest(BaseModel):
    username: str
    password: str

class DeviceVerifyRequest(BaseModel):
    user_id: int
    device_hash: str
    browser: str
    os: str
    ip: str

@router.post("/auth/login")
def login(req: LoginRequest, db = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT id, password_hash FROM users WHERE username = ?", (req.username,))
    user = cursor.fetchone()
    
    if not user or not verify_password(req.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")
        
    return {"status": "success", "user_id": user["id"]}

@router.post("/auth/verify-device")
def verify_device(req: DeviceVerifyRequest, db = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT id FROM devices WHERE device_hash = ?", (req.device_hash,))
    existing_device = cursor.fetchone()

    if existing_device:
        trust_score = 0.8
        cursor.execute(
            "UPDATE devices SET ip = ?, browser = ?, os = ? WHERE device_hash = ?",
            (req.ip, req.browser, req.os, req.device_hash),
        )
    else:
        trust_score = 0.3
        cursor.execute(
            "INSERT INTO devices (user_id, device_hash, browser, os, ip) VALUES (?, ?, ?, ?, ?)",
            (req.user_id, req.device_hash, req.browser, req.os, req.ip),
        )
    db.commit()

    return {"status": "success", "trust_score": trust_score}