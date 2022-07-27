from flask import *
import mysql.connector as sql

home=Blueprint('home',__name__)

@home.route('/')
def index():
    if session.get('name')=='ADMIN@NBKRIST.ORG':
        return redirect(url_for('admin.admin_home'))
    if session.get('name') :
        name=session['name']
        return render_template('home/index.html',name=name)
    else:

        '''roll_no = session[ 'name' ]
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
        name = basic_data[ 1 ]'''
        return render_template('home/index.html')
@home.route('/Redirecting')
def FeePay():
    return redirect(url_for('Fee_app.home'))