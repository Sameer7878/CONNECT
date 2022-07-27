from flask import url_for, render_template, request, redirect, session, abort,Blueprint
import os
from datetime import date
from werkzeug.utils import secure_filename
import mysql.connector as sql


Fee_app = Blueprint('Fee_app',__name__,template_folder='templates')

ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg'}

name = academic =class1 =section =gender=roll_no=None
APP_ROOT = '/Users/sameershaik/PycharmProjects/NBKR_CONNECT'
UPLOAD_FOLD = '/static/admin/uploadeddata'
UPLOAD_FOLDER=APP_ROOT+UPLOAD_FOLD
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@Fee_app.errorhandler(404)
def handle_404(e):
    return redirect('/')


@Fee_app.errorhandler(500)
def handle_500(e):
    return redirect('/')


@Fee_app.route('/signout/')
def signout():
    session.pop('name')
    return redirect(url_for('login.login1'))


@Fee_app.route('/')
def home():
    global name,academic,class1,section,gender,roll_no
    if not session.get('name'):
        return redirect(url_for('login.login1'))
    roll_no=session['name']
    con = sql.connect(
        host="127.0.0.1",
        user="root",
        password="password",
        database="MINI_PROJECT"

    )
    cur = con.cursor()
    cur.execute('SELECT LOGIN.ROLLNO,STUDENT_INFO.NAME,STUDENT_INFO.ACADEMIC,'
                'STUDENT_INFO.CLASS,STUDENT_INFO.SECTION,STUDENT_INFO.GENDER '
                'FROM LOGIN INNER JOIN STUDENT_INFO ON LOGIN.ROLLNO = STUDENT_INFO.ROLLNO WHERE '
                'LOGIN.ROLLNO= "%s"' % roll_no)
    basic_data = cur.fetchone()
    con.close()
    name = basic_data[ 1 ]
    academic = basic_data[ 2 ]
    class1 = basic_data[ 3 ]
    section = basic_data[ 4 ]
    gender = basic_data[ 5 ]
    return redirect(url_for('Fee_app.index'))
    #return render_template('')


@Fee_app.route('/forgot/')
def forgot():
    return 'sameer'



@Fee_app.route('/index/')
def index():
    if not session.get('name'):
        return redirect(url_for('login.login1'))
    return render_template('feepay/home.html', name=name)

'''@Fee_app.route('/register', methods=[ "POST", "GET" ])
def register():
    if not session.get('name'):
        return redirect('login')
    if request.method == 'POST':
        name=request.form['name']
        password=request.form['password']
        gender=request.form['gender']
        profile_link=f'images/{verify.roll_no}.jpg'
        filesz = request.files['file'].read()
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename=file.filename
            filename=filename.split('.')

            filename = secure_filename(verify.roll_no+ filename[1])
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            try:
                con = sql.connect('logins')
                cur = con.cursor()
                cur.execute("INSERT INTO STUDENT_INFO(rollno, name, academic, class, section, gender, profile_link) VALUES(?,?,?,?,?,?,?)",(verify.roll_no,name,3,'INFORMATION TECHNOLOGY',"A",gender,profile_link))
                cur.execute("UPDATE LOGIN SET PASSWORD=? where ROLLNO=?",(password,verify.roll_no))
                con.commit()
                con.close()
                return redirect('/login')
            except:
                return 'DATABASE ERROR'''



