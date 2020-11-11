<div align="center"><img src="./images/109_logo_ver.png" width="300">
</div>


![RPi](https://img.shields.io/badge/Raspberry%20Pi-4B-brightgreen)
![Python](https://img.shields.io/badge/Python-3.7.4-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.1.2-orange)
![Flask](https://img.shields.io/badge/Flask-1.1.2-red)
![Snowboy](https://img.shields.io/badge/Snowboy-1.3.0-9cf)
![Flutter](https://img.shields.io/badge/Flutter-1.22.2-green)
![Mysql](https://img.shields.io/badge/MySQL-5.7.32-blueviolet)
![Website](https://img.shields.io/badge/WebSite-HERE-yellow)

# Overview


SW Maestro 11기 109팀이 진행하는 '독거노인을 위한 돌봄서비스 반려로봇' 프로젝트는 혼자 거주하는 어르신을 대상으로 강아지 외형의 로봇을 보급하여 생활패턴을 케어하고 위급상황을 감지하는, 정신적/신체적 케어서비스를 제공합니다.


<div align="center"><img src="./images/109info.png" width=600 ></div>


# Development
### 1. 백구 로봇
실행 방법

```
pip3 install -r requirements.txt
python3 main.py
```

options

| options | functions |
|----------|----------|
| -a or --all | 모든 프로세스 실행 |
| -i or --image | 영상 프로세스 실행 |
| -v or --voice | 음성 프로세스 실행 |
| -s or --sensor | 센서 관련 프로세스 실행 | 

### 2. 관제 대시보드 웹

[www.109center.com:5000/](url)

<div><img src="./images/map.png" width=400 >&nbsp;&nbsp;&nbsp;<img src="./images/realtime.gif" width=400 ></div>

### 3. 보호자용 앱

[https://play.google.com/store/apps/details?id=swm.app109](url)

<div><img src="./images/app_menu.png" width=150 >&nbsp;&nbsp;<img src="./images/app_dash1.png" width=150 >&nbsp;&nbsp;<img src="./images/app_meidicine_input.png" width=150 ></div>

# Versions

> ### v1.0.0 (released on 2020.11.08)
- 영상, 음성 및 각종 센서 기능 초기 완성

> ### v1.0.1 (released on 2020.11.08)
- 사용자 평균 데이터 시각화
- 데이터 정책 수립

# Main Functions
| 주요 기능 | 설명 | 
| ------ | ------ | 
| 낙상 인식 | 영상인식을 통해 사용자의 자세와 자세 변화 속도를 계산하고 낙상 인식 알고리즘을 통해 낙상 사고 인식 |
| 생활 패턴 학습 | 사용자의 평균 기상 및 취침시간대를 파악하고 활동량 등을 계산하여 사용자의 생활 패턴 학습 |
| 능동적 말벗 | 능동적 말벗 알고리즘과 음성 인식 기능을 통해 홀로 거주하는 사용자에게 정서적 유대감 제공 |
| 약 복용 알림 | 보호자용 앱과 음성 인식 기능을 통해 사용자에게 약 복용 시간 알림 |
| 응급 상황 알림 | 영상, 음성 및 각종 센서들을 통해 수집된 사용자의 상황을 인식하여 자체적으로 응급 상황을 판단하고 관제 대시보드 웹을 통해 보호자에게 알림 |
| 하드웨어 | 서보모터를 통해 고개를 움직여 시야 제한을 극복하고, 이중 서보모터로 이루어진 꼬리와 터치센서로 사용자와의 정서적 유대감 형성
| 보호자용 앱 | 보호자, 사용자 등록 및 네트워크 연결 등 로봇의 초기 설정과 사용자 상태 모니터링, 약 정보 등록 등의 기능
| 웹 관제 | 사용자의 상태 데이터를 수집하여 시각화하고 응급 상황 알림 등의 컨트롤 타워 기능 |
| 3D 모델링 | 친근한 강아지 외형을 형상화하여 3D 모델링 및 프린팅


# Others
- 특허 및 상표권 출원

출원번호 : 40-2020-0199523

- MOU 체결 (with 꼬마빌리지)

<div><img src="./images/MOU.jpeg" width="200"></div>

- SW 프로그램 저작권 등록

# Contribution
<div align="center"><img src="./images/109_logo.png" width="200">&nbsp;&nbsp;&nbsp;<img src="./images/swm_logo.png" width="150">&emsp;<img src="./images/ict_logo.jpeg " width="300">
</div>
