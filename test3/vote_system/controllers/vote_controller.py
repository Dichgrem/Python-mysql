import hashlib
import time
from typing import Optional
from peewee import fn
from models import User, Option, UserVote
from models import db, UserVote, Option, User
from peewee import IntegrityError

def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def register(username: str, password: str) -> Optional[int]:
    try:
        u = User.create(username=username, password_hash=_hash_password(password))
        return u.id
    except Exception:
        return None

def login(username: str, password: str) -> Optional[int]:
    p = _hash_password(password)
    u = User.select().where((User.username == username) & (User.password_hash == p)).first()
    if not u:
        return None
    return u.id

# def vote(user_id: int, option_id: int) -> bool:
#     user = User.get_or_none(User.id == user_id)
#     option = Option.get_or_none(Option.id == option_id)
#     if not user or not option:
#         return False
#     exists = UserVote.select().where(UserVote.user == user).exists()
#     time.sleep(1.5)
#     if exists:
#         return False
#     try:
#         UserVote.create(user=user, option=option)
#         Option.update({Option.vote_count: Option.vote_count + 1}).where(Option.id == option_id).execute()
#         return True
#     except Exception:
#         return False

def vote(user_id: int, option_id: int) -> bool:
    user = User.get_or_none(User.id == user_id)
    option = Option.get_or_none(Option.id == option_id)
    if not user or not option:
        return False

    try:
        with db.atomic():  # 开启事务，保证原子性
            # 直接插入，如果并发会触发唯一约束
            UserVote.create(user=user, option=option)

            # 原子自增
            Option.update(
                {Option.vote_count: Option.vote_count + 1}
            ).where(
                Option.id == option_id
            ).execute()

        return True

    except IntegrityError:
        # 说明已经被其他线程插入了（并发冲突）
        return False

def cancel(user_id: int) -> bool:
    user = User.get_or_none(User.id == user_id)
    if not user:
        return False
    uv = UserVote.select().where(UserVote.user == user).order_by(UserVote.created_at.desc()).first()
    time.sleep(1.5)
    if not uv:
        return False
    try:
        opt_id = uv.option_id
        uv.delete_instance()
        Option.update({Option.vote_count: Option.vote_count - 1}).where(Option.id == opt_id).execute()
        return True
    except Exception as e:
        print(e)
        return False

