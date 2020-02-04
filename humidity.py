import time
import os
import Adafruit_DHT

from json import dumps
from kafka import KafkaProducer
from kafka.errors import KafkaError

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4
ROOM = os.getenv("ROOM")
KAFKA = '10.0.0.111:9092'

# def publish_message(producer_instance, topic_name, data):
#     try:
#         producer_instance.send(topic_name, value=data)
#         print("Message published successfully")
#     except Exception as ex:
#         print("Failed to publish message")
#         print(str(ex))
#
# def connect_kafka_producer():
#     _producer = None
#     try:
#         _producer = KafkaProducer(bootstrap_servers=[KAFKA],
#                                   value_serializer=lambda x: dumps(x).encode('utf-8'))
#     except Exception as ex:
#         print("Failed to connect to Kafka")
#         print(str(ex))
#     finally:
#         return _producer

def on_send_error(excp):
    log.error("Error", exc_info=excp)

def on_send_success(record_metadata):
    print(record_metadata.topic)
    print(record_metadata.partition)
    print(record_metadata.offset)

def to_fahrenheit(temp):
    return (temp * 9/5) + 32

producer = KafkaProducer(bootstrap_servers=[KAFKA])
while True:
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

    if humidity is not None and temperature is not None:
        temp_f = to_fahrenheit(temperature)
        temp_str = "Room: {0} Temp={1:0.1f}*F  Humidity={2:0.1f}%".format(ROOM, temp_f, humidity)
        print(temp_str)
        producer.send(bytes(temp_str, encoding='utf-8')).add_callback(on_send_success).add_errback(on_send_error)
        producer.flush()
        # data = {'temp': temp_f, 'humidity': humidity}
        # publish_message(kafka_producer, 'office-temp', data)
    else:
        print("Failed to retrieve data from humidity sensor")

    time.sleep(10)
