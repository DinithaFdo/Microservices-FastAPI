import os
import jwt
import datetime
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
import httpx
from typing import Any

SECRET_KEY = "my_super_secret_key"
ALGORITHM = "HS256"
security = HTTPBearer()

# Mock user for testing
USER_DATA = {"username": "admin", "password": "password123"}

app = FastAPI(title="API Gateway", version="1.0.0")

# Service URLs
SERVICES = {"student": "http://localhost:8001", "course": "http://localhost:8002"}


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


async def forward_request(service: str, path: str, method: str, **kwargs) -> Any:
    """Forward request to the appropriate microservice"""

    if service not in SERVICES:
        raise HTTPException(status_code=404, detail="Service not found")

    url = f"{SERVICES[service]}{path}"

    async with httpx.AsyncClient() as client:
        try:
            if method == "GET":
                response = await client.get(url, **kwargs)
            elif method == "POST":
                response = await client.post(url, **kwargs)
            elif method == "PUT":
                response = await client.put(url, **kwargs)
            elif method == "DELETE":
                response = await client.delete(url, **kwargs)
            else:
                raise HTTPException(status_code=405, detail="Method not allowed")

            return JSONResponse(
                content=response.json() if response.text else None,
                status_code=response.status_code,
            )

        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503, detail=f"Service unavailable: {str(e)}"
            )


@app.get("/")
def read_root():
    return {
        "message": "API Gateway is running",
        "available_services": list(SERVICES.keys()),
    }


# Student Service Routes


@app.get("/gateway/students")
async def get_all_students(token: dict = Depends(verify_token)):
    """Get all students through gateway"""
    return await forward_request("student", "/api/students", "GET")


@app.get("/gateway/students/{student_id}")
async def get_student(student_id: int):
    """Get a student by ID through gateway"""
    return await forward_request("student", f"/api/students/{student_id}", "GET")


@app.post("/gateway/students")
async def create_student(request: Request):
    """Create a new student through gateway"""
    body = await request.json()
    return await forward_request("student", "/api/students", "POST", json=body)


@app.put("/gateway/students/{student_id}")
async def update_student(student_id: int, request: Request):
    """Update a student through gateway"""
    body = await request.json()
    return await forward_request(
        "student", f"/api/students/{student_id}", "PUT", json=body
    )


@app.delete("/gateway/students/{student_id}")
async def delete_student(student_id: int):
    """Delete a student through gateway"""
    return await forward_request("student", f"/api/students/{student_id}", "DELETE")


# Course Service Routes


@app.get("/gateway/courses")
async def get_all_courses(token: dict = Depends(verify_token)):
    return await forward_request("course", "/api/courses", "GET")


@app.get("/gateway/courses/{course_id}")
async def get_course(course_id: int):
    return await forward_request("course", f"/api/courses/{course_id}", "GET")


@app.post("/gateway/courses")
async def create_course(request: Request):
    body = await request.json()
    return await forward_request("course", "/api/courses", "POST", json=body)


@app.put("/gateway/courses/{course_id}")
async def update_course(course_id: int, request: Request):
    body = await request.json()
    return await forward_request(
        "course", f"/api/courses/{course_id}", "PUT", json=body
    )


@app.delete("/gateway/courses/{course_id}")
async def delete_course(course_id: int):
    return await forward_request("course", f"/api/courses/{course_id}", "DELETE")


@app.post("/login")
def login(data: dict):
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
