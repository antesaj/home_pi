import time
import os
import Adafruit_DHT

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4
ROOM = os.getenv("ROOM")

def to_fahrenheit(temp):
    return (temp * 9/5) + 32

while True:
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

    if humidity is not None and temperature is not None:
        temp_f = to_fahrenheit(temperature)
        print("Room: {0:%s} Temp={1:0.1f}*F  Humidity={2:0.1f}%"
            .format(ROOM, temp_f, humidity))
    else:
        print("Failed to retrieve data from humidity sensor")

    time.sleep(5)
