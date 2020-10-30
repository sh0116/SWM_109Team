import requests


global realtime, hour_activity,hour
realtime=0
hour_activity = 0
hour = -1

global avg_act ,AVG
avg_act = [0 for i in range(15)]
AVG = 0

URL = 'http://13.125.221.213:5000/sensor'

def realtime_count(Cpx, Cpy, Bpx, Bpy):
    global realtime
    if abs(Cpx - Bpx) >= 2 or abs(Cpy - Bpy) >= 2:
        realtime += 1

def request_realtime():
    global realtime,hour_activity
    data = {'user_id' : '1', 'sendor_id':6, 'num' : realtime,'day': '토요일'}
    #res = requests.post(URL, json=data)
    #print(realtime)
    hour_activity += realtime
    print("hour_activity : ", hour_activity)
    realtime = 0
    
def avg_activity():
    global hour,hour_activity,avg_act,AVG

    if AVG > 0:
        print(AVG)
        activity_dis = abs(hour_activity - AVG)
        if  activity_dis> 200:
            print("emergency")
        else :
            print("!!!!!!!!!!!! more activity !!!!!!!!")
            
    hour +=1
    avg_act[hour] = hour_activity
    print(avg_act)
    if hour >= 2 and hour <= 15:
        AVG = sum(avg_act[hour-2:hour])/3
    elif hour > 15:
        hour = 0
        avg_act = [0 for i in range(15)]
    hour_activity = 0

