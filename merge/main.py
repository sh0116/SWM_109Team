import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray
import re
from tflite_runtime.interpreter import Interpreter
import tflite_tf
import tflite_falldown
import tflite_activity
import temperature
import servo


import RPi.GPIO as GPIO
import numpy as np
import time
import Adafruit_DHT

import sys
from apscheduler.schedulers.background import BackgroundScheduler
import requests
sys.path.append("/home/pi/109system/NLP")
#import NLP_Main as NLP

URL = 'http://13.125.221.213:5000/sensor'
sched = BackgroundScheduler()

# GPIO
GPIO.setmode(GPIO.BOARD)

head_pin = 16 # servo for head
headtouch_pin = 11 # touch for head
bodytouch_pin = 13 # touch for body

GPIO.setup(headtouch_pin,GPIO.IN)
GPIO.setup(bodytouch_pin,GPIO.IN)

# variables for cv
global beforeStatus, nowStatus
beforeStatus = tflite_falldown.status.standing
nowStatus = tflite_falldown.status.standing

# variables for touch sensor
#initialise a previous input variable to 0 (Assume no pressure applied)
global prev_input_body, prev_input_head, touch_count
prev_input_body = 0
prev_input_head = 0
touch_count = 0

global realtime,BeforeCenterPointX,BeforeCenterPointY 
realtime = 0
BeforeCenterPointX = 0
BeforeCenterPointY = 0

def request_temper():
    humid, temper = temperature.get_temp()
    temperature_data = {'user_id' : 1 , 'sensor_id' : 1, 'num': temper, 'day' : 'sunday'}
    request = requests.post(URL, json=temperature_data)
    humidity_data = {'user_id' : 1 , 'sensor_id' : 2, 'num' : humid, 'day' : 'sunday'}
    request = requests.post(URL, json=humidity_data)
def request_realtime():
    global realtime
    data = {'user_id' : 1, 'sensor_id': 6, 'num' : realtime, 'day': 'Sunday'}
    res = requests.post(URL, json=data)
    print(realtime)
    realtime = 0

# scheduler
sched.add_job(request_temper,'interval',seconds=20)
sched.add_job(request_realtime,'interval',seconds = 10)
sched.start()

def draw_rect(frame, xmin, ymin, xmax, ymax, nowStatus, color,CenterPointX,CenterPointY):
    label = str(nowStatus)[7:]
    font = cv2.FONT_HERSHEY_PLAIN
    cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), color, 5)
    cv2.putText(frame, label, (xmin, ymin - 5), font, 2, color, 5)
    cv2.circle(frame,(CenterPointX,CenterPointY),10,(0,255,255),-1)
    
min_confidence = 0.6
def main():
    global beforeStatus
    global prev_input_body, prev_input_head, touch_count
    global realtime,BeforeCenterPointX,BeforeCenterPointY
    # Open cam
    cap = PiCamera()
    try:
        cap.framerate = 32
        cap.resolution = (320,240)
    except:
        print("cannot open cam")
    rawCapture = PiRGBArray(cap, size=(320, 240))
    rawCapture.truncate(0)
    interpreter = tflite_tf.load_interpreter()

    # Detecting objects
    for frame in cap.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        input_head = GPIO.input(headtouch_pin)
        input_body = GPIO.input(bodytouch_pin)
        if prev_input_head and ((not prev_input_body) and input_body):
            print("head to body")
            touch_count +=1
        elif prev_input_body and ((not prev_input_head) and input_head):
            print("body to head")
            touch_count +=1 
        elif (not prev_input_head) and input_head :
            print("only head")
        elif (not prev_input_body) and input_body:
            print("only body")

        if touch_count == 15:
            #servo.shake_tail(count=3)
            #time.sleep(1)
            #NLP.call_TTS("기분이 좋아요")
            touch_count = 0
        prev_input_head = input_head
        prev_input_body = input_body

        #start_time = time.time()
        img = np.asarray(frame.array)
        height, width, channels = img.shape
        img = cv2.resize(img, (300,300))

        outs = tflite_tf.detect_objects(interpreter, img, min_confidence)

        for out in outs:
            if out['class_id'] == 0 and out['score'] > min_confidence:
                # Convert the bounding box figures from relative coordinates
                # to absolute coordinates based on the original resolution
                ymin, xmin, ymax, xmax = out['bounding_box']
                xmin = int(xmin * width)
                xmax = int(xmax * width)
                ymin = int(ymin * height)
                ymax = int(ymax * height)
                CenterPointX = int((xmin + xmax)/2)
                CenterPointY = int((ymin + ymax)/2)
                w = xmax - xmin
                h = ymax - ymin

                if w/2 > h: # fall down
                    nowStatus, color = tflite_falldown.falldown_process(beforeStatus)
                elif w > h: # lying
                    nowStatus, color = tflite_falldown.lying_process(beforeStatus)
                else: # standing
                    nowStatus, color = tflite_falldown.standing_process(beforeStatus)
                    #BeforeCenterPointX = CenterPointX
                    #BeforeCenterPointY = CenterPointY
                    activity = tflite_activity.realtime_count(CenterPointX,CenterPointY,BeforeCenterPointX,BeforeCenterPointY)
                    if activity is True:
                        realtime +=1 
                beforeStatus = nowStatus
                draw_rect(img, xmin, ymin, xmax, ymax, nowStatus, color,CenterPointX,CenterPointY)
                BeforeCenterPointX = CenterPointX
                BeforeCenterPointY = CenterPointY
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
