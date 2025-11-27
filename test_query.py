# test_query.py
from database import create_database_manager


def query_students_over_20():
    db = create_database_manager()
    if not db.connect():
        print("无法连接数据库")
        return []
    students = db.query_students_by_min_age(20)
    db.close()
    return students


if __name__ == "__main__":
    for s in query_students_over_20():
        print(f"{s.student_id} {s.name} {s.age} {s.email}")
