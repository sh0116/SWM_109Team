# 네이버 음성합성 Open API 예제
import os
import sys
import urllib.request
client_id = "bs5q7b82h1"
client_secret = "V5e9yDEgGoKvW9HeH8P5ijXtzcJD9lgerYAulYMs"
def get_TTS(NLP_Text):
    encText = urllib.parse.quote(NLP_Text)
    data = "speaker=ndain&volume=0&speed=0&pitch=0&format=mp3&text=" + encText;
    url = "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts"
    request = urllib.request.Request(url)
    request.add_header("X-NCP-APIGW-API-KEY-ID",client_id)
    request.add_header("X-NCP-APIGW-API-KEY",client_secret)
    response = urllib.request.urlopen(request, data=data.encode('utf-8'))
    rescode = response.getcode()

    if(rescode==200):
        response_body = response.read()
        with open('/home/pi/robot109/voice_processing/voice_file/TTS.mp3', 'wb') as f:
            f.write(response_body)
    else:
        print("Error Code:" + rescode)
        
if __name__ == "__main__":
    pass
