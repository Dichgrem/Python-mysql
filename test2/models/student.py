from peewee import CharField, IntegerField, DateTimeField
from .base import BaseModel
from datetime import datetime

class Student(BaseModel):
    student_id = CharField(primary_key=True, max_length=10)
    name = CharField(max_length=50)
    gender = CharField(max_length=2)
    age = IntegerField()
    email = CharField(max_length=100, null=True)
    created_at = DateTimeField(default=datetime.now)

    @classmethod
    def get_by_name(cls, name: str):
        return list(cls.select().where(cls.name == name))
