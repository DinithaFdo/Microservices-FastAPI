import time
from fastapi import FastAPI, Request
from routes import students, courses, auth

app = FastAPI(title="Modular API Gateway")


# Global Middleware [cite: 402, 403]
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    print(
        f"LOG: {request.method} {request.url.path} - Time: {time.time() - start_time:.4f}s"
    )
    return response


# modular routes
app.include_router(students.router)
app.include_router(courses.router)
app.include_router(auth.router)
