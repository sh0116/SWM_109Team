import os
import sensor.touch_main as touch
import sensor.temperature_main as temperature
import image_processing.image_main as image
# import voice_processing.voice_main as voice
#from threading import Thread
from multiprocessing import Process

# from apscheduler.schedulers.background import BackgroundScheduler

# # scheduler
# sched = BackgroundScheduler()
# sched.add_job(sensor_temp.request_temper, 'interval', seconds = dataCenter.temp_interval)
# sched.add_job(sensor_touch.request_touch,'interval', seconds = dataCenter.touch_interval)
# sched.add_job(tflite_activity.request_realtime, 'interval', seconds = dataCenter.activ_interval)
# sched.start()

if __name__ == "__main__":
    th1 = Process(target=touch.main)
    #th2 = Process(target=temperature.main)
    #th3 = Process(target=image.main)
    # th4 = Process(target=voice.main)
    th1.start()
    #th2.start()
    #th3.start()
    # th4.start()

    print("109mac")