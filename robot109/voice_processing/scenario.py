from voice_processing import voice_main
from voice_processing.ApisNLP import Crawling
from data import DBapi

def call_func(fun_name,NLP_Text):
    globals()[fun_name](NLP_Text)

def call_music(file_name):
    music_name = file_name[1]
    print(music_name)
    voice_main.play_mp3.play_mp3(music_name)

def call_Ask_Lotto(Text):
    TTS_Text = voice_main.Crawling.get_weather(Dialogflow_Text)
    #print("call Weather : ",TTS_Text)
    voice_main.call_TTS(Crawling.get_Lotto())

def call_emergency(Text):
    with open('/home/pi/robot109/data/user_info.txt','r') as inf:
        user_id = eval(inf.read())["id"]
    voice_main.call_TTS("응급 상황을 감지 했습니다. 보호자에게 연락하겠습니다")
    DBapi.request("insert into sensor_data(user_id,sensor_id) values ({},8);".format(user_id))

    #sensoe_id 8번으로 insert into

def call_Ask_temp(Text):
    TTS_Text = Crawling.get_weather(Dialogflow_Text)
    if not TTS_Text:
        voice_main.call_TTS(TTS_Text)
    else:
        voice_main.call_TTS(TTS_Text+"도 확인했습니다.")
        if float(TTS_Text) > 37:
            voice_main.call_TTS("체온이 너무 높습니다. 보호자에게 알릴까요?")
        elif float(TTS_Text) > 39:
            voice_main.call_TTS("체온이 너무 높습니다. 보호자에게 알릴까요?")
        elif float(TTS_Text) > 40:
            voice_main.call_TTS("체온이 비정상적으로 높습니다. 보호자에게 연락하겠습니다.")

def call_weather(NLP_Text):
    voice_main.call_TTS(Crawling.get_weather())

##############################################################################################################
#bool#########################################################################################################
##############################################################################################################


def call_Ask_feeling():
    voice_main.call_TTS("오늘은 기분이 어떠세요?")
    voice_main.call_record()
    STT_Text = voice_main.call_STT()
    ans = voice_main.call_Dialogflow("Ask_checkouting,"+STT_Text)
    if ans == "positive":
        voice_main.call_TTS("기분이 좋으시다니 저도 좋아요")
    elif ans == "negative":
        voice_main.call_TTS("기분이 안좋으시다니 저도 슬퍼요")
    else:
        voice_main.call_TTS("그렇군요")

def call_Ask_checkouting():
    voice_main.call_TTS("나갔다 오셨어요?")
    voice_main.call_record()
    STT_Text = voice_main.call_STT()
    ans = voice_main.call_Dialogflow("Ask_checkouting,"+STT_Text)
    if ans == "positive":
        voice_main.call_TTS("잘 다녀오셨어요?")
    elif ans == "negative":
        voice_main.call_TTS("알겠습니다 나갔다 오신줄 알았어요")
    else:
        voice_main.call_TTS("그렇군요")

def call_Ask_eat():
    voice_main.call_TTS("밥은 드셨어요?")
    voice_main.call_record()
    STT_Text = voice_main.call_STT()
    ans = voice_main.call_Dialogflow("Ask_eat,"+STT_Text)
    if ans == "positive":
        voice_main.call_TTS("맛있게 드셨어요?")
    elif ans == "negative":
        voice_main.call_TTS("배고프겠네요 얼른 드세요")
    else:
        voice_main.call_TTS("그렇군요")

def call_Ask_dq():
    ans = ""
    def ch(ans):
        if ans == "positive":
            return "1"
        elif ans == "negative":
            return "0"
        else:
            return "0"

    voice_main.call_TTS("사회복지사의 질문이 왔어요 네 아니오로 대답해주세요")
    voice_main.call_TTS("오늘 잠은 잘 주무셨나요?")
    voice_main.call_record()
    STT_Text = voice_main.call_STT()
    ans += ch(voice_main.call_Dialogflow("Ask_dq ,"+STT_Text))

    voice_main.call_TTS("오늘 이상 체온이 있으신가요?")
    voice_main.call_record()
    STT_Text = voice_main.call_STT()
    ans += ch(voice_main.call_Dialogflow("Ask_dq ,"+STT_Text))

    voice_main.call_TTS("오늘 아픈 곳이 있으신가요?")
    voice_main.call_record()
    STT_Text = voice_main.call_STT()
    ans += ch(voice_main.call_Dialogflow("Ask_dq ,"+STT_Text))

    voice_main.call_TTS("오늘 식사는 잘 하셨나요?")
    voice_main.call_record()
    STT_Text = voice_main.call_STT()
    ans += ch(voice_main.call_Dialogflow("Ask_dq ,"+STT_Text))
    print(ans)
    return ans

def call_Ask_medicine(name,hour,minute):
    voice_main.call_TTS("{}시 {}분 이에요 {} 드셨어요?".format(hour,minute,name))
    voice_main.call_record()
    STT_Text = voice_main.call_STT()
    ans = voice_main.call_Dialogflow("Ask_medicine,"+STT_Text)
    if ans == "positive":
        voice_main.call_TTS("잘챙겨드셔서 기분이 좋아요")
    elif ans == "negative":
        voice_main.call_TTS("약 먹을 시간이에요 챙겨드세요")
    else:
        voice_main.call_TTS("그렇군요")

if __name__ == "__main__":
    # locals()["call_STT"]()
    #call_TTS("인녕하세요")
    #call_Ask_medicine()
    pass
