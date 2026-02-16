from fastapi import APIRouter, HTTPException
import jwt
import datetime
from config import SECRET_KEY, ALGORITHM

# Simple router for auth
router = APIRouter(tags=["Authentication"])

# Mock user for testing
USER_DATA = {"username": "admin", "password": "password123"}


@router.post("/login")
def login(data: dict):
    """
    Public endpoint to exchange credentials for a JWT token.
    """
    if (
        data.get("username") == USER_DATA["username"]
        and data.get("password") == USER_DATA["password"]
    ):
        payload = {
            "sub": data["username"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return {"access_token": token, "token_type": "bearer"}

    raise HTTPException(status_code=401, detail="Invalid credentials")
