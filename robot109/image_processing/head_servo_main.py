import RPi.GPIO as GPIO
import time
import numpy as np
import dataCenter

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

def setup_head(head_pin):
    # set up pins
    GPIO.setup(head_pin, GPIO.OUT)
    head_servo = GPIO.PWM(head_pin, 50)
    head_servo.start(7.5)
    return head_servo

def cleanup_head(head_pin):
    GPIO.cleanup(head_pin)

def changeServo(head_servo, duty, sleepTime=DEFAULT_SLEEP):
    head_servo.ChangeDutyCycle(duty)
    time.sleep(sleepTime)

def turn_head(head_servo, sleepTime=DEFAULT_SLEEP):
    global LEFT_RIGHT_SLEEP
    # center to right
    for i in np.arange(7.5, 4.5, -0.1): 
        changeServo(head_servo, i,sleepTime=LEFT_RIGHT_SLEEP)
    print("1 | 7.5 to 4.5")

    # right to left
    for i in np.arange(4.5, 10.5, 0.1):
        changeServo(head_servo, i,sleepTime=LEFT_RIGHT_SLEEP)
    print("2 | 4.5 to 10.5")

    # left to center
    for i in np.arange(10.5, 7.5, -0.1):
        changeServo(head_servo, i,sleepTime=LEFT_RIGHT_SLEEP)
    print("3 | 10.5 to 7.5")

def turn_head_right(head_servo, sleepTime=DEFAULT_SLEEP):
    global LEFT_RIGHT_SLEEP
    # center to right
    for i in np.arange(7.5, 4.5, -0.1): 
        changeServo(head_servo, i,sleepTime=LEFT_RIGHT_SLEEP)   

def turn_head_left(head_servo, sleepTime=DEFAULT_SLEEP):
    global LEFT_RIGHT_SLEEP
    # right to left
    for i in np.arange(4.5, 10.5, 0.1):
        changeServo(head_servo, i,sleepTime=LEFT_RIGHT_SLEEP)

def turn_head_center(head_servo, sleepTime=DEFAULT_SLEEP):
    global LEFT_RIGHT_SLEEP
    # left to center
    for i in np.arange(10.5, 7.5, -0.1):
        changeServo(head_servo, i,sleepTime=LEFT_RIGHT_SLEEP)

def main():
    head_servo = setup_head(dataCenter.head_pin)
    turn_head(head_servo)
    cleanup_head(dataCenter.head_pin)

if __name__ == "__main__": 
    main()