import dataCenter
import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray
import re
from tflite_runtime.interpreter import Interpreter
import tflite_tf
import tflite_falldown
import tflite_activity
import sensor_temp
import sensor_servo
import sensor_touch


import RPi.GPIO as GPIO
import numpy as np
import time
import Adafruit_DHT

import sys
from apscheduler.schedulers.background import BackgroundScheduler
import requests
sys.path.append("/home/pi/109system/NLP")
#import NLP_Main as NLP

# GPIO
GPIO.setmode(GPIO.BOARD)

head_pin = 16 # servo for head
headtouch_pin = 11 # touch for head
bodytouch_pin = 13 # touch for body

GPIO.setup(headtouch_pin,GPIO.IN)
GPIO.setup(bodytouch_pin,GPIO.IN)

# variables for opencv
global beforeStatus, nowStatus
beforeStatus = tflite_falldown.status.standing
nowStatus = tflite_falldown.status.standing

global BeforeCenterPointX, BeforeCenterPointY
BeforeCenterPointX = 0
BeforeCenterPointY = 0

# scheduler
sched = BackgroundScheduler()
sched.add_job(sensor_temp.request_temper, 'interval', seconds = dataCenter.temp_interval)
sched.add_job(sensor_touch.request_touch,'interval', seconds = dataCenter.touch_interval)
sched.add_job(tflite_activity.request_realtime, 'interval', seconds = dataCenter.activ_interval)
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
    global BeforeCenterPointX, BeforeCenterPointY
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
        sensor_touch.check_touch(input_head, input_body)

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
                    tflite_activity.realtime_count(CenterPointX,CenterPointY,BeforeCenterPointX,BeforeCenterPointY) # calculate activity 
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
