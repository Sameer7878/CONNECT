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
        print('hello')
        try:
            con =sql.connect(
                    host="127.0.0.1",
                    user="root",
                    password="password",
                    database="MINI_PROJECT"

                            )
            print('connected')
            cur = con.cursor()
            cur.execute('SELECT * FROM LOGIN WHERE USERNAME="%s" AND PASSWORD="%s";' % (username,password))
            login_data = cur.fetchone()
            con.close()
            print(login_data)
            if login_data is None:
                msg = 'Invalid login details'
                return render_template('home/login.html', msg=msg)
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

        except:
            return abort(401)
    return abort(404)
