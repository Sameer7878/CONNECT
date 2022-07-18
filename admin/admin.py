from flask import *
import mysql.connector as sql


admin=Blueprint('admin',__name__)

@admin.route('/')
def admin_home():
    if session.get('name') == 'ADMIN@NBKRIST.ORG':
        con = sql.connect(
                    host="127.0.0.1",
                    user="root",
                    password="password",
                    database="MINI_PROJECT"

                )
        cur = con.cursor()
        cur.execute(
            "SELECT STATUS.ROWID, STUDENT_INFO.NAME,STUDENT_INFO.ROLLNO, STUDENT_INFO.CLASS ,STATUS.AMOUNT,STATUS.UTR_NO, STATUS.CATEGORY,STATUS.DATE,STATUS.STATUS,STATUS.PROOF_LINK FROM STATUS INNER JOIN STUDENT_INFO ON STATUS.ROLLNO=STUDENT_INFO.ROLLNO where STATUS.STATUS=0 and STATUS.ADMIN_TYPE=0;")

        admin_data = cur.fetchall()
        con.close()

        return render_template('admin/admin.html', status1=admin_data)
    else:
        abort(404)


@admin.route('/search/', methods=[ 'POST', 'GET' ])
def search():
    if not session.get('name') == 'ADMIN@NBKRIST.ORG':
        return redirect(url_for('login.login1'))
    if request.method == 'POST':
        searchd = request.form['search']
        print('enter')
        searchd=str(searchd)
        con = sql.connect(
                    host="127.0.0.1",
                    user="root",
                    password="password",
                    database="MINI_PROJECT"

                )
        cur = con.cursor()
        print('connetedd')
        cur.execute("SELECT STATUS.ROWID, STUDENT_INFO.NAME,STUDENT_INFO.ROLLNO,STUDENT_INFO.CLASS ,STATUS.AMOUNT,STATUS.UTR_NO,"
                    " STATUS.CATEGORY,STATUS.DATE,STATUS.STATUS,STATUS.PROOF_LINK FROM STATUS INNER JOIN STUDENT_INFO ON "
                    "STATUS.ROLLNO=STUDENT_INFO.ROLLNO WHERE STATUS.UTR_NO='%s' OR STATUS.ROLLNO='%s' OR STATUS.ROWID='%s' OR STUDENT_INFO.NAME='%s' OR STUDENT_INFO.CLASS ='%s' OR STATUS.CATEGORY='%s'" % (searchd,searchd,searchd,searchd,searchd,searchd))

        admin_data = cur.fetchall()
        print(admin_data)
        con.close()
        return render_template('admin/admin.html', status1=admin_data)
    return redirect(url_for('admin.admin_home'))


@admin.route('/undo', methods=[ 'POST', 'GET' ])
def undo():
    if not session.get('name') == 'ADMIN@NBKRIST.ORG':
        return redirect(url_for('login.login1'))
    if request.method == 'POST':
        utrno = request.form.get('utrno')
        con = sql.connect(
                    host="127.0.0.1",
                    user="root",
                    password="password",
                    database="MINI_PROJECT"

                )
        cur = con.cursor()
        cur.execute('SELECT AMOUNT,CATEGORY,ROLLNO FROM STATUS WHERE UTR_NO="%s"'%(utrno))
        amount = cur.fetchone()
        if  amount[1]=='Canteen':
            cur.execute('UPDATE STATUS SET STATUS=0  WHERE UTR_NO="%s"' % (utrno))
            cur.execute('UPDATE STUDENT_INFO SET wallet=wallet-"%s"' % (int(amount[0])))
            con.commit()
            con.close()
            return redirect(url_for('admin.admin_home'))
        category = amount[ 1 ].upper().split(' ')
        category = category[ 0 ] + '_' + category[ 1 ]
        cur.execute(f'SELECT PAID_AMOUNT ,TOTAL_AMOUNT  FROM {category} WHERE ROLLNO="%s"'%(amount[2]))
        pamount = cur.fetchone()

        tamount = pamount[0] - amount[0]
        damount = pamount[1] -tamount
        cur.execute(f'UPDATE {category} SET PAID_AMOUNT="%s" WHERE ROLLNO="%s"'%(tamount, amount[2]))

        cur.execute('UPDATE STATUS SET STATUS=0 WHERE UTR_NO="%s"'%(utrno))
        con.commit()
        con.close()
        return redirect(url_for('admin.accepted'))
    return abort(404)


@admin.route('/deny', methods=[ 'POST', 'GET' ])
def deny():
    if not session.get('name') == 'ADMIN@NBKRIST.ORG':
        return redirect(url_for('login.login1'))

    if request.method == 'POST':
        utrno = request.form.get('utrno')
        con = sql.connect(
                    host="127.0.0.1",
                    user="root",
                    password="password",
                    database="MINI_PROJECT"

                )
        cur = con.cursor()

        cur.execute('SELECT CATEGORY,AMOUNT,ROLLNO FROM STATUS WHERE UTR_NO="%s"'%(utrno))
        categ=cur.fetchone()
        if  categ[0]=='Canteen':
            cur.execute('UPDATE STATUS SET STATUS=2  WHERE UTR_NO="%s"' % (utrno))
            con.commit()
            con.close()
            return redirect(url_for('admin.admin_home'))
        category = categ[0].upper().split(' ')
        category = category[ 0 ] + '_' + category[ 1 ]
        cur.execute('UPDATE STATUS SET STATUS=2 WHERE UTR_NO="%s"'%(utrno))
        cur.execute(f'UPDATE {category} SET DUE_AMOUNT=DUE_AMOUNT+{categ[1]} WHERE ROLLNO="%s"'%(categ[2]))
        con.commit()
        con.close()
        return redirect(url_for('admin.admin_home'))
    return abort(404)


