import time
import enum
from datetime import datetime
import tflite_sleep

class status(enum.Enum):
    standing = 0
    lying = 1
    falldown = 2
    
blue_color = (255,0,0)
red_color = (0,0,255)
green_color = (0,255,0)

standing_time = time.time()
lying_time = time.time()
falldown_time = time.time()

hasPrinted = False

global origin_time, now_time, sleeptime
origin_time = 0
now_time = 0
sleeptime = 0

def status_detected(status):
    if status == status.standing:
        standing_time = time.time()
        nowStatus = status.standing
        color = blue_color
    elif status == status.lying:
        lying_time = time.time()
        nowStatus = status.lying
        color = green_color
    elif status == status.falldown:
        falldown_time = time.time()
        nowStatus = status.falldown
        color = red_color
    return nowStatus, color

def standing_process(beforeStatus):
    global origin_time, sleeptime
    nowStatus, color = status_detected(status.standing)

    if sleeptime >= 10:
        seconds = (tflite_sleep.pre_time.hour * 60 + tflite_sleep.pre_time.minute) * 60 + tflite_sleep.pre_time.second
        sleep_time = seconds/3600
        if seconds >= 14400 and seconds<=27000:
            if wake_check == 0:
                wake_check +=1
                tflite_sleep.day_wake_time()
        else:
            wake_check = 0
    origin_time = 0
    sleeptime = 0
    return nowStatus, color


def lying_process(beforeStatus):
    global sleeptime
    nowStatus, color = status_detected(status.lying)
    
    sleeptime = sleeptime+1
    if sleeptime >= 5:
        seconds = (tflite_sleep.pre_time.hour * 60 + tflite_sleep.pre_time.minute) * 60 + tflite_sleep.pre_time.second
        sleep_time = seconds/3600
        if (seconds >= 75600 and seconds <= 86339) or (seconds >= 0 and seconds <= 1800) :
            if sleep_check == 0:
                sleep_check +=1
                tflite_tf.day_sleep_time()
        else:
            sleep_check = 0
    return nowStatus, color

def falldown_process(beforeStatus):
    now_time = time.time()
    diff_time = now_time - standing_time
    if diff_time <= 1:
        nowStatus, color = status_detected(status.falldown)
        print("fall down 111")
    elif beforeStatus == status.falldown:
        if diff_time >= 5 and diff_time < 10:
            nowStatus, color = status_detected(status.falldown)
            if hasPrinted == False:
                print("fall down 222")
                hasPrinted2 = True
        elif diff_time >= 10:
            nowStatus, color = status_detected(status.falldown)
            print("fall down 333")
    else: # lying
        nowStatus, color = lying_process(beforeStatus)
    return nowStatus, color

