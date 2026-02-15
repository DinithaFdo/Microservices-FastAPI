from fastapi import APIRouter, Request, Depends
from utils.forwarder import forward_request
from auth import verify_token

router = APIRouter(prefix="/gateway/students", tags=["Students"])


@router.get("/")
async def get_all_students(token: dict = Depends(verify_token)):
    return await forward_request("student", "/api/students", "GET")


@router.get("/{student_id}")
async def get_student(student_id: int, token: dict = Depends(verify_token)):
    return await forward_request("student", f"/api/students/{student_id}", "GET")


@router.post("/")
async def create_student(request: Request, token: dict = Depends(verify_token)):
    body = await request.json()
    return await forward_request("student", "/api/students", "POST", json=body)


@router.put("/{student_id}")
async def update_student(
    student_id: int, request: Request, token: dict = Depends(verify_token)
):
    body = await request.json()
    return await forward_request(
        "student", f"/api/students/{student_id}", "PUT", json=body
    )


@router.delete("/{student_id}")
async def delete_student(student_id: int, token: dict = Depends(verify_token)):
    return await forward_request("student", f"/api/students/{student_id}", "DELETE")
