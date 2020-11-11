<div align="center"><img src="../../images/109_logo_ver.png" width="300">

![Python](https://img.shields.io/badge/Python-3.7.4-blue)
![WebRtcvad](https://img.shields.io/badge/WebRtcvad-2.0.10-orange)
![Snowboy](https://img.shields.io/badge/Snowboy-1.3.0-9cf)

# Development

### 1. Snowboy Hot word detect

robot109/voice_processing/snowboy_dir/snowboydecoder.py
```
while self._running is True:
   ...
   status = self.detector.RunDetection(data)
   #반복문을 돌면서 status를 반환하여 검사한다. ACTIVE or PASSIVE
   ...
```


### 2. PY-WebRTCVAD
PY-WebRTCVAD는 Google에서 만든 WebRTC VAD (Voice Activity Detector)에 대한 Python 인터페이스 입니다.
VAD기술은 오디오 데이터에서 음성 데이터와 무성음 데이터를 구분 합니다.
또한 Google에서 WebRTC프로젝트를 위해 개발한 VAD는 가장 빠르며 오픈소스로 알려져있습니다.

[https://github.com/wiseman/py-webrtcvad](url)

robot109/voice_processing/ApisNLP/record.py
```
stream.start_stream()

while not got_a_sentence and not leave:
   ...
   active = vad.is_speech(chunk, RATE)
   #반복문을 돌면서 active 를 반환하여 검사한다. ACTIVE or PASSIVE
   ...
   
stream.stop_stream()
```


# Main Functions
| 주요 기능 | 설명 | 
| ------ | ------ | 
| Snowboy | 학습된 Hot Word모델을 통해 실시간 Wake up word를 감지하여, NLP기능을 활성화 시키는 기능
| VAD | 구글에서 만든 WebRTCVAD기술을 응용하여 만든 사람의 목소리만 추출하여 녹음하는 기능 (STT에 넣기전 녹음 파일을 만드는 과정)|
| STT | GCP의 STT(Speech to Text) API |
| TTS | 클로바의 TTS(Text to Speech) API ( '하준' 목소리 )|
| DialogFlow | 자연어 인식을 위한 GCP의 챗봇 인터페이스 |
| Crawling | 당일 날씨 및 로또 번호 추출을 위한 크롤링 기능 |
| Scheduler | 약 복용 알림 및 Daily Question을 위한 스케쥴러 기능 |