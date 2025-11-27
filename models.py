# models.py
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Student:
    student_id: str
    name: str
    gender: str
    age: int
    email: Optional[str] = None
    created_at: Optional[datetime] = None


@dataclass
class Course:
    course_id: str
    course_name: str
    credit: float
    teacher: str
    max_students: int


@dataclass
class SC:
    id: Optional[int]
    student_id: str
    course_id: str
    score: Optional[float] = None
    selected_at: Optional[datetime] = None
