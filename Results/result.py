"""This is for Results"""
from flask import *
import mysql.connector as sql
result=Blueprint('result',__name__)

@result.route('/')
def home():
    rollno=session['name']
    con=sql.connect(
        host="127.0.0.1",
        user="root",
        password="password",
        database="MINI_PROJECT"

    )
    cur=con.cursor()
    cur.execute('SELECT STUDENT_INFO.ROLLNO,STUDENT_INFO.NAME,STUDENT_INFO.CLASS,STUDENT_INFO.SECTION,RESULTS.WHOLE_RESULT,RESULTS.SEMESTER,RESULTS.SUBJECT_DATA FROM RESULTS INNER JOIN STUDENT_INFO ON STUDENT_INFO.ROLLNO=RESULTS.ROLLNO WHERE RESULTS.ROLLNO="%s"'%(rollno,))
    res=cur.fetchone()
    sub_data=json.loads(res[6])
    return render_template('results/result.html',res=res,sub_data=sub_data)
