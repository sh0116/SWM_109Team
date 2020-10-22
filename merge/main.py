import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray
import re
from tflite_runtime.interpreter import Interpreter
import tflite_tf
import tflite_falldown
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
import NLP_Main as NLP

#time_URL = 'http://109center.com:5000/sensor_data'
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

push_temperature = 0
push_humidity = 0

def request_temper():
    humidity, temperature = temperature.get_temp()
    temperature_data = {'user_id' : 1 , 'sensor_id' : 1, 'num': temperature, 'day' : 'sunday'}
    request = requests.post(URL, json=temperature_data)
    humidity_data = {'user_id' : 1 , 'sensor_id' : 2, 'num' : humidity, 'day' : 'sunday'}
    request = requests.post(URL, json=humidity_data)

# scheduler
sched.add_job(request_temper,'interval',seconds=20)
sched.start()

def draw_rect(frame, xmin, ymin, xmax, ymax, nowStatus, color):
    label = str(nowStatus)[7:]
    font = cv2.FONT_HERSHEY_PLAIN
    cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), color, 5)
    cv2.putText(frame, label, (xmin, ymin - 5), font, 2, color, 5)

min_confidence = 0.6
def main():
    global beforeStatus
    global prev_input_body, prev_input_head, touch_count
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

        if ((not prev_input_body) and input_body):
            print("Under Pressure")
            touch_count +=1
            print(touch_count)
        if ((not prev_input_head) and input_head):
            print("Under2 Pressure")
            touch_count +=1
            print(touch_count)
        if touch_count == 5:
            servo.shake_tail(count=3)
            time.sleep(1)
            NLP.call_TTS("기분이 좋아요")
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
                w = xmax - xmin
                h = ymax - ymin

                if w/2 > h: # fall down
                    nowStatus, color = tflite_falldown.falldown_process(beforeStatus)
                elif w > h: # lying
                    nowStatus, color = tflite_falldown.lying_process(beforeStatus)
                else: # standing
                    nowStatus, color = tflite_falldown.standing_process(beforeStatus)
                beforeStatus = nowStatus
                draw_rect(img, xmin, ymin, xmax, ymax, nowStatus, color)
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
