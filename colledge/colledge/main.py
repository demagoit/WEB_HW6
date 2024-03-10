import sqlite3
from contextlib import contextmanager
import faker
import random

database = './test.db'
n_students = 50
n_groups = 3
l_subjects = ['Math', 'Phisics', 'Chemistry', 'English', 'Ukrainian', 'History']
n_proffessors = 5
n_marks = 20

class Colledge_db():
    def __init__(self, db_name:str = './test.db'):
        self.databasse = db_name
        self.conn = None
        self.CREATE_SCRIPTS = [
   '''CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(10) NOT NULL,
    surname VARCHAR(30) NOT NULL,
    group_id INTEGER,
    FOREIGN KEY (group_id) REFERENCES groups (id) ON UPDATE CASCADE ON DELETE SET NULL
    );''',

    '''CREATE TABLE IF NOT EXISTS proffessors(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(10) NOT NULL,
    surname VARCHAR(30) NOT NULL
    );''',

    '''CREATE TABLE IF NOT EXISTS groups(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(10) NOT NULL
    );''',

    '''CREATE TABLE IF NOT EXISTS subjects(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(30) NOT NULL,
        proffessor_id INTEGER,
        FOREIGN KEY (proffessor_id) REFERENCES proffessors (id) ON UPDATE CASCADE ON DELETE SET NULL
    );''',

    '''CREATE TABLE IF NOT EXISTS marks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        subject_id INTEGER,
        proffessor_id INTEGER,
        mark INTEGER,
        set_at DATETIME DEFAULT CURRENT_DATETIME,
        FOREIGN KEY (student_id) REFERENCES students (id) ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (subject_id) REFERENCES subjects (id) ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (proffessor_id) REFERENCES proffessors (id) ON UPDATE CASCADE ON DELETE SET NULL
    );'''
]
        self.INSERT_SCRIPTS = {
            'student': '''INSERT INTO students(name, surname, group_id) VALUES (?, ?, ?);''',
            'group': '''INSERT INTO groups(name) VALUES (?);''',
            'proffessor': '''INSERT INTO proffessors(name, surname) VALUES (?, ?);''',
            'subject': '''INSERT INTO subjects(title, proffessor_id) VALUES (?, ?);''',
            'mark': '''INSERT INTO marks(student_id, subject_id, proffessor_id, mark, set_at) VALUES (?, ?, ?, ?, ?);'''
        }
        self.SELECT_SCRIPTS = {
    '01': '''
            SELECT AVG(m.mark) AS avg, s.name AS Name, s.surname AS Surname 
            FROM marks AS m LEFT JOIN students AS s ON s.id = m.student_id 
            GROUP BY Name, Surname ORDER BY avg DESC LIMIT 5;''',
    '02': '''
            SELECT sb.title AS Subject, AVG(m.mark) as avg, s.name AS Name, s.surname AS Surname 
            FROM marks AS m LEFT JOIN students AS s ON m.student_id = s.id 
            LEFT JOIN subjects AS sb ON sb.id = m.subject_id
            GROUP BY Name, Surname, Subject 
            HAVING Subject=(?)
            ORDER BY avg DESC LIMIT 1;''',
    '03': '''
            SELECT g.name AS Team, sb.title AS Subject, AVG(m.mark) AS avg 
            FROM marks AS m LEFT JOIN subjects AS sb ON m.subject_id = sb.id
            LEFT JOIN students AS s ON m.student_id = s.id
            LEFT JOIN groups as g ON s.group_id = g.id
            GROUP BY Subject, Team
            HAVING Subject=(?)
            ORDER BY Team ;''',
    '04': '''
            SELECT AVG(mark) AS avg FROM marks;''',
    '05': '''
            SELECT p.name AS Name, p.surname AS Surname, sb.title AS Subject
            FROM proffessors AS p LEFT JOIN subjects AS sb ON sb.proffessor_id = p.id
            WHERE Surname = (?);''',
    '06': '''
            SELECT g.name AS Team, s.name AS Name, s.surname as Surname
            FROM students AS s LEFT JOIN groups AS g ON s.group_id = g.id
            WHERE Team = (?);''',
    '07': '''
            SELECT g.name AS Team, sb.title AS Subject, m.mark AS Mark, s.name AS Name, s.surname AS Surname
            FROM marks AS m LEFT JOIN subjects AS sb ON m.subject_id = sb.id
            LEFT JOIN students AS s ON m.student_id = s.id
            LEFT JOIN groups AS g ON s.group_id = g.id
            WHERE Team = (?) AND Subject = (?);''',
    '08': '''
            SELECT p.name AS Name, p.surname AS Surname, sb.title AS Subject, AVG(m.mark) AS avg
            FROM marks AS m LEFT JOIN subjects AS sb ON m.subject_id = sb.id
            LEFT JOIN proffessors AS p ON sb.proffessor_id = p.id
            GROUP BY Name, Surname, Subject
            HAVING Surname = (?);''',
    '09': '''
            SELECT s.name AS Name, s.surname AS Surname, sb.title AS Subject
            FROM marks AS m LEFT JOIN students AS s ON m.student_id = s.id
            LEFT JOIN subjects AS sb ON m.subject_id = sb.id
            GROUP BY Name, Surname, Subject
            HAVING Surname = (?);''',
    '10': '''
            SELECT s.surname AS Student, p.surname AS Proffessor, sb.title AS Subject
            FROM marks AS m LEFT JOIN subjects AS sb ON m.subject_id = sb.id
            LEFT JOIN students AS s ON m.student_id = s.id
            LEFT JOIN proffessors AS p ON sb.proffessor_id = p.id
            GROUP BY Student, Proffessor, Subject
            HAVING Student = (?) AND Proffessor = (?);''',
    '11': '''
            SELECT p_m.Surname AS Proffessor, s_m.Surname AS Student, AVG(s_m.Mark) AS avg
            FROM
            (SELECT p.surname AS Surname, m.id AS id
            FROM marks AS m LEFT JOIN proffessors AS p ON m.proffessor_id = p.id
            WHERE Surname = (?)) AS p_m
            INNER JOIN
            (SELECT s.surname AS Surname, m.mark AS Mark, m.id AS id
            FROM marks AS m LEFT JOIN students AS s ON m.student_id = s.id
            WHERE Surname = (?)) AS s_m
            ON p_m.id = s_m.id
            GROUP BY Student, Proffessor;''',
    '12': '''
            SELECT s_g.Name AS Name, s_g.Surname AS Surname, s_m.Mark AS Mark, s_m.Date AS Date
            FROM
            (SELECT s.name AS Name, s.surname AS Surname, s.id AS id
            FROM groups AS g LEFT JOIN students AS s ON g.id = s.group_id
            WHERE g.name = (?)) AS s_g
            INNER JOIN
            (SELECT m.student_id AS id, m.mark AS Mark, m.set_at AS Date
            FROM subjects AS sb LEFT JOIN marks AS m ON m.subject_id = sb.id
            WHERE sb.title = (?)) AS s_m
            ON s_g.id = s_m.id
            WHERE Date = (
                SELECT MAX(s_m.Date) AS max
                FROM
                (SELECT s.id AS id
                FROM groups AS g LEFT JOIN students AS s ON g.id = s.group_id
                WHERE g.name = (?)) AS s_g
                INNER JOIN
                (SELECT m.student_id AS id, m.set_at AS Date
                FROM subjects AS sb LEFT JOIN marks AS m ON m.subject_id = sb.id
                WHERE sb.title = (?)) AS s_m
                ON s_g.id = s_m.id
                );'''
}

    @contextmanager
    def create_connection(self):
        """ create a database connection to a SQLite database """
        self.conn = sqlite3.connect(self.databasse)
        yield self.conn
        # conn.rollback()
        self.conn.close()
        print(f'Connection to {self.databasse} closed.')

    def execute_sql(self, script:str, *params) -> None:
        '''executes given SQL script with *params (if any) in self.database'''
        try:
            cur = self.conn.cursor()
            if params:
                cur.execute(script, *params)
            else:
                cur.execute(script)
            self.conn.commit()
        except Exception as e:
            print(e)
        finally:
            cur.close()

    def create_db(self) -> None:
        '''creates tables in self.database'''
        for script in self.CREATE_SCRIPTS:
            self.execute_sql(script)

    def execute_sql_many(self, script:str, data:tuple) -> None:
        '''executes given SQL script with multiple data in self.database'''
        try:
            cur = self.conn.cursor()
            cur.executemany(script, data)
            self.conn.commit()
        except Exception as e:
            print(e)
        finally:
            cur.close()

    def fetch_data(self, script, *params):
        '''executes sql script with *params(if any) to fetch data from self.database'''
        cur = self.conn.cursor()
        if params:
            cur.execute(script, *params)
        else:
            cur.execute(script)
        result = cur.fetchall()
        # cur.close()
        return result

    def generate_fake_data(self, n_students:int=1, n_groups:int=1, n_proffessors:int=1, l_subjects:list = ['Math'], n_marks:int = 1):
        '''generates fake data to fill self.database tables'''
        students = []
        groups = []
        proffessors = []
        subjects = []
        marks = []

        fake_data = faker.Faker()

        for i in range(n_groups):
            groups.append((f'Group_{i}',))

        for _ in range(n_students):
            group_id = random.randint(1, n_groups)
            students.append((fake_data.first_name(), fake_data.last_name(), group_id))

        for _ in range(n_proffessors):
            proffessors.append((fake_data.first_name(), fake_data.last_name()))

        for subject in l_subjects:
            subjects.append((subject, random.randint(1, n_proffessors)))

        for student in range(1, n_students+1):
            for subject in enumerate(subjects,1):
                if random.randint(0,2) == 0:
                    continue
                subj = subject[0]
                proffessor = subject[1][1]
                for _ in range(n_marks):
                    mark = random.randint(random.randint(1, 5),random.randint(6, 13))
                    set_at = fake_data.date_between(start_date="-1y", end_date='today')
                    marks.append((student, subj, proffessor, mark, set_at))

        return students, groups, proffessors, subjects, marks

    def output(self, data:list) -> None:
        '''prints fetch results output'''
        for row in data:
            print(*row)

