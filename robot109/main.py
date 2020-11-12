import os
import sensor.touch_main as touch
import sensor.temperature_main as temperature
import image_processing.image_main as image
#import image_processing.image_activity as activity
import voice_processing.voice_main as voice
import dataCenter
#from threading import Thread
from multiprocessing import Process

from apscheduler.schedulers.background import BackgroundScheduler
import apscheduler.schedulers.blocking

import argparse

# scheduler
sched = BackgroundScheduler()
sched.add_job(temperature.request_temper, 'interval', seconds = dataCenter.temp_interval)
sched.add_job(touch.request_touch,'interval', seconds = dataCenter.touch_interval)
sched.start()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--all', action="store_true", help="execute all the process")
    parser.add_argument('-i', '--image', action="store_true", help="execute the image process")
    parser.add_argument('-v', '--voice', action="store_true", help="execute the voice process")
    parser.add_argument('-s', '--sensor', action="store_true", help="execute the sensor process")

    process1 = Process(target=touch.main)
    process2 = Process(target=temperature.main)
    process3 = Process(target=image.main)
    process4 = Process(target=voice.main)
    #process1.start()
    #process2.start()
    #process3.start()
    process4.start()

    print("109mac")

if __name__ == "__main__":
    main()