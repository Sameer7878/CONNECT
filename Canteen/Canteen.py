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