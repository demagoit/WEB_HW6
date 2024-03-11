# from sqlalchemy import create_engine, MetaData
import sqlalchemy
import sqlalchemy.orm

engine = sqlalchemy.create_engine('sqlite:///:memory:', echo=False)
DBSession = sqlalchemy.orm.sessionmaker(bind=engine)
session = DBSession()

Base = sqlalchemy.orm.declarative_base()

class Student(Base):
    __tablename__ = 'students'
    id:sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(primary_key=True, autoincrement='auto')
    name:sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column(sqlalchemy.String(10))
    surname:sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column(sqlalchemy.String(30))
    group_id:sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(sqlalchemy.Integer, sqlalchemy.ForeignKey('groups.id'))
    
'''CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(10) NOT NULL,
    surname VARCHAR(30) NOT NULL,
    group_id INTEGER,
    FOREIGN KEY (group_id) REFERENCES groups (id) ON UPDATE CASCADE ON DELETE SET NULL
    );''',




metadata = sqlalchemy.MetaData()



users = sqlalchemy.Table('users', metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('name', sqlalchemy.String),
    sqlalchemy.Column('fullname', sqlalchemy.String),
)

addresses = sqlalchemy.Table('addresses', metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('user_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column('email_address', sqlalchemy.String, nullable=False)
)

metadata.create_all(engine)


with engine.connect() as conn:
    ins = users.insert().values(name='jack', fullname='Jack Jones')
    print(str(ins))
    result = conn.execute(ins)

    s = sqlalchemy.sql.select(users)
    result = conn.execute(s)
    for row in result:
        print(row)  # (1, u'jack', u'Jack Jones')