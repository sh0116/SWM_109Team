import requests
import dataCenter

global realtime
realtime = 0

def request_realtime():
    global realtime
    data = {'user_id' : 1, 'sensor_id': dataCenter.activity, 'num' : realtime, 'day': 'Sunday'}
    requests.post(dataCenter.URL, json=data)
    print(realtime)
    realtime = 0

def realtime_count(Cpx, Cpy, Bpx, Bpy):
    global realtime
    if abs(Cpx - Bpx) >= 2 or abs(Cpy - Bpy) >= 2:
        realtime += 1
