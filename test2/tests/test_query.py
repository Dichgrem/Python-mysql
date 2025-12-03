from models import create_tables
from models.student import Student

def run():
    create_tables()
    rows = Student.select().where(Student.age > 20)
    for r in rows:
        print(f"{r.student_id} {r.name} {r.age}")

if __name__ == '__main__':
    run()