@admin.route('/accept', methods=[ 'POST', 'GET' ])
def accept():
    if not session.get('name') == 'ADMIN@NBKRIST.ORG':
        return redirect(url_for('login.login1'))
    if request.method == 'POST':
        utrno = request.form.get('utrno')
        con = sql.connect(
                    host="127.0.0.1",
                    user="root",
                    password="password",
                    database="MINI_PROJECT"

                )
        cur = con.cursor()
        cur.execute('SELECT AMOUNT,CATEGORY,ROLLNO FROM STATUS WHERE UTR_NO="%s"'% (utrno))
        amount = cur.fetchone()
        if  amount[1]=='Canteen':
            cur.execute('UPDATE STATUS SET STATUS=1  WHERE UTR_NO="%s"' % (utrno))
            cur.execute('UPDATE STUDENT_INFO SET wallet=wallet+"%s"'%(int(amount[0])))
            con.commit()
            con.close()
            return redirect(url_for('admin.admin_home'))
        category=amount[1].upper().split(' ')
        category=category[0]+'_'+category[1]
        cur.execute(f'SELECT PAID_AMOUNT ,TOTAL_AMOUNT  FROM {category} WHERE ROLLNO="%s"'%(amount[2]))
        pamount = cur.fetchone()

        tamount=amount[0]+pamount[0]
        damount=pamount[1]-tamount
        cur.execute(f'UPDATE {category} SET PAID_AMOUNT="%s" , DUE_AMOUNT="%s" WHERE ROLLNO="%s"'%(tamount,damount,amount[2]))
        cur.execute('UPDATE STATUS SET STATUS=1  WHERE UTR_NO="%s"'% (utrno))
        con.commit()
        con.close()
        return redirect(url_for('admin.admin_home'))
    return abort(404)


@admin.route('/accepted/')
def accepted():
    if not session.get('name'):
        return redirect('login.login1')
    con = sql.connect(
                    host="127.0.0.1",
                    user="root",
                    password="password",
                    database="MINI_PROJECT"

                )
    cur = con.cursor()
    cur.execute("SELECT STATUS.ROWID, STUDENT_INFO.NAME,STUDENT_INFO.ROLLNO,STUDENT_INFO.CLASS,STATUS.AMOUNT,STATUS.UTR_NO, STATUS.CATEGORY,STATUS.DATE,STATUS.STATUS,STATUS.PROOF_LINK FROM STATUS INNER JOIN STUDENT_INFO ON STATUS.ROLLNO=STUDENT_INFO.ROLLNO WHERE STATUS.STATUS=1 and STATUS.ADMIN_TYPE=0;")
    data = cur.fetchall()
    con.close()
    return render_template('admin/admin.html', status1=data)

@admin.route('/rejected/')
def rejected():
    if not session.get('name'):
        return redirect('login.login1')
    con = sql.connect(
                    host="127.0.0.1",
                    user="root",
                    password="password",
                    database="MINI_PROJECT"

                )
    cur = con.cursor()
    cur.execute("SELECT STATUS.ROWID, STUDENT_INFO.NAME,STUDENT_INFO.ROLLNO,STUDENT_INFO.CLASS,STATUS.AMOUNT,STATUS.UTR_NO, STATUS.CATEGORY,STATUS.DATE,STATUS.STATUS,STATUS.PROOF_LINK FROM STATUS INNER JOIN STUDENT_INFO ON STATUS.ROLLNO=STUDENT_INFO.ROLLNO WHERE STATUS.STATUS=2 and STATUS.ADMIN_TYPE=0;")
    data = cur.fetchall()
    con.close()
    return render_template('admin/admin.html', status1=data)

@admin.route('/student_register/')
def stureg():
    if not session.get('name'):
        return redirect('login.login1')
    con=sql.connect(
                    host="127.0.0.1",
                    user="root",
                    password="password",
                    database="MINI_PROJECT"

                )
    cur=con.cursor()
    cur.execute('SELECT STUDENT_REG.ROWID,STUDENT_INFO.NAME, STUDENT_REG.ROLLNO,STUDENT_INFO.CLASS,'
                'STUDENT_INFO.ACADEMIC,STUDENT_REG.STATUS FROM STUDENT_REG INNER JOIN STUDENT_INFO  on '
                'STUDENT_REG.ROLLNO = STUDENT_INFO.ROLLNO where STUDENT_REG.STATUS=0')
    data=cur.fetchall()
    con.close()
    return render_template('home/studentreg.html', stureg=data)
