import random
import paho.mqtt.client as mqtt
from cryptography.fernet import Fernet
import json
import time

class Sensor:
    def __init__(self, name, room_number):
        self.name = name
        self.room_number = room_number

class TemperatureSensor(Sensor):
    def measure_temperature(self):
        simulated_temperature = random.uniform(36.0, 40.0)
        return simulated_temperature

class HeartRateSensor(Sensor):
    def measure_heart_rate(self):
        simulated_heart_rate = random.randint(60, 100)
        return simulated_heart_rate

class HumiditySensor(Sensor):
    def measure_humidity(self):
        simulated_humidity = random.uniform(30, 70)
        return simulated_humidity

class GasSensor(Sensor):
    def measure_gas_level(self):
        simulated_gas_level = random.uniform(0, 100)
        return simulated_gas_level

class RaspberryPi:
    def __init__(self, room_number):
        self.room_number = room_number
        self.connected_sensors = []

    def connect_sensor(self, sensor):
        self.connected_sensors.append(sensor)

    def send_data_to_computer(self, topic, data):
        client = mqtt.Client()
        client.connect("127.0.0.1", 1883 )
        client.publish(topic, data)
        client.disconnect()

# الجزء الرئيسي

def main():
    room_number = 3 # استبدل برقم الغرفة الصحيح
    pi = RaspberryPi(room_number)

    temp_sensor = TemperatureSensor(name="Temperature Sensor", room_number=room_number)
    heart_rate_sensor = HeartRateSensor(name="Heart Rate Sensor", room_number=room_number)
    humidity_sensor = HumiditySensor(name="Humidity Sensor", room_number=room_number)
    gas_sensor = GasSensor(name="Gas Sensor", room_number=room_number)

    pi.connect_sensor(temp_sensor)
    pi.connect_sensor(heart_rate_sensor)
    pi.connect_sensor(humidity_sensor)
    pi.connect_sensor(gas_sensor)

    # تشفير البيانات وإرسالها
    data_encryption = 'W1ZbJI5IrBg5pPcUUOIcQAGBWa5Ozye8kM-syAUP3gM=' # استبدل بالمفتاح الصحيح
    print(data_encryption)
        
    while True:
        temperature = temp_sensor.measure_temperature()
        heart_rate = heart_rate_sensor.measure_heart_rate()
        humidity = humidity_sensor.measure_humidity()
        gas_level = gas_sensor.measure_gas_level()

        
        cipher_suite = Fernet(data_encryption)

        encrypted_temp = cipher_suite.encrypt(str(temperature).encode())
        encrypted_hr = cipher_suite.encrypt(str(heart_rate).encode())
        encrypted_humidity = cipher_suite.encrypt(str(humidity).encode())
        encrypted_gas_level = cipher_suite.encrypt(str(gas_level).encode())

        pi.send_data_to_computer(topic=f"sensor_data/{room_number}/Temperature", data=encrypted_temp)
        time.sleep(1)
        pi.send_data_to_computer(topic=f"sensor_data/{room_number}/HeartRate", data=encrypted_hr)
        time.sleep(1)
        pi.send_data_to_computer(topic=f"sensor_data/{room_number}/Humidity", data=encrypted_humidity)
        time.sleep(1)
        pi.send_data_to_computer(topic=f"sensor_data/{room_number}/Gas", data=encrypted_gas_level)
        
        # room_number += 1
        # if room_number > 8 :
        #     room_number = 1

        
        
if __name__ == "__main__":
    main()
