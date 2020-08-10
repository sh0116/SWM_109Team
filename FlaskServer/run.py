from flask import Flask
from flask import render_template
from flask_restful import Resource, Api
from flask_bootstrap import Bootstrap
#from flask_mysqldb import MySQL
import dbapi
app = Flask(__name__)
api = Api(app)
Bootstrap(app)

class RegistUser(Resource):
    def post(self):
        return{'result':'ok'}

api.add_resource(RegistUser,'/user')
@app.route('/')
def index():
    row = dbapi.select_fall_down()
    data = dbapi.select_body_temp()
    data1 = dbapi.select_user_info()
    data2 = dbapi.select_addresstest()
    return render_template('index.html',row=row, data = data, data1 = data1, data2 = data2)

@app.route('/weekly')
def index1():
    row = dbapi.select_fall_down()
    data = dbapi.select_body_temp()
    data1 = dbapi.select_user_info()
    return render_template('index1.html',row=row, data = data, data1 = data1)


@app.route('/monthly')
def index2():
    return render_template('index2.html')

@app.route('/contact')
def index3():
    return render_template('Contacts.html')



if __name__=='__main__':
    app.run(host='0.0.0.0',port=5000, debug=True)