@Fee_app.route('/College Fee', methods=[ 'GET', 'POST' ])
def college_fee():
    if not session.get('name'):
        return redirect(url_for('login.login1'))
    roll_no1=session['name']
    con = sql.connect(
                    host="127.0.0.1",
                    user="root",
                    password="password",
                    database="MINI_PROJECT"

                )
    cur = con.cursor()
    cur.execute('SELECT LOGIN.ROLLNO,STUDENT_INFO.NAME,STUDENT_INFO.ACADEMIC,STUDENT_INFO.CLASS,'
                'STUDENT_INFO.SECTION,STUDENT_INFO.GENDER,STUDENT_INFO.profile_link,'
                ' COLLEGE_FEE.TOTAL_AMOUNT,COLLEGE_FEE.PAID_AMOUNT,'
                'COLLEGE_FEE.DUE_AMOUNT FROM LOGIN INNER JOIN STUDENT_INFO ON LOGIN.ROLLNO = STUDENT_INFO.ROLLNO '
                'INNER JOIN COLLEGE_FEE ON LOGIN.ROLLNO = COLLEGE_FEE.ROLLNO WHERE LOGIN.ROLLNO="%s"'%(roll_no1))

    data = cur.fetchone()
    print(data)
    cur.execute("SELECT STATUS.STATUS,COLLEGE_FEE.DUE_AMOUNT,STATUS.AMOUNT FROM COLLEGE_FEE INNER JOIN STATUS ON STATUS.ROLLNO=COLLEGE_FEE.ROLLNO WHERE STATUS.CATEGORY='College Fee' AND  STATUS.STATUS=0 AND STATUS.ROLLNO='%s'"%(roll_no1,))
    fee_details=cur.fetchall()
    con.close()
    print(data)
    name = data[1]
    rollno = data[0]
    class1 = data[3]
    year = str(data[2])
    gender = data[5]
    section = data[4]
    profile_link = data[6]
    tamount = data[7]
    pamount = data[8]
    if fee_details!=[]:
        pamount_str=str(pamount)
        for i in fee_details:
            pamount_str+='+'+str(i[2])
    else:
        pamount_str=str(pamount)

    ramount = data[9]
    return render_template('feepay/fee.html', name=name,cat_img='feepay/images/univf80.png',cat_name='College Fee', rollno=rollno, class1=class1, year=year, gender=gender,
                           section=section, tamount=tamount, pamount=pamount_str, ramount=ramount,
                           profile_link=profile_link)


@Fee_app.route('/bus_fee', methods=[ 'GET', 'POST' ])
def bus_fee():
    if not session.get('name'):
        return redirect('login.login1')
    roll_no1 = session['name']
    con =sql.connect(
                    host="127.0.0.1",
                    user="root",
                    password="password",
                    database="MINI_PROJECT"

                )
    cur = con.cursor()
    cur.execute('SELECT LOGIN.ROLLNO,STUDENT_INFO.NAME,STUDENT_INFO.ACADEMIC,STUDENT_INFO.CLASS,'
                'STUDENT_INFO.SECTION,STUDENT_INFO.GENDER,STUDENT_INFO.profile_link,'
                'BUS_FEE.TOTAL_AMOUNT,BUS_FEE.PAID_AMOUNT,'
                'BUS_FEE.DUE_AMOUNT FROM LOGIN INNER JOIN STUDENT_INFO ON LOGIN.ROLLNO = STUDENT_INFO.ROLLNO '
                'INNER JOIN BUS_FEE ON LOGIN.ROLLNO = BUS_FEE.ROLLNO WHERE LOGIN.ROLLNO="%s"'%(roll_no1))
    data = cur.fetchone()
    print(data)
    cur.execute("SELECT STATUS.STATUS,BUS_FEE.DUE_AMOUNT,STATUS.AMOUNT FROM BUS_FEE INNER JOIN STATUS ON STATUS.ROLLNO=BUS_FEE.ROLLNO WHERE STATUS.CATEGORY='Bus Fee' AND  STATUS.STATUS=0 AND STATUS.ROLLNO='%s'"%(roll_no1,))
    fee_details=cur.fetchall()
    con.close()
    name = data[1]
    rollno = data[0]
    class1 = data[3]
    year = str(data[2])
    gender = data[5]
    section = data[4]
    profile_link =  data[6]
    tamount = data[7]
    pamount = data[ 8 ]
    if fee_details != [ ]:
        pamount_str = str(pamount)
        for i in fee_details:
            pamount_str += '+' + str(i[ 2 ])
    else:
        pamount_str = str(pamount)

    ramount = data[ 9 ]
    return render_template('feepay/fee.html', name=name,cat_img='feepay/images/busf1.png',cat_name='Bus Fee', rollno=rollno, class1=class1, year=year, gender=gender,
                           section=section, tamount=tamount, pamount=pamount_str, ramount=ramount,
                           profile_link=profile_link)


