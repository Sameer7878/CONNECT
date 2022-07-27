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

        return render_template('admin/fee_admin.html', status1=admin_data)
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
        return render_template('admin/fee_admin.html', status1=admin_data)
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
    if not session.get('name') == 'ADMIN@NBKRIST.ORG':
        return redirect(url_for('login.login1'))
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
    return render_template('admin/fee_admin.html', status1=data)

@admin.route('/rejected/')
def rejected():
    if not session.get('name') == 'ADMIN@NBKRIST.ORG':
        return redirect(url_for('login.login1'))
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
    return render_template('admin/fee_admin.html', status1=data)

@admin.route('/student_details/')
def student_details():
    return render_template('admin/student_details.html')


@admin.route('/student_register/')
def stureg():
    if not session.get('name') == 'ADMIN@NBKRIST.ORG':
        return redirect(url_for('login.login1'))
    con=sql.connect(
                    host="127.0.0.1",
                    user="root",
                    password="password",
                    database="MINI_PROJECT"

                )
    cur=con.cursor()
    cur.execute('SELECT ROLLNO,NAME,PROFILE_LINK,STATUS FROM STUDENT_REG')
    data=cur.fetchall()
    print(data)
    con.close()
    return render_template('admin/studentreg.html', stureg=data)
@admin.route('/add_det/<roll>')
def add_det(roll):
    return render_template('admin/add_fee_det.html',roll=roll)
@admin.route('/update_det/',methods=['POST'])
def update_det():
    if request.method == 'POST':
        roll1=request.form['roll']
        class1 = request.form['class']
        branch = request.form['branch']
        acd = request.form['year']
        clg = request.form['clg']
        clg_pd = request.form['clg_pd']
        clg_unp = request.form['clg_unp']
        bus = request.form['bus']
        bus_pd = request.form['bus_pd']
        bus_unp = request.form['bus_unp']
        hots = request.form['hots']
        hots_pd = request.form['hots_pd']
        hots_unp = request.form['hots_unp']
        exm = request.form['exm']
        exm_pd = request.form['exm_pd']
        exm_unp = request.form['exm_unp']
        oth = request.form['oth']
        oth_pd = request.form['oth_pd']
        oth_unp = request.form['oth_unp']
        con = sql.connect(
            host="127.0.0.1",
            user="root",
            password="password",
            database="MINI_PROJECT"

        )
        cur = con.cursor()
        cur.execute('SELECT * FROM STUDENT_REG WHERE ROLLNO="%s";'%(roll1,))
        data=cur.fetchone()
        cur.execute("INSERT INTO LOGIN VALUES('%s','%s','%s')"%(data[0],data[1],data[4]))
        cur.execute(
            'INSERT INTO STUDENT_INFO(ROLLNO,NAME,ACADEMIC,CLASS,SECTION,GENDER,PROFILE_LINK) VALUES ("%s","%s","%s","%s","%s","%s","%s")'%(roll1,data[2],acd,class1,branch,data[3],data[6]))
        cur.execute('INSERT INTO COLLEGE_FEE VALUES ("%s","%s","%s","%s")'%(roll1,clg,clg_pd,clg_unp))
        cur.execute('INSERT INTO BUS_FEE VALUES ("%s","%s","%s","%s")' % (roll1, bus, bus_pd, bus_unp))
        cur.execute('INSERT INTO HOSTEL_FEE VALUES ("%s","%s","%s","%s")' % (roll1, hots, hots_pd, hots_unp))
        cur.execute('INSERT INTO EXAM_FEE VALUES ("%s","%s","%s","%s")' % (roll1, exm, exm_pd, exm_unp))
        cur.execute('INSERT INTO OTHER_FEE VALUES ("%s","%s","%s","%s")' % (roll1, oth, oth_pd, oth_unp))
        cur.execute('UPDATE STUDENT_REG SET STATUS="1" WHERE ROLLNO="%s"'%(roll1,))
        con.commit()
        con.close()
        return redirect(url_for('admin.stureg'))