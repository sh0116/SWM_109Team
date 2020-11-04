import cv2
import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray
import re
from tflite_runtime.interpreter import Interpreter
import image_processing.image_tf as image_tf
import image_processing.image_falldown as image_falldown
import image_processing.image_sleep as image_sleep
import image_processing.image_activity as image_activity
import image_processing.head_servo_main as head_servo_main
import time
import dataCenter
import requests

global beforeStatus, nowStatus
beforeStatus = image_falldown.status.standing
nowStatus = image_falldown.status.standing

global beforeCenterPointX, beforeCenterPointY
beforeCenterPointX = 0
beforeCenterPointY = 0

global realtime, nowTime, hourrealtime, hourTime
realtime = 0
hourrealtime = 0
nowTime = time.time()
hourTime = time.time()

def realtime_count(Cpx,Cpy,Bpx,Bpy):
    global realtime, nowTime, hourrealtime, hourTime
    count_check = time.time()
    
    if abs(Cpx - Bpx) >= 15 or abs(Cpy-Bpy) >=15:
        realtime+=1

    if count_check - nowTime > dataCenter.activ_interval:
        data = {'user_id' : dataCenter.user_id, 'sensor_id': dataCenter.activity, 'num' : realtime, 'day': 'sunday'}
        requests.post(dataCenter.URL, json=data)
        nowTime = time.time()
        hourrealtime += realtime
        realtime = 0 
    #schedule per minute activity
    if count_check - hourTime > dataCenter.hour_activ_interval:
        data = {'user_id' : dataCenter.user_id, 'sensor_id': dataCenter.hour_activity, 'num' : hourrealtime, 'day': 'sunday'}
        requests.post(dataCenter.URL, json=data)
        image_activity.avg_activity(hourrealtime)
        hourTime = time.time()

def draw_rect(frame, xmin, ymin, xmax, ymax, headPoint, nowStatus, color):
    label = str(nowStatus)[7:]
    font = cv2.FONT_HERSHEY_PLAIN
    cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), color, 5)
    cv2.putText(frame, label, (xmin, ymin - 5), font, 2, color, 5)
    cv2.circle(frame, (headPoint[0], headPoint[1]), 10, (0,0,255), -1)

minConfidence = 0.6
def main():
    global beforeStatus
    global beforeCenterPointX, beforeCenterPointY
    global realtime
    # Open cam
    cap = PiCamera()
    try:
        cap.framerate = 32
        cap.resolution = (320,240)
    except:
        print("cannot open cam")
    rawCapture = PiRGBArray(cap, size=(320, 240))
    rawCapture.truncate(0)
    interpreter = image_tf.load_interpreter()

    # setup head servo
    head_servo = head_servo_main.setup_head(dataCenter.head_pin)
    isHeadClean = False
    nowTime = time.time()
    hourTime = time.time()
    showTime = time.time()
    isTurned1 = isTurned2 = isTurned3 = False

    standingPoint = [0,0,0,0]
    # Detecting objects
    for frame in cap.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        #schedule.run_pending()
        #start_time = time.time()
        img = np.asarray(frame.array)
        height, width, channels = img.shape
        img = cv2.resize(img, (300,300))
    
        outs = image_tf.detect_objects(interpreter, img, minConfidence)

        if not outs: # nothing detected
            #print("nothing detected | {} {} {} ".format(isTurned1, isTurned2, isTurned3))
            notShowTime = time.time()
            diffTime = notShowTime - showTime
            if diffTime >= dataCenter.head_interval: # turn head again
                isTurned1 = isTurned2 = isTurned3 = False
                showTime = time.time()
                continue
            if diffTime >= dataCenter.head_interval: # turn head 30 minutes after nothing detected
                if isHeadClean: 
                    head_servo = head_servo_main.setup_head(dataCenter.head_pin)
                if not isTurned1:
                    head_servo_main.turn_head_right(head_servo)
                    isTurned1 = True
                else:
                    if not isTurned2:
                        head_servo_main.turn_head_left(head_servo)
                        isTurned2 = True
                    else:
                        if not isTurned3:
                            head_servo_main.turn_head_center(head_servo)
                            isTurned3= True
        for out in outs: # anything detected 
            if out['class_id'] == 0 and out['score'] > minConfidence: # person detected
                # refresh head servo variables
                if isTurned1 or isTurned2 or isTurned3:
                    isTurned1 = isTurned2 = isTurned3 = False
                    head_servo_main.cleanup_head(dataCenter.head_pin)
                    isHeadClean = True
                showTime = time.time()
                #print("person detected")
                # Convert the bounding box figures from relative coordinates
                # to absolute coordinates based on the original resolution

                ymin, xmin, ymax, xmax = out['bounding_box']
                xmin = int(xmin * width)
                xmax = int(xmax * width)
                ymin = int(ymin * height)
                ymax = int(ymax * height)
                w = xmax - xmin
                h = ymax - ymin

                centerPointX = int((xmin + xmax)/2)
                centerPointY = int((ymin + ymax)/2)
                headPointX = int(centerPointX)
                headPointY = int(ymin)
                footPointX = int(centerPointX)
                footPointY = int(h + headPointY)

                # make list format
                personPoint = [xmin, xmax, ymin, ymax]
                centerPoint = [centerPointX, centerPointY]
                beforeCenterPoint = [beforeCenterPointX, beforeCenterPointY]
                headPoint = [headPointX, headPointY]
                footPoint = [footPointX, footPointY]
                
                if w/2 > h: # fall down
                    nowStatus, color, headPoint = image_falldown.falldown_process(beforeStatus, personPoint, standingPoint, beforeCenterPoint)
                elif w > h: # lying
                    nowStatus, color, headPoint = image_falldown.lying_process(beforeStatus, personPoint, standingPoint)
                else: # standing
                    nowStatus, color, standingPoint = image_falldown.standing_process(beforeStatus, personPoint)
                    #real_activity = image_activity.realtime_count(CenterPointX, CenterPointY, BeforeCenterPointX, BeforeCenterPointY,real_activity) # calculate activity 
                    realtime_count(centerPointX, centerPointY, beforeCenterPointX, beforeCenterPointY) # calculate activity 
                # save now center point
                beforeCenterPointX = centerPointX
                beforeCenterPointY = centerPointY
                beforeStatus = nowStatus
                # draw rectangle
                draw_rect(img, xmin, ymin, xmax, ymax, headPoint, nowStatus, color)
                
        cv2.imshow("frame", img)
        rawCapture.truncate(0)
        #end_time = time.time()
        #process_time = end_time - start_time
        #print("=== A frame took {:.3f} seconds".format(process_time))
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            cap.close()
            break
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
