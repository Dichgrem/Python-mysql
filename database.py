# database.py
import mysql.connector
from mysql.connector import Error
from typing import Optional, List
from config import DB_CONFIG
from models import Student, Course, SC
from datetime import datetime

# ---- SQL 表定义 ----
TABLE_DEFINITIONS = {
    "student": """
        CREATE TABLE IF NOT EXISTS student (
            student_id VARCHAR(10) PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            gender ENUM('男','女') NOT NULL,
            age INT CHECK (age >= 0 AND age <= 100),
            email VARCHAR(100) UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """,
    "course": """
        CREATE TABLE IF NOT EXISTS course (
            course_id VARCHAR(10) PRIMARY KEY,
            course_name VARCHAR(100) NOT NULL,
            credit DECIMAL(2,1) NOT NULL CHECK (credit >= 0 AND credit <= 10),
            teacher VARCHAR(50) NOT NULL,
            max_students INT DEFAULT 50
        )
    """,
    "sc": """
        CREATE TABLE IF NOT EXISTS sc (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_id VARCHAR(10) NOT NULL,
            course_id VARCHAR(10) NOT NULL,
            score DECIMAL(4,1) CHECK (score >= 0 AND score <= 100),
            selected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES student(student_id) ON DELETE CASCADE,
            FOREIGN KEY (course_id) REFERENCES course(course_id) ON DELETE CASCADE,
            UNIQUE KEY unique_student_course (student_id, course_id)
        )
    """,
}

# ---- 初始示例数据 ----
INITIAL_DATA = {
    "students": [
        ("S001", "张三", "男", 20, "zhangsan@example.com"),
        ("S002", "李四", "女", 21, "lisi@example.com"),
        ("S003", "王五", "男", 19, "wangwu@example.com"),
        ("S004", "赵六", "女", 22, "zhaoliu@example.com"),
    ],
    "courses": [
        ("C001", "数据库原理", 3.0, "王教授", 100),
        ("C002", "数据结构", 4.0, "李教授", 80),
        ("C003", "操作系统", 3.5, "张教授", 60),
        ("C004", "计算机网络", 3.0, "刘教授", 70),
    ],
    "sc_records": [
        ("S001", "C001", 85.5),
        ("S001", "C002", 92.0),
        ("S002", "C001", 78.0),
        ("S002", "C003", 88.5),
        ("S003", "C002", 95.0),
        ("S004", "C004", 76.5),
    ],
}


