import sqlite3
from contextlib import contextmanager

database = './test.db'

CREATE = [
   '''CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(10) NOT NULL,
    surname VARCHAR(30) NOT NULL,
    group_id INTEGER,
    FOREIGN KEY (group_id) REFERENCES groups (id) ON UPDATE CASCADE
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
        proffesor_id INTEGER,
        FOREIGN KEY (proffesor_id) REFERENCES proffesors (id)
    );''',

    '''CREATE TABLE IF NOT EXISTS marks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        subject_id INTEGER,
        proffesor_id INTEGER,
        FOREIGN KEY (student_id) REFERENCES students (id),
        FOREIGN KEY (subject_id) REFERENCES subjects (id),
        FOREIGN KEY (proffesor_id) REFERENCES proffessors (id),
        mark INTEGER NOT NULL,
        set_at DATETIME DEFAULT CURRENT_DATETIME
    )'''
]

@contextmanager
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = sqlite3.connect(db_file)
    yield conn
    # conn.rollback()
    conn.close()
    print('done')

def create_table(conn, sql_script):
    try:
        cur = conn.cursor()
        cur.execute(sql_script)
        conn.commit()
    except Exception as e:
        print(e)


def run():
    with create_connection(database) as conn:
        if conn is not None:
            i = 0
            for script in CREATE:
                create_table(conn, script)
                i += 1
                print(i)
        else:
            print('Error connection.')

if __name__ == '__main__':
    run()