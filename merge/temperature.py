import Adafruit_DHT

global thermo, temp_pin
thermo = Adafruit_DHT.DHT22
temp_pin = 21

def get_temp():
    global thermo, temp_pin
    humidity, temperature = Adafruit_DHT.read_retry(thermo, temp_pin)
    if humidity is not None and temperature is not None:
        print('temperature = {0:0.3f}C | humidity = {1:0.3f}%'.format(temperature, humidity))
    else:
        print('temperature fail')
    return humidity, temperature