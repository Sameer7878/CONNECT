import datetime
import mysql.connector as sql
from flask import *

canteen=Blueprint('canteen',__name__)

@canteen.route('/')
def home():
    return render_template('canteen/main.html')
@canteen.route('/menu')
def menu():
    return render_template('canteen/menu.html')
@canteen.route('/breakfast')
def breakfast():
    con = sql.connect(
        host="127.0.0.1",
        user="root",
        password="password",
        database="MINI_PROJECT"

    )
    cur = con.cursor()
    cur.execute("SELECT * FROM ITEMS WHERE ITEM_CATEGORY='BREAKFAST'")
    breakfast_items=cur.fetchall()
    con.close()

    return render_template('canteen/breakfast.html',items=breakfast_items)
@canteen.route('/dinner')
def dinner():
    return render_template('canteen/dinner.html')
@canteen.route('/lunch')
def lunch():
    con = sql.connect(
        host="127.0.0.1",
        user="root",
        password="password",
        database="MINI_PROJECT"

    )
    cur = con.cursor()
    cur.execute("SELECT * FROM ITEMS WHERE ITEM_CATEGORY='LUNCH'")
    lunch_items=cur.fetchall()
    con.close()
    return render_template('canteen/lunch.html',items=lunch_items)
@canteen.route('/special')
def special():
    return render_template('canteen/todayspl.html')
@canteen.route('/cart')
def cart():
    return render_template('canteen/cart.html')
@canteen.route('/dashboard')
def dashboard():
    return render_template('canteen/dashboard.html')
