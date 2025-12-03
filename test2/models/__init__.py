from .base import init_db
from .student import Student
from .course import Course
from .sc import SC


def create_tables():
    db = init_db()
    db.create_tables([Student, Course, SC])
    return db
