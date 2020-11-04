import time
import enum
from datetime import datetime
import image_processing.image_sleep as image_sleep
import dataCenter

class status(enum.Enum):
    standing = 0
    lying = 1
    falldown = 2
    
global blue_color, red_color, green_color
blue_color = (255,0,0)
red_color = (0,0,255)
green_color = (0,255,0)

global standingTime, lyingTime, falldownTime
standingTime = time.time()
lyingTime = time.time()
falldownTime = time.time()

global hasPrinted
hasPrinted = False

global sleeptime, sleep_check, wake_check
sleeptime = 0
sleep_check = 0
wake_check = 0

global flag, userHeight, beforeH
flag = False
userHeight = 163
beforeH = 1

global realFallDown
realFallDown = False

def status_detected(status):
    global blue_color, red_color, green_color
    global standingTime, lyingTime, falldownTime
    global realFallDown
    nowStatus = status.standing
    color = blue_color
    if status == status.standing: # standing
        standingTime = time.time()
        nowStatus = status.standing
        color = blue_color
    elif status == status.lying: # lying
        lyingTime = time.time()
        nowStatus = status.lying
        color = green_color
        realFallDown = False
    elif status == status.falldown: # falldown
        falldownTime = time.time()
        nowStatus = status.falldown
        color = red_color
        realFallDown = False
    return nowStatus, color

def standing_process(beforeStatus, personPoint):
    global flag, beforeH
    global sleeptime, wake_check
    nowStatus, color = status_detected(status.standing)

    standingMinX = personPoint[0]
    standingMaxX = personPoint[1]
    standingMinY = personPoint[2]
    standingMaxY = personPoint[3]
    beforeH = standingMaxY - standingMinY
    flag = False

    if sleeptime >= 60:
        wake_check = image_sleep.day_wake_time(wake_check, sleeptime)
    sleeptime = 0

    standingPoint = [standingMinX, standingMaxX, standingMinY, standingMaxY]
    return nowStatus, color, standingPoint

def lying_process(beforeStatus, personPoint, standingPoint):
    global sleeptime, sleep_check
    nowStatus, color = status_detected(status.lying)

    lyingMinX = personPoint[0]
    lyingMaxX = personPoint[1]
    lyingMinY = personPoint[2]
    lyingMaxY = personPoint[3]

    centerPointX = int((lyingMinX + lyingMaxX)/2)
    centerPointY = int((lyingMinY + lyingMaxY)/2)

    standingMinX = standingPoint[0]
    standingMaxX = standingPoint[1]
    standingMinY = standingPoint[2]
    standingMaxY = standingPoint[3]

    # calculate head point
    headPointX = lyingMinX if abs(lyingMaxX - standingMaxX) < abs(lyingMinX - standingMinX) else lyingMaxX
    headPointY = centerPointY

    # calculate sleeping time
    sleeptime = sleeptime+1
    print(sleeptime)
    if sleeptime >= 10:
        sleep_check = image_sleep.day_sleep_time(sleep_check)
    headPoint = [headPointX, headPointY]
    return nowStatus, color, headPoint

def falldown_process(beforeStatus, personPoint, standingPoint, beforeCenterPoint):
    global flag, userHeight, beforeH
    global realFallDown
    global standingTime

    fallMinX = personPoint[0]
    fallMaxX = personPoint[1]
    fallMinY = personPoint[2]
    fallMaxY = personPoint[3]

    standingMinX = standingPoint[0]
    standingMaxX = standingPoint[1]
    standingMinY = standingPoint[2]
    standingMaxY = standingPoint[3]

    centerPointX = int((fallMinX + fallMaxX)/2)
    centerPointY = int((fallMinY + fallMaxY)/2)

    # calculate head point
    headPointX = centerPoint[0] # CenterPointX
    headPointY = personPoint[2] # fallMinY

    now_time = time.time()
    diff_time = now_time - standingTime
    if diff_time <= 1:
        nowStatus, color = status_detected(status.falldown)

        beforeCenterPointX = beforeCenterPoint[0]
        beforeCenterPointY = beforeCenterPoint[1]

        # calculate head point
        headPointX = fallMinX if abs(fallMaxX - standingMaxX) < abs(fallMinX - standingMinX) else fallMaxX
        headPointY = centerPointY
        # footPointX = fallMinX if headPointX == fallMaxX else fallMaxX
        # footPointY = centerPointY

        distance = math.sqrt( (beforeCenterPointX - headPointX)**2 + (standingMinY - headPointY)**2 ) # calculate distance
        realDist = userHeight * distance / beforeH # calculate real distance based user height
        if (time.time() - standingTime) != 0:
            v = realDist / (time.time() - standingTime) # calculate speed
            if flag is False:
                print(str(nowStatus)[7:])
                print(v/100)
                #print("HP : {},{}".format(HeadPointX,HeadPointY))
                #print("CP : {},{}".format(CenterPointX,CenterPointY))
                # request for falldown 
                data = {'user_id' : dataCenter.user_id, 'sensor_id': dataCenter.fall_down, 'num' : v, 'day': 'sunday'}
                requests.post(dataCenter.URL, json=data)
                flag = True
                realFallDown = True
                print("fall down 111")
    elif beforeStatus == status.falldown and realFallDown is True:
        if diff_time >= 5 and diff_time < 10:
            nowStatus, color = status_detected(status.falldown)
            if hasPrinted == False:
                print("fall down 222")
                hasPrinted2 = True
        elif diff_time >= 10:
            nowStatus, color = status_detected(status.falldown)
            print("fall down 333")
    else: # lying
        nowStatus, color = lying_process(beforeStatus, personPoint)

        beforeCenterPointX = beforeCenterPoint[0]
        beforeCenterPointY = beforeCenterPoint[1]

        # calculate head point
        headPointX = fallMinX if abs(fallMaxX - standingMaxX) < abs(fallMinX - standingMinX) else fallMaxX
        headPointY = centerPointY
        # footPointX = fallMinX if headPointX == fallMaxX else fallMaxX
        # footPointY = centerPointY

        distance = math.sqrt( (beforeCenterPointX - headPointX)**2 + (standingMinY - headPointY)**2 )
        realDist = userHeight * distance / beforeH
        if (time.time() - standingTime) != 0:
            v = realDist / (time.time() - standingTime)
            if flag is False:
                print(str(nowStatus)[7:])
                print(v/100)
                #print("HP : {},{}".format(HeadPointX,HeadPointY))
                #print("CP : {},{}".format(CenterPointX,CenterPointY))
                flag = True
    headPoint = [headPointX, headPointY]
    return nowStatus, color, headPoint

