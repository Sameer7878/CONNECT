from flask import Flask
import os
from Fee_Pay.Fee_Pay import Fee_app
from Registration.login import login
from Registration.home import home
from Registration.registration import register
from Payment.status import status
from admin.admin import admin
from Canteen.Canteen import canteen

app = Flask(__name__)
app.register_blueprint(login)
app.register_blueprint(register,url_prefix='/register/')
app.register_blueprint(canteen,url_prefix='/canteen/')
app.register_blueprint(admin,url_prefix='/admin/')
app.register_blueprint(home,url_prefix='/index/')
app.register_blueprint(Fee_app,url_prefix='/FeePay/')
app.register_blueprint(status,url_prefix='/status/')
app.config['DEBUG']=True
app.secret_key = '27009e15fbad776cfb3cf6fe174790e42574c8af5be4eb884f76acc874b4c0a9'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLD = '/static/uploadeddata'
UPLOAD_FOLDER = APP_ROOT + UPLOAD_FOLD
app.config[ 'UPLOAD_FOLDER' ] = UPLOAD_FOLDER
if __name__ == '__main__':
    app.run(debug=True)
