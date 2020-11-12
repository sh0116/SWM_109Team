#!/usr/bin/python
import RPi.GPIO as GPIO
import time

#from voice_process import voice_main

global ch
ch = True

def callback(channel):
        print("detect")
        global ch
        ch = False
        """        
        if GPIO.input(channel):
                voice_main.call_TTS("큰 소리가 감지 됐어요 괜찮으세요?")
                if voice_main.call_record():
                        voice_main.call_TTS("괜찮으세요? 할아버지?")
                else:
                        voice_main.call_TTS("답변이 없으면 응급상황을 알리겠습니다. 괜찮으세요?")
                        if voice_main.call_record():
        else:
        return "detect"
        """

# infinite loop

def main():
        print("sound start")
        #GPIO SETUP
        channel = 22
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(channel, GPIO.IN)
        GPIO.add_event_detect(channel, GPIO.RISING,callback=callback , bouncetime=300)  # let us know when the pin goes HIGH$
        #GPIO.add_event_callback(channel, callback)  # assign function to GPIO PIN, Run function on chan$
        try:
                ch2 = True
                while ch2:
                         global ch
                         ch2 = ch
                         print("recording..")
                         time.sleep(1)
        finally:
                GPIO.cleanup()
if __name__ == "__main__":
        main()
