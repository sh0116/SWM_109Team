import RPi.GPIO as GPIO
import time
import requests
import sys
import numpy as np
import socket
import sensor.tail_servo_main as tail_servo_main
import dataCenter

#initialise a previous input variable to 0 (Assume no pressure applied)
global prev_head_touch, prev_body_touch
prev_head_touch = False
prev_body_touch = False

global touch_count
touch_count = 0

GPIO.setmode(GPIO.BOARD)

def request_touch():
    global touch_count
    data = {'user_id' : dataCenter.user_id, 'sensor_id': dataCenter.touch, 'num' : touch_count, 'day': 'Sunday'}
    # data = {'user_id' : 1, 'sensor_id': 5, 'num' : touch_count, 'day': 'Sunday'}
    requests.post(dataCenter.URL, json=data)
    touch_count = 0
    print(touch_count)

def setup_touch(head_touch_pin, body_touch_pin):
    # set up pins
    GPIO.setup(head_touch_pin,GPIO.IN)
    GPIO.setup(body_touch_pin,GPIO.IN)

    return head_touch_pin, body_touch_pin

def cleanup_touch(head_touch_pin, body_touch_pin):
    GPIO.cleanup(head_touch_pin)
    GPIO.cleanup(body_touch_pin)

def check_touch(head_touch_pin, body_touch_pin):
    head_touch = GPIO.input(head_touch_pin)
    body_touch = GPIO.input(body_touch_pin)
    return head_touch, body_touch

def main():
    # setup pins
    body_servo, tail_servo = tail_servo_main.setup_tail(dataCenter.body_pin, dataCenter.tail_pin)
    head_touch_pin, body_touch_in = setup_touch(dataCenter.head_touch_pin, dataCenter.body_touch_pin)
    # body_servo, tail_servo = tail_servo_main.setup_tail(36, 38)
    # head_touch_pin, body_touch_pin = setup_touch(11, 13)
    while True:
        global touch_count
        global prev_head_touch, prev_body_touch
        head_touch, body_touch = check_touch(dataCenter.head_touch_pin, dataCenter.body_touch_pin)
        # head_touch, body_touch = check_touch(11, 13)
        #check_touch(input_head, input_body)
        if (prev_head_touch and (not prev_body_touch)) and body_touch:
            print("head to body")
            # touch_count += 1
            # shake tail
            #tail_servo_main.shake_tail(body_servo, tail_servo)
        elif (prev_body_touch and (not prev_head_touch)) and head_touch:
            print("body to head")
            # touch_count += 1 
        elif (not prev_head_touch) and head_touch:
            print("only head")
        elif (not prev_body_touch) and body_touch:
            print("only body")
            tail_servo_main.shake_tail(body_servo, tail_servo)
            touch_count += 1

        #update previous input
        prev_head_touch = head_touch
        prev_body_touch = body_touch

        time.sleep(0.1)
    tail_servo_main.cleanup_tail(dataCenter.body_pin, dataCenter.tail_pin)
    cleanup_touch(dataCenter.head_pin, dataCenter.body_pin)
    # tail_servo_main.cleanup_tail(36, 38)
    # cleanup_touch(11, 13)

if __name__ == "__main__":
    main()