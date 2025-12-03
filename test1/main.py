# main.py
from database import create_database_manager
from models import Student, Course, SC


def prompt_yes_no(prompt: str) -> bool:
    a = input(prompt).strip().lower()
    return a == "y" or a == "yes"


def print_students(students):
    if not students:
        print("(无)")
        return
    for s in students:
        created = s.created_at if getattr(s, "created_at", None) else ""
        print(f"{s.student_id}\t{s.name}\t{s.gender}\t{s.age}\t{s.email}\t{created}")


def print_courses(courses):
    if not courses:
        print("(无)")
        return
    for c in courses:
        print(
            f"{c.course_id}\t{c.course_name}\t{c.credit}\t{c.teacher}\t{c.max_students}"
        )


def main():
    db_manager = create_database_manager()

    # 连接
    if not db_manager.connect():
        print("无法连接到数据库，请检查配置")
        return
    print("数据库连接成功")

    # 创建表
    if not db_manager.create_tables():
        print("创建数据表失败")
        db_manager.close()
        return
    print("数据表创建/确认完成")

    # 初始化数据提示（保留原有交互）
    if prompt_yes_no("是否初始化示例数据（会插入若干示例记录）? (y/n): "):
        if db_manager.insert_initial_data():
            print("初始数据插入完成")
        else:
            print("插入初始数据错误，可能已存在（请先清空数据库或跳过）")
    else:
        print("跳过示例数据插入")

    # 进入交互菜单
    while True:
        print(
            """
==== 学生选课管理（交互菜单） ====
1  添加学生
2  更新学生
3  删除学生
4  查询所有学生
5  查询年龄大于 X 的学生

6  添加课程
7  删除课程
8  查询所有课程

9  学生选课（添加选课记录）
10 更新选课成绩
11 退选（删除选课记录）
12 查询某学生的课程
13 查询某课程的学生

0  退出
=================================
"""
        )
        choice = input("请输入编号: ").strip()
        try:
            if choice == "1":
                sid = input("student_id: ").strip()
                name = input("name: ").strip()
                gender = input("gender (男/女): ").strip()
                age = int(input("age: ").strip())
                email = input("email (可空): ").strip() or None
                s = Student(
                    student_id=sid, name=name, gender=gender, age=age, email=email
                )
                ok = db_manager.add_student(s)
                print("ADD_OK" if ok else "ADD_FAIL")

            elif choice == "2":
                sid = input("要更新的 student_id: ").strip()
                name = input("new name (回车跳过): ").strip() or None
                gender = input("new gender (回车跳过): ").strip() or None
                age_input = input("new age (回车跳过): ").strip()
                age = int(age_input) if age_input else None
                email = input("new email (回车跳过): ").strip() or None
                ok = db_manager.update_student(
                    sid, name=name, gender=gender, age=age, email=email
                )
                print("UPDATE_OK" if ok else "UPDATE_FAIL")

            elif choice == "3":
                sid = input("要删除的 student_id: ").strip()
                ok = db_manager.delete_student(sid)
                print("DELETE_OK" if ok else "DELETE_FAIL")

            elif choice == "4":
                # 查询所有学生（简单 SELECT *）
                cursor = db_manager.connection.cursor(dictionary=True)
                cursor.execute(
                    "SELECT student_id, name, gender, age, email, created_at FROM student"
                )
                rows = cursor.fetchall()
                cursor.close()
                students = [
                    Student(
                        student_id=r["student_id"],
                        name=r["name"],
                        gender=r["gender"],
                        age=r["age"],
                        email=r.get("email"),
                        created_at=r.get("created_at"),
                    )
                    for r in rows
                ]
                print_students(students)

            elif choice == "5":
                x = int(input("请输入最小年龄 X: ").strip())
                res = db_manager.query_students_by_min_age(x)
                print_students(res)

            elif choice == "6":
                cid = input("course_id: ").strip()
                cname = input("course_name: ").strip()
                credit = float(input("credit (如 3.0): ").strip())
                teacher = input("teacher: ").strip()
                max_s = int(input("max_students: ").strip())
                c = Course(
                    course_id=cid,
                    course_name=cname,
                    credit=credit,
                    teacher=teacher,
                    max_students=max_s,
                )
                ok = db_manager.add_course(c)
                print("ADD_COURSE_OK" if ok else "ADD_COURSE_FAIL")

            elif choice == "7":
                cid = input("要删除的 course_id: ").strip()
                ok = db_manager.delete_course(cid)
                print("DELETE_COURSE_OK" if ok else "DELETE_COURSE_FAIL")

            elif choice == "8":
                cursor = db_manager.connection.cursor(dictionary=True)
                cursor.execute(
                    "SELECT course_id, course_name, credit, teacher, max_students FROM course"
                )
                rows = cursor.fetchall()
                cursor.close()
                courses = [
                    Course(
                        course_id=r["course_id"],
                        course_name=r["course_name"],
                        credit=float(r["credit"]),
                        teacher=r["teacher"],
                        max_students=int(r["max_students"]),
                    )
                    for r in rows
                ]
                print_courses(courses)

            elif choice == "9":
                sid = input("student_id: ").strip()
                cid = input("course_id: ").strip()
                sc = SC(id=None, student_id=sid, course_id=cid, score=None)
                ok = db_manager.add_sc(sc)
                print("选课 OK" if ok else "选课 FAIL")

            elif choice == "10":
                sid = input("student_id: ").strip()
                cid = input("course_id: ").strip()
                score = float(input("score (0-100): ").strip())
                ok = db_manager.update_sc_score(sid, cid, score)
                print("更新成绩 OK" if ok else "更新成绩 FAIL")

            elif choice == "11":
                sid = input("student_id: ").strip()
                cid = input("course_id: ").strip()
                ok = db_manager.delete_sc(sid, cid)
                print("退选 OK" if ok else "退选 FAIL")

            elif choice == "12":
                sid = input("student_id: ").strip()
                courses = db_manager.query_courses_by_student(sid)
                print_courses(courses)

            elif choice == "13":
                cid = input("course_id: ").strip()
                students = db_manager.query_students_by_course(cid)
                print_students(students)

            elif choice == "0":
                print("退出。")
                break

            else:
                print("无效选项，请重试。")

        except Exception as e:
            # 捕获任何未预期的错误，不让程序崩掉
            print("操作时出错:", e)

    db_manager.close()


if __name__ == "__main__":
    main()
