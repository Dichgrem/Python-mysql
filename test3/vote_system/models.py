from datetime import datetime
from peewee import Model, AutoField, CharField, IntegerField, ForeignKeyField, DateTimeField
from database import db

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    id = AutoField()
    username = CharField(unique=True, max_length=50)
    password_hash = CharField(max_length=128)
    created_at = DateTimeField(default=datetime.now)

class Option(BaseModel):
    id = AutoField()
    title = CharField(unique=True, max_length=100)
    vote_count = IntegerField(default=0)

# class UserVote(BaseModel):
#     id = AutoField()
#     user = ForeignKeyField(User, backref='votes')
#     option = ForeignKeyField(Option, backref='user_votes')
#     created_at = DateTimeField(default=datetime.now)

class UserVote(BaseModel):
    id = AutoField()
    user = ForeignKeyField(User, backref='votes')
    option = ForeignKeyField(Option, backref='user_votes')
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        indexes = (
            (('user',), True),  # 用户只能投一次
        )
