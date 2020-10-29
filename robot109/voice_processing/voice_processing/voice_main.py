from voice_processing.ApisNLP import STT_GCP 
from voice_processing.ApisNLP import TTS_GCP 
from voice_processing.ApisNLP import Dialogflow_GCP 
from voice_processing.ApisNLP import Crawling
from voice_processing.ApisNLP import play_mp3
from voice_processing.ApisNLP import record

#snowboy에 필요한 모듈
from voice_processing.snowboy_dir import snowboydecoder

def detected_callback():
    call_play("네에할아버지저여기있어요.mp3")
    print("wake up word detected")
    # wake up word 감지 후 STT에 보낼 mp3파일 녹음
    record.recording()
    # mp3 파일 -> Text파일
    call_STT()
    return	    
	
def main():
    # 감지 설정  baekgu.pmdl == 모델 , sensitivity == 감지 민감도 
    detector = snowboydecoder.HotwordDetector("/home/pi/NLP/baekgu.pmdl", sensitivity=0.8, audio_gain=3)
    try:
        while(True):
            print("---Start_detected---")
            # 감지 시작
            detector.start(detected_callback)
    except KeyboardInterrupt:
        pass


def call_STT():
    STT_TEXT = STT_GCP.get_STT()
    if STT_TEXT == "error":
        call_TTS("잘 알아듣지 못했어요 할아버지")
        return 
    #print("STT_TEXT : " , STT_Text)
    call_Dialogflow(STT_TEXT)

def call_TTS(NLP_Text):
    TTS_GCP.get_TTS(NLP_Text)
    call_play("TTS.mp3")



def call_play(file_name):
    play_mp3.play_mp3(file_name)

def call_music(file_name):
    music_name = file_name[1]
    print(music_name)
    play_mp3.play_mp3(music_name)

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
    # locals()["call_STT"]()
    main()