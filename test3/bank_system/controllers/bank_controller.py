from typing import Optional
from peewee import fn
from models import Account, BankTransaction
from database import db


# ===========================
# 创建账户
# ===========================
def create_account(name: str, balance: int = 0) -> Optional[int]:
    try:
        a = Account.create(name=name, balance=balance)
        return a.id
    except Exception:
        return None


# ===========================
# 存款（并发安全）
# ===========================
def deposit(account_id: int, amount: int) -> bool:
    if amount <= 0:
        return False

    try:
        with db.atomic():  # 开启事务
            # 使用 SELECT ... FOR UPDATE 加锁
            a = (
                Account.select()
                .where(Account.id == account_id)
                .for_update()  # 行级锁！
                .get()
            )

            # 执行更新
            Account.update({Account.balance: Account.balance + amount}).where(
                Account.id == account_id
            ).execute()

            BankTransaction.create(type="deposit", amount=amount, to_account=a)
        return True

    except Exception as e:
        print("deposit error:", e)
        return False


# ===========================
# 取款（并发安全）
# ===========================
def withdraw(account_id: int, amount: int) -> bool:
    if amount <= 0:
        return False

    try:
        with db.atomic():  # 开启事务
            # 加锁读取
            a = Account.select().where(Account.id == account_id).for_update().get()

            # 余额检查必须在事务内
            if a.balance < amount:
                return False

            # 执行扣款
            Account.update({Account.balance: Account.balance - amount}).where(
                Account.id == account_id
            ).execute()

            BankTransaction.create(type="withdraw", amount=amount, from_account=a)
        return True

    except Exception as e:
        print("withdraw error:", e)
        return False


# ===========================
# 转账（并发安全）
# ===========================
def transfer(from_id: int, to_id: int, amount: int) -> bool:
    if from_id == to_id or amount <= 0:
        return False

    try:
        with db.atomic():  # 一个事务中执行所有步骤
            # 给两个账户上锁，按 id 排序避免死锁
            ids = sorted([from_id, to_id])
            acc_list = Account.select().where(Account.id.in_(ids)).for_update()

            accounts = {acc.id: acc for acc in acc_list}
            if from_id not in accounts or to_id not in accounts:
                return False

            src = accounts[from_id]
            dst = accounts[to_id]

            if src.balance < amount:
                return False

            # 扣钱、加钱
            Account.update({Account.balance: Account.balance - amount}).where(
                Account.id == from_id
            ).execute()

            Account.update({Account.balance: Account.balance + amount}).where(
                Account.id == to_id
            ).execute()

            BankTransaction.create(
                type="transfer", amount=amount, from_account=src, to_account=dst
            )
        return True

    except Exception as e:
        print("transfer error:", e)
        return False