class DatabaseManager:
    def __init__(
        self, host: str, user: str, password: str, database: Optional[str] = None
    ):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection: Optional[mysql.connector.connection_cext.CMySQLConnection] = (
            None
        )

    def connect(self) -> bool:
        try:
            params = {"host": self.host, "user": self.user, "password": self.password}
            if self.database:
                params["database"] = self.database
            self.connection = mysql.connector.connect(**params)
            if self.connection.is_connected():
                return True
            return False
        except Error as e:
            print(f"连接错误: {e}")
            return False

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()

    # ---------- 表与数据初始化 ----------
    def create_tables(self) -> bool:
        try:
            cursor = self.connection.cursor()
            for name, sql in TABLE_DEFINITIONS.items():
                cursor.execute(sql)
            self.connection.commit()
            cursor.close()
            print("数据表创建/确认完成")
            return True
        except Error as e:
            print(f"创建数据表错误: {e}")
            if self.connection:
                self.connection.rollback()
            return False

    def insert_initial_data(self) -> bool:
        try:
            cursor = self.connection.cursor()
            # students
            student_sql = "INSERT INTO student (student_id, name, gender, age, email) VALUES (%s, %s, %s, %s, %s)"
            cursor.executemany(student_sql, INITIAL_DATA["students"])
            # courses
            course_sql = "INSERT INTO course (course_id, course_name, credit, teacher, max_students) VALUES (%s, %s, %s, %s, %s)"
            cursor.executemany(course_sql, INITIAL_DATA["courses"])
            # sc
            sc_sql = "INSERT INTO sc (student_id, course_id, score) VALUES (%s, %s, %s)"
            cursor.executemany(sc_sql, INITIAL_DATA["sc_records"])
            self.connection.commit()
            cursor.close()
            print("初始数据插入完成")
            return True
        except Error as e:
            print(f"插入初始数据错误: {e}")
            if self.connection:
                self.connection.rollback()
            return False

    # ---------- Student CRUD & Query ----------
    def add_student(self, student: Student) -> bool:
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO student (student_id, name, gender, age, email) VALUES (%s, %s, %s, %s, %s)",
                (
                    student.student_id,
                    student.name,
                    student.gender,
                    student.age,
                    student.email,
                ),
            )
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            # 可能是主键冲突或其他错误
            print(f"add_student 错误: {e}")
            if self.connection:
                self.connection.rollback()
            return False

    def update_student(
        self,
        student_id: str,
        name: Optional[str] = None,
        gender: Optional[str] = None,
        age: Optional[int] = None,
        email: Optional[str] = None,
    ) -> bool:
        fields = []
        values = []
        if name is not None:
            fields.append("name = %s")
            values.append(name)
        if gender is not None:
            fields.append("gender = %s")
            values.append(gender)
        if age is not None:
            fields.append("age = %s")
            values.append(age)
        if email is not None:
            fields.append("email = %s")
            values.append(email)
        if not fields:
            return False
        values.append(student_id)
        sql = f"UPDATE student SET {', '.join(fields)} WHERE student_id = %s"
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, tuple(values))
            self.connection.commit()
            rc = cursor.rowcount
            cursor.close()
            return rc > 0
        except Error as e:
            print(f"update_student 错误: {e}")
            if self.connection:
                self.connection.rollback()
            return False

    def delete_student(self, student_id: str) -> bool:
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM student WHERE student_id = %s", (student_id,))
            self.connection.commit()
            rc = cursor.rowcount
            cursor.close()
            return rc > 0
        except Error as e:
            print(f"delete_student 错误: {e}")
            if self.connection:
                self.connection.rollback()
            return False

    def query_students_by_min_age(self, min_age: int) -> List[Student]:
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(
                "SELECT student_id, name, gender, age, email, created_at FROM student WHERE age > %s",
                (min_age,),
            )
            rows = cursor.fetchall()
            cursor.close()
            result = []
            for r in rows:
                result.append(
                    Student(
                        student_id=r["student_id"],
                        name=r["name"],
                        gender=r["gender"],
                        age=r["age"],
                        email=r.get("email"),
                        created_at=r.get("created_at"),
                    )
                )
            return result
        except Error as e:
            print(f"查询学生数据错误: {e}")
            return []

    # ---------- Course CRUD & Query ----------
    def add_course(self, course: Course) -> bool:
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO course (course_id, course_name, credit, teacher, max_students) VALUES (%s, %s, %s, %s, %s)",
                (
                    course.course_id,
                    course.course_name,
                    float(course.credit),
                    course.teacher,
                    course.max_students,
                ),
            )
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"add_course 错误: {e}")
            if self.connection:
                self.connection.rollback()
            return False

    def delete_course(self, course_id: str) -> bool:
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM course WHERE course_id = %s", (course_id,))
            self.connection.commit()
            rc = cursor.rowcount
            cursor.close()
            return rc > 0
        except Error as e:
            print(f"delete_course 错误: {e}")
            if self.connection:
                self.connection.rollback()
            return False

    # ---------- SC (选课) 操作 ----------
    def add_sc(self, sc: SC) -> bool:
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO sc (student_id, course_id, score) VALUES (%s, %s, %s)",
                (sc.student_id, sc.course_id, sc.score),
            )
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"add_sc 错误: {e}")
            if self.connection:
                self.connection.rollback()
            return False

    def update_sc_score(self, student_id: str, course_id: str, score: float) -> bool:
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "UPDATE sc SET score = %s WHERE student_id = %s AND course_id = %s",
                (score, student_id, course_id),
            )
            self.connection.commit()
            rc = cursor.rowcount
            cursor.close()
            return rc > 0
        except Error as e:
            print(f"update_sc_score 错误: {e}")
            if self.connection:
                self.connection.rollback()
            return False

    def delete_sc(self, student_id: str, course_id: str) -> bool:
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "DELETE FROM sc WHERE student_id = %s AND course_id = %s",
                (student_id, course_id),
            )
            self.connection.commit()
            rc = cursor.rowcount
            cursor.close()
            return rc > 0
        except Error as e:
            print(f"delete_sc 错误: {e}")
            if self.connection:
                self.connection.rollback()
            return False

    # ---------- 额外查询：学生的课程和课程的学生 ----------
    def query_courses_by_student(self, student_id: str) -> List[Course]:
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(
                "SELECT c.course_id, c.course_name, c.credit, c.teacher, c.max_students "
                "FROM course c JOIN sc s ON c.course_id = s.course_id WHERE s.student_id = %s",
                (student_id,),
            )
            rows = cursor.fetchall()
            cursor.close()
            return [
                Course(
                    course_id=r["course_id"],
                    course_name=r["course_name"],
                    credit=float(r["credit"]),
                    teacher=r["teacher"],
                    max_students=int(r["max_students"]),
                )
                for r in rows
            ]
        except Error as e:
            print(f"query_courses_by_student 错误: {e}")
            return []

    def query_students_by_course(self, course_id: str) -> List[Student]:
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(
                "SELECT s.student_id, s.name, s.gender, s.age, s.email, s.created_at "
                "FROM student s JOIN sc sc ON s.student_id = sc.student_id WHERE sc.course_id = %s",
                (course_id,),
            )
            rows = cursor.fetchall()
            cursor.close()
            return [
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
        except Error as e:
            print(f"query_students_by_course 错误: {e}")
            return []


# 工厂函数（main.py 调用）
def create_database_manager():
    return DatabaseManager(
        host=DB_CONFIG.get("host"),
        user=DB_CONFIG.get("user"),
        password=DB_CONFIG.get("password"),
        database=DB_CONFIG.get("database"),
    )
