from fastapi import APIRouter, Request, Depends
from utils.forwarder import forward_request
from auth import verify_token

router = APIRouter(prefix="/gateway/courses", tags=["Courses"])


@router.get("/")
async def get_all_courses(token: dict = Depends(verify_token)):
    return await forward_request("course", "/api/courses", "GET")


@router.get("/{course_id}")
async def get_course(course_id: int, token: dict = Depends(verify_token)):
    return await forward_request("course", f"/api/courses/{course_id}", "GET")


@router.post("/")
async def create_course(request: Request, token: dict = Depends(verify_token)):
    body = await request.json()
    return await forward_request("course", "/api/courses", "POST", json=body)


@router.put("/{course_id}")
async def update_course(
    course_id: int, request: Request, token: dict = Depends(verify_token)
):
    body = await request.json()
    return await forward_request(
        "course", f"/api/courses/{course_id}", "PUT", json=body
    )


@router.delete("/{course_id}")
async def delete_course(course_id: int, token: dict = Depends(verify_token)):
    return await forward_request("course", f"/api/courses/{course_id}", "DELETE")
