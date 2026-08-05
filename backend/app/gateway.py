from fastapi import APIRouter, Header
from pydantic import BaseModel

router = APIRouter()
class RevokeRequest(BaseModel):
    session_id: str

@router.get("/access/{resource}")
def access_resource(resource: str, authorization: str = Header(None)):
    
    # Temporary mock verification
    if authorization != "Bearer valid-token":
        return {
            "access": "denied",
            "message": "Invalid Token"
        }

    return {
        "access": "granted",
        "resource_data": {
            "resource": resource,
            "message": "Access Granted"
        }
    }
@router.post("/revoke")
def revoke_session(request: RevokeRequest):

    return {
        "status": "Session Revoked",
        "session_id": request.session_id
    }