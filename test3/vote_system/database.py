from peewee import MySQLDatabase, SqliteDatabase
from config import DB_CONFIG

if DB_CONFIG.get('engine') == 'sqlite':
    db = SqliteDatabase(
        DB_CONFIG['database'] + '.db',
        pragmas={
            'journal_mode': 'wal',
            'synchronous': 0,
            'foreign_keys': 1
        }
    )
else:
    db = MySQLDatabase(
        DB_CONFIG['database'],
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        port=DB_CONFIG.get('port', 3306)
    )

def connect_db():
    if db.is_closed():
        db.connect(reuse_if_open=True)

def close_db():
    if not db.is_closed():
        db.close()
