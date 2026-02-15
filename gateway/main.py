import os
import jwt
import time
import datetime
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import FastAPI, HTTPException, Request, Depends, status
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

# --- AUTHENTICATION LOGIC ---


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )


# --- GLOBAL ERROR HANDLING ---


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    """
    Catch any HTTPException and return a structured JSON response.
    This ensures all errors follow the same professional format.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "fail",
            "error_type": "Gateway Error",
            "message": exc.detail,
            "path": request.url.path,
            "timestamp": datetime.datetime.utcnow().isoformat(),
        },
    )


# --- REFINED FORWARDING LOGIC ---


async def forward_request(service: str, path: str, method: str, **kwargs) -> Any:
    if service not in SERVICES:
        raise HTTPException(status_code=404, detail=f"Service '{service}' not found.")

    url = f"{SERVICES[service]}{path}"

    async with httpx.AsyncClient() as client:
        try:
            # 5-second timeout to prevent the Gateway from hanging
            response = await client.request(method, url, timeout=5.0, **kwargs)

            # If the microservice itself returns an error (4xx or 5xx), pass it through
            if response.status_code >= 400:
                return JSONResponse(
                    status_code=response.status_code,
                    content=(
                        response.json()
                        if response.text
                        else {"detail": "Microservice Error"}
                    ),
                )

            return JSONResponse(
                content=response.json() if response.text else None,
                status_code=response.status_code,
            )

        except httpx.ConnectError:
            # Better error message
            raise HTTPException(
                status_code=503,
                detail=f"The {service} microservice is offline. Ensure it is running on {SERVICES[service]}.",
            )
        except httpx.TimeoutException:
            raise HTTPException(
                status_code=504,
                detail=f"The request to {service} microservice timed out.",
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=502,
                detail=f"Bad Gateway: Error communicating with {service}.",
            )


# ---  EQUEST LOGGING MIDDLEWARE ---


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    # Logs visible in the Gateway terminal [cite: 403]
    print(
        f"LOG: {request.method} {request.url.path} - Status: {response.status_code} - Time: {duration:.4f}s"
    )
    return response


# --- AUTHENTICATION APPLIED TO ALL ROUTES ---


@app.get("/")
def read_root():
    return {
        "message": "API Gateway is running",
        "available_services": list(SERVICES.keys()),
    }


# Student Service Routes
@app.get("/gateway/students")
async def get_all_students(token: dict = Depends(verify_token)):
    return await forward_request("student", "/api/students", "GET")


@app.get("/gateway/students/{student_id}")
async def get_student(student_id: int, token: dict = Depends(verify_token)):
    return await forward_request("student", f"/api/students/{student_id}", "GET")


@app.post("/gateway/students")
async def create_student(request: Request, token: dict = Depends(verify_token)):
    body = await request.json()
    return await forward_request("student", "/api/students", "POST", json=body)


@app.put("/gateway/students/{student_id}")
async def update_student(
    student_id: int, request: Request, token: dict = Depends(verify_token)
):
    body = await request.json()
    return await forward_request(
        "student", f"/api/students/{student_id}", "PUT", json=body
    )


@app.delete("/gateway/students/{student_id}")
async def delete_student(student_id: int, token: dict = Depends(verify_token)):
    return await forward_request("student", f"/api/students/{student_id}", "DELETE")


# Course Service Routes
@app.get("/gateway/courses")
async def get_all_courses(token: dict = Depends(verify_token)):
    return await forward_request("course", "/api/courses", "GET")


@app.get("/gateway/courses/{course_id}")
async def get_course(course_id: int, token: dict = Depends(verify_token)):
    return await forward_request("course", f"/api/courses/{course_id}", "GET")


@app.post("/gateway/courses")
async def create_course(request: Request, token: dict = Depends(verify_token)):
    body = await request.json()
    return await forward_request("course", "/api/courses", "POST", json=body)


@app.put("/gateway/courses/{course_id}")
async def update_course(
    course_id: int, request: Request, token: dict = Depends(verify_token)
):
    body = await request.json()
    return await forward_request(
        "course", f"/api/courses/{course_id}", "PUT", json=body
    )


@app.delete("/gateway/courses/{course_id}")
async def delete_course(course_id: int, token: dict = Depends(verify_token)):
    return await forward_request("course", f"/api/courses/{course_id}", "DELETE")


# Login Route (Public)
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
