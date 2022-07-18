from flask import Blueprint, render_template, session,request
import mysql.connector as sql
import pdfkit


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
        "SELECT STATUS.ROWID, STUDENT_INFO.NAME,STUDENT_INFO.ROLLNO,STATUS.AMOUNT,STATUS.CATEGORY,STATUS.DATE,STATUS.STATUS,STATUS.TOKEN_NO,STATUS.Order_Status FROM STATUS INNER JOIN STUDENT_INFO ON STATUS.ROLLNO=STUDENT_INFO.ROLLNO WHERE STATUS.ROLLNO= '%s' " % (
            roll_no))
    data = cur.fetchall()
    con.close()
    return render_template('status.html', status1=data)
@status.route('/reciept/<reciept_id>')
def reciept(reciept_id):
    con = sql.connect(
        host="127.0.0.1",
        user="root",
        password="password",
        database="MINI_PROJECT"

    )
    cur = con.cursor()
    cur.execute(
        "SELECT STATUS.ROWID, STUDENT_INFO.NAME,STUDENT_INFO.ROLLNO,STUDENT_INFO.CLASS,STUDENT_INFO.ACADEMIC,STATUS.AMOUNT,STATUS.CATEGORY,STATUS.DATE FROM STATUS INNER JOIN STUDENT_INFO ON STATUS.ROLLNO=STUDENT_INFO.ROLLNO WHERE STATUS.ROWID= '%s' " % (reciept_id))
    data=cur.fetchone()
    return render_template('feereceipt.html',data=data)
@status.route('/download')
def download():
    link=request.referrer
    pdfkit.from_url(link, 'connect.pdf')