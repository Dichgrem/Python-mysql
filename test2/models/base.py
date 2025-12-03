from peewee import Model, MySQLDatabase, SqliteDatabase, DatabaseProxy
from config import DB_BACKEND, MYSQL_CONFIG, SQLITE_CONFIG

db = DatabaseProxy()


def init_db():
    if DB_BACKEND == "mysql":
        database = MySQLDatabase(
            MYSQL_CONFIG["database"],
            host=MYSQL_CONFIG["host"],
            user=MYSQL_CONFIG["user"],
            password=MYSQL_CONFIG["password"],
            port=MYSQL_CONFIG["port"],
            charset=MYSQL_CONFIG["charset"],
        )
    else:
        database = SqliteDatabase(
            SQLITE_CONFIG["path"],
            pragmas={
                "foreign_keys": 1,
                "journal_mode": "wal",
                "cache_size": -1024 * 64,
            },
        )

    db.initialize(database)
    database.connect()
    return database


class BaseModel(Model):
    class Meta:
        database = db
