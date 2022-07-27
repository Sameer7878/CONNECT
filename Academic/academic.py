"""
This is for Academic Details
"""
from flask import *

acad=Blueprint('AcadDetail',__name__)

@acad.route('/')
def home():
    return render_template('academic/academic.html')
@acad.route('/update/',methods=['POST','GET'])
def update():
    pass