"""This is for Results"""
from flask import *
result=Blueprint('result',__name__)

@result.route('/')
def home():
    return render_template('results/home.html')