@Fee_app.route('/exam_fee', methods=[ 'GET', 'POST', 'PUT' ])
def exam_fee():
    if not session.get('name'):
        return redirect('login.login1')
    roll_no1 = session['name']
    con = sql.connect(
                    host="127.0.0.1",
                    user="root",
                    password="password",
                    database="MINI_PROJECT"

                )
    cur = con.cursor()
    cur.execute('SELECT LOGIN.ROLLNO,STUDENT_INFO.NAME,STUDENT_INFO.ACADEMIC,STUDENT_INFO.CLASS,'
                'STUDENT_INFO.SECTION,STUDENT_INFO.GENDER,STUDENT_INFO.profile_link,'
                ' EXAM_FEE.TOTAL_AMOUNT,EXAM_FEE.PAID_AMOUNT,'
                'EXAM_FEE.DUE_AMOUNT FROM LOGIN INNER JOIN STUDENT_INFO ON LOGIN.ROLLNO = STUDENT_INFO.ROLLNO '
                'INNER JOIN EXAM_FEE ON LOGIN.ROLLNO = EXAM_FEE.ROLLNO WHERE LOGIN.ROLLNO= "%s"'%(roll_no1))
    data = cur.fetchone()
    cur.execute("SELECT STATUS.STATUS,EXAM_FEE.DUE_AMOUNT,STATUS.AMOUNT FROM EXAM_FEE INNER JOIN STATUS ON STATUS.ROLLNO=EXAM_FEE.ROLLNO WHERE STATUS.CATEGORY='Exam Fee' AND  STATUS.STATUS=0 AND STATUS.ROLLNO='%s'"%(roll_no1,))
    fee_details=cur.fetchall()
    con.close()
    name = data[1]
    rollno = data[0]
    class1 = data[3]
    year = str(data[2])
    gender = data[5]
    section = data[4]
    profile_link = data[6]
    tamount = data[7]
    pamount = data[ 8 ]
    if fee_details != [ ]:
        pamount_str = str(pamount)
        for i in fee_details:
            pamount_str += '+' + str(i[ 2 ])
    else:
        pamount_str = str(pamount)

    ramount = data[ 9 ]
    return render_template('feepay/fee.html', name=name,cat_img='feepay/images/examf.png',cat_name='Exam Fee', rollno=rollno, class1=class1, year=year, gender=gender,
                           section=section, tamount=tamount, pamount=pamount_str, ramount=ramount,
                           profile_link=profile_link)


@Fee_app.route('/hostel_fee')
def hostel_fee():
    if not session.get('name'):
        return redirect('login.login1')
    roll_no1 = session['name']
    con = sql.connect(
                    host="127.0.0.1",
                    user="root",
                    password="password",
                    database="MINI_PROJECT"

                )
    cur = con.cursor()
    cur.execute('SELECT LOGIN.ROLLNO,STUDENT_INFO.NAME,STUDENT_INFO.ACADEMIC,STUDENT_INFO.CLASS,'
                'STUDENT_INFO.SECTION,STUDENT_INFO.GENDER,STUDENT_INFO.profile_link,'
                ' HOSTEL_FEE.TOTAL_AMOUNT,HOSTEL_FEE.PAID_AMOUNT,'
                'HOSTEL_FEE.DUE_AMOUNT FROM LOGIN INNER JOIN STUDENT_INFO ON LOGIN.ROLLNO = STUDENT_INFO.ROLLNO '
                'INNER JOIN HOSTEL_FEE ON LOGIN.ROLLNO = HOSTEL_FEE.ROLLNO WHERE LOGIN.ROLLNO="%s"'%(roll_no1))
    data = cur.fetchone()
    cur.execute("SELECT STATUS.STATUS,HOSTEL_FEE.DUE_AMOUNT,STATUS.AMOUNT FROM HOSTEL_FEE INNER JOIN STATUS ON STATUS.ROLLNO=HOSTEL_FEE.ROLLNO WHERE STATUS.CATEGORY='Hostel Fee' AND  STATUS.STATUS=0 AND STATUS.ROLLNO='%s'"%(roll_no1,))
    fee_details=cur.fetchall()
    con.close()
    name = data[1]
    rollno = data[0]
    class1 = data[3]
    year = str(data[2])
    gender = data[5]
    section = data[4]
    profile_link = data[6]
    tamount = data[7]
    pamount = data[ 8 ]
    if fee_details != [ ]:
        pamount_str = str(pamount)
        for i in fee_details:
            pamount_str += '+' + str(i[ 2 ])
    else:
        pamount_str = str(pamount)

    ramount = data[ 9 ]
    return render_template('feepay/fee.html', name=name,cat_img='feepay/images/hostelf.png',cat_name='Hostel Fee', rollno=rollno, class1=class1, year=year, gender=gender,
                           section=section, tamount=tamount, pamount=pamount_str, ramount=ramount,
                           profile_link=profile_link)


