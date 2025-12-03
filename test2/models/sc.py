from peewee import AutoField, DecimalField, ForeignKeyField, DateTimeField
from datetime import datetime
from .base import BaseModel
from .student import Student
from .course import Course


class SC(BaseModel):
    id = AutoField()
    student = ForeignKeyField(Student, backref="courses", on_delete="CASCADE")
    course = ForeignKeyField(Course, backref="students", on_delete="CASCADE")
    score = DecimalField(max_digits=4, decimal_places=1, null=True)
    selected_at = DateTimeField(default=datetime.now)

    @classmethod
    def get_by_student_course(cls, student_id: str, course_id: str):
        return list(
            cls.select().where((cls.student == student_id) & (cls.course == course_id))
        )
