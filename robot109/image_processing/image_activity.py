import requests

global realtime
realtime = 0

URL = 'http://13.125.221.213:5000/sensor'

def request_realtime():
    global realtime
    data = {'user_id' : 1, 'sensor_id': 6, 'num' : realtime, 'day': 'Sunday'}
    requests.post(URL, json=data)
    print(realtime)
    realtime = 0

def realtime_count(Cpx, Cpy, Bpx, Bpy):
    global realtime
    if abs(Cpx - Bpx) >= 2 or abs(Cpy - Bpy) >= 2:
        realtime += 1
    
