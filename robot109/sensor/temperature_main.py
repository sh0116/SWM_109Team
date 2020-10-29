import Adafruit_DHT
import requests

global thermo, temp_pin
thermo = Adafruit_DHT.DHT22
temp_pin = 21

def request_temper():
    humid, temper = get_temp()
    temperature_data = {'user_id' : 1 , 'sensor_id' : 1, 'num': temper, 'day' : 'sunday'}
    requests.post(dataCenter.URL, json=temperature_data)
    humidity_data = {'user_id' : 1 , 'sensor_id' : 2, 'num' : humid, 'day' : 'sunday'}
    requests.post(dataCenter.URL, json=humidity_data)

def main():
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(thermo, temp_pin, delay_seconds=1)
        if humidity is not None and temperature is not None:
            print('temperature = {0:0.3f}C | humidity = {1:0.3f}%'.format(temperature, humidity))
        else:
            print('temperature fail')
        
    return humidity, temperature


if __name__ == "__main__":
    main()