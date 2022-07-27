import mysql.connector as sql
con = sql.connect(
        host="127.0.0.1",
        user="root",
        password="password",
        database="MINI_PROJECT"
    )
cur = con.cursor()
cur.execute("alter table STUDENT_INFO modify NAME varchar(60) null;")
con.commit()
con.close()
