from voice_processing.ApisNLP import STT_GCP 
from voice_processing.ApisNLP import TTS_NAVER 
from voice_processing.ApisNLP import Dialogflow_GCP 
from voice_processing.ApisNLP import play_mp3
from voice_processing.ApisNLP import record

from voice_processing import scenario
from voice_processing import scheduler
from multiprocessing import Process

#snowboy에 필요한 모듈
from voice_processing.snowboy_dir import snowboydecoder
import time
import os

def detected_callback():
    call_TTS("네 부르셨어요?")
    print("wake up word detected")
    call_record()
    # mp3 파일 -> Text파일
    call_Dialogflow( call_STT() )   
	
def call_record():
    try:
        record.recording()
    except:
        call_TTS("잘 알아듣지 못했어요 어르신")
        return False

def call_STT():
    STT_TEXT = STT_GCP.get_STT()
    if STT_TEXT == "error":
        call_TTS("잘 알아듣지 못했어요 어르신")
        return "error"
    #print("STT_TEXT : " , STT_Text)
    return STT_TEXT
    #call_Dialogflow(STT_TEXT)

def call_TTS(NLP_Text):
    TTS_NAVER.get_TTS(NLP_Text)
    call_play("TTS.mp3")

def call_play(file_name):
    play_mp3.play_mp3(file_name)

def call_Dialogflow(STT_Text):
    NLP_Text = Dialogflow_GCP.get_Dialogflow(STT_Text)
    #print("Dialogflow TEXT : ",NLP_Text)
    if NLP_Text[0] == "bool":
        return NLP_Text[1]
    try:
        scenario.call_func(NLP_Text[1],NLP_Text)
    except:
        call_TTS("다시 한번 말해주세요 어르신")


def main():
    Process1 = Process(target = scheduler.main)
    Process1.start()

    # 감지 설정  baekgu.pmdl == 모델 , sensitivity == 감지 민감도 
    detector = snowboydecoder.HotwordDetector("/home/pi/robot109/voice_processing/baekgu.pmdl", sensitivity=0.6, audio_gain=3)

    try:
        while(True):
            print("---Start_detected---")
            # 감지 시작
            detector.start(detected_callback)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    # locals()["call_STT"]()
    #call_TTS("인녕하세요")
    main()
