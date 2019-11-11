import psycopg2 as pg
from datetime import datetime


DATA = {
    'dbname': 'learningdb',
    'user': 'postgres',
    'password': '13524',
    'host': 'localhost',
    'port': '5432'
    }


def create_db():  # создает таблицы

    with pg.connect(**DATA) as conn:
        with conn.cursor() as curs:
            curs.execute("""CREATE TABLE student (
                    id serial PRIMARY KEY NOT NULL,
                    name varchar(100) NOT NULL,
                    gpa numeric(10, 2),
                    birth timestamp with time zone);
                    """)
            curs.execute("""CREATE TABLE course (
                    id serial PRIMARY KEY NOT NULL,
                    name varchar(100)) NOT NULL;
                    """)
            curs.execute("""CREATE TABLE student_course (
                    id serial PRIMARY KEY,
                    student_id INTEGER REFERENCES student(id),
                    course_id INTEGER REFERENCES  course(id));
                    """)


def create_course():
    name = (input('Введите название курса:'))
    with pg.connect(**DATA) as conn:
        with conn.cursor() as curs:
            curs.execute("insert into course (name) values (%s) RETURNING id", (name,))
            print('Курс {} создан с id: {}'.format(name, curs.fetchone()[0]))


def get_students(course_id):  # возвращает студентов определенного курса
    with pg.connect(**DATA) as conn:
        with conn.cursor() as curs:
            curs.execute("""select s.id, s.name, c.name from student_course sc
                        join student s on s.id = sc.student_id
                        join course c on c.id = sc.course_id
                        where c.id = %s
                        """, (course_id,))
            for row in curs:
                print('Курс {} - студент {} с id-{}'.format(row[2], row[1], row[0]))


def add_students(course_id, students):  # создает студентов и записывает их на курс
    conn = pg.connect(**DATA)
    curs = conn.cursor()
    curs.execute("select * from course where id = %s", (course_id,))
    id_course = curs.fetchone()
    if id_course:
        for item in students:
            curs.execute("insert into student (name, gpa, birth) values (%s, %s, %s) RETURNING id",
                        (item.get('name'), item.get('gpa'), item.get('birth')))
            ids = curs.fetchone()
            curs.execute("insert into student_course (student_id, course_id) values (%s, %s)",
                        (ids, course_id))
        curs.close()
        conn.commit()
    else:
        print('Курс с таким ID не найден\nСоздайте курс\n')
        return create_course()


def add_student(student):  # просто создает студента
    with pg.connect(**DATA) as conn:
        with conn.cursor() as curs:
            curs.execute("insert into student (name, gpa, birth) values (%s, %s, %s) RETURNING id",
                         (student.get('name'), student.get('gpa'), student.get('birth')))
            print('Студент добавлен')


def get_student(student_id):
    with pg.connect(**DATA) as conn:
        with conn.cursor() as curs:
            curs.execute("select * from student where id = %s", (student_id,))
            data = curs.fetchall()
            if data:
                for row in data:
                    print(f'ID: {row[0]}\nИмя: {row[1]}\ngpa: {row[2]}\nДата рождения: {datetime.date(row[3])}\n')
            else:
                print('Студент с id:{} отсутствует'.format(student_id))


if __name__ == '__main__':
    # create_db()
    # add_students(7, [{'name': 'Антон 11', 'birth': '03.10.1986'},
    #                  {'name': 'Антон 14', 'gpa': '7', 'birth': '10.10.1986'}])
    # get_students(7)
    # get_student(1344)
    # add_student({'name': 'Элина 11', 'birth': '03.10.1986'})