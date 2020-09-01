import Adafruit_DHT
import time
import requests
import pygame

sensor = Adafruit_DHT.DHT22
pin = '4'

def play_mp3():
    pygame.mixer.init()
    pygame.mixer.music.load("./온도경고.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
    return

while True:
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
	#print(humidity)
	#print(temperature)
    if humidity is not None and temperature is not None:
        print('temperature = {0:0.3f}C | humidity = {1:0.3f}%'.format(temperature, humidity))
        if temperature >= 30:
            play_mp3()
            break
        #requests.post('http://13.125.221.213:5555/sensor', json={'table_name':'temperature','num':temperature,'user_id':1})
	#requests.post('http://13.125.221.213:5555/sensor', json={'table_name':'humidity', 'num': humidity, 'user_id':1})
        time.sleep(5)
    else:
        print('fail')
