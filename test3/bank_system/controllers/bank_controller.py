import time
from typing import Optional
from peewee import fn
from models import Account, BankTransaction

def create_account(name: str, balance: int = 0) -> Optional[int]:
    try:
        a = Account.create(name=name, balance=balance)
        return a.id
    except Exception:
        return None

def deposit(account_id: int, amount: int) -> bool:
    a = Account.get_or_none(Account.id == account_id)
    if not a or amount <= 0:
        return False
    time.sleep(1.5)
    try:
        Account.update({Account.balance: Account.balance + amount}).where(Account.id == account_id).execute()
        BankTransaction.create(type='deposit', amount=amount, to_account=a)
        return True
    except Exception:
        return False

def withdraw(account_id: int, amount: int) -> bool:
    a = Account.get_or_none(Account.id == account_id)
    if not a or amount <= 0:
        return False
    if a.balance < amount:
        return False
    time.sleep(1.5)
    try:
        Account.update({Account.balance: Account.balance - amount}).where(Account.id == account_id).execute()
        BankTransaction.create(type='withdraw', amount=amount, from_account=a)
        return True
    except Exception:
        return False

def transfer(from_id: int, to_id: int, amount: int) -> bool:
    if from_id == to_id:
        return False
    src = Account.get_or_none(Account.id == from_id)
    dst = Account.get_or_none(Account.id == to_id)
    if not src or not dst or amount <= 0:
        return False
    if src.balance < amount:
        return False
    time.sleep(1.0)
    try:
        Account.update({Account.balance: Account.balance - amount}).where(Account.id == from_id).execute()
        time.sleep(1.0)
        Account.update({Account.balance: Account.balance + amount}).where(Account.id == to_id).execute()
        BankTransaction.create(type='transfer', amount=amount, from_account=src, to_account=dst)
        return True
    except Exception:
        return False

