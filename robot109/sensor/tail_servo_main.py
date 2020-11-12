import RPi.GPIO as GPIO
import time
import numpy as np
import socket
import sys
#import dataCenter

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

def setup_tail(body_pin, tail_pin):
    # set up pins
    GPIO.setup(body_pin, GPIO.OUT)
    GPIO.setup(tail_pin, GPIO.OUT)
    body_servo = GPIO.PWM(body_pin, 50)
    tail_servo = GPIO.PWM(tail_pin, 50)
    body_servo.start(7)
    tail_servo.start(7.5)

    return body_servo, tail_servo

def cleanup_tail(body_pin, tail_pin):
    GPIO.cleanup(body_pin)
    GPIO.cleanup(tail_pin)

def changeServo(servo, duty, sleepTime=DEFAULT_SLEEP):
    #print("change tail")
    servo.ChangeDutyCycle(duty)
    time.sleep(sleepTime)

def down_tail(body_servo, tail_servo, sleepTime=DEFAULT_SLEEP):
    global UP_DOWN_SLEEP
    changeServo(tail_servo, 7.5, sleepTime)
    for i in np.arange(3.0,7.0,0.1):
        changeServo(body_servo, i,sleepTime=UP_DOWN_SLEEP)

def up_tail(body_servo, tail_servo, sleepTime=DEFAULT_SLEEP):
    global UP_DOWsuN_SLEEP
    changeServo(tail_servo, 7.5,sleepTime)
    for i in np.arange(7.0,3.0,-0.1):
        changeServo(body_servo, i,sleepTime=UP_DOWN_SLEEP)

def shake_tail(body_servo, tail_servo, sleepTime=DEFAULT_SLEEP, count=DEFAULT_COUNT):
    global SLEEP_START, SLEEP_END
    up_tail(body_servo, tail_servo, sleepTime)

    # to center 
    sleepStart = SLEEP_START
    sleepCur = sleepStart
    sleepEnd = SLEEP_END
    shakeRange = np.arange(7.5,9.0,0.05)
    for idx,j in enumerate(shakeRange):
        changeServo(tail_servo, j,sleepCur)
        sleepCur=sleepStart+((sleepEnd-sleepStart)/len(shakeRange))*idx
    # shake tail
    for i in range(count):
        sleepCur = sleepStart
        shakeRange = np.arange(9.0,6.0,-0.05)
        for idx,j in enumerate(shakeRange):
            changeServo(tail_servo,j,sleepCur)
            sleepCur=sleepStart+((sleepEnd-sleepStart)/len(shakeRange))*idx
        shakeRange = np.arange(6.0,9.0,0.05)
        for idx,j in enumerate(shakeRange):
            changeServo(tail_servo,j,sleepCur)
            sleepCur=sleepStart+((sleepEnd-sleepStart)/len(shakeRange))*idx
    # to center 
    sleepCur = sleepStart
    shakeRange = np.arange(9.0,7.5,-0.05)
    for idx,j in enumerate(shakeRange):
        changeServo(tail_servo,j,sleepCur)
        sleepCur=sleepStart+((sleepEnd-sleepStart)/len(shakeRange))*idx
    #changeServo(body_servo,6.0)
    #GPIO.cleanup(body_pin)
    #GPIO.cleanup(tail_pin)

def main():
    body_servo, tail_servo = setup_tail(36, 38)
    #body_servo, tail_servo = setup_tail(dataCenter.body_pin, dataCenter.tail_pin)
    shake_tail(body_servo, tail_servo)
    down_tail(body_servo, tail_servo)
    cleanup_tail(36, 38)
    #cleanup_tail(dataCenter.body_pin, dataCenter.tail_pin)

if __name__ == "__main__":
    main()
