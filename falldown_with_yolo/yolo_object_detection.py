import cv2
import numpy as np
import time
import enum
import requests
import time
from apscheduler.schedulers.background import BackgroundScheduler
import math

URL = 'http://13.125.221.213:5000/sensor'
sched = BackgroundScheduler()
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
    #cap = cv2.VideoCapture('./example1.mp4')
except:
    print("not working")
#cap.set(3, 800)
#cap.set(4, 600)

class status(enum.Enum):
    standing = 0
    lying = 1
    falldown = 2


origin_time = 0
now_time = 0
beforeStatus = status.standing
nowStatus = status.standing
beforeCenterX = 0
beforeCenterY = 0

global realtime
standingMinX=0
standingMaxX=0
standingMinY=0
standingMaxY=0
fallMinX=0
fallMaxX=0
fallMinY=0
fallMaxY=0
flag = False

beforeH = 1
standingTime = time.time()

userHeight = 160

realtime=0

def realtime_count(Cpx,Cpy,Bpx,Bpy):
    global realtime
    if abs(Cpx - Bpx) >=15 or abs(Cpy-Bpy) >=15:
        realtime+=1

def push_realtime():
    global realtime
    data = {'user_id' : '1', 'sendor_id':6, 'num' : realtime,'day': 'saturday'}
    #res = requests.post(URL, json=data)
    #print(realtime)
    realtime = 0
sched.add_job(push_realtime, 'interval', seconds=20)
            
sched.start()

# Taking video
while True:
    # Loading image
    ret, frame = cap.read()
    #frame = cv2.resize(frame, (600,600), cv2.INTER_AREA)
    height, width, channels = frame.shape
    #height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    #width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)

    # Detecting objects
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    #blob = cv2.dnn.blobFromImage(frame)

    net.setInput(blob)
    outs = net.forward(output_layers)

    # Showing informations on the screen
    class_ids = []
    confidences = []
    boxes = []
    
    # sched = BlockingScheduler()
    # sched.add_job(push_realtime, 'interval', seconds=1)
    # sched.start()
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            if str(classes[class_id]) != 'person': continue
            confidence = scores[class_id]
            if confidence > 0.8: # person detected when confidence is over 0.8
                CenterPointX = int(detection[0] * width)
                CenterPointY = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                # Rectangle coordinates
                x = int(CenterPointX - w/2)
                y = int(CenterPointY - h/2)
                
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    font = cv2.FONT_HERSHEY_PLAIN
    
    for i in range(len(boxes)):
        if i in indexes:
            x,y,w,h = boxes[i]
            HeadPointX = CenterPointX
            HeadPointY = y
            FootPointX = CenterPointX
            FootPointY = h+y

            if w/2 > h: # detected
                color = red_color
                if beforeStatus == status.standing or beforeStatus == status.falldown:
                    nowStatus = status.falldown
                    if origin_time == 0:
                        origin_time = time.time() # count start
                        #print("fall detected!")
                        
                        fallMinX = x
                        fallMaxX = x+w
                        fallMinY = y
                        fallMaxY = y+h

                        HeadPointX = fallMinX if abs(fallMaxX-standingMaxX) < abs(fallMinX-standingMinX) else fallMaxX
                        HeadPointY = CenterPointY

                        FootPointX = fallMinX if HeadPointX==fallMaxX else fallMaxX
                        FootPointY = CenterPointY
                    
                        distance = math.sqrt( (beforeCenterX-HeadPointX)**2 + (standingMinY-HeadPointY)**2 )
                        realDist = userHeight * distance / beforeH
                        if (time.time() - standingTime) != 0:
                            v = realDist / (time.time() - standingTime)
                            if flag is False:
                                print(str(nowStatus)[7:])
                                print(v/100)
                                #print("HP : {},{}".format(HeadPointX,HeadPointY))
                                #print("CP : {},{}".format(CenterPointX,CenterPointY))
                                flag = True
                            
                        #play_mp3_question()
                    else:
                        now_time = time.time()
                        if now_time - origin_time >= 5 and now_time - origin_time < 10 and origin_time != 0:
                            #print(args)
                            print("fall down 22!")
                            #play_mp3_question()
                        elif now_time - origin_time >= 10 and origin_time != 0:
                            #print(args)
                            print("fall down 33!")
                            #play_mp3_notice()
                            #res = requests.post(URL, json=data)
                            #origin_time = 0
                            #exit()
                else: # lying
                    nowStatus = status.lying
                    origin_time = 0
                    color = green_color
                    
                    fallMinX = x
                    fallMaxX = x+w
                    fallMinY = y
                    fallMaxY = y+h

                    HeadPointX = fallMinX if abs(fallMaxX-standingMaxX) < abs(fallMinX-standingMinX) else fallMaxX
                    HeadPointY = CenterPointY

                    FootPointX = fallMinX if HeadPointX==fallMaxX else fallMaxX
                    FootPointY = CenterPointY
                    distance = math.sqrt( (beforeCenterX-HeadPointX)**2 + (standingMinY-HeadPointY)**2 )
                    realDist = userHeight * distance / beforeH
                    if (time.time() - standingTime) != 0:
                        v = realDist / (time.time() - standingTime)
                        if flag is False:
                            print(str(nowStatus)[7:])
                            print(v/100)
                            #print("HP : {},{}".format(HeadPointX,HeadPointY))
                            #print("CP : {},{}".format(CenterPointX,CenterPointY))
                            flag = True
            elif w > h: # lying
                nowStatus = status.lying
                color = green_color
                origin_time = 0
            else: # standing
                nowStatus = status.standing
                color = blue_color
                origin_time = 0
                realtime_count(CenterPointX,CenterPointY,beforeCenterX,beforeCenterY)
                beforeCenterX = CenterPointX
                beforeCenterY = CenterPointY
                standingMinX = x
                standingMaxX = x+w
                standingMinY = y
                standingMaxY = y+h
                beforeH = h
                standingTime = time.time()
                flag = False
                
            label = str(nowStatus)[7:]
            font = cv2.FONT_HERSHEY_PLAIN
            #color = colors[i]
            hpstr = "HP : {},{}".format(HeadPointX,HeadPointY)
            cpstr = "CP : {},{}".format(CenterPointX,CenterPointY)
            #cv2.putText(frame, hpstr,(5,20), font, 2, red_color,2)
            #cv2.putText(frame, cpstr,(5,60), font, 2, red_color,2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 10)
            cv2.putText(frame, label, (x, y - 30), font, 7, color, 7)
            cv2.circle(frame, (CenterPointX, CenterPointY), 10, (0,255,255), -1)
            cv2.circle(frame, (HeadPointX, HeadPointY), 10, (0,0,255), -1)
            cv2.line(frame,(HeadPointX, HeadPointY),(FootPointX, FootPointY),green_color,5)
            #print(center_Pointw,center_Pointy)
            boxes.append([x, y, w, h])
            confidences.append(float(confidence))
            class_ids.append(class_id)
            beforeStatus = nowStatus
    cv2.imshow("Frame", frame)
    k = cv2.waitKey(1) & 0xFF
    if k == 27: break
    #time.sleep(0.5)
cv2.destroyAllWindows()
