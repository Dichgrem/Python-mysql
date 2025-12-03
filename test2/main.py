from models import create_tables
from models.student import Student
from models.course import Course
from models.sc import SC

def main():
    db = create_tables()

    Student.insert_many([
        {'student_id': 'S001', 'name': '张三', 'gender': '男', 'age': 20, 'email': 'zhangsan@example.com'},
        {'student_id': 'S002', 'name': '李四', 'gender': '女', 'age': 21, 'email': 'lisi@example.com'},
        {'student_id': 'S003', 'name': '王五', 'gender': '男', 'age': 19, 'email': 'wangwu@example.com'},
        {'student_id': 'S004', 'name': '赵六', 'gender': '女', 'age': 22, 'email': 'zhaoliu@example.com'}
    ]).execute()

    Course.insert_many([
        {'course_id': 'C001', 'course_name': '数据库原理', 'credit': 3.0, 'teacher': '王教授', 'max_students': 100},
        {'course_id': 'C002', 'course_name': '数据结构', 'credit': 4.0, 'teacher': '李教授', 'max_students': 80},
        {'course_id': 'C003', 'course_name': '操作系统', 'credit': 3.5, 'teacher': '张教授', 'max_students': 60},
        {'course_id': 'C004', 'course_name': '计算机网络', 'credit': 3.0, 'teacher': '刘教授', 'max_students': 70}
    ]).execute()

    SC.insert_many([
        {'student': 'S001', 'course': 'C001', 'score': 85.5},
        {'student': 'S001', 'course': 'C002', 'score': 92.0},
        {'student': 'S002', 'course': 'C001', 'score': 78.0},
        {'student': 'S002', 'course': 'C003', 'score': 88.5},
        {'student': 'S003', 'course': 'C002', 'score': 95.0},
        {'student': 'S004', 'course': 'C004', 'score': 76.5}
    ]).execute()

if __name__ == '__main__':
    main()
