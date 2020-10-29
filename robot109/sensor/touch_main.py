import RPi.GPIO as GPIO
import time
import requests
import sys
import numpy as np
import socket
import sensor.tail_servo_main as tail_servo_main

#initialise a previous input variable to 0 (Assume no pressure applied)
global prev_input_head, prev_input_body
prev_input_head = False
prev_input_body = False

global touch_count
touch_count = 0

headtouch_pin = 11
bodytouch_pin = 13

GPIO.setmode(GPIO.BOARD)

GPIO.setup(headtouch_pin,GPIO.IN)
GPIO.setup(bodytouch_pin,GPIO.IN)

# variables
global SERVO_MAX_DUTY, SERVO_MIN_DUTY
SERVO_MAX_DUTY = 12
SERVO_MIN_DUTY = 3

global DEFAULT_SLEEP, UP_DOWN_SLEEP, DEFAULT_COUNT
DEFAULT_SLEEP = 1
UP_DOWN_SLEEP = 0.04
DEFAULT_COUNT = 5

global SLEEP_START, SLEEP_END
SLEEP_START = 0.001
SLEEP_END = 0.01

def request_touch():
    global touch_count
    
    data = {'user_id' : 1, 'sensor_id': dataCenter.touch, 'num' : touch_count, 'day': 'Sunday'}
    requests.post(dataCenter.URL, json=data)
    touch_count = 0
    print(touch_count)

def run_client(host='127.0.0.1', port=4000):
    global touch_count
    with socket.socket() as sock:
        sock.connect((host, port))
        data = touch_count
        sock.sendall(data.encode())
        if data == 'bye':
            sock.close()
        res = sock.recv()
        print(res.decode())

def changeTail(body_servo, tail_servo, duty, sleepTime=DEFAULT_SLEEP):
    #print("change tail")
    tail_servo.ChangeDutyCycle(duty)
    time.sleep(sleepTime)

def changeBody(body_servo, tail_servo, duty, sleepTime=DEFAULT_SLEEP):
    body_servo.ChangeDutyCycle(duty)
    time.sleep(sleepTime)

def up_tail(body_servo, tail_servo, sleepTime=DEFAULT_SLEEP):
    global UP_DOWN_SLEEP
    changeTail(body_servo, tail_servo, 7.5,sleepTime)
    for i in np.arange(3.0,6.0,0.1):
        changeBody(body_servo, tail_servo, i,sleepTime=UP_DOWN_SLEEP)
    
def shake_tail(body_servo, tail_servo, sleepTime=DEFAULT_SLEEP, count=DEFAULT_COUNT):
    print("shake tail")
    global SLEEP_START, SLEEP_END
    up_tail(body_servo, tail_servo, sleepTime)

    # to center 
    sleepStart = SLEEP_START
    sleepCur = sleepStart
    sleepEnd = SLEEP_END
    shakeRange = np.arange(7.5,9.0,0.05)
    for idx,j in enumerate(shakeRange):
        changeTail(body_servo, tail_servo, j,sleepCur)
        sleepCur=sleepStart+((sleepEnd-sleepStart)/len(shakeRange))*idx
    print("shake tail 2")
    # shake tail
    for i in range(count):
        sleepCur = sleepStart
        shakeRange = np.arange(9.0,6.0,-0.05)
        for idx,j in enumerate(shakeRange):
            changeTail(body_servo, tail_servo, j,sleepCur)
            sleepCur=sleepStart+((sleepEnd-sleepStart)/len(shakeRange))*idx
        shakeRange = np.arange(6.0,9.0,0.05)
        for idx,j in enumerate(shakeRange):
            changeTail(body_servo, tail_servo, j,sleepCur)
            sleepCur=sleepStart+((sleepEnd-sleepStart)/len(shakeRange))*idx
    print("shake tail 3")
    # to center 
    sleepCur = sleepStart
    shakeRange = np.arange(9.0,7.5,-0.05)
    for idx,j in enumerate(shakeRange):
        changeTail(body_servo, tail_servo, j,sleepCur)
        sleepCur=sleepStart+((sleepEnd-sleepStart)/len(shakeRange))*idx
    print("shake tail 4 ")
    changeBody(body_servo, tail_servo, 6.0)
    # GPIO.cleanup(body_pin)
    # GPIO.cleanup(tail_pin)

def main():
    # pins
    body_pin = 36
    tail_pin = 38

    # set up pins
    GPIO.cleanup(body_pin)
    GPIO.cleanup(tail_pin)
    GPIO.setup(body_pin, GPIO.OUT)
    GPIO.setup(tail_pin, GPIO.OUT)
    body_servo = GPIO.PWM(body_pin, 50)
    tail_servo = GPIO.PWM(tail_pin, 50)
    body_servo.start(3)
    tail_servo.start(7.5)

    while True:
        global touch_count
        global prev_input_head, prev_input_body
        input_head = GPIO.input(headtouch_pin)
        input_body = GPIO.input(bodytouch_pin)
        #check_touch(input_head, input_body)
        if (prev_input_head and (not prev_input_body)) and input_body:
            print("head to body")
            touch_count += 1
        elif (prev_input_body and (not prev_input_head)) and input_head:
            print("body to head")
            touch_count += 1 
        elif (not prev_input_head) and input_head:
            print("only head")
            shake_tail(body_servo, tail_servo)
        elif (not prev_input_body) and input_body:
            print("only body")

        #update previous input
        prev_input_head = input_head
        prev_input_body = input_body

        time.sleep(0.1)

if __name__ == "__main__":
    main()