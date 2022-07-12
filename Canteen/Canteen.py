import datetime

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
    return render_template('canteen/breakfast.html')
@canteen.route('/dinner')
def dinner():
    return render_template('canteen/dinner.html')
@canteen.route('/lunch')
def lunch():
    return render_template('canteen/lunch.html')
@canteen.route('/special')
def special():
    return render_template('canteen/todayspl.html')
@canteen.route('/cart')
def cart():
    return render_template('canteen/cart.html')
@canteen.route('/dashboard')
def dashboard():
    return render_template('canteen/dashboard.html')
