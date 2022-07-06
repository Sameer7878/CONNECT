from flask import Blueprint, render_template, session
import mysql.connector as sql

status = Blueprint('status', __name__)


@status.route('/')
def all_status():
    roll_no = session[ 'name' ]
    con = sql.connect(
        host="127.0.0.1",
        user="root",
        password="password",
        database="MINI_PROJECT"

        )
    cur = con.cursor()
    cur.execute(
        "SELECT STATUS.ROWID, STUDENT_INFO.NAME,STUDENT_INFO.ROLLNO,STATUS.AMOUNT,STATUS.CATEGORY,STATUS.DATE,STATUS.STATUS FROM STATUS INNER JOIN STUDENT_INFO ON STATUS.ROLLNO=STUDENT_INFO.ROLLNO WHERE STATUS.ROLLNO= '%s' " % (
            roll_no))
    data = cur.fetchall()
    print(data)
    con.close()
    return render_template('status.html', status1=data)
