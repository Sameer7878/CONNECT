from __init__ import app
from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy(app)

class login(db.Model):
    __tablename__='login'
    rollno=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.VARCHAR(50),unique=True,nullable=False)
    password=db.Column(db.VARCHAR(100),unique=False,nullable=False)
class student_info(db.Model):
    __tablename__='student_info'
    rollno=db
    CREATE
    TABLE
    STUDENT_INFO(ROLLNO VARCHAR(10), NAME
    VARCHAR(20), ACADEMIC
    NUMBER(5), CLASS
    VARCHAR(10), SECTION
    VARCHAR(5), GENDER
    VARCHAR(10), profile_link
    varchar(30), FOREIGN
    KEY(ROLLNO)
    REFERENCES
    LOGIN(ROLLNO))


