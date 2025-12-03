import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from models import create_tables
from models.student import Student
from models.course import Course
from models.sc import SC
from datetime import datetime


# ========== 学生管理模块 ==========
def student_operations():
    """学生管理交互菜单"""
    while True:
        print("\n" + "=" * 50)
        print("学生管理")
        print("=" * 50)
        print("1. 查询所有学生")
        print("2. 按姓名查询")
        print("3. 按年龄范围查询")
        print("4. 添加学生")
        print("5. 修改学生信息")
        print("6. 删除学生")
        print("0. 返回")
        print("=" * 50)

        choice = input("请选择: ").strip()

        if choice == "1":
            list_all_students()
        elif choice == "2":
            search_student_by_name()
        elif choice == "3":
            search_student_by_age()
        elif choice == "4":
            create_student()
        elif choice == "5":
            modify_student()
        elif choice == "6":
            remove_student()
        elif choice == "0":
            break


def list_all_students():
    """查询所有学生"""
    students = Student.select()
    print("\n所有学生信息:")
    for s in students:
        print(
            f"学号:{s.student_id} 姓名:{s.name} 性别:{s.gender} 年龄:{s.age} 邮箱:{s.email}"
        )


def search_student_by_name():
    """按姓名查询"""
    name = input("请输入姓名: ").strip()
    students = Student.get_by_name(name)
    if students:
        for s in students:
            print(f"学号:{s.student_id} 姓名:{s.name} 性别:{s.gender} 年龄:{s.age}")
    else:
        print("未找到该学生")


def search_student_by_age():
    """按年龄范围查询"""
    min_age = int(input("最小年龄: "))
    max_age = int(input("最大年龄: "))
    students = Student.select().where(
        (Student.age >= min_age) & (Student.age <= max_age)
    )
    for s in students:
        print(f"学号:{s.student_id} 姓名:{s.name} 年龄:{s.age}")


def create_student():
    """添加学生"""
    print("\n添加新学生")
    sid = input("学号: ").strip()
    if Student.select().where(Student.student_id == sid).exists():
        print("学号已存在！")
        return
    name = input("姓名: ").strip()
    gender = input("性别: ").strip()
    age = int(input("年龄: "))
    email = input("邮箱: ").strip()

    Student.create(
        student_id=sid,
        name=name,
        gender=gender,
        age=age,
        email=email,
        created_at=datetime.now(),
    )
    print("添加成功！")


def modify_student():
    """修改学生信息"""
    sid = input("请输入学号: ").strip()
    try:
        s = Student.get(Student.student_id == sid)
        print(f"当前: {s.name} {s.gender} {s.age} {s.email}")

        name = input(f"姓名[{s.name}]: ").strip() or s.name
        gender = input(f"性别[{s.gender}]: ").strip() or s.gender
        age = input(f"年龄[{s.age}]: ").strip()
        age = int(age) if age else s.age
        email = input(f"邮箱[{s.email}]: ").strip() or s.email

        s.name = name
        s.gender = gender
        s.age = age
        s.email = email
        s.save()
        print("修改成功！")
    except Student.DoesNotExist:
        print("学号不存在！")


def remove_student():
    """删除学生"""
    sid = input("请输入学号: ").strip()
    try:
        s = Student.get(Student.student_id == sid)
        confirm = input(f"确认删除 {s.name} (y/n)? ").lower()
        if confirm == "y":
            s.delete_instance()
            print("删除成功！")
    except Student.DoesNotExist:
        print("学号不存在！")


# ========== 课程管理模块 ==========
def course_operations():
    """课程管理交互菜单"""
    while True:
        print("\n" + "=" * 50)
        print("课程管理")
        print("=" * 50)
        print("1. 查询所有课程")
        print("2. 按课程名查询")
        print("3. 按学分查询")
        print("4. 添加课程")
        print("5. 修改课程信息")
        print("6. 删除课程")
        print("0. 返回")
        print("=" * 50)

        choice = input("请选择: ").strip()

        if choice == "1":
            list_all_courses()
        elif choice == "2":
            search_course_by_name()
        elif choice == "3":
            search_course_by_credit()
        elif choice == "4":
            create_course()
        elif choice == "5":
            modify_course()
        elif choice == "6":
            remove_course()
        elif choice == "0":
            break


def list_all_courses():
    """查询所有课程"""
    courses = Course.select()
    print("\n所有课程信息:")
    for c in courses:
        print(
            f"课程号:{c.course_id} 课程名:{c.course_name} 学分:{c.credit} 教师:{c.teacher} 最大人数:{c.max_students}"
        )


def search_course_by_name():
    """按课程名查询"""
    name = input("请输入课程名: ").strip()
    courses = Course.get_by_name(name)
    if courses:
        for c in courses:
            print(
                f"课程号:{c.course_id} 课程名:{c.course_name} 学分:{c.credit} 教师:{c.teacher}"
            )
    else:
        print("未找到该课程")


def search_course_by_credit():
    """按学分查询"""
    min_credit = float(input("最小学分: "))
    max_credit = float(input("最大学分: "))
    courses = Course.select().where(
        (Course.credit >= min_credit) & (Course.credit <= max_credit)
    )
    for c in courses:
        print(f"课程号:{c.course_id} 课程名:{c.course_name} 学分:{c.credit}")


def create_course():
    """添加课程"""
    print("\n添加新课程")
    cid = input("课程号: ").strip()
    if Course.select().where(Course.course_id == cid).exists():
        print("课程号已存在！")
        return
    name = input("课程名: ").strip()
    credit = float(input("学分: "))
    teacher = input("教师: ").strip()
    max_students = int(input("最大人数: "))

    Course.create(
        course_id=cid,
        course_name=name,
        credit=credit,
        teacher=teacher,
        max_students=max_students,
    )
    print("添加成功！")