def run():
    db = Colledge_db(database)
    with db.create_connection():
        # db.create_db()
        # students, groups, proffessors, subjects, marks = db.generate_fake_data(n_students, n_groups, n_proffessors, l_subjects, n_marks)
        # db.execute_sql_many(db.INSERT_SCRIPTS['student'], students)
        # db.execute_sql_many(db.INSERT_SCRIPTS['group'], groups)
        # db.execute_sql_many(db.INSERT_SCRIPTS['proffessor'], proffessors)
        # db.execute_sql_many(db.INSERT_SCRIPTS['subject'], subjects)
        # db.execute_sql_many(db.INSERT_SCRIPTS['mark'], marks)

        prof = db.fetch_data('SELECT surname FROM proffessors LIMIT 1;')[0]
        stud = db.fetch_data('SELECT surname FROM students LIMIT 1;')[0]
        gr = db.fetch_data('SELECT name FROM groups LIMIT 1;')[0]
        sb = db.fetch_data('SELECT title FROM subjects LIMIT 1;')[0]
        
        # result = db.fetch_data(db.SELECT_SCRIPTS['01'])
        # result = db.fetch_data(db.SELECT_SCRIPTS['02'], (l_subjects[0],))
        # result = db.fetch_data(db.SELECT_SCRIPTS['03'], (l_subjects[0],))
        # result = db.fetch_data(db.SELECT_SCRIPTS['04'])
        # result = db.fetch_data(db.SELECT_SCRIPTS['05'], prof)
        # result = db.fetch_data(db.SELECT_SCRIPTS['06'], gr)
        # result = db.fetch_data(db.SELECT_SCRIPTS['07'], (gr[0], l_subjects[0]))
        # result = db.fetch_data(db.SELECT_SCRIPTS['08'], prof)
        # result = db.fetch_data(db.SELECT_SCRIPTS['09'], stud)
        # result = db.fetch_data(db.SELECT_SCRIPTS['10'], (stud[0], prof[0]))
        # result = db.fetch_data(db.SELECT_SCRIPTS['11'], (prof[0], stud[0]))
        result = db.fetch_data(db.SELECT_SCRIPTS['12'], (gr[0], sb[0], gr[0], sb[0]))

        db.output(result)

if __name__ == '__main__':
    run()