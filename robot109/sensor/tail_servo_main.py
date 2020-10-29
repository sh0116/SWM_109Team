import RPi.GPIO as GPIO
import time
import numpy as np
import socket
import sys

GPIO.setmode(GPIO.BOARD)

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

# # pins
# body_pin = 36
# tail_pin = 38

# # set up pins
# GPIO.cleanup(body_pin)
# GPIO.cleanup(tail_pin)
# GPIO.setup(body_pin, GPIO.OUT)
# GPIO.setup(tail_pin, GPIO.OUT)
# body_servo = GPIO.PWM(body_pin, 50)
# tail_servo = GPIO.PWM(tail_pin, 50)
# body_servo.start(3)
# tail_servo.start(7.5)

def main(host = "127.0.0.1", port = 4000):
    with socket.socket() as s:
        s.bind((host, port))
        s.listen()
        conn, addr = s.accept()
        while True:
            data = conn.recv()
            msg = data.decode()
            print(msg)
            if msg == 'bye':
                conn.close()
                break

def changeTail(duty, sleepTime=DEFAULT_SLEEP):
    #print("change tail")
    tail_servo.ChangeDutyCycle(duty)
    time.sleep(sleepTime)

def changeBody(duty, sleepTime=DEFAULT_SLEEP):
    body_servo.ChangeDutyCycle(duty)
    time.sleep(sleepTime)

def down_tail(sleepTime=DEFAULT_SLEEP):
    global UP_DOWN_SLEEP
    changeTail(7.5,sleepTime)
    for i in np.arange(6.0,3.0,-0.05):
        changeBody(i,sleepTime=UP_DOWN_SLEEP)

def up_tail(sleepTime=DEFAULT_SLEEP):
    global UP_DOWN_SLEEP
    changeTail(7.5,sleepTime)
    for i in np.arange(3.0,6.0,0.1):
        changeBody(i,sleepTime=UP_DOWN_SLEEP)

def shake_tail(sleepTime=DEFAULT_SLEEP, count=DEFAULT_COUNT):
    print("shake tail")
    global SLEEP_START, SLEEP_END
    up_tail(sleepTime)

    # to center 
    sleepStart = SLEEP_START
    sleepCur = sleepStart
    sleepEnd = SLEEP_END
    shakeRange = np.arange(7.5,9.0,0.05)
    for idx,j in enumerate(shakeRange):
        changeTail(j,sleepCur)
        sleepCur=sleepStart+((sleepEnd-sleepStart)/len(shakeRange))*idx
    print("shake tail 2")
    # shake tail
    for i in range(count):
        sleepCur = sleepStart
        shakeRange = np.arange(9.0,6.0,-0.05)
        for idx,j in enumerate(shakeRange):
            changeTail(j,sleepCur)
            sleepCur=sleepStart+((sleepEnd-sleepStart)/len(shakeRange))*idx
        shakeRange = np.arange(6.0,9.0,0.05)
        for idx,j in enumerate(shakeRange):
            changeTail(j,sleepCur)
            sleepCur=sleepStart+((sleepEnd-sleepStart)/len(shakeRange))*idx
    print("shake tail 3")
    # to center 
    sleepCur = sleepStart
    shakeRange = np.arange(9.0,7.5,-0.05)
    for idx,j in enumerate(shakeRange):
        changeTail(j,sleepCur)
        sleepCur=sleepStart+((sleepEnd-sleepStart)/len(shakeRange))*idx
    print("shake tail 4 ")
    changeBody(6.0)
    # GPIO.cleanup(body_pin)
    # GPIO.cleanup(tail_pin)

if __name__ == "__main__":
    shake_tail()
