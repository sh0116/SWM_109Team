# -*- coding:utf-8 -*-
import json
from time import time
from random import random
from flask import Flask,session,escape
from flask import render_template, make_response
from flask_restful import Resource, Api
from flask_bootstrap import Bootstrap
from flask import  request, Response
from flask import stream_with_context,flash                                                                                                                         
from time import sleep
from flask_socketio import SocketIO, emit
#from flask_mysqldb import MySQL
import dbAPI
import sys
import psutil
import json
reload(sys)
sys.setdefaultencoding("utf-8")
app = Flask(__name__)
app.secret_key = b'gsgewgqhrrfha@!'
app.config['JSON_AS_ASCII']=False
api = Api(app)
Bootstrap(app)
socketio = SocketIO(app)
class RegistUser(Resource):
    def post(self):
        return{'result':'ok'}

api.add_resource(RegistUser,'/user')

@app.route('/sensor', methods = ['POST'])
def sensor():
    #print(request)

    user_id = request.get_json().get('user_id')
    sensor_id = request.get_json().get('sensor_id')
    num = request.get_json().get('num')
    day = request.get_json().get('day')
    dbAPI.insert_data("sensor_data",str(user_id), str(sensor_id), str(num), str(day))
    if str(sensor_id) == '5':
        socketio.emit('message', {'data': 'Records Affected'}, broadcast=True)

    return 'sensor'


@app.route('/robot_info/<data>', methods = ['POST'])
def robot_info_post(data):
	if request.method == 'POST': # INSERT
		name = request.get_json().get('name')
		robot_id = request.get_json().get('robot_id')
		user_id = request.get_json().get('user_id')
		print(name, robot_id, user_id)
		dbAPI.insert_robot_info(name, robot_id, user_id)
		return 'robot_info_post'
	else:
		return 'else'

@app.route('/user_info/<data>', methods = ['GET','POST'])
def user_info_post(data):
    if request.method == 'GET': # SELECT    
        prot_id = request.args['prot_id']
        if(data == 'id'):
            user = dbAPI.select_where("user_info",0,'id',prot_id=prot_id)
        elif(data == 'name'):
            user = dbAPI.select_where("user_info",0,"name",prot_id=prot_id)
        elif(data == 'gender'):
            user = dbAPI.select_where("user_info",0,"gender",prot_id=prot_id)
        elif(data == 'birth'):
            user = dbAPI.select_where("user_info",0,"birth",prot_id=prot_id)
        elif(data == 'address'):
            user = dbAPI.select_where("user_info",0,"address",prot_id=prot_id)
        elif(data == 'contact'):
            user = dbAPI.select_where("user_info",0,"contact",prot_id=prot_id)
        #print(user)
        return str(decodeList(user))
    else: # POST (INSERT)
        name = request.get_json().get('name')
        gender = request.get_json().get('gender')
        birth = request.get_json().get('birth')
        address = request.get_json().get('address')
        contact = request.get_json().get('contact')
        prot_id = request.get_json().get('prot_id')
        #print(name, contact, prot_id)
        dbAPI.insert_user_info(name, gender, birth, address, contact, prot_id)
        socketio.emit('user_info', {'data': 'uuuu'}, broadcast=True)
        return "user_info_post"

@app.route('/prot_info/<data>', methods = ['GET','POST'])
def prot_info_post(data):
    if request.method == 'GET': # SELECT
        if(data == 'name'):
            contact = request.args['contact']
            prot = dbAPI.select_where("prot_info",1,"name",contact=contact)
        elif(data == 'contact'):
            name = request.args['name']
            prot = dbAPI.select_where("prot_info",1,"contact",name=name)
        elif(data == 'id'):
            contact = request.args['contact']
            prot = dbAPI.select_where("prot_info",1,"id",contact=contact)
            print(prot)
        return str(decodeList(prot))
    else: # POST (INSERT)
        name = request.get_json().get('name')
        contact = request.get_json().get('contact')
        #print(dbAPI.select_where("activity",1,"timestamp",id=1))
        #dbAPI.insert_data("activity",70,1)
        #dbAPI.insert_data("fall_down",1)
        dbAPI.insert_prot_info(name, contact)
        return "prot_info_post"