@Fee_app.route('/other_fee')
def other_fee():
    if not session.get('name'):
        return redirect('login.login1')
    roll_no1 = session['name']
    con = sql.connect(
                    host="127.0.0.1",
                    user="root",
                    password="password",
                    database="MINI_PROJECT"

                )
    cur = con.cursor()
    cur.execute('SELECT LOGIN.ROLLNO,STUDENT_INFO.NAME,STUDENT_INFO.ACADEMIC,STUDENT_INFO.CLASS,'
                'STUDENT_INFO.SECTION,STUDENT_INFO.GENDER,STUDENT_INFO.profile_link,'
                ' OTHER_FEE.TOTAL_AMOUNT,OTHER_FEE.PAID_AMOUNT,'
                'OTHER_FEE.DUE_AMOUNT FROM LOGIN INNER JOIN STUDENT_INFO ON LOGIN.ROLLNO = STUDENT_INFO.ROLLNO '
                'INNER JOIN OTHER_FEE ON LOGIN.ROLLNO = OTHER_FEE.ROLLNO WHERE LOGIN.ROLLNO = "%s"'%(roll_no1))
    data = cur.fetchone()
    cur.execute("SELECT STATUS.STATUS,OTHER_FEE.DUE_AMOUNT,STATUS.AMOUNT FROM OTHER_FEE INNER JOIN STATUS ON STATUS.ROLLNO=OTHER_FEE.ROLLNO WHERE STATUS.CATEGORY='Other Fee' AND  STATUS.STATUS=0 AND STATUS.ROLLNO='%s'"%(roll_no1,))
    fee_details=cur.fetchall()
    con.close()
    name = data[1]
    rollno = data[0]
    class1 = data[3]
    year = str(data[2])
    gender = data[5]
    section = data[4]
    profile_link = data[6]
    tamount = data[7]
    pamount = data[ 8 ]
    if fee_details != [ ]:
        pamount_str = str(pamount)
        for i in fee_details:
            pamount_str += '+' + str(i[ 2 ])
    else:
        pamount_str = str(pamount)

    ramount = data[ 9 ]
    return render_template('feepay/fee.html', name=name,cat_img='feepay/images/otherf.png',cat_name='Other Fee', rollno=rollno, class1=class1, year=year, gender=gender,
                           section=section, tamount=tamount, pamount=pamount_str, ramount=ramount,
                           profile_link=profile_link)


@Fee_app.route('/Pay/', methods=[ "GET", "POST" ])
def pay():
    if not session.get('name'):
        return redirect(url_for('login.login1'))
    if request.method=='POST':
        amount = request.form['ramount']
        fee_name=request.form['fee-type']
        date1 = date.today()
        return render_template('pay.html', amount=amount, date=date1, fee_name=fee_name)
    else:
        amount = request.args.get('amount')
        tr_date = date.today()
        fee_type = request.args.get('fee_name')
        return render_template('pay.html', amount=amount, date=tr_date,fee_name=fee_type)


@Fee_app.route('/updating', methods=[ 'POST', 'GET' ])
def updating():
    if not session.get('name'):
        return redirect(url_for('login.login1'))
    roll_no=session.get('name')
    if request.method == 'POST':
        fee_type=request.form['fee-type']
        transaction_no = request.form['utrno']
        amount = request.form['amount']
        tr_date = request.form['date']
        #filesz = request.files['file'].read()
        file = request.files['file']
        if not fee_type=='Canteen':
            category = fee_type.upper().split(' ')
            category = category[ 0 ] + '_' + category[ 1 ]
        else:
            category='Canteen'
        if file and allowed_file(file.filename):
            """filename = secure_filename(file.filename)"""
            filename=str(transaction_no)+'.jpeg'
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            con = sql.connect(
                    host="127.0.0.1",
                    user="root",
                    password="password",
                    database="MINI_PROJECT"

                )
            cur = con.cursor()
            cur.execute(
                'INSERT INTO STATUS(ROLLNO, AMOUNT, CATEGORY, UTR_NO, DATE, PROOF_LINK,UDATE)  VALUES ("%s","%s","%s","%s","%s","%s","%s");'%(roll_no, amount, fee_type, transaction_no, tr_date, filename, date.today()))
            if not fee_type=='Canteen':
                cur.execute(f'UPDATE {category} SET DUE_AMOUNT=DUE_AMOUNT-{amount} WHERE ROLLNO="%s"'%(roll_no))
            con.commit()
            con.close()
            return redirect(url_for('status.all_status'))
        else:
            return redirect(url_for('Fee_app.pay',amount=amount,date=tr_date,number=transaction_no,fee_name=fee_type))
