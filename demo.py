import mysql.connector as sql
db=sql.connect(
    host="127.0.0.1",
    user="root",
    password="password",
    database="MINI_PROJECT"

)
cur=db.cursor()
roll_no='8'
username='19KB1A1244@NBKRIST.ORG'
password='sameer123'
cur.execute("SELECT STATUS.ROWID, STUDENT_INFO.NAME,STUDENT_INFO.ROLLNO,STATUS.AMOUNT,STATUS.UTR_NO,"
                    " STATUS.CATEGORY,STATUS.DATE,STATUS.STATUS FROM STATUS INNER JOIN STUDENT_INFO ON "
                    "STATUS.ROLLNO=STUDENT_INFO.ROLLNO WHERE STATUS.UTR_NO='%s' OR STATUS.ROLLNO='%s' OR STATUS.ROWID='%s' OR STUDENT_INFO.NAME='%s'"%(roll_no,roll_no,roll_no,roll_no))

print(cur.fetchall())