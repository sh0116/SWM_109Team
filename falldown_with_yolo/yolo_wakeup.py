import cv2
import numpy as np
import time
import enum
import requests
from datetime import datetime
#import pygame

#URL = 'http://13.125.221.213:5555/fall_down'
#data = {'user_id' : '1'}
time_URL = 'http://13.125.221.213:5000/wake_up'
day = ['월요일','화요일','수요일', '목요일', '금요일', '토요일', '일요일']
cal_day = datetime.today().weekday()

sleep_check = 0
wake_check = 0

# Load Yolo
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
blue_color = (255,0,0)
red_color = (0,0,255)
green_color = (0,255,0)

# Open Cam
try:
    print("open cam")
    cap = cv2.VideoCapture(0)
    #cap = cv2.VideoCapture('/Users/hyunjigonji/yolo_object_detection')
except:
    print("not working")
cap.set(3, 800)
cap.set(4, 600)

'''
def play_mp3_question():
    pygame.mixer.init()
    pygame.mixer.music.load("./question.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
    #print("play over...")
    return

def play_mp3_notice():
    pygame.mixer.init()
    pygame.mixer.music.load("./notice.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
    #print("play over...")
    return
'''

def day_sleep_time():
    sleep_hour = int(nowTuple.tm_hour) 
    sleep_min = int(nowTuple.tm_min)
    seconds = (pre_time.hour * 60 + pre_time.minute) * 60 + pre_time.second
    sleep_time = seconds/3600
    data = {'user_id' : '1', 'graph' : sleep_time,'day':day[cal_day]}
    print("취침일시 : {}-{}-{} {}:{}:{}".format(pre_time.year, pre_time.month, pre_time.day
                                            ,pre_time.hour,pre_time.minute,pre_time.second))
    print("잠들었습니다. %d",sleep_time,day[cal_day])
    #res = requests.post(time_URL, json=data)
    
def day_wake_time():
    wake_up_hour = int(nowTuple.tm_hour)
    wake_up_min = int(nowTuple.tm_min)
    seconds = (pre_time.hour * 60 + pre_time.minute) * 60 + pre_time.second
    wake_up_time = seconds/3600
    if seconds >= 14400 and seconds<=27000:
        data = {'user_id' : '3', 'graph' : wake_up_time,'day':day[cal_day]}
        print("기상일시 : {}-{}-{} {}:{}:{}".format(pre_time.year, pre_time.month, pre_time.day
                                                ,pre_time.hour,pre_time.minute,pre_time.second))
        print("깨어났네요 %d",wake_up_time,day[cal_day])
        #res = requests.post(time_URL, json=data)

class status(enum.Enum):
    standing = 0
    lying = 1
    falldown = 2
    
pre_time = datetime.now()
nowTuple = pre_time.timetuple()

origin_time = 0
now_time = 0
sleeptime=0

beforeStatus = status.standing
nowStatus = status.standing

standing_time = time.time()
lying_time = time.time()
falldown_time = time.time()

hasPrinted = False

# Taking video
while True:
    # Loading image
    ret, frame = cap.read()
    height, width, channels = frame.shape

    # Detecting objects
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            if str(classes[class_id]) != 'person': continue
            confidence = scores[class_id]
            if confidence > 0.8: # person detected when confidence is over 0.8
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                # Rectangle coordinates
                x = int(center_x - w/2)
                y = int(center_y - h/2)
                if w/2 > h: # fall down
                    now_time = time.time()
                    diff_time = now_time - standing_time
                    if diff_time <= 1:
                        falldown_time = time.time()
                        nowStatus = status.falldown
                        color = redf_color
                        print("fall down 111")
                        #play_mp3_question()
                    elif beforeStatus == status.falldown:
                        if diff_time >= 5 and diff_time < 10:
                            falldown_time = time.time()
                            nowStatus = status.falldown
                            color = red_color
                            if hasPrinted == False:
                                print("fall down 222")
                                #play_mp3_question()
                                hasPrinted2 = True
                        elif diff_time >= 10:
                            falldown_time = time.time()
                            nowStatus = status.falldown
                            color = red_color
                            print("fall down 333")
                            #play_mp3_notice()
                            #quit()
                    else: # lying
                        lying_time = time.time()
                        nowStatus = status.lying
                        sleeptime = sleeptime+1
                        if sleeptime >= 5:
                            seconds = (pre_time.hour * 60 + pre_time.minute) * 60 + pre_time.second
                            sleep_time = seconds/3600
                            if (seconds >= 75,600 and seconds<=86339) or (seconds >=0 and seconds <=1800) :
                                if sleep_check == 0:
                                    sleep_check +=1
                                    day_sleep_time()
                                else:
                                    continue
                            else:
                                sleep_check = 0
                            
                        
                elif w > h: # lying
                    lying_time = time.time()
                    nowStatus = status.lying
                    sleeptime = sleeptime+1
                    if sleeptime >= 5:
                            seconds = (pre_time.hour * 60 + pre_time.minute) * 60 + pre_time.second
                            sleep_time = seconds/3600
                            if (seconds >= 75,600 and seconds<=86339) or (seconds >=0 and seconds <=1800) :
                                if sleep_check == 0:
                                    sleep_check +=1
                                    day_sleep_time()
                                else:
                                    continue
                            else:
                                sleep_check = 0
                    color = green_color
                else: # standing
                    standing_time = time.time()
                    nowStatus = status.standing
                    if sleeptime >= 10:
                        seconds = (pre_time.hour * 60 + pre_time.minute) * 60 + pre_time.second
                            sleep_time = seconds/3600
                            if seconds >= 14400 and seconds<=27000:
                                if wake_check == 0:
                                    wake_check +=1
                                    day_wake_time()
                                else:
                                    continue
                            else:
                                wake_check = 0
                        
                    color = blue_color
                    origin_time = 0
                    sleeptime=0
                label = str(nowStatus)[7:] # parsing status to label
                font = cv2.FONT_HERSHEY_SIMPLEX # define font style
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 10) # draw rectangle
                cv2.putText(frame, label, (x, y - 30), font, 3, color, 7) # write text
                beforeStatus = nowStatus
    cv2.imshow("Frame", frame)
    k = cv2.waitKey(1) & 0xFF
    if k == 27: break
cv2.destroyAllWindows()
