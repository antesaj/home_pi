import time
import os
import Adafruit_DHT

from kafka import KafkaProducer

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4
ROOM = os.getenv("ROOM")
KAFKA = '10.0.0.111:9092'

def publish_message(producer_instance, topic_name, key, value):
    try:
        key_bytes = bytes(key, encoding='utf-8')
        value_bytes = bytes(value, encoding='utf-8')
        producer_instance.send(topic_name, key=key_bytes, value=value_bytes)
        producer_instance.flush()
        print("Message published successfully")
    except Exception as ex:
        print("Failed to publish message")
        print(str(ex))

def connect_kafka_producer():
    _producer = None
    try:
        _producer = KafkaProducer(bootstrap_server=[KAFKA], api_version=(0, 10))
    except Exception as ex:
        print("Failed to connect to Kafka")
        print(str(ex))
    finally:
        return _producer

def to_fahrenheit(temp):
    return (temp * 9/5) + 32

kafka_producer = connect_kafka_producer()

while True:
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

    if humidity is not None and temperature is not None:
        temp_f = to_fahrenheit(temperature)
        temp_str = "Room: {0} Temp={1:0.1f}*F  Humidity={2:0.1f}%".format(ROOM, temp_f, humidity)
        print(temp_str)
        publish_message(kafka_producer, 'office-temp', 'raw', temp_str)
    else:
        print("Failed to retrieve data from humidity sensor")

    time.sleep(10)
