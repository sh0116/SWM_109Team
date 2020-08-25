from ApisNLP import STT_GCP 
from ApisNLP import TTS_GCP 
from ApisNLP import Dialogflow_GCP 
from ApisNLP import Crawling
from ApisNLP import play_mp3
from ApisNLP import record

#snowboy에 필요한 모듈
from snowboy_dir import snowboydecoder

def detected_callback():
    print("wake up word detected")
    # wake up word 감지 후 STT에 보낼 mp3파일 녹음
    record.recording()
    # mp3 파일 -> Text파일
    call_STT()
    return	
	
def wake_up_word_detect():
    # 감지 설정  baekgu.pmdl == 모델 , sensitivity == 감지 민감도 
    detector = snowboydecoder.HotwordDetector("/home/pi/my_dir/NLP/baekgu.pmdl", sensitivity=0.5, audio_gain=3)
    try:
        while(True):
            print("---Start_detected---")
            # 감지 시작
            detector.start(detected_callback)
    except KeyboardInterrupt:
        pass

def call_play():
    play_mp3.play_mp3()

def call_STT():
    STT_TEXT = STT_GCP.get_STT()
    if STT_TEXT == "error":
        call_TTS("잘 알아듣지 못했어요 할아버지")
        return 
    #print("STT_TEXT : " , STT_Text)
    call_Dialogflow(STT_TEXT)

def call_TTS(NLP_Text):
    TTS_GCP.get_TTS(NLP_Text)
    call_play()

def call_weather(Dialogflow_Text):
    TTS_Text = Crawling.get_weather(Dialogflow_Text)
    #print("call Weather : ",TTS_Text)
    call_TTS(TTS_Text)

def call_Dialogflow(STT_Text):
    NLP_Text = Dialogflow_GCP.get_Dialogflow(STT_Text)
    #print("Dialogflow TEXT : ",NLP_Text)
    fun_name = NLP_Text[0]
    try:
        globals()[fun_name](NLP_Text)
    except:
        call_TTS("다시 한번 말해주세요 할아버지")


if __name__ == "__main__":
    #인증 내용 있어야 한다.
    # locals()["call_STT"]()
    wake_up_word_detect()
