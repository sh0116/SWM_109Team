import RPi.GPIO as GPIO
import time
import dataCenter
import requests

#initialise a previous input variable to 0 (Assume no pressure applied)
global prev_input_head, prev_input_body
prev_input_head = False
prev_input_body = False

global touch_count
touch_count = 0

def request_touch():
    global touch_count
    
    data = {'user_id' : 1, 'sensor_id': dataCenter.touch, 'num' : touch_count, 'day': 'Sunday'}
    requests.post(dataCenter.URL, json=data)
    touch_count = 0
    print(touch_count)

def check_touch(input_head, input_body):
    global touch_count
    global prev_input_head, prev_input_body
    
    if (prev_input_head and (not prev_input_body)) and input_body:
        print("head to body")
        touch_count += 1
    elif (prev_input_body and (not prev_input_head)) and input_head:
        print("body to head")
        touch_count += 1 
    elif (not prev_input_head) and input_head:
        print("only head")
    elif (not prev_input_body) and input_body:
        print("only body")

    #update previous input
    prev_input_head = input_head
    prev_input_body = input_body
    #slight pause
    #time.sleep(0.10)