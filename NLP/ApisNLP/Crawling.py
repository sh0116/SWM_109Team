# -*- coding: utf-8 -*-
from urllib.request import urlopen, Request
import urllib
import bs4

def get_weather(Dialogflow_Text):

    fun_name, location, date = Dialogflow_Text[0],Dialogflow_Text[1],Dialogflow_Text[2]
    
    # location을 말하지않았다면 사용자 집주소 == lacation
    if location == '내위치':
        location == '구리시'
 
    # enc_location 사용자가 말한 위치
    enc_location = urllib.parse.quote(location + '+날씨')
    # enc_location위치에 날씨를 검색
    url = 'https://search.naver.com/search.naver?ie=utf8&query='+ enc_location

    req = Request(url)
    page = urlopen(req)
    html = page.read()
    soup = bs4.BeautifulSoup(html,'html5lib')
    soup.find('p', class_='info_temperature').find('span', class_='todaytemp').text

    if date == '오늘': 
        # 현재 온도 
        NowTemp = soup.find('span', {'class': 'todaytemp'}).text
        # 날씨 캐스트 
        WeatherCast = soup.find('p', {'class' : 'cast_txt'}).text 

        # 오늘 오전온도, 오후온도, 체감온도 
        TodayMorningTemp = soup.find('span', {'class' : 'min'}).text[:-1] 
        TodayAfternoonTemp = soup.find('span', {'class' : 'max'}).text[:-1] 
        TodayFeelTemp = soup.find('span', {'class' : 'sensible'}).text[5:-1] 

        # 자외선 지수 
        TodayUV = soup.find('span', {'class' : 'indicator'}).text[4:-2] + " " + soup.find('span', {'class' : 'indicator'}).text[-2:] 

        # 미세먼지, 초미세먼지, 오존 지수 
        CheckDust1 = soup.find('div', {'class': 'sub_info'}) 
        CheckDust2 = CheckDust1.find('div', {'class': 'detail_box'}) 
        CheckDust = []
        for i in CheckDust2.select('dd'): 
            CheckDust.append(i.text) 
        FineDust = CheckDust[0][:-2] + " " + CheckDust[0][-2:] 
        UltraFineDust = CheckDust[1][:-2] + " " + CheckDust[1][-2:] 
        Ozon = CheckDust[2][:-2] + " " + CheckDust[2][-2:]

        #print('오늘' + location + '오전 기온은'+ TodayMorningTemp +'도'+', 오후 기온은' + TodayAfternoonTemp +'도 입니다')
        text_Temp = '오늘 ' + location + ' 오전 기온은 '+ TodayMorningTemp +'도'+', 오후 기온은 ' + TodayAfternoonTemp +'도 입니다'
        
        #print('체감 온도은'+ TodayFeelTemp +'도')
        if float(TodayFeelTemp)<29:
            text_feel_temp = '체감 온도은 '+ TodayFeelTemp +'도입니다'
        elif 29 <= float(TodayFeelTemp) < 31:
            text_feel_temp = '체감 온도은 '+ TodayFeelTemp +'도로 더운 날씨에요, 할아버지 야외 활동을 자제해주세요'
        elif 31 <= float(TodayFeelTemp) < 37:
            text_feel_temp = '체감 온도은 '+ TodayFeelTemp +'도로 무더운 날씨에요, 할아버지 에어컨을 켜주세요.'
        elif 37 <= float(TodayFeelTemp):
            text_feel_temp = '체감 온도은 '+ TodayFeelTemp +'도로 폭염이에요, 할아버지 야외 활동을 자제하고 꼭 에어컨을 켜주세요'
        
        
        return text_Temp + ". " + text_feel_temp

    elif date == '내일':
            # 내일 오전, 오후 온도 및 상태 체크 
        tomorrowArea = soup.find('div', {'class': 'tomorrow_area'}) 
        tomorrowCheck = tomorrowArea.find_all('div', {'class': 'main_info morning_box'}) 

        # 내일 오전온도 
        tomorrowMoring = tomorrowCheck[0].find('span', {'class': 'todaytemp'}).text 

        # 내일 오전상태 
        tomorrowMState1 = tomorrowCheck[0].find('div', {'class' : 'info_data'}) 
        tomorrowMState2 = tomorrowMState1.find('ul', {'class' : 'info_list'})
        tomorrowMState3 = tomorrowMState2.find('p', {'class' : 'cast_txt'}).text 
        tomorrowMState4 = tomorrowMState2.find('div', {'class' : 'detail_box'}) 
        tomorrowMState5 = tomorrowMState4.find('span').text.strip() 
        tomorrowMState = tomorrowMState3 + " " + tomorrowMState5 

        # 내일 오후온도 
        tomorrowAfter_info = tomorrowCheck[1].find('p', {'class' : 'info_temperature'}) 
        tomorrowAfter = tomorrowAfter_info.find('span', {'class' : 'todaytemp'}).text 

        # 내일 오후상태 
        tomorrowAState1 = tomorrowCheck[1].find('div', {'class' : 'info_data'}) 
        tomorrowAState2 = tomorrowAState1.find('ul', {'class' : 'info_list'})
        tomorrowAState3 = tomorrowAState2.find('p', {'class' : 'cast_txt'}).text 
        tomorrowAState4 = tomorrowAState2.find('div', {'class' : 'detail_box'}) 
        tomorrowAState5 = tomorrowAState4.find('span').text.strip() 
        tomorrowAState = tomorrowAState3 + " " + tomorrowAState5

        #print('내일 ' + location + ' 오전 기온은 '+ tomorrowMoring +'도'+', 오후 기온은 ' + tomorrowAfter +'도 입니다')
        text_Temp = '내일 ' + location + ' 오전 기온은 '+ tomorrowMoring +'도'+', 오후 기온은 ' + tomorrowAfter +'도 입니다'
        return text_Temp


if __name__ == "__main__":
    pass
