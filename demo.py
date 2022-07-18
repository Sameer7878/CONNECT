import mysql.connector as sql
con = sql.connect(
        host="127.0.0.1",
        user="root",
        password="password",
        database="MINI_PROJECT"
    )
cur = con.cursor()
cur.execute('SELECT * FROM ITEM_ORDERS WHERE STATUS=0')
print(cur.fetchall())
