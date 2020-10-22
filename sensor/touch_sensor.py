import RPi.GPIO as GPIO
import Adafruit_DHT
#from time import sleep
import time
import sys
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import numpy as np

sys.path.append("/home/pi/109system/NLP")
import NLP_Main as NLP

URL = 'http://13.125.221.213:5000/sensor'
sched = BackgroundScheduler()

GPIO.setmode(GPIO.BOARD)

SERVO_MAX_DUTY = 12
SERVO_MIN_DUTY = 3

DEFAULT_SLEEP = 1
UP_DOWN_SLEEP = 0.04
DEFAULT_COUNT = 5
SLEEP_START = 0.001
SLEEP_END = 0.01

sensor = Adafruit_DHT.DHT22
temp_pin = 21
body_pin = 36
tail_pin = 38
head_pin = 16
headtouch_pin = 11
bodytouch_pin = 13
GPIO.setup(body_pin, GPIO.OUT)
GPIO.setup(tail_pin, GPIO.OUT)
GPIO.setup(headtouch_pin,GPIO.IN)
GPIO.setup(bodytouch_pin,GPIO.IN)
#initialise a previous input variable to 0 (Assume no pressure applied)
prev_input_body = 0
prev_input_head = 0
touch_count = 0

push_temperature = 0
push_humidity = 0

body_servo = GPIO.PWM(body_pin, 50)
tail_servo = GPIO.PWM(tail_pin, 50)

body_servo.start(3)
tail_servo.start(7.5)


def request_temper():
	humidity, temperature = Adafruit_DHT.read_retry(sensor, temp_pin)
	if humidity is not None and temperature is not None:
		print('temperature = {0:0.3f}C | humidity = {1:0.3f}%'.format(temperature, humidity))
	temperature_data = {'user_id' : 1 , 'sensor_id':1, 'num':temperature,'day':'sunday'}
	request = requests.post(URL, json=temperature_data)
	humidity_data = {'user_id' : 1 , 'sensor_id':2, 'num':humidity,'day':'sunday'}
	request = requests.post(URL, json=humidity_data)

def request_touch():
	global touch_count
	touch_data = {'user_id' : 1 , 'sensor_id':7, 'num':touch_count,'day':'sunday'}
	request = requests.post(URL, json=touch_data)
	print(touch_count)
	touch_count = 0

#sched.add_job(request_touch, 'interval',seconds=10)
#sched.add_job(request_temper,'interval',seconds=11)
sched.start()

def changeTail(duty, sleepTime=DEFAULT_SLEEP):
	tail_servo.ChangeDutyCycle(duty)
	time.sleep(sleepTime)

def changeBody(duty, sleepTime=DEFAULT_SLEEP):
	body_servo.ChangeDutyCycle(duty)
	time.sleep(sleepTime)

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
		# servo = raw_input("command: ")
		# if(servo == "end"): break
		# elif(servo == "body"): 
		# 	duty = int(input("duty: "))
		# 	changeBody(duty)
		# elif(servo == "tail"):
		# 	duty = int(input("duty: "))
		# 	changeTail(duty)
		# elif(servo == "up"): up_tail()
		# elif(servo == "down"): down_tail()
		# elif(servo == "shake"): shake_tail(count=3)

		#humidity, temperature = Adafruit_DHT.read_retry(sensor, temp_pin)
		
		input_head = GPIO.input(headtouch_pin)
		input_body = GPIO.input(bodytouch_pin)
        #print("1")
		#if the last reading was low and this one high, alert us
		#if humidity is not None and temperature is not None:
		#	print('temperature = {0:0.3f}C | humidity = {1:0.3f}%'.format(temperature, humidity))
		#	time.sleep(1)
		
		# 머리를 만지고 있고 몸을 만지는 순간 
		if prev_input_head and ((not prev_input_body) and input_body)):
			print ("head to body")
			touch_count +=1
		elif prev_input_body and ((not prev_input_head) and input_head):
			print("body to head")
			touch_count +=1 
		elif (not prev_input_head) and input_head :
			print("only head")
		elif (not prev_input_body) and input_body:
			print("only body")
		
		prev_input_head = input_head
		prev_input_body = input_body
        	#slight pause
		time.sleep(0.10)
		
		if touch_count > 15 : 
			NLP.call_TTS("기분이 좋아요")
			time.sleep(0.5)
			shake_tail(count=3)
			# 서보 끄는거 추가 

			

		
		# if(prev_input_head and input_body):
		# 	print("head to body")
		# if ((not prev_input_body) and input_body):
		# 	if((not prev_input_head) and input_head):
		# 		print("body to head")
		# 		touch_count +=1
		# 	touch_count +=1
		# 	print(touch_count)
		# if ((not prev_input_head) and input_head):
		# 	if ((not  prev_input_body) and input_body):
		# 		print("Head to body")
		# 		touch_count +=1
		# 	touch_count +=1
		# 	print(touch_count)
		#if touch_count == 5:
			#shake_tail(count=3)
			#time.sleep(1)
			#NLP.call_TTS("기분이 좋아요")
		#if touch_count == 10:
		#	shake_tail(count=3)
        #update previous input
		
	



