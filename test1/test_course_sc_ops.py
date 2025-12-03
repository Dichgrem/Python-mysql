# test_course_sc_ops.py
from database import create_database_manager
from models import Course, SC


def run():
    db = create_database_manager()
    if not db.connect():
        print("无法连接数据库")
        return

    c = Course(
        course_id="C101",
        course_name="数据库系统",
        credit=3.0,
        teacher="张老师",
        max_students=60,
    )
    print("添加课程:", "OK" if db.add_course(c) else "FAIL")

    sc = SC(id=None, student_id="S001", course_id="C101", score=None)
    print("学生选课:", "OK" if db.add_sc(sc) else "FAIL")

    print("更新成绩:", "OK" if db.update_sc_score("S001", "C101", 95.5) else "FAIL")

    print(
        "查询学生 S001 的课程:",
        [
            c.course_id + ":" + c.course_name
            for c in db.query_courses_by_student("S001")
        ],
    )

    print("删除选课:", "OK" if db.delete_sc("S001", "C101") else "FAIL")
    print("删除课程:", "OK" if db.delete_course("C101") else "FAIL")

    db.close()


if __name__ == "__main__":
    run()
