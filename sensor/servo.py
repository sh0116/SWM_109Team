import RPi.GPIO as GPIO
from time import sleep
import numpy as np

GPIO.setmode(GPIO.BOARD)

SERVO_MAX_DUTY = 12
SERVO_MIN_DUTY = 3

DEFAULT_SLEEP = 1
UP_DOWN_SLEEP = 0.04
DEFAULT_COUNT = 5

SLEEP_START = 0.001
SLEEP_END = 0.01

body_pin = 12
tail_pin = 13

GPIO.setup(body_pin, GPIO.OUT)
GPIO.setup(tail_pin, GPIO.OUT)

body_servo = GPIO.PWM(body_pin, 50)
tail_servo = GPIO.PWM(tail_pin, 50)

body_servo.start(3)
tail_servo.start(7.5)

def changeTail(duty, sleepTime=DEFAULT_SLEEP):
	tail_servo.ChangeDutyCycle(duty)
	sleep(sleepTime)

def changeBody(duty, sleepTime=DEFAULT_SLEEP):
	body_servo.ChangeDutyCycle(duty)
	sleep(sleepTime)

def down_tail(sleepTime=DEFAULT_SLEEP):
	changeTail(7.5,sleepTime)
	for i in np.arange(6.0,3.0,-0.05):
		changeBody(i,sleepTime=UP_DOWN_SLEEP)

def up_tail(sleepTime=DEFAULT_SLEEP):
	changeTail(7.5,sleepTime)
	for i in np.arange(3.0,6.0,0.1):
		changeBody(i,sleepTime=UP_DOWN_SLEEP)

def shake_tail(sleepTime=DEFAULT_SLEEP,count=DEFAULT_COUNT):
	up_tail(sleepTime)
	sleepStart = SLEEP_START
 	sleepCur = sleepStart
 	sleepEnd = SLEEP_END
 	shakeRange = np.arange(7.5,9.0,0.05)
 	for idx,j in enumerate(shakeRange):
 		changeTail(j,sleepCur)
 		sleepCur=sleepStart+((sleepEnd-sleepStart)/len(shakeRange))*idx
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
 	sleepCur = sleepStart
 	shakeRange = np.arange(9.0,7.5,-0.05)
 	for idx,j in enumerate(shakeRange):
 		changeTail(j,sleepCur)
 		sleepCur=sleepStart+((sleepEnd-sleepStart)/len(shakeRange))*idx
	changeBody(6.0)	

if __name__ == "__main__":
	while True:
		servo = raw_input("command: ")
		if(servo == "end"): break
		elif(servo == "body"): 
			duty = int(input("duty: "))
			changeBody(duty)
		elif(servo == "tail"):
			duty = int(input("duty: "))
			changeTail(duty)
		elif(servo == "up"): up_tail()
		elif(servo == "down"): down_tail()
		elif(servo == "shake"): shake_tail(count=3)
	GPIO.cleanup()
