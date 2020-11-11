<div align="center"><img src="./images/109_logo_ver.png" width="300">
</div>

![Python](https://img.shields.io/badge/Python-3.7.4-blue)
![Flask](https://img.shields.io/badge/Flask-1.1.2-red)
![Mysql](https://img.shields.io/badge/MySQL-5.7.32-blueviolet)
![Website](https://img.shields.io/badge/WebSite-HERE-yellow)]
![Bootrtap](https://img.shields.io/badge/bootstrap-Flask--Bootstrap%203.3.7.1-brightgreen)

Flask는 Python으로 구동되는 웹 어플리케이션 프레임워크이다. Django 프레임워크보다 가볍고, 스케일이 작은 서버부터 큰 서버까지 만들 수가 있으며, Jinja와 Werkzeug를 포함하고 있습니다. 

부트스트랩은 트위터에서 사용하는 각종 레이아웃, 버튼, 입력창 등의 디자인을 CSS와 Javascript로 만들어 놓은 것이다. 웹 디자이너나 개발자 사이에서는 웹 디자인의 혁명이라고 불릴 정도로 폭발적은 반응을 얻는 프레임워크입니다.

# Development
### 실행 방법 

```
pip3 install -r requirements.txt
python3 run.py
```
### 파일 구조 
```
.
├── dbAPI.py
├── run.py
├── static
│   ├── css
│   ├── fonts
│   ├── img  
│   ├── js
│   └── sass      
└── templates
    ├── index.html
    ├── map.html
    ├── test.html
    └── userapp.html
```

### 백구 센터 메인 페이지
>index.html


**1. 전체 사용자 지도**

kakao map api를 통해 마커에 user_id를 입력하여 전체 정보를 띄운다.

새로운 사용자가 등록되면 실시간 알림을 주어 확인 할 수 있도록 한다.


**2.전체 사용자의 평균 데이터 시각화**

관리하고 있는 사용자들의 평균 데이터를 분석하여 개인별 데이터 수치 이상을 판별하기 위해 통합적인 평균 데이터를 수집하도록 한다. 



노인이 평소 활동하는 시간(6am-9pm)을 기준으로 전체 사용자의 시간대 별 평균 활동량을 시각화한다.

또한 노인의 생활 패턴을 파악하기 위해 필요한 데이터를 시각화 한다.




### 백구 센터 모니터링 페이지
>map.html

**1. 사용자의 기본 정보 및 실시간 활동량**

모니터링 대상자를 선택한 후, 대상자의 기본 정보를 출력하여 실시간 모니터링 할 수 있도록 한다.  

백구 로봇에서 정제된 활동량을 서버로 전송 받아 가장 최신의 데이터를 30분 단위 당 실시간 그래프로 작성한다.



**2. 센서 데이터 수집**

사용자의 백구 로봇으로 부터 전송 받은 센서 데이터를 직관적으로 확인할 수 있도록 정제하여 시각화 한다. 

수치 이상의 온도 또는 낙상과 같은 데이터가 입력된다면 소리와 함께 경고 알림 메세지를 주도록 한다. 


하루 전의 데이터를 목표치로 설정하여 비교된 데이터를 수치화하여 시각화 한다. 

보호자는 이상 데이터를 직관적으로 파악할 수 있도록 한다. 

낙상 데이터 또한 최근 5번의 낙상을 기준으로 한다. 


개인 사용자의 시간대 별 평균 활동량을 시각화 한다. 

백구 로봇을 통해 얻어온 안부 전화 지표를 활용하여 2pm을 기준으로 답변 받도록 한다.
