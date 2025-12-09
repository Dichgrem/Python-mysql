from datetime import datetime
from peewee import Model, AutoField, CharField, IntegerField, ForeignKeyField, DateTimeField
from database import db

class BaseModel(Model):
    class Meta:
        database = db

class Account(BaseModel):
    id = AutoField()
    name = CharField(unique=True, max_length=50)
    balance = IntegerField(default=0)
    created_at = DateTimeField(default=datetime.now)

class BankTransaction(BaseModel):
    id = AutoField()
    type = CharField(max_length=20)
    amount = IntegerField()
    from_account = ForeignKeyField(Account, backref='outgoing', null=True)
    to_account = ForeignKeyField(Account, backref='incoming', null=True)
    created_at = DateTimeField(default=datetime.now)