@app.route('/userapp')
def Userapp():
    temp = request.args.get('prot_id')
    temp1 = request.args.get('user_id')
    session['userid'] = temp1
    graph_fall = dbAPI.select_fall_down(user_id = int(temp1))
    touch_count = dbAPI.select_touch(user_id = int(temp1))
    count_fall = dbAPI.select_fall_down_count(user_id = int(temp1))
    wake_up = dbAPI.select_wake_up(user_id = int(temp1))
    sleep = dbAPI.select_sleep(user_id = int(temp1))
    temperature = dbAPI.select_where("sensor_data",0,"num", user_id = int(temp1), sensor_id = 1)
    humidity = dbAPI.select_where("sensor_data",0,"num",sensor_id = 2, user_id = int(temp1))
    user_info = dbAPI.select_where("user_info",0,"*",id=int(temp1))
    all_user_info = dbAPI.select("user_info",0, "*")
    prot_info = dbAPI.select_where("prot_info",0,"*",id=int(temp))
    
    return render_template('userapp.html',row = graph_fall, data = temperature, data1 = user_info, data2 = prot_info,row1 = count_fall, data3 = humidity,wake_up = wake_up,touch_count = touch_count, sleep=sleep)


#temperature(1), humidity(2), wake_up(3), sleep(4), fall_down(5), activity(6) 
@app.route('/')
def index():
    temp1 = request.args.get('user_id')
    graph_fall = dbAPI.select_fall_down(user_id = 2)
    count_fall = dbAPI.select_fall_down_count(user_id = 1)
    wake_up = dbAPI.select_wake_up(user_id = 1)
    sleep = dbAPI.select_sleep(user_id = 1)
    temperature = dbAPI.select_where("sensor_data",0,"num",sensor_id = 1, user_id = 1)
    humidity = dbAPI.select_where("sensor_data",0,"num",sensor_id = 2, user_id = 1)
    user_info = dbAPI.select_where("user_info",0,"*",id=1)
    all_user_info = dbAPI.select("user_info",0, "*")
    user_avg_actibity = dbAPI.user_avg_activity()
    
    return render_template('index.html',row = graph_fall, data = temperature, data1 = user_info, data2 = all_user_info ,row1 = count_fall, data3 = humidity,user_avg_actibity=user_avg_actibity)

@app.route('/map')
def map():
    temp1 = request.args.get('user_id')
    session['userid'] = temp1
    graph_fall = dbAPI.select_fall_down(user_id = int(temp1))
    touch_count = dbAPI.select_touch(user_id = int(temp1))
    count_fall = dbAPI.select_fall_down_count(user_id = int(temp1))
    wake_up = dbAPI.select_wake_up(user_id = int(temp1))
    sleep = dbAPI.select_sleep(user_id = int(temp1))
    temperature = dbAPI.select_where("sensor_data",0,"num", user_id = int(temp1), sensor_id = 1)
    humidity = dbAPI.select_where("sensor_data",0,"num",sensor_id = 2, user_id = int(temp1))
    user_info = dbAPI.select_where("user_info",0,"*",id=int(temp1))
    all_user_info = dbAPI.select("user_info",0, "*")
    prot_info = dbAPI.select_prot_info(int(temp1))
    return render_template('map.html',row = graph_fall, data = temperature, data1 = user_info, data2 = all_user_info ,row1 = count_fall, data3 = humidity,wake_up = wake_up, sleep = sleep, touch_count = touch_count, prot_info = prot_info)

