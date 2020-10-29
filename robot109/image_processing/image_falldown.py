import time
import enum
from datetime import datetime
import image_processing.image_sleep as image_sleep

class status(enum.Enum):
    standing = 0
    lying = 1
    falldown = 2
    
global blue_color, red_color, green_color
blue_color = (255,0,0)
red_color = (0,0,255)
green_color = (0,255,0)

global standing_time, lying_time, falldown_time
standing_time = time.time()
lying_time = time.time()
falldown_time = time.time()

global hasPrinted
hasPrinted = False

global origin_time, sleeptime
origin_time = 0
sleeptime = 0

def status_detected(status):
    global blue_color, red_color, green_color
    global standing_time, lying_time, falldown_time
    nowStatus = status.standing
    color = blue_color
    if status == status.standing: # standing
        standing_time = time.time()
        nowStatus = status.standing
        color = blue_color
    elif status == status.lying: # lying
        lying_time = time.time()
        nowStatus = status.lying
        color = green_color
    elif status == status.falldown: # falldown
        falldown_time = time.time()
        nowStatus = status.falldown
        color = red_color
    return nowStatus, color

def standing_process(beforeStatus):
    global origin_time, sleeptime
    nowStatus, color = status_detected(status.standing)

    if sleeptime >= 10:
        image_sleep.day_wake_time()
    origin_time = 0
    sleeptime = 0
    return nowStatus, color


def lying_process(beforeStatus):
    global sleeptime
    nowStatus, color = status_detected(status.lying)
    
    sleeptime = sleeptime+1
    if sleeptime >= 60:
        image_sleep.day_sleep_time()
    return nowStatus, color

def falldown_process(beforeStatus):
    global standing_time
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

