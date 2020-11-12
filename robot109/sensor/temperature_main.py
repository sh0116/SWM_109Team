import Adafruit_DHT
import requests
import dataCenter

global thermo
thermo = Adafruit_DHT.DHT22

global MAX_TEMP, MIN_TEMP
MAX_TEMP = 29
MIN_TEMP = 20

global FIRE_TEMP
FIRE_TEMP = 35

def request_temper():
    humid, temper = get_temp()
    temperature_data = {'user_id' : dataCenter.user_id , 'sensor_id' : dataCenter.temperature, 'num': temper, 'day' : 'sunday'}
    if temper > 0: requests.post(dataCenter.URL, json=temperature_data)
    humidity_data = {'user_id' : dataCenter.user_id , 'sensor_id' : dataCenter.humidity, 'num' : humid, 'day' : 'sunday'}
    if humid > 0: requests.post(dataCenter.URL, json=humidity_data)

def get_temp():
    global MAX_TEMP, MIN_TEMP
    humidity, temperature = Adafruit_DHT.read_retry(thermo, dataCenter.temp_pin, delay_seconds=1)
    if humidity is not None and temperature is not None:
        print('temperature = {0:0.3f}C | humidity = {1:0.3f}%'.format(temperature, humidity))
        if temperature >= FIRE_TEMP:
            print('화재가 감지되었습니다')
        elif temperature >= MAX_TEMP:
            print("에어컨을 틀어주세요")
        elif temperature < MIN_TEMP:
            print("난방을 켜주세요")
    else:
        print("temperature fail")

    return humidity, temperature

def main():
    while True:
        get_temp()

if __name__ == "__main__":
    main()