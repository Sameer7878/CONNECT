import requests.cookies
from flask import *

app=Flask(__name__)

@app.route('/')
def index():
    return 'Home'

data1={
    "name":"sameer",
    "class":"IT"
}

@app.route('/getdata/',methods=['GET'])
def getdata():
    if request.method=='GET':
        return jsonify(data1)

if __name__ =='__main__':
    app.run()