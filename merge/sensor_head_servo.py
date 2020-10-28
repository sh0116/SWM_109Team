import RPi.GPIO as GPIO
import time
import numpy as np
import os

GPIO.setmode(GPIO.BOARD)

# variables
global SERVO_MAX_DUTY, SERVO_MIN_DUTY
SERVO_MAX_DUTY = 12.0
SERVO_MIN_DUTY = 3.0

global DEFAULT_SLEEP, UP_DOWN_SLEEP
DEFAULT_SLEEP = 1
LEFT_RIGHT_SLEEP = 0.04

global SLEEP_START, SLEEP_END
SLEEP_START = 0.001
SLEEP_END = 0.01

# pins
head_pin = 16

# set up pins
GPIO.setup(head_pin, GPIO.OUT)
head_servo = GPIO.PWM(head_pin, 50)
head_servo.start(5.5)

def execute_turn_head():
    os.system("python3 sensor_head_servo.py&")

def changeHead(duty, sleepTime=DEFAULT_SLEEP):
    head_servo.ChangeDutyCycle(duty)
    time.sleep(sleepTime)

def turn_head(sleepTime=DEFAULT_SLEEP):
    global LEFT_RIGHT_SLEEP
    # center to left
    for i in np.arange(5.5, 3.0, -0.1): 
        changeHead(i,sleepTime=LEFT_RIGHT_SLEEP)
    print("1 | 5.5 to 3")

    for i in np.arange(3.0, 8.0, 0.1):
        changeHead(i,sleepTime=LEFT_RIGHT_SLEEP)
    print("2 | 3 to 8")

    # left to center
    for i in np.arange(8.0, 5.5, -0.1):
        changeHead(i,sleepTime=LEFT_RIGHT_SLEEP)
    print("3 | 8 to 5.5")

if __name__ == "__main__":
    print("start head")
    turn_head()
    GPIO.cleanup(head_pin)
    print("end head")