def modify_course():
    """修改课程信息"""
    cid = input("请输入课程号: ").strip()
    try:
        c = Course.get(Course.course_id == cid)
        print(f"当前: {c.course_name} {c.credit} {c.teacher} {c.max_students}")

        name = input(f"课程名[{c.course_name}]: ").strip() or c.course_name
        credit = input(f"学分[{c.credit}]: ").strip()
        credit = float(credit) if credit else c.credit
        teacher = input(f"教师[{c.teacher}]: ").strip() or c.teacher
        max_students = input(f"最大人数[{c.max_students}]: ").strip()
        max_students = int(max_students) if max_students else c.max_students

        c.course_name = name
        c.credit = credit
        c.teacher = teacher
        c.max_students = max_students
        c.save()
        print("修改成功！")
    except Course.DoesNotExist:
        print("课程号不存在！")


def remove_course():
    """删除课程"""
    cid = input("请输入课程号: ").strip()
    try:
        c = Course.get(Course.course_id == cid)
        confirm = input(f"确认删除 {c.course_name} (y/n)? ").lower()
        if confirm == "y":
            c.delete_instance()
            print("删除成功！")
    except Course.DoesNotExist:
        print("课程号不存在！")


# ========== 选课管理模块 ==========
def sc_operations():
    """选课管理交互菜单"""
    while True:
        print("\n" + "=" * 50)
        print("选课管理")
        print("=" * 50)
        print("1. 查询所有选课记录")
        print("2. 查询学生选课")
        print("3. 查询课程学生")
        print("4. 学生选课")
        print("5. 录入成绩")
        print("6. 退课")
        print("0. 返回")
        print("=" * 50)

        choice = input("请选择: ").strip()

        if choice == "1":
            list_all_sc()
        elif choice == "2":
            query_student_courses()
        elif choice == "3":
            query_course_students()
        elif choice == "4":
            enroll_course()
        elif choice == "5":
            input_score()
        elif choice == "6":
            drop_course()
        elif choice == "0":
            break


def list_all_sc():
    """查询所有选课记录"""
    records = SC.select()
    print("\n所有选课记录:")
    for sc in records:
        score = sc.score if sc.score else "未录入"
        print(
            f"学生:{sc.student.name}({sc.student.student_id}) 课程:{sc.course.course_name}({sc.course.course_id}) 成绩:{score}"
        )


def query_student_courses():
    """查询学生选课"""
    sid = input("请输入学号: ").strip()
    try:
        student = Student.get(Student.student_id == sid)
        records = SC.select().where(SC.student == sid)
        print(f"\n{student.name} 的选课:")
        for sc in records:
            score = sc.score if sc.score else "未录入"
            print(f"课程:{sc.course.course_name} 学分:{sc.course.credit} 成绩:{score}")
    except Student.DoesNotExist:
        print("学号不存在！")


def query_course_students():
    """查询课程学生"""
    cid = input("请输入课程号: ").strip()
    try:
        course = Course.get(Course.course_id == cid)
        records = SC.select().where(SC.course == cid)
        print(f"\n{course.course_name} 的学生:")
        for sc in records:
            score = sc.score if sc.score else "未录入"
            print(f"学生:{sc.student.name}({sc.student.student_id}) 成绩:{score}")
    except Course.DoesNotExist:
        print("课程号不存在！")


def enroll_course():
    """学生选课"""
    sid = input("学号: ").strip()
    cid = input("课程号: ").strip()

    try:
        student = Student.get(Student.student_id == sid)
        course = Course.get(Course.course_id == cid)

        if SC.select().where((SC.student == sid) & (SC.course == cid)).exists():
            print("已选过该课程！")
            return

        SC.create(student=sid, course=cid, score=None, selected_at=datetime.now())
        print(f"{student.name} 选修 {course.course_name} 成功！")
    except Student.DoesNotExist:
        print("学号不存在！")
    except Course.DoesNotExist:
        print("课程号不存在！")


def input_score():
    """录入成绩"""
    sid = input("学号: ").strip()
    cid = input("课程号: ").strip()

    records = SC.get_by_student_course(sid, cid)
    if records:
        sc = records[0]
        current = sc.score if sc.score else "未录入"
        print(f"当前成绩: {current}")
        score = float(input("新成绩: "))
        sc.score = score
        sc.save()
        print("录入成功！")
    else:
        print("未找到选课记录！")


def drop_course():
    """退课"""
    sid = input("学号: ").strip()
    cid = input("课程号: ").strip()

    records = SC.get_by_student_course(sid, cid)
    if records:
        sc = records[0]
        confirm = input(f"确认退选 {sc.course.course_name} (y/n)? ").lower()
        if confirm == "y":
            sc.delete_instance()
            print("退课成功！")
    else:
        print("未找到选课记录！")


# ========== 主菜单 ==========
def main():
    """主菜单"""
    create_tables()

    while True:
        print("\n" + "=" * 50)
        print("学生选课管理系统")
        print("=" * 50)
        print("1. 学生管理")
        print("2. 课程管理")
        print("3. 选课管理")
        print("0. 退出")
        print("=" * 50)

        choice = input("请选择: ").strip()

        if choice == "1":
            student_operations()
        elif choice == "2":
            course_operations()
        elif choice == "3":
            sc_operations()
        elif choice == "0":
            print("再见！")
            break
        else:
            print("无效选择！")


if __name__ == "__main__":
    main()
