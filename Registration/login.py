from flask import *
import mysql.connector as sql

login=Blueprint('login',__name__)
referrer=None
@login.route('/')
def red():
    return redirect('index')


@login.route('/login/')
def login1():
    global referrer
    if session.get('name'):
        return redirect(url_for('home.index'))
    referrer = request.referrer
    return render_template('home/login.html')

@login.route('/verify',methods=['POST','GET'])
def verify():
    if request.method == "POST":
        username = request.form['username']
        username = username.upper()
        username=username+'@NBKRIST.ORG'
        password = request.form['password']
        try:
            print('1')
            con =sql.connect(
                    host="127.0.0.1",
                    user="root",
                    password="password",
                    database="MINI_PROJECT"

                            )
            cur = con.cursor()
            print('database not connected')
            cur.execute('SELECT * FROM LOGIN WHERE USERNAME="%s" AND PASSWORD="%s";' % (username,password))
            login_data = cur.fetchone()
            print(login_data)
            cur.execute('SELECT * FROM STUDENT_REG WHERE MAIL_ID="%s" AND PASSWORD="%s";' % (username,password))
            login_data2=cur.fetchone()
            con.close()
            if login_data is None and login_data2 is None:
                flash('Invalid login details or Not register')
                return redirect(url_for('login.login1'))
            elif login_data2 and login_data2[5]=='0':
                flash('Your account is waiting for authorization')
                return redirect(url_for('login.login1'))
            elif login_data[1] == 'ADMIN@NBKRIST.ORG' and login_data[2] == 'admin123':
                print('admin')
                session['name'] = login_data[1]
                return redirect(url_for('admin.admin_home'))
            else:
                verify.roll_no = login_data[0]
                session['name'] = login_data[0]
                if login_data[2] == '':
                    return render_template('home/register.html')
                msg = 'Login Successfully'
                print(referrer)
                return redirect(url_for('home.index'))

        except Exception as e:
            print(e)
            print('erroor')
            return abort(401)
    return abort(404)
