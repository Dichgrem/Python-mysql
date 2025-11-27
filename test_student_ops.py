# test_student_ops.py
from database import create_database_manager
from models import Student


def run():
    db = create_database_manager()
    if not db.connect():
        print("无法连接数据库")
        return

    s = Student(
        student_id="S008", name="学生008", gender="男", age=23, email="s008@example.com"
    )
    print("添加学生:", "OK" if db.add_student(s) else "FAIL")
    print(
        "更新学生:",
        "OK" if db.update_student("S008", email="s008-new@example.com") else "FAIL",
    )
    print("删除学生:", "OK" if db.delete_student("S008") else "FAIL")

    db.close()


if __name__ == "__main__":
    run()