@app.route('/test')
def test():
    temp1 = request.args.get('user_id')
    session['userid'] = temp1
    graph_fall = dbAPI.select_fall_down(user_id = int(temp1))
    touch_count = int(dbAPI.select_touch(user_id = int(temp1)))
    count_fall = dbAPI.select_fall_down_count(user_id = int(temp1))
    wake_up = dbAPI.select_wake_up(user_id = int(temp1))
    sleep = dbAPI.select_sleep(user_id = int(temp1))
    temperature = dbAPI.select_where("sensor_data",0,"num", user_id = int(temp1), sensor_id = 1)
    humidity = dbAPI.select_where("sensor_data",0,"num",sensor_id = 2, user_id = int(temp1))
    user_info = dbAPI.select_where("user_info",0,"*",id=int(temp1))
    all_user_info = dbAPI.select("user_info",0, "*")
    prot_info = dbAPI.select_prot_info(int(temp1))
    avg_realtime = int(dbAPI.select_avg_realtime(user_id = int(temp1)))
    latest_realtime = int(dbAPI.select_latest_realtime(user_id = int(temp1)))
    user_activity = dbAPI.select_where("sensor_data",0,"*", sensor_id = 8)
    sub_activity = dbAPI.select_sub_activity(sensor_id=6,user_id = int(temp1))
    sub_touch = dbAPI.select_sub_activity(sensor_id=7,user_id = int(temp1))
    sub_sleeping = dbAPI.select_sub_activity(sensor_id=9,user_id = int(temp1))
    temper_min_max = dbAPI.select_min_max(sensor_id=1,user_id=int(temp1))
    avg_wake = dbAPI.select_avg_sleep(sensor_id=3,user_id=int(temp1))
    avg_sleep = dbAPI.select_avg_sleep(sensor_id=4,user_id=int(temp1))
    ONEuser_avg_activity = dbAPI.ONEuser_avg_activity(user_id=int(temp1))

    
    return render_template('test.html',row = graph_fall, data = temperature, data1 = user_info, data2 = all_user_info ,
    row1 = count_fall, data3 = humidity,wake_up = wake_up, sleep = sleep, touch_count = touch_count, prot_info = prot_info,avg_realtime = avg_realtime, 
    latest_realtime = latest_realtime, user_activity = user_activity,sub_activity = sub_activity, sub_touch = sub_touch,sub_sleeping = sub_sleeping,temper_min_max=temper_min_max,avg_wake=avg_wake,avg_sleep=avg_sleep,ONEuser_avg_activity = dbAPI.ONEuser_avg_activity(user_id=int(temp1)))


@app.route('/contact')
def Contact():
    user_info = dbAPI.select_where("user_info",0,"*",id=1)
    all_user_info = dbAPI.select("user_info",0, "*")
    prot_info = dbAPI.select_prot_info(1)
    return render_template('Contacts.html',data1 = user_info,data2 = all_user_info,prot_info = prot_info)


@app.route('/medicine_data/<data>', methods = ['GET','POST'])
def medicine_data(data):
    if request.method == 'GET':
        user_id = request.args['user_id']
        #print(user_id)
        val = dbAPI.select_where('medicine_data',0,'name','월','화','수','목','금','토','일','time1','time2','time3',user_id=user_id)
        print(val)
        return str(decodeList(val))
    else: # POST
        name = request.get_json().get('name')
        user_id = request.get_json().get('user_id')
        mon = request.get_json().get('mon')
        tue = request.get_json().get('tue')
        wed = request.get_json().get('wed')
        thu = request.get_json().get('thu')
        fri = request.get_json().get('fri')
        sat = request.get_json().get('sat')
        sun = request.get_json().get('sun')
        time1 = request.get_json().get('time1')
        time2 = request.get_json().get('time2')
        time3 = request.get_json().get('time3')
        print(name + user_id + time1)
        if(time2=='000000'): dbAPI.insert_medicine_data(name,user_id,mon,tue,wed,thu,fri,sat,sun,time1);
        elif(time3=='000000'): dbAPI.insert_medicine_data(name,user_id,mon,tue,wed,thu,fri,sat,sun,time1,time2);
        else: dbAPI.insert_medicine_data(name,user_id,mon,tue,wed,thu,fri,sat,sun,time1,time2,time3);
        return 'medicine_data_post';

# @app.route('/ajax-trigger') 
# def ajax_trigger(): 
#     return my_algorithm()

@app.route('/live-data')
def live_data():
    temp1 = session['userid']
    #print("세션값" + temp1)
    realtime = dbAPI.select_realtime(user_id = int(temp1))
    
    data = [time() * 1000,float(realtime)]
    print(data)
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response


def decodeList(input):
	return repr(input).decode('string-escape')
    
@app.route('/set_rasinfo', methods = ['POST'])
def get_rasinfo():
    if request.method == 'POST':
        query = request.form.get('query')
        info = list()
        try:
            info = dbAPI.get_target_data2db(query)
        except:
            return str(info)
    return str(info)

if __name__=='__main__':
    app.run(host='0.0.0.0',port=5000, debug=True)
