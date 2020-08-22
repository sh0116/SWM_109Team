from flask import Flask
from flask import render_template
from flask_restful import Resource, Api
from flask_bootstrap import Bootstrap
from flask import  request, Response
#from flask_mysqldb import MySQL
import dbapi
app = Flask(__name__)
api = Api(app)
Bootstrap(app)

class RegistUser(Resource):
    def post(self):
        return{'result':'ok'}

api.add_resource(RegistUser,'/user')


# @app.route('/fall_down', methods = ['POST'])
# def fall_down():
#     if request.method == 'POST':
#         print(request.get_json())
#         user_id = request.get_json().get('user_id')
#         dbapi.insert_data('fall_down',user_id)
#         return 'fall_down'
#     else:
#         return 'fall_down'



@app.route('/wake_up', methods = ['POST'])
def fall_down():
    if request.method == 'POST':
        print(request.get_json())
        user_id = request.get_json().get('user_id')
        graph = request.get_json().get('graph')
        dbapi.insert_data('wake_up',user_id,graph)
        return 'wake_up'
    else:
        return 'wake_up'


@app.route('/')
def index():
    row = dbapi.select_fall_down()
    row1 = dbapi.select_fall_down_count()
    data = dbapi.select_temp()
    data3 = dbapi.select_humidity()
    data1 = dbapi.select_user_info()
    sleep = dbapi.select_wake_up()
    row2 = dbapi.select_ffff()
    return render_template('index.html',row=row, data = data, data1 = data1, row1 = row1, data3 = data3,sleep = sleep,row2=row2)

@app.route('/weekly')
def index1():
    row = dbapi.select_fall_down()
    data = dbapi.select_body_temp()
    data1 = dbapi.select_user_info()
    return render_template('index1.html',row=row, data = data, data1 = data1)


@app.route('/monthly')
def index2():
    row = dbapi.select_fall_down()
    row1 = dbapi.select_fall_down_count()
    data = dbapi.select_temp()
    data3 = dbapi.select_humidity()
    data1 = dbapi.select_user_info()
    data2 = dbapi.select_addresstest()
    
    return render_template('index2.html',row=row, data = data, data1 = data1, data2 = data2, row1 = row1, data3 = data3)


@app.route('/contact')
def index3():
    return render_template('Contacts.html')



if __name__=='__main__':
    app.run(host='0.0.0.0',port=5000, debug=True)


