from pydantic import BaseModel
from typing import Optional


class Course(BaseModel):
    id: int
    title: str
    code: str
    description: str


class CourseCreate(BaseModel):
    title: str
    code: str
    description: str


class CourseUpdate(BaseModel):
    title: Optional[str] = None
    code: Optional[int] = None
    description: Optional[str] = None
