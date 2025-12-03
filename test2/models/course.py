from peewee import CharField, DecimalField, IntegerField
from .base import BaseModel


class Course(BaseModel):
    course_id = CharField(primary_key=True, max_length=10)
    course_name = CharField(max_length=100)
    credit = DecimalField(max_digits=2, decimal_places=1)
    teacher = CharField(max_length=50)
    max_students = IntegerField(default=50)

    @classmethod
    def get_by_name(cls, name: str):
        return list(cls.select().where(cls.course_name == name))
