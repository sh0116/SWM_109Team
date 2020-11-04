import dataCenter
import requests
from datetime import datetime
from voice_processing import voice_main
import sensor.tail_servo_main as tail_servo_main
import random

global pre_time,nowTuple,sleep_hour, sleep_min, seconds, sleep_time
pre_time = datetime.now()
nowTuple = pre_time.timetuple()
sleep_hour = int(nowTuple.tm_hour)
sleep_min = int(nowTuple.tm_min)
seconds = (pre_time.hour * 60 + pre_time.minute) * 60 + pre_time.second
sleep_time = seconds/3600


def day_sleep_time(sleep_check):
    global sleep_time, sleep_hour, sleep_min
    sleep_time = seconds/3600
    print(sleep_hour, sleep_min)
    #75600
    if (seconds >= 75600 and seconds <= 86339) or (seconds >= 0 and seconds <= 1800) :
        if sleep_check == 0:
            sleep_check +=1
            data = {'user_id' : dataCenter.user_id, 'sensor_id': dataCenter.sleep, 'num' : sleep_time, 'day': 'sunday'}
            requests.post(dataCenter.URL, json=data)
            return sleep_check
    else:
        sleep_check = 0

def day_wake_time(wake_check, sleepingtime):
    global sleep_time, sleep_hour, sleep_min
    sleep_time = seconds/60
    sleepingtime /= 3600 
    if seconds >= 14400 and seconds<=27000:
        if wake_check == 0:
            wake_check +=1
            # request
            data = {'user_id' : dataCenter.user_id, 'sensor_id': dataCenter.sleep, 'num' : sleep_time, 'day': 'sunday'}
            sleepdata = {'user_id' : dataCenter.user_id, 'sensor_id': dataCenter.sleep, 'num' : sleep_time, 'day': 'sunday'}          
            requests.post(dataCenter.URL, json=data)
            # NLP
            text_list = ["일어나셨어요?","안녕히 주무셨어요?","오늘도 좋은 하루 보내세요"]
            n = randint(0,len(text_list)-1)
            voice_main.call_TTS(text_list[n])
            # shake tail
            body_servo, tail_servo = tail_servo_main.setup_tail(dataCenter.body_pin, dataCenter.tail_pin)
            tail_servo_main.shake_tail(body_servo, tail_servo)
            #tail_servo_main.cleanup_tail(dataCenter.body_pin, dataCenter.tail_pin)
    else:
        wake_check = 0
