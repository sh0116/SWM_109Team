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

# scheduler
sched = BackgroundScheduler()
sched.add_job(temperature.request_temper, 'interval', seconds = dataCenter.temp_interval)
sched.add_job(touch.request_touch,'interval', seconds = dataCenter.touch_interval)
sched.start()

if __name__ == "__main__":
    process1 = Process(target=touch.main)
    process2 = Process(target=temperature.main)
    process3 = Process(target=image.main)
    process4 = Process(target=voice.main)
    process1.start()
    process2.start()
    process3.start()
    process4.start()

    print("109mac